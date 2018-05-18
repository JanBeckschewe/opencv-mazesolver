#!/usr/bin/env python3
import subprocess
import threading
import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import maze
import motors
import opencv
import pid_from_github


class MainClass:
    def __init__(self):
        self.w, self.h, self.framerate = 128, 96, 50
        self.camera = PiCamera()
        self.camera.resolution = (self.w, self.h)
        self.camera.framerate = self.framerate
        self.camera.exposure_mode = "off"

        self.raw_capture = PiRGBArray(self.camera, size=(self.w, self.h))
        self.frame = None

        self.maze = maze.Maze()
        self.opencv = opencv.OpenCV(self.maze, self.w, self.h)
        self.pid = pid_from_github.PID(1, .05, .4)
        self.motors = motors.Motors()

        self.total_frames = 0

        self.is_first_run = True
        self.is_finished = False

        self.is_in_backwards_left_turn = False

        self.saw_right_turn_last_frame = False

        self.current_direction = self.maze.forward

        time.sleep(0.1)

        self.ffmpeg_process = subprocess.Popen(
            "ffmpeg "
            "-y "
            "-f rawvideo "
            "-video_size 128x96 "
            "-pixel_format bgr24 "
            "-r 43 "
            "-i - "
            "-vcodec h264 "
            "-profile:v baseline "
            "-bf 0 "
            "-pix_fmt yuv420p "
            "-loglevel warning "
            "-reset_timestamps 1 "
            "-movflags frag_keyframe+empty_moov "
            "-fflags nobuffer "
            "-tune zerolatency "
            "-f tee "
            "-map 0:v "
            "\"[f=rtp]rtp://127.0.0.1:8004|httpdocs/lastrun.mp4\"",
            stdin=subprocess.PIPE, shell=True)

        threading.Thread(target=self.loop_over_camera).start()

    def loop_over_camera(self):
        started = False
        time_last_frame = time.time()
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            self.frame = frame
            self.raw_capture.truncate(0)

            print("camera:" + str(1 / (time.time() - time_last_frame)), end='\r')
            time_last_frame = time.time()

            if not started:
                threading.Thread(target=self.solve_maze).start()
                started = True

    def store_image(self, img):
        self.ffmpeg_process.stdin.write(img.tostring())

    def solve_maze(self):
        time_last_frame = time.time()
        while True:
            print("solver:" + str(1 / (time.time() - time_last_frame)), end='\r')
            time_last_frame = time.time()

            img_canny, lines, num_black_pixels = self.opencv.modify_image(self.frame)

            average_line_position = self.w / 2

            are_turns_seen_rn = [False] * 4

            motor_steer = 0

            i = 0
            if lines is not None:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        average_line_position += ((x1 + x2) / 2 - average_line_position) / (i + 1)
                        i += 1

                        self.opencv.find_lines(img_canny, x1, y1, x2, y2, are_turns_seen_rn)

            # when reset from website
            if self.is_finished and len(self.maze.full_path) == 0:
                self.is_finished = False

            # when reached end
            if not self.is_finished and num_black_pixels > self.w * self.h * .5:
                self.is_finished = True
                print("is finished", end='\r')

            if not self.maze.is_paused and not self.is_finished:
                if not self.is_first_run:
                    opposite_direction = self.maze.simple_path[self.maze.simple_path_position]
                    self.current_direction = self.maze.forward if opposite_direction == self.maze.forward else abs(
                        2 - opposite_direction)

                if lines is None and self.current_direction == self.maze.forward:
                    self.maze.add_turn(self.maze.backward)
                    self.current_direction = self.maze.backward
                    print("added_backward")

                if self.current_direction == self.maze.backward:
                    if are_turns_seen_rn[self.maze.forward] or are_turns_seen_rn[self.maze.backward]:
                        self.current_direction = self.maze.forward
                    if are_turns_seen_rn[self.maze.left]:
                        self.is_in_backwards_left_turn = True
                else:
                    self.is_in_backwards_left_turn = False

                if self.is_in_backwards_left_turn:
                    motor_steer = -2

                if ((self.current_direction == self.maze.left and not are_turns_seen_rn[self.maze.left]) or (
                        self.current_direction == self.maze.right and not are_turns_seen_rn[self.maze.right])) and (
                        are_turns_seen_rn[self.maze.forward] or are_turns_seen_rn[self.maze.backward]):
                    self.current_direction = self.maze.forward

                if self.current_direction == self.maze.forward:
                    if are_turns_seen_rn[self.maze.left]:
                        new_turn = self.maze.left
                        print("added_left")
                    elif are_turns_seen_rn[self.maze.forward] and are_turns_seen_rn[self.maze.right] \
                            and not self.saw_right_turn_last_frame:
                        self.saw_right_turn_last_frame = True
                        new_turn = self.maze.forward
                        print("added_forward")
                    elif are_turns_seen_rn[self.maze.right] and not are_turns_seen_rn[self.maze.forward]:
                        new_turn = self.maze.right
                        print("added_right")
                    else:
                        new_turn = None

                    if new_turn is not None:
                        if self.is_first_run:
                            self.maze.add_turn(new_turn)
                            self.current_direction = new_turn
                        else:
                            self.maze.simple_path_position -= 1

                if not are_turns_seen_rn[self.maze.right]:
                    self.saw_right_turn_last_frame = False

                # main driving part
                if self.current_direction == self.maze.left:
                    motor_steer = -2
                elif self.current_direction == self.maze.forward:
                    pos_to_mid = (self.w / 2 + (average_line_position - self.w)) / self.w * 2

                    # PID
                    self.pid.update(pos_to_mid)
                    motor_steer = - self.pid.output

                elif self.current_direction == self.maze.right:
                    motor_steer = 2
                elif self.current_direction == self.maze.backward:
                    if self.is_in_backwards_left_turn:
                        motor_steer = -2
                    else:
                        motor_steer = 2
                else:
                    print("something went horrible")

                self.motors.set_speed_from_speed_steer(.33, motor_steer)
            else:
                self.motors.set_speed(0, 0)

            cv2.putText(img_canny, 'directNr: ' + str(motor_steer), (5, 10), 0, .5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img_canny, 'direction: ' + self.maze.get_direction_string(self.current_direction),
                        (5, 30), 0, .5, (0, 0, 255), 1, cv2.LINE_AA)

            threading.Thread(target=self.store_image, args=(img_canny,)).start()


if __name__ == "__main__":
    MainClass()
