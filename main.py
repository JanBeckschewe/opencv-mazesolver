import time

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

import linecalc
import motors

w, h = 600, 450

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    img = cv2.rotate(img, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    src = np.array([[.36 * w, .65 * h], [.64 * w, .65 * h], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

    img_warped = cv2.warpPerspective(img_gray, cv2.getPerspectiveTransform(src, dst), (w, h))
    img_warped_masked = cv2.inRange(img_warped, 0, 65)

    img_warped_blurred = cv2.GaussianBlur(img_warped_masked, (15, 15), 0)
    img_warped_sharpened = cv2.addWeighted(img_warped_masked, 1.5, img_warped_blurred, -0.5, 0)

    img_warped_canny = cv2.Canny(img_warped_sharpened, 30, 60)

    lines = cv2.HoughLinesP(image=img_warped_canny, rho=1, theta=np.pi / 180, threshold=60, minLineLength=50,
                            maxLineGap=10)

    img_warped_canny = cv2.cvtColor(img_warped_canny, cv2.COLOR_GRAY2BGR)

    # Finds the line in the most simplistic possible way:
    # Look for the side of the image where more lines start and end on and move in that direction.
    # ̶i̶̶t̶̶ ̶̶f̶̶a̶̶i̶̶l̶̶s̶̶ ̶̶w̶̶h̶̶e̶̶n̶̶ ̶̶t̶̶h̶̶e̶̶r̶̶e̶̶ ̶̶i̶̶s̶̶ ̶̶a̶̶ ̶̶c̶̶r̶̶o̶̶s̶̶s̶̶i̶̶n̶̶g̶̶ ̶̶o̶̶f̶̶ ̶̶l̶̶i̶̶n̶̶e̶̶s̶ but on a single line with not so strong curves it works
    # ̶i̶̶t̶̶ ̶̶c̶̶a̶̶n̶̶ ̶̶g̶̶e̶̶t̶̶ ̶̶o̶̶p̶̶t̶̶i̶̶m̶̶i̶̶z̶̶e̶̶d̶̶ ̶̶w̶̶i̶̶t̶̶h̶̶ ̶̶p̶̶d̶̶ ̶̶c̶̶o̶̶n̶̶t̶̶r̶̶o̶̶l̶̶.̶

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

                    cv2.line(img_warped_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                else:
                    averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                    cv2.line(img_warped_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if is_horizontal_line_near and is_horizontal_line_left:
            motors_steer = -1
        else:
            motors_steer = (w / 2 + (averageLinePosition - w)) / w * 2

        print(motors_steer)
        motors.set_speed_from_speed_steer(1, motors_steer)
    else:
        motors.set_speed_from_speed_steer(0, 0)

    cv2.imshow("Frame", img_warped_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
