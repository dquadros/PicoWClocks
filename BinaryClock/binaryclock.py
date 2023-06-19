# Binary Clock
import rp2
import network
import time
import secrets

from machine import Pin, SPI
from sys import exit

class LedMatrix:
    def __init__(self, spi, pinCS):
        self.spi = spi
        self.cs = Pin(pinCS, mode=Pin.OUT, value=1)
        self.MAX7219_MODE = 0x09  
        self.MAX7219_INT = 0x0A  
        self.MAX7219_LIM = 0x0B
        self.MAX7219_SHUT = 0x0C
        self.MAX7219_TEST = 0x0F
        self.write(self.MAX7219_SHUT, 0)
        self.write(self.MAX7219_INT, 7)
        self.write(self.MAX7219_MODE, 0)
        self.write(self.MAX7219_LIM, 7)
        self.write(self.MAX7219_TEST, 0)
        for i in range(1, 9):
            self.write(i, 0)
        self.write(self.MAX7219_SHUT, 1)
        
    def write(self, addr, data):
        self.cs(0)
        spi.write(bytearray([addr,data]))
        self.cs(1)


TIMEOUT = 20

# Init display
# Inicia o display
spi = SPI(1, baudrate=100_000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(14), mosi=Pin(15), miso=None)
led = LedMatrix(spi, 13)

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
    led.write(8,now[2])
    led.write(7,now[1])
    led.write(6,now[0]//100)
    led.write(5,now[0]%100)
    led.write(3,now[3])
    led.write(2,now[4])
    led.write(1,now[5])
    time.sleep(0.5)
