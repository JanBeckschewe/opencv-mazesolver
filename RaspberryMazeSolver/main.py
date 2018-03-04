import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from RaspberryMazeSolver import cv_stuff
from RaspberryMazeSolver import linecalc
from RaspberryMazeSolver import motors

left, right, forward, backward = range(4)
direction = forward
simple_path = []
simple_path_position = 0
path = []
path_position = 0

start = 0

proportional_const, derivate_const = 0.2, 1
last_error = 0

w, h = 640, 480

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    end = time.clock()
    img_canny, lines = cv_stuff.modify_image(frame)

    averageLinePosition = w / 2
    i = 0
    # noinspection PyRedeclaration
    is_horizontal_line_right = False
    is_horizontal_line_left = False
    # noinspection PyRedeclaration
    is_vertical_line = False

    if lines is None:
        path.append(backward)
    else:
        for line in lines:
            for x1, y1, x2, y2 in line:
                averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                if linecalc.is_line_horizontal(x1, x2, y1, y2) and linecalc.is_line_left(x1, x2, y1, y2, h, w):
                    is_horizontal_line_left = True

                    # draw a blue line for left horizontal lines
                    cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                if linecalc.is_line_horizontal(x1, x2, y1, y2) and linecalc.is_line_right(x1, x2, y1, y2, h, w):
                    is_horizontal_line_right = True

                    # draw a red line for right horizontal lines
                    cv2.line(img_canny, (x1, y1), (x2, y2), (0, 0, 255), 2)

                if linecalc.is_line_vertical(x1, x2, y1, y2):
                    is_vertical_line = True

                    # draw a green line for vertical lines
                    cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if is_horizontal_line_left:
            if end - start > 3 or start == 0:
                path.append(left)
                start = time.clock()
            motor_steer = -1

        elif is_vertical_line and is_horizontal_line_right:
            if end - start > 3 or start == 0:
                path.append(forward)
                start = time.clock()
            pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2
            motor_steer = proportional_const * pos_to_mid + derivate_const * (pos_to_mid - last_error)
            last_error = pos_to_mid

        elif is_horizontal_line_right:
            if end - start > 3 or start == 0:
                path.append(right)
                start = time.clock()
            motor_steer = 1

        else:
            pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2
            motor_steer = proportional_const * pos_to_mid + derivate_const * (pos_to_mid - last_error)
            last_error = pos_to_mid

        print(motor_steer)
        motors.set_speed_from_speed_steer(.35, motor_steer)

        cv2.imshow("Frame", img_canny)
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
            break



