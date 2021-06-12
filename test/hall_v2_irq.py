import utime
from machine import Pin

#定义一个针脚，输入信号
hall = Pin(36, Pin.IN)
g_count = 0 #计数器
g_position = False  # 磁铁位置：在感应区为T，不在感应区为F
g_triggertime = utime.ticks_ms() #上次触发时间
g_delta = 20 #触发最小间隔时间，单位毫秒

def count(_):
    global g_count,g_triggertime,g_delta,g_position    
    if utime.ticks_diff(utime.ticks_ms(),g_triggertime) > g_delta:        
        if (g_position==False):        
            print(g_count,utime.ticks_diff(utime.ticks_ms(),g_triggertime))
            g_count += 1
            g_position = True 
            hall.irq(count,trigger=Pin.IRQ_FALLING)
        else:
            #print("mark False")
            g_position = False 
            hall.irq(count, trigger=Pin.IRQ_RISING)
    g_triggertime = utime.ticks_ms()

print("start")
#首次调用            
hall.irq(count, trigger=Pin.IRQ_RISING)
