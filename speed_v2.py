import utime
from machine import Pin

#初始化引脚
hall = Pin(36, Pin.IN)

# init 所有参数
speed = 0
position = False  # 磁铁位置：在感应区为T，不在感应区为F
i = 0  # 定义计数器
wheel_len = 2  # 自行车轮子周长，单位，米
last_time = utime.ticks_ms()  # 上次时间点
now = utime.ticks_ms()  # 当前时间点
time_gap = utime.ticks_diff(now, last_time)  # 两个时间点的时间差，单位毫秒

def getData():
    global speed, position, i, wheel_len
    global last_time, now, time_gap
    # 读取当前状态，status为0，表示有磁力感应到
    status = hall.value()

    if status == 0 and position == False:
        i += 1
        now = utime.ticks_ms()
        time_gap = utime.ticks_diff(now, last_time)  # 注意是毫秒
        if time_gap != 0:
            speed = int(wheel_len/(time_gap/1000)*3.6)
        last_time = now
        position = True  # 设置磁铁位置
        print(speed, "km/h")
    elif status == 1:
        position = False  # 设置磁铁位置
        utime.sleep_ms(20)

while True:
    getData()
