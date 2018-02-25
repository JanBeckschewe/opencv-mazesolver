import time

import cv2
import numpy as np
import yaml
from picamera import PiCamera
from picamera.array import PiRGBArray

import linecalc
import motors

with open("camera_calibration_values.yaml") as calibration_matrix:
    cal_mat = yaml.load(calibration_matrix)

np_camera_matrix = np.array(cal_mat['camera_matrix'])
np_distortion_coefficients = np.array(cal_mat['distortion_coefficients'])

w, h = 600, 450

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    img = cv2.rotate(img, 1)
    img = cv2.undistort(img, np_camera_matrix, np_distortion_coefficients)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_masked = cv2.inRange(img, 0, 50)

    img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_sharpened = cv2.addWeighted(img_gray, 1.5, img_blurred, -0.5, 0)

    img_canny = cv2.Canny(img_sharpened, 30, 60)

    lines = cv2.HoughLinesP(image=img_canny, rho=1, theta=np.pi / 180, threshold=60, minLineLength=50,
                            maxLineGap=10)

    img_canny = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)

    averageLinePosition = w / 2
    i = 0
    is_horizontal_line_near = False
    is_horizontal_line_left = False

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if linecalc.is_line_horizontal(x1, x2, y1, y2):
                    is_horizontal_line_near = True

                    # does not actually work because the turn will start too early and only find the new line back after
                    # about 20 to 30 cm, which is way too much for our small maze
                    # can maybe get solved with a delay
                    if (x1 < w * .4 or x2 < w * .4) and (y1 > h * .85 or y2 > h * .85):
                        is_horizontal_line_left = True

                    cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                else:
                    averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                    cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if is_horizontal_line_near and is_horizontal_line_left:
            motors_steer = -1
        else:
            motors_steer = (w / 2 + (averageLinePosition - w)) / w * 2

        print(motors_steer)
        motors.set_speed_from_speed_steer(1, motors_steer)
    else:
        motors.set_speed_from_speed_steer(0, 0)

    cv2.imshow("Frame", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
