from machine import Pin
from neopixel import NeoPixel

pin = Pin(22, Pin.OUT)
np = NeoPixel(pin, 8)
np[1] = (0, 0, 200)
np[2] = (100, 0, 0)
np.write()
