# Basic Clock
import rp2
import network
import time
import secrets

from machine import Pin, I2C
from sys import exit

from i2c_lcd_dq import lcd_pcf8574

TIMEOUT = 20

# Init display
# Inicia o display
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
lcd = lcd_pcf8574(i2c)
lcd.init()
lcd.backlightOn()

# Connects to WiFi network
# Conecta à rede WiFi
rp2.country('BR')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ESSID, secrets.PASSWD)

print ('Conecting...')
lcd.displayWrite(0,0,'Conecting...')
timeout = time.ticks_add(time.ticks_ms(), TIMEOUT*1000)
while not wlan.isconnected() and wlan.status() >= 0 and \
      time.ticks_diff(timeout, time.ticks_ms()) > 0:
    time.sleep(0.2)

if not wlan.isconnected(): 
    print ('Could not connect')
    lcd.displayWrite(1,0,'No connection')
    exit()

print('Connected')
print('IP: '+wlan.ifconfig()[0])
print()

# Get current time
# Obtem a hora atual
import ntptime
UTC_OFFSET = -3 * 60 * 60
ntptime.settime()
lcd.displayWrite(0,0,'Connected    ')

# Main loop
while True:
    now = time.localtime(time.time() + UTC_OFFSET)
    date_time =  "{:02}/{:02} {:02}:{:02}:{:02}".format(
        now[2],now[1],now[3],now[4],now[5])
    print(date_time)
    lcd.displayWrite(1,0,date_time)
    time.sleep(0.5)
