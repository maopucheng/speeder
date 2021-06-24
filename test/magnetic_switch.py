from machine import Pin
import utime

pin36 = Pin(36, Pin.IN, Pin.PULL_UP)

# init其他所有参数
WHEEL_LEN = 2  # 常量，自行车轮子周长，单位，米

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

def get_count():
    global g_speed, g_position, g_count, WHEEL_LEN
    global g_last_time, now, g_time_gap
    global g_distance, g_time, g_break
    # 读取当前状态，status为0，表示有磁力感应到
    status = pin36.value()

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
  
    elif status == 1:
        g_position = False  # 设置磁铁位置

while True:
    get_count()
