import time

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

w, h = 600, 450

camera = PiCamera()
camera.resolution = (w, h)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(w, h))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    img = cv2.rotate(img, 1)

    img_edges = cv2.Canny(img, 100, 200)

    src = np.array([[.36 * w, .65 * h], [.64 * w, .65 * h], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

    img_trans = cv2.warpPerspective(img, cv2.getPerspectiveTransform(src, dst), (w, h))

    img_trans_gray = cv2.cvtColor(img_trans, cv2.COLOR_BGR2GRAY)
    img_trans_thres = cv2.adaptiveThreshold(img_trans_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,
                                            2)
    lines = cv2.HoughLinesP(image=img_trans_thres, rho=1, theta=np.pi / 180, threshold=16, minLineLength=50, maxLineGap=10)

    number_of_lines = 0

    for line in lines:
        for x1, y1, x2, y2 in line:
            number_of_lines = number_of_lines + 1
            cv2.line(img_trans_thres, (x1, y1), (x2, y2), (0, 255, 0), 2)

    print(number_of_lines)
    cv2.imshow("Frame", img_trans_thres)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
