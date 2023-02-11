import math
import time

from machine import Pin
from micropython import const

from rklib.servo import Servo

PWM_PIN = const(21)

p2 = Pin(2, Pin.OUT)
p2.off()

servo = Servo(PWM_PIN)

p2.on()

i = 0
while True:
    servo.angle(90 + 20 * math.sin(i * math.pi / 2))
    i = (i + 1) % 4
    time.sleep_ms(300)
