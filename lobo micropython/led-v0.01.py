import machine, time

#np=machine.Neopixel(machine.Pin(22), 8)

np = machine.Neopixel(22, 8, machine.Neopixel.TYPE_RGB)
np.brightness(50)
color,r,g,b = 0,0,0,0
for pos in range(1,9):
    time.sleep(0.5)
    color = (r<<16)+(g<<8)+b
    np.set(pos, color)

    r = r+30
    g = g+0
    b = b+0
    
#RGB color
#    color = (r<<16)+(g<<8)+b