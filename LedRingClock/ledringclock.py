# RGB LED Ring Clock
import rp2
import network
import time
import secrets

from machine import Pin
from sys import exit
import neopixel

TIMEOUT = 20

# Init display
# Inicia o display
p = Pin(15)
led = neopixel.NeoPixel(p, 12)
led.fill((0,0,0))
led.write()
OFF12 = 7

def setLed (pos, cor, intensidade):
    pos = (pos + OFF12) % 12
    x = list(led[pos])
    x[cor] = intensidade
    led[pos] = x

# Connects to WiFi network
# Conecta à rede WiFi
rp2.country('BR')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ESSID, secrets.PASSWD)

print ('Conecting...')
timeout = time.ticks_add(time.ticks_ms(), TIMEOUT*1000)
while not wlan.isconnected() and wlan.status() >= 0 and \
      time.ticks_diff(timeout, time.ticks_ms()) > 0:
    time.sleep(0.2)

if not wlan.isconnected(): 
    print ('Could not connect')
    exit()

print('Connected')
print('IP: '+wlan.ifconfig()[0])
print()

# Get current time
# Obtem a hora atual
import ntptime
UTC_OFFSET = -3 * 60 * 60
ntptime.settime()

# Main loop
while True:
    now = time.localtime(time.time() + UTC_OFFSET)
    print(now)
    led.fill((0,0,0))
    hora = now[3] % 12
    setLed(hora,0,64)
    m = now[4] // 5
    setLed(m,1,64)
    s = now[5] // 5
    setLed(s,2,64)
    led.write()
    time.sleep(0.5)

