import time
from machine import Pin

b2 = Pin(0, Pin.IN)
i = 0

triggertime = time.ticks_ms()
delta = 200

print(triggertime-delta)

#while True:
def my_func(_):    
    global i,triggertime,delta
    if (time.ticks_ms()-triggertime) > delta:
        i += 1
        triggertime = time.ticks_ms()
        print(i)
            
b2.irq(my_func, trigger=Pin.IRQ_FALLING, wake=None)

