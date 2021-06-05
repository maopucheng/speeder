import time
from machine import Pin

def main():
    #定义一个针脚，输入信号
    hall = Pin(36, Pin.IN)
    
    i = 0 #定义计数器
    mark = True #磁铁不在感应区？
    while True:
        #读取当前状态，status为0，表示有磁力感应到
        status = hall.value()
        
        if status==0 and mark:
            i += 1
            print("b2=", i)
            mark = False #磁铁在哪里？
            time.sleep(0.02)
        elif status==1:
            mark = True  #磁铁在哪里？
            time.sleep(0.02)
        else:
            pass #思考磁铁的位置和状态？
 
main()


