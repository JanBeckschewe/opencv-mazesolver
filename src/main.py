import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import linecalc
import maze
import motors
import opencv

pconst, iconst, dconst = 1., 0., 0.
integral = 0
last_error = 0
last_time = time.time()

w, h = 160, 120

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 40

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

is_in_backwards_turn = False
is_in_left_turn = False
is_in_right_turn = False
is_seeing_right_turn = False

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img_canny, lines = opencv.modify_image(frame)

    averageLinePosition = w / 2
    i = 0
    is_horizontal_line_right = False
    is_horizontal_line_left = False
    is_vertical_line = False

    motor_steer = 0

    if lines is None:
        if not is_in_backwards_turn:
            maze.add_turn(maze.backward)
        motor_steer = 1
        is_in_backwards_turn = True
    else:
        for line in lines:
            for x1, y1, x2, y2 in line:
                averageLinePosition += (((x1 + x2) / 2) - averageLinePosition) / (i + 1)

                if not linecalc.is_line_horizontal(x1, y1, x2, y2):
                    is_vertical_line = True
                    # green
                    cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

                else:
                    if linecalc.contains_line_bottom_left(x1, y1, x2, y2, h, w):
                        is_horizontal_line_left = True
                        # blue
                        cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    if linecalc.contains_line_bottom_right(x1, y1, x2, y2, h, w):
                        is_horizontal_line_right = True
                        # red
                        cv2.line(img_canny, (x1, y1), (x2, y2), (0, 0, 255), 2)

        k = 0
        if is_in_backwards_turn:
            k += 1
            print("is_in_backwards_turn")
        if is_in_right_turn:
            k += 1
            print("is_in_right_turn")
        if is_in_left_turn:
            k += 1
            print("is_in_left_turn")

        if k > 1:
            print("alert")

        if is_in_backwards_turn:
            motor_steer = 1
            if is_vertical_line:
                is_in_backwards_turn = False
            elif is_horizontal_line_left:
                motor_steer = -1

        if not is_in_backwards_turn:
            if is_in_left_turn and is_vertical_line:
                is_in_left_turn = False

            if is_in_right_turn and is_vertical_line:
                is_in_right_turn = False

            if is_horizontal_line_left:
                if not is_in_left_turn:
                    maze.add_turn(maze.left)
                    is_in_left_turn = True
                motor_steer = -1

            elif is_vertical_line:
                if is_horizontal_line_right:
                    if not is_seeing_right_turn:
                        maze.add_turn(maze.forward)
                        is_seeing_right_turn = True

                pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2

                # PD control
                motor_steer = pconst * pos_to_mid + dconst * (pos_to_mid - last_error)
                last_error = pos_to_mid

                # PID Control
                # does not work yet, will maybe work later
                # current_time = time.time()
                # delta_time = current_time - last_time
                # delta_error = pos_to_mid - last_error
                # integral += pos_to_mid * delta_time
                # integral = min(1., max(-1., integral))
                # pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2
                # motor_steer = pconst * pos_to_mid + dconst * (delta_error / delta_time) + iconst * integral
                # last_error = pos_to_mid
                # last_time = current_time

            elif is_horizontal_line_right:
                if not is_in_right_turn:
                    maze.add_turn(maze.right)
                    is_in_right_turn = True
                motor_steer = 1
            else:
                print("this should never happen, something is wrong")

        print(motor_steer)
        motors.set_speed_from_speed_steer(.4, motor_steer)

    cv2.imshow("Frame", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
