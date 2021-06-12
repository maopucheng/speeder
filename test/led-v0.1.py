from machine import Pin
from neopixel import NeoPixel
import utime

pin = Pin(22, Pin.OUT, Pin.PULL_UP)
np = NeoPixel(pin, 8)
while True:
    np[1] = (0, 0, 200)
    np[2] = (100, 0, 0)
    np.write()
    utime.sleep_ms(300)
