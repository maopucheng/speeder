import time
from machine import Pin

# 定义一个输出针脚
led = Pin(21, Pin.OUT)  

while True:
    led.value(1)  # 高电平，开
    time.sleep(1)
    led.value(0)  # 低电平，关
    time.sleep(1)
