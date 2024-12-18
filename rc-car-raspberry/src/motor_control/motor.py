from adafruit_servokit import ServoKit

class MotorControl:
    def __init__(self):
        self.kit = ServoKit(channels=16)

    def set_servo_angle(self, channel, angle):
        print(f"Setze Servo {channel} auf Winkel {angle}")
        self.kit.servo[channel].angle = angle

    def set_throttle(self, channel, throttle):
        print(f"Setze Motor {channel} auf Geschwindigkeit {throttle}")
        self.kit.continuous_servo[channel].throttle = throttle