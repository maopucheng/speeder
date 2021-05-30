import utime
from machine import Pin, SPI
import st7789

import vga1_bold_16x32 as font1
import vga1_bold_16x16 as font2


#初始化显示屏
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

def display(speed, distance=0 , seconds=0):
    
    global tft
    
    #line1:time    
    tft.text(font2, "time:", 5, 5+16, st7789.WHITE, st7789.BLACK)
    time_str = str(seconds//60)+'m'+str(seconds%60)+'s'
    tft.fill_rect(5+16*5, 5, 16*7, 32, st7789.BLACK)
    tft.text(font1, time_str, 5+16*5, 5,  st7789.WHITE, st7789.BLACK)
    #line2:speed
    tft.text(font1, "SPEED:", 5, 50, st7789.YELLOW, st7789.BLACK)
    tft.fill_rect(5+16*6, 50, 16*2, 32, st7789.BLACK)
    tft.text(font1, '{:0>2d}'.format(speed), 5+16*6, 50, st7789.YELLOW, st7789.BLACK)
    tft.text(font1, "KM/H", 5+16*8, 50, st7789.YELLOW, st7789.BLACK)
    #line3:distance
    tft.text(font2, "dist:", 5, 105, st7789.WHITE, st7789.BLACK)
    tft.fill_rect(5+16*5, 105-16, 16*5, 32, st7789.BLACK)
    tft.text(font1, '{:3.1f}'.format(distance), 5+16*5, 105-16, st7789.WHITE, st7789.BLACK)
    tft.text(font2, "KM", 5+16*10, 105, st7789.WHITE, st7789.BLACK)
  

while True:
    display(3,2,630)
    utime.sleep(1)
    display(20,12,30)
    utime.sleep(1)