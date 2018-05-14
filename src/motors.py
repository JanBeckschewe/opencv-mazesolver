from enum import IntEnum

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Pin(IntEnum):
    LB = 23
    LF = 21
    RB = 16
    RF = 18


class Motor:
    def __init__(self, pin_fw, pin_bw):
        self.pwm_fw = self.setup_gpio(pin_fw)
        self.pwm_bw = self.setup_gpio(pin_bw)

    def setup_gpio(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 1000)
        pwm.start(0)

        return pwm

    def speed(self, speed):
        speed = min(1, (max(-1, speed)))

        if speed >= 0:
            self.pwm_bw.ChangeDutyCycle(0)
            self.pwm_fw.ChangeDutyCycle(speed * 100)
        if speed < 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(abs(speed * 100))


class Motors:
    def __init__(self):
        self.left_motor = Motor(Pin.LF, Pin.LB)
        self.right_motor = Motor(Pin.RF, Pin.RB)

    def set_speed(self, left, right):
        self.left_motor.speed(left)
        self.right_motor.speed(right)

    def set_speed_from_speed_steer(self, speed, steer):
        self.set_speed(left=min(1.0, max(-1.0, speed + speed * steer)),
                       right=min(1.0, max(-1.0, speed - speed * steer)))
