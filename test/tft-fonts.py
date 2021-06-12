"""
fonts.py
    Pages through all characters of four fonts on the LILYGO® TTGO T-Display.
    https://www.youtube.com/watch?v=2cnAhEucPD4
"""
import utime
from machine import Pin, SPI
import st7789

import vga1_16x16 as small_font
import vga1_bold_16x32 as large_font
import inconsolata_64 as font_64

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
    # col = 0
    # line = 0
    # tft.text(small_font, "distance", col+30, line, st7789.WHITE, st7789.BLUE)
    # tft.text(large_font, "speed:001", col+30+small_font.WIDTH, line+small_font.HEIGHT, st7789.WHITE, st7789.RED)
    tft.text(font_64, "speed:001", 60, 60, st7789.WHITE, st7789.BLACK)
    # for font in (small_font, large_font):
    #     tft.fill(st7789.BLACK)
    #     line = 0
    #     col = 0
    #     for char in range(font.FIRST, font.LAST):
    #         tft.text(font, chr(char), col, line, st7789.WHITE, st7789.BLACK)
    #         col += font.WIDTH
    #         if col > tft.width() - font.WIDTH:
    #             col = 0
    #             line += font.HEIGHT

    #             if line > tft.height()-font.HEIGHT:
    #                 utime.sleep(3)
    #                 tft.fill(st7789.BLACK)
    #                 line = 0
    #                 col = 0
    # utime.sleep(3)


while True:
    display(10)