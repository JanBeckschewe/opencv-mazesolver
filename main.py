import time

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
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

    src = np.array([[.36 * w, .65 * h], [.64 * w, .65 * h], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

    img_smooth = cv2.GaussianBlur(img, (5, 5), 0)
    img_trans = cv2.warpPerspective(img_smooth, cv2.getPerspectiveTransform(src, dst), (w, h))
    img_trans_gray = cv2.cvtColor(img_trans, cv2.COLOR_BGR2GRAY)

    img_trans_canny = cv2.Canny(img_trans_gray, 100, 200)

    lines = cv2.HoughLinesP(image=img_trans_canny, rho=1, theta=np.pi / 180, threshold=60, minLineLength=50,
                            maxLineGap=10)

    averageLinePosition = w / 2
    i = 0

    # Finds the line in the most simplistic possible way:
    # Look for the side of the image where more lines start and end on and move in that direction.
    # It fails when there is a crossing of lines but on a single line with not so strong curves it works
    # It can get optimized with PD control.

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                averageLinePosition = averageLinePosition + (((x1 + x2) / 2) - averageLinePosition) / (i + 1)
                print("avgline: ", averageLinePosition)
                cv2.line(img_trans, (x1, y1), (x2, y2), (0, 255, 0), 2)

        k = (w / 2 + (averageLinePosition - w)) / w / 2
        print("k: ", k)
        motors.set_speed_from_speed_steer(1, k)
    else:
        motors.set_speed_from_speed_steer(0, 0)

    cv2.imshow("Frame", img_trans)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
