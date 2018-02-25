import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import cv_stuff
import linecalc
import motors

proportional_const, derivate_const = 0.2, 1
last_error = 0

w, h = 640, 480

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img_canny, lines = cv_stuff.modify_image(frame)

    averageLinePosition = w / 2
    i = 0
    is_horizontal_line_near = False
    is_horizontal_line_left = False

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if linecalc.is_line_horizontal(x1, x2, y1, y2):
                    is_horizontal_line_near = True

                    if (x1 < w * .4 or x2 < w * .4) and (y1 > h * .5 or y2 > h * .5):
                        is_horizontal_line_left = True

                    # draw a blue line for horizontal lines
                    cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                else:
                    averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                    # draw a green line for vertical lines
                    cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if is_horizontal_line_near and is_horizontal_line_left:
            motor_steer = -1
        else:
            # PD control
            pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2
            motor_steer = proportional_const * pos_to_mid + derivate_const * (pos_to_mid - last_error)
            last_error = pos_to_mid

        print(motor_steer)
        motors.set_speed_from_speed_steer(.35, motor_steer)
    else:
        motors.set_speed_from_speed_steer(0, 0)

    cv2.imshow("Frame", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
