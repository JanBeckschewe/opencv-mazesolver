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

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img_canny, lines, num_black_pixels = opencv.modify_image(frame)

    averageLinePosition = w / 2

    are_turns_seen_rn = [False] * 4

    motor_steer = 0

    i = 0
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                averageLinePosition += ((x1 + x2) / 2 - averageLinePosition) / (i + 1)
                i += 1

                opencv.find_lines(img_canny, x1, y1, x2, y2, w, h,
                                  are_turns_seen_rn)

    # when reset from website
    if is_finished and len(maze.full_path) == 0:
        is_finished = False

    # when reached end
    if not is_finished and num_black_pixels > w * h * .5:
        is_finished = True
        print("is finished")

    if not maze.is_paused and not is_finished:
        if not is_first_run:
            opposite_direction = maze.simple_path[maze.simple_path_position]
            current_direction = maze.forward if opposite_direction == maze.forward else abs(2 - opposite_direction)

        if lines is None:
            if current_direction != maze.backward:
                maze.add_turn(maze.backward)
                current_direction = maze.backward

        if current_direction == maze.backward:
            if are_turns_seen_rn[maze.forward]:
                current_direction = maze.forward
            if are_turns_seen_rn[maze.left]:
                is_in_backwards_left_turn = True
        else:
            is_in_backwards_left_turn = False

        if is_in_backwards_left_turn:
            motor_steer = -2

        if ((current_direction == maze.left and not are_turns_seen_rn[maze.left]) or (
                current_direction == maze.right and not are_turns_seen_rn[maze.right])) and are_turns_seen_rn[maze.forward]:
            current_direction = maze.forward

        if current_direction == maze.forward:
            if are_turns_seen_rn[maze.left] and current_direction != maze.left:
                new_turn = maze.left
            elif are_turns_seen_rn[maze.forward] and are_turns_seen_rn[maze.right] and not saw_right_turn_last_frame:
                saw_right_turn_last_frame = True
                new_turn = maze.forward
            elif are_turns_seen_rn[maze.right] and current_direction != maze.right:
                new_turn = maze.right
            else:
                new_turn = None

            if new_turn is not None:
                if is_first_run:
                    maze.add_turn(new_turn)
                    current_direction = new_turn
                else:
                    maze.simple_path_position -= 1

        if not are_turns_seen_rn[maze.right]:
            saw_right_turn_last_frame = False

        # main driving part
        if current_direction == maze.left:
            motor_steer = -2
        elif current_direction == maze.forward:
            pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2

            motor_steer = pid_control.pid_drive(pos_to_mid)
        elif current_direction == maze.right:
            motor_steer = 2
        elif current_direction == maze.backward:
            if is_in_backwards_left_turn:
                motor_steer = -2
            else:
                motor_steer = 2
        else:
            print("something went horrible")

        motors.set_speed_from_speed_steer(.28, motor_steer)
    else:
        motors.set_speed(0, 0)

    cv2.imwrite("httpdocs/img.png", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
