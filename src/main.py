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

is_finished = False

saw_right_turn_last_frame = False

current_direction = maze.forward

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img_canny, lines, num_black_pixels = opencv.modify_image(frame)

    averageLinePosition = w / 2

    are_turns_seen_rn = [False] * 4

    motor_steer = 0

    if not maze.is_paused:

        if is_finished and len(maze.full_path) == 0:
            is_finished = False

        if not is_finished and num_black_pixels > w * h * .35:
            is_finished = True
            print("is finished")

        if is_finished:
            pass
        elif lines is None:
            if not current_direction == maze.backward:
                maze.add_turn(maze.backward)
            motor_steer = 1
            current_direction = maze.backward
        else:
            i = 0
            for line in lines:
                for x1, y1, x2, y2 in line:
                    averageLinePosition += (((x1 + x2) / 2) - averageLinePosition) / (i + 1)

                    # TODO we need to check the bottom part aswell because otherwise it will e.g. go right
                    # TODO although there might be a left in the upper half of the image
                    if not linecalc.is_line_horizontal(x1, y1, x2, y2):
                        are_turns_seen_rn[maze.forward] = True
                        # green
                        cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    else:
                        if linecalc.contains_line_bottom_left(x1, y1, x2, y2, h, w):
                            are_turns_seen_rn[maze.left] = True
                            # blue
                            cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

                        if linecalc.contains_line_bottom_right(x1, y1, x2, y2, h, w):
                            are_turns_seen_rn[maze.right] = True
                            # red
                            cv2.line(img_canny, (x1, y1), (x2, y2), (0, 0, 255), 2)

            if current_direction == maze.backward:
                motor_steer = 1
                if are_turns_seen_rn[maze.forward]:
                    current_direction = maze.forward
                elif are_turns_seen_rn[maze.left]:
                    motor_steer = -1

            # TODO I think this should work but I'm not sure, please test this
            if ((current_direction == maze.right and not are_turns_seen_rn[maze.right]) \
                        or (current_direction == maze.right and not are_turns_seen_rn[maze.left])) \
                    and are_turns_seen_rn[maze.forward]:
                current_direction = maze.forward

            if are_turns_seen_rn[maze.left]:
                if not current_direction == maze.left:
                    maze.add_turn(maze.left)
                    current_direction = maze.left
                motor_steer = -1

            elif are_turns_seen_rn[maze.forward]:
                if are_turns_seen_rn[maze.right]:
                    if not saw_right_turn_last_frame:
                        maze.add_turn(maze.forward)
                        current_direction = maze.forward

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

            elif are_turns_seen_rn[maze.right]:
                if not current_direction == maze.right:
                    maze.add_turn(maze.right)
                    current_direction = maze.right
                motor_steer = 1
            else:
                print("something went wrong")

            if not are_turns_seen_rn[maze.right]:
                saw_right_turn_last_frame = False

        motors.set_speed_from_speed_steer(0 if is_finished else .4, motor_steer)

    else:
        motors.set_speed(0, 0)
        print("paused")

    cv2.imshow("Frame", img_canny)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
