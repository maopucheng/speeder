import utime
import utime as t
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

#初始化引脚
hall = Pin(36, Pin.IN)

# init 所有参数
speed = 0
position = False  # 磁铁位置：在感应区为T，不在感应区为F
i = 0  # 定义计数器
wheel_len = 2  # 自行车轮子周长，单位，米
last_time = t.ticks_ms()  # 上次时间点
now = t.ticks_ms()  # 当前时间点
time_gap = t.ticks_diff(now, last_time)  # 两个时间点的时间差，单位毫秒

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

def getData():
    global speed, position, i, wheel_len
    global last_time, now, time_gap
    # 读取当前状态，status为0，表示有磁力感应到
    status = hall.value()

    if status == 0 and position == False:
        i += 1
        now = t.ticks_ms()
        time_gap = t.ticks_diff(now, last_time)  # 注意是毫秒
        if time_gap != 0:
            speed = int(wheel_len/(time_gap/1000)*3.6)
        last_time = now
        position = True  # 设置磁铁位置
        print(speed, "km/h")
    elif status == 1:
        position = False  # 设置磁铁位置
        t.sleep_ms(20)

while True:
    getData()
    display(speed,10,500)
    utime.sleep_ms(50)
