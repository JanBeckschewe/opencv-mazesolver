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
    # It fails when there is a crossing of lines but on a single line with not so strong curves it works
    # It can get optimized with PD control.

    averageLinePosition = w / 2
    i = 0

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                print("angle: ", linecalc.is_line_horizontal(x1, x2, y1, y2))
                if not linecalc.is_line_horizontal(x1, x2, y1, y2):
                    averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                    cv2.line(img_warped_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)
                else:
                    cv2.line(img_warped_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

        k = (w / 2 + (averageLinePosition - w)) / w / 2
        print("k: ", k)
        motors.set_speed_from_speed_steer(1, k)
    else:
        motors.set_speed_from_speed_steer(0, 0)

    cv2.imshow("Frame", img_warped_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
