import machine, time, network, webrepl

SSID = "codemao"  #修改为你的WiFi名称
PASSWORD = "82221515"  #修改为你WiFi密码
wlan = None  #wlan

#连接WiFi
def connectWifi(ssid,passwd):   
  global wlan
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(True)   #激活网络
  wlan.disconnect()   #断开WiFi连接
  wlan.connect(ssid, passwd)   #连接WiFi
  while(wlan.ifconfig()[0] == '0.0.0.0'):   #等待连接
    time.sleep(1)
  return True

#Catch exceptions,stop program if interrupted accidentally in the 'try'
connectWifi(SSID,PASSWORD)
ip = wlan.ifconfig()[0]   #获取IP地址
print(wlan.ifconfig()[0])

webrepl.start()

