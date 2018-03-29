#!/usr/bin/env python3
import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import maze
import motors
import opencv
import pid_control

w, h = 128, 96

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 40
camera.exposure_mode = "off"

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

is_first_run = True
is_finished = False

is_in_backwards_left_turn = False

saw_right_turn_last_frame = False

current_direction = maze.forward

for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):

    img_canny, lines, num_black_pixels = opencv.modify_image(frame)

    averageLinePosition = w / 2

    are_turns_seen_rn = [False] * 4

    motor_steer = 0

    i = 0
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                averageLinePosition += ((x1 + x2) / 2
                                        - averageLinePosition) / (i + 1)
                i += 1

                opencv.find_lines(img_canny, x1, y1, x2, y2, w, h,
                                  are_turns_seen_rn)

    if not maze.is_paused:
        if not is_first_run:
            oppsite_direction = maze.simple_path[maze.simple_path_position]
            current_direction = maze.forward \
                if oppsite_direction == maze.forward \
                else abs(2 - oppsite_direction)

        # when reset from website
        if is_finished and len(maze.full_path) == 0:
            is_finished = False

        # when reached end
        if not is_finished and num_black_pixels > w * h * .5:
            is_finished = True
            print("is finished")

        if is_finished:
            pass
        elif lines is None:
            if not current_direction == maze.backward:
                maze.add_turn(maze.backward)
            motor_steer = 2
            current_direction = maze.backward

        else:
            if current_direction == maze.backward:
                motor_steer = 2
                if are_turns_seen_rn[maze.forward]:
                    current_direction = maze.forward
                elif are_turns_seen_rn[maze.left] or is_in_backwards_left_turn:
                    is_in_backwards_left_turn = True
                    motor_steer = -2
            else:
                is_in_backwards_left_turn = False

            if ((current_direction == maze.right
                 and not are_turns_seen_rn[maze.right])
                or (current_direction == maze.right
                    and not are_turns_seen_rn[maze.left])) \
                    and are_turns_seen_rn[maze.forward]:
                current_direction = maze.forward

            if are_turns_seen_rn[maze.left]:
                if not current_direction == maze.left:
                    if is_first_run:
                        maze.add_turn(maze.left)
                    else:
                        maze.simple_path_position -= 1
                    current_direction = maze.left
                motor_steer = -2
            elif are_turns_seen_rn[maze.forward]:
                if are_turns_seen_rn[maze.right]:
                    if not saw_right_turn_last_frame:
                        if is_first_run:
                            maze.add_turn(maze.forward)
                            current_direction = maze.forward
                        else:
                            maze.simple_path_position -= 1

                pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2

                motor_steer = pid_control.pid_drive(pos_to_mid)
            elif are_turns_seen_rn[maze.right]:
                if not current_direction == maze.right:
                    if is_first_run:
                        maze.add_turn(maze.right)
                        current_direction = maze.right
                    else:
                        maze.simple_path_position -= 1
                motor_steer = 2
            else:
                print("something went wrong")

            if not are_turns_seen_rn[maze.right]:
                saw_right_turn_last_frame = False

        motors.set_speed_from_speed_steer(
            0 if is_finished else .4, motor_steer)

    else:
        motors.set_speed(0, 0)

    cv2.imwrite("httpdocs/img.png", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
