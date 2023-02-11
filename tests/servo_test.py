import math
import time

from machine import Pin
from micropython import const

from rklib.servo import Servo

HEAD_PIN = const(0)
LEFT_ARM_PIN = const(5)
RIGHT_ARM_PIN = const(4)
LEFT_LEG_PIN = const(14)
RIGHT_LEG_PIN = const(12)
LEFT_FOOT_PIN = const(13)
RIGHT_FOOT_PIN = const(15)

p2 = Pin(2, Pin.OUT)
p2.off()

servos = [Servo(HEAD_PIN), Servo(LEFT_ARM_PIN), Servo(RIGHT_ARM_PIN), Servo(LEFT_LEG_PIN), Servo(RIGHT_LEG_PIN),
          Servo(LEFT_FOOT_PIN), Servo(RIGHT_FOOT_PIN)]
for servo in servos:
    servo.angle(90)
    time.sleep_ms(300)

p2.on()

i = 0
while True:
    for servo in servos:
        servo.angle(90 + 20 * math.sin(i * math.pi / 2))
        i = (i + 1) % 4
        time.sleep_ms(300)
