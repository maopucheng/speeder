import utime
from machine import Pin, SPI
import st7789
from neopixel import NeoPixel
import vga1_bold_16x32 as font1
import vga1_bold_16x16 as font2

#初始化引脚
hall = Pin(36, Pin.IN)

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

#初始化LED灯带
pin = Pin(22, Pin.OUT)
np = NeoPixel(pin, 8)

# init 所有参数
g_speed = 0
g_position = False  # 磁铁位置：在感应区为T，不在感应区为F
g_count = 0  # 定义计数器
g_wheel_len = 3  # 自行车轮子周长，单位，米
g_last_time = utime.ticks_ms()  # 上次时间点
g_now = utime.ticks_ms()  # 当前时间点
g_time_gap = utime.ticks_diff(g_now, g_last_time)  # 两个时间点的时间差，单位毫秒
g_distance = 0 #骑行距离
first_time = g_now
g_time = 0 #骑行时间
g_triggertime = utime.ticks_ms() #上次触发时间
g_delta = 20 #触发最小间隔时间，单位毫秒
g_display = False #是否屏幕显示刷新标志位

def update_speed(_):
    global g_triggertime,g_delta  
    global g_speed, g_position, g_count, g_wheel_len
    global g_last_time, g_now, g_time_gap
    global g_distance, g_time  
    if utime.ticks_diff(utime.ticks_ms(),g_triggertime) > g_delta:        
        if (g_position==False):        
            print(g_count,utime.ticks_diff(utime.ticks_ms(),g_triggertime))
            g_count += 1
            g_now = utime.ticks_ms()
            g_time_gap = utime.ticks_diff(g_now, g_last_time)  # 注意是毫秒
            if g_time_gap != 0:
                g_speed = int(g_wheel_len/(g_time_gap/1000)*3.6)
            g_last_time = g_now
            g_position = True  # 设置磁铁位置
            g_distance = g_wheel_len*g_count/1000 #骑行距离，单位公里
            g_time = int(utime.ticks_diff(g_now, first_time)/1000) #骑行时长，单位秒  
            display(g_speed,g_distance,g_time) 
            hall.irq(update_speed,trigger=Pin.IRQ_FALLING)            
        else:
            #print("mark False")
            g_position = False 
            hall.irq(update_speed, trigger=Pin.IRQ_RISING)
    g_triggertime = utime.ticks_ms()



def display(speed, distance=0 , seconds=0):
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
    tft.text(font1, '{:2.2f}'.format(distance), 5+16*5, 105-16, st7789.WHITE, st7789.BLACK)
    tft.text(font2, "KM", 5+16*10, 105, st7789.WHITE, st7789.BLACK)

def led(speed):
    if speed<15:
        np[1] = (0,0,200)
    elif 15<speed<25:
        np[2] = (0,200,0)
    else:
        np[3] = (200,0,0)
    np.write()

#先初始化显示速度

display(0)
hall.irq(update_speed, trigger=Pin.IRQ_RISING)
while True:
    #getData()
    utime.sleep_ms(10)  # 设置抖动延时
    led(g_speed)

