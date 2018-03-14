import cv2
import numpy as np
import yaml

with open("camera_calibration_values.yaml") as calibration_matrix:
    cal_mat = yaml.load(calibration_matrix)

np_camera_matrix = np.array(cal_mat['camera_matrix'])
np_distortion_coefficients = np.array(cal_mat['distortion_coefficients'])


def modify_image(frame):
    img = frame.array
    img = cv2.rotate(img, 1)
    img = cv2.undistort(img, np_camera_matrix, np_distortion_coefficients)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_sharpened = cv2.addWeighted(img_gray, 1.5, img_blurred, -0.5, 0)

    img_canny = cv2.Canny(img_sharpened, 130, 190)

    lines = cv2.HoughLinesP(image=img_canny, rho=1, theta=np.pi / 180, threshold=20, minLineLength=30,
                            maxLineGap=10)

    num_black_pixels = img_sharpened.size - cv2.countNonZero(img_sharpened)

    img_sharpened = cv2.cvtColor(img_sharpened, cv2.COLOR_GRAY2BGR)
    # img_canny = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)

    return img_sharpened, lines, num_black_pixels
