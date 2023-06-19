# Stepper Motor Clock
import rp2
import network
import time
import secrets

from machine import Pin
from sys import exit
import neopixel

TIMEOUT = 20

# Stepper motor control class
class Stepper():
  # set motor control pins
  def setpins(self, val=[0,0,0,0]):
    for i in range(len(self.pins)):
      self.pins[i].value(val[i])
 
  # init
  def __init__(self, pins=None):
    if pins is None:
      raise ValueError("Must specify pins!")
    if len(pins) != 4:
      raise ValueError("There must be 4 pins")
    self.pins = pins
    self.steps = [[1,0,0,1], [1,1,0,0], [0,1,1,0], [0,0,1,1]]
    self.steps = [[0,0,1,1], [0,1,1,0], [1,1,0,0], [1,0,0,1]]
    self.setpins()
    self.step = 0
 
  # advance one step
  def onestep(self):
    self.setpins(self.steps[self.step])
    self.step = self.step+1
    if self.step >= len(self.steps):
      self.step = 0

# Stepper connections
pins = [
  Pin(2, Pin.OUT),
  Pin(3, Pin.OUT),
  Pin(4, Pin.OUT),
  Pin(5, Pin.OUT)
]
stepper = Stepper(pins)

# Position at 12 o'clock
# Posiciona nas 12 horas
print ('Searching')
sensor = Pin(16, Pin.IN)
for i in range(2500):
    stepper.onestep()
    if sensor.value() == 1:
        print('Found starting point')
        break
    time.sleep(0.01)

STEPS_PER_TURN = 2048
cur_pos = 0

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
    # 12 hours = STEPS_PER_TURN steps from strting point
    # 12 horas = STEPS_PER_TURN passos do ponto inicial
    new_pos = (STEPS_PER_TURN * ((now[3] % 12) + (now[4]/60) + (now[5]/3600)))//12
    # For 2048 Steps per Turn, aprox 1 step per 21 seconds
    # Para 2048 Passos por Volta, aprox 1 passo a cada 21 segundos
    while cur_pos != new_pos:
       stepper.onestep()
       cur_pos = (cur_pos+1) % STEPS_PER_TURN
       time.sleep (0.01)
    time.sleep(1)


