import time

pconst, iconst, dconst = 1., .3, 0.
integral = 0
last_error = 0
last_time = time.time()


def pid_drive(pos_to_mid):
    global motor_steer, last_error, last_time, integral

    # PD control
    motor_steer = pconst * pos_to_mid \
                  + dconst * (pos_to_mid - last_error)
    last_error = pos_to_mid

    return motor_steer

    # # PID Control
    # # TODO needs some tweaking to work better
    # current_time = time.time()
    # delta_time = current_time - last_time
    # delta_error = pos_to_mid - last_error
    # integral += pos_to_mid * delta_time
    # integral = min(1., max(-1., integral))
    # pos_to_mid = (w / 2 + (averageLinePosition - w)) / w * 2
    # motor_steer = pconst * pos_to_mid \
    #               + dconst * (delta_error / delta_time) \
    #               + iconst * integral
    # last_error = pos_to_mid
    # last_time = current_time
