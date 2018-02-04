# this code will never ever get touched by anybody.

from enum import IntEnum

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Pin(IntEnum):
    LB = 23
    LF = 21
    RB = 16
    RF = 18


def setup_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 1000)
    pwm.start(0)

    return pwm


class Motor:

    def __init__(self, pin_fw, pin_bw):
        self.pwm_fw = setup_gpio(pin_fw)
        self.pwm_bw = setup_gpio(pin_bw)

    def speed(self, speed):
        speed = min(1, (max(-1, speed)))

        if speed >= 0:
            self.pwm_bw.ChangeDutyCycle(0)
            self.pwm_fw.ChangeDutyCycle(speed * 100)
        if speed < 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(abs(speed * 100))


left_motor = Motor(Pin.LF, Pin.LB)
right_motor = Motor(Pin.RF, Pin.RB)


def set_speed(left, right):
    left_motor.speed(left)
    right_motor.speed(right)


def set_speed_from_speed_steer(speed, steer):
    set_speed(left=min(1.0, max(-1.0, speed + speed * steer)), right=min(1.0, max(-1.0, speed - speed * steer)))
