import random,time
from machine import Pin, SPI, ADC

def main():
    h1 = Pin(36, Pin.IN)
    hm = Pin(37, Pin.IN)
    hma = ADC(Pin(39))
    while True:
        print("hall=", h1.value(),
              " mdl_D=",hm.value(),
              " mdl_A=",hma.read(),
              sep='')
        time.sleep(1)
main()

