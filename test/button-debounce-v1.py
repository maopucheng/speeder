from machine import Pin, Timer

i = 0

def on_pressed(timer):
    global i
    i = i+1
    print('count:',i)

def debounce(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    timer.init(mode=Timer.ONE_SHOT, period=160, callback=on_pressed)

# Register a new hardware timer.
timer = Timer(0)

# Setup the button input pin with a pull-up resistor.
button = Pin(37, Pin.IN, Pin.PULL_UP)

# Register an interrupt on rising button input.
button.irq(debounce, Pin.IRQ_FALLING)

