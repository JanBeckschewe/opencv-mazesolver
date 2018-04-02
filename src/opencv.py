import cv2
import numpy as np

import linecalc
import maze

np_camera_matrix = np.array([[47., 0., 70.], [0., 93., 48.], [0., 0., 1.]])
np_distortion_coefficients = np.array([-3.0048e-01, 8.4940e-02, -3.5780e-03, -2.08614e-03, -1.0185e-02])


def modify_image(frame):
    img = frame.array
    img = cv2.rotate(img, 1)
    img = cv2.undistort(img, np_camera_matrix, np_distortion_coefficients)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_sharpened = cv2.addWeighted(img_gray, 1.5, img_blurred, -0.5, 0)

    img_canny = cv2.Canny(img_sharpened, 130, 190)

    lines = cv2.HoughLinesP(image=img_canny,
                            rho=1,
                            theta=np.pi / 180,
                            threshold=20,
                            minLineLength=30,
                            maxLineGap=10)

    img_black_thres = cv2.inRange(img_sharpened, 0, 50)

    num_black_pixels = cv2.countNonZero(img_black_thres)

    return cv2.cvtColor(img_sharpened, cv2.COLOR_GRAY2BGR), lines, num_black_pixels


def find_lines(img_canny, x1, y1, x2, y2, w, h, are_turns_seen_rn):
    # TODO we need to check the bottom part as well because
    # TODO otherwise it will e.g. go right although there
    # TODO might be a left in the upper half of the image
    if not linecalc.is_line_horizontal(x1, y1, x2, y2):
        are_turns_seen_rn[maze.forward] = True
        # green
        cv2.line(img_canny,
                 (x1, y1), (x2, y2), (0, 255, 0), 2)

    else:
        if linecalc.contains_line_bottom_left(
                x1, y1, x2, y2, h, w):
            are_turns_seen_rn[maze.left] = True
            # red
            cv2.line(img_canny,
                     (x1, y1), (x2, y2), (255, 0, 0), 2)

        if linecalc.contains_line_bottom_right(
                x1, y1, x2, y2, h, w):
            are_turns_seen_rn[maze.right] = True
            # blue
            cv2.line(img_canny,
                     (x1, y1), (x2, y2), (0, 0, 255), 2)
