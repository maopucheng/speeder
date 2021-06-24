import utime
from machine import Pin, SPI
import st7789
from neopixel import NeoPixel
import vga1_bold_16x32 as font1
import vga1_bold_16x16 as font2

#初始化霍尔传感器输入引脚
#经过测试，改良为干簧管
hall = Pin(36, Pin.IN)

#初始化LED灯带输出引脚
pin = Pin(22, Pin.OUT, Pin.PULL_UP)
np = NeoPixel(pin, 8)

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



# init其他所有参数
WHEEL_LEN = 10  # 常量，自行车轮子周长，单位，米

g_speed = 0
g_position = False  # 磁铁位置：在感应区为T，不在感应区为F
g_count = 0  # 定义计数器
g_last_time = utime.ticks_ms()  # 上次时间点
now = utime.ticks_ms()  # 当前时间点
g_time_gap = utime.ticks_diff(now, g_last_time)  # 两个时间点的时间差，单位毫秒
g_distance = 0 #骑行距离
g_first_time = now
g_time = 0 #骑行时间
g_break = False

def getData():
    global g_speed, g_position, g_count, WHEEL_LEN
    global g_last_time, now, g_time_gap
    global g_distance, g_time, g_break
    # 读取当前状态，status为0，表示有磁力感应到
    status = hall.value()

    if status == 0 and g_position == False:
        g_count += 1
        now = utime.ticks_ms()
        g_time_gap = utime.ticks_diff(now, g_last_time)  # 注意是毫秒
        if g_time_gap != 0:
            now_speed = int(WHEEL_LEN/(g_time_gap/1000)*3.6)
            if now_speed<(g_speed-2): #刹车了
                g_break = True
            else:
                g_break = False
            g_speed = now_speed
        g_last_time = now
        g_position = True  # 设置磁铁位置
        g_distance = WHEEL_LEN*g_count #骑行距离
        print(g_speed, "km/h", "i=", g_count, g_break)
        g_time = utime.ticks_diff(now, g_first_time)   
        display(g_speed,g_distance/1000,int(g_time/1000))     
    elif status == 1:
        g_position = False  # 设置磁铁位置

def display(speed, distance=0 , seconds=0):
  
    #line1:time    
    tft.text(font2, "time:", 5, 5+16, st7789.WHITE, st7789.BLACK)
    time_str = str(seconds//60)+'m'+str(seconds%60)+'s'
    tft.fill_rect(5+16*5, 5, 16*7, 32, st7789.BLACK)
    tft.text(font1, time_str, 5+16*5, 5,  st7789.WHITE, st7789.BLACK)
    #line2:speed
    tft.text(font1, "SPEED:", 5, 50, st7789.YELLOW, st7789.BLACK)
    tft.fill_rect(5+16*6, 50, 16*2, 32, st7789.BLACK)
    tft.text(font1, '{:0>2.1f}'.format(speed), 5+16*6, 50, st7789.YELLOW, st7789.BLACK)
    tft.text(font1, "KM/H", 5+16*10, 50, st7789.YELLOW, st7789.BLACK)
    #line3:distance
    tft.text(font2, "dist:", 5, 105, st7789.WHITE, st7789.BLACK)
    tft.fill_rect(5+16*5, 105-16, 16*5, 32, st7789.BLACK)
    tft.text(font1, '{:2.2f}'.format(distance), 5+16*5, 105-16, st7789.WHITE, st7789.BLACK)
    tft.text(font2, "KM", 5+16*10, 105, st7789.WHITE, st7789.BLACK)

def my_sleep_ms(ms):
    for i in range(ms//10):
        utime.sleep_ms(10)
        getData()

def run_led(speed):
    global np
    n = np.n
    if g_break: #刹车红灯警示
        for i in range(2): 
            np.fill((0,0,0))
            np.write()
            my_sleep_ms(100)
            np.fill((128,0,0))
            np.write()
            my_sleep_ms(100)
    else: #速度灯效
        if speed<10:
            #彩虹
            for j in range(16): #按顺序移动灯色
                for i in range(n): #设置每个灯的彩虹色，将256色平均分
                    rc_index = (i * 256 // n) + int(j*16)
                    np[i] = color_map(rc_index & 255)
                np.write()
                my_sleep_ms(50) #移动速度
        elif 10<=speed<20:
            # 滚珠
            for i in range(4 * n):
                for j in range(n):
                    np[j] = (0, 0, 0)
                np[i % n] = (255, 255, 255)
                np.write()
                my_sleep_ms(30)
        elif speed>=20:
            # 弹球
            for i in range(4 * n):
                for j in range(n):
                    np[j] = (0, 100, 0)
                if (i // n) % 2 == 0:
                    np[i % n] = (0, 0, 0)
                else:
                    np[n - 1 - (i % n)] = (0, 0, 0)
                np.write()
                my_sleep_ms(50)

#辅助函数，将灯分成256个颜色，类似HSB模式
def color_map(pos): 
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

display(0)
while True:
    run_led(g_speed)
    # for i in range(256):
    #     np.fill(color_map(i))
    #     np.write()
    #     utime.sleep_ms(100)
