import time
from machine import Pin

print("Hello World")
# ledPin = Pin(2, Pin.OUT)  # Wemos D1 mini
ledPin = Pin(15, Pin.OUT)  # Wemos S2 mini
# ledPin = Pin(22, Pin.OUT)  # Wemos D32

while True:
    ledPin.on()
    time.sleep_ms(1000)
    ledPin.off()
    time.sleep_ms(1000)
