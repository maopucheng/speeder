"""
hello.py

    Writes "Hello!" in random colors at random locations on a
    LILYGO® TTGO T-Display.

    https://youtu.be/z41Du4GDMSY

"""
import random,time,st7789,random
from machine import Pin, SPI
from neopixel import NeoPixel
import vga1_bold_16x32 as font


def main():
    #显示屏初始化
    tft = st7789.ST7789(
        SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
        135,
        240,
        reset=Pin(23, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(4, Pin.OUT),
        rotation=3)
    tft.init()

    #led灯引脚定义
    led = Pin(21, Pin.OUT)  
    i,j = 0,0
    time.sleep(2)
    pin = Pin(22, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
    np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
    
    while True:
      
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(0)
            col_max = tft.width() - font.WIDTH*6
            row_max = tft.height() - font.HEIGHT
            num = j%8
            for r in range(8):
                np[r] = (0,0,0)
            np[num] = (random.randint(0,100), random.randint(0,100), random.randint(0,100)) # set the first pixel to white
            np.write()              # write data to all pixels
            i+=1
            j+=1                
            for _ in range(32):
                tft.text(
                    font,
                    "MaoTou",
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8)),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8))
                )
                time.sleep(0.02)
                
            if i %2 == 0:
                led.value(1)
            else:
                led.value(0) 
 
main()
