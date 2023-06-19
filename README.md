# PicoWClocks

**Nifty clock projects built with the Raspberry Pi Pico W**

**Projetos bacanas de relógio usando o Raspberry Pi Pico W**

./PicoWClocks.jpg

The softwares are written in MicroPython. To use them you have to create in the Pico W a secrets.py file.

Os softwares foram escritos em MicroPython. Para usá-los você precisa criar no Pico W um arquivo chamado secrets.py.

secrets.py:
```
ESSID = 'router_essid'
PASSWD = 'router_password'
```

## BasicClock

Basic project for testing SNTP connection. Uses an alphanumeric 2 line x 16 columns display with I^2^C interface.

Projeto básico para testar a conexão SNTP. Usa um display alfanumérico de 2 lihas x 16 columas com interface I^2^C.

## BinaryClock

This project uses an 8x8 LED display with a MAX7219 controller to display day, month, year, hour, minutes, and seconds in binary.

Este projeto usa um display LED 8x8 com controlador MAX7219 para mostrar dia, mês, ano, hora, minutos e segundos em binário.

## LedRingClock

This project shows the current time using an RGB LED ring (with 12 LEDs).

Este projeto mostra a hora atual usado um anel de doze LEDs RGB.

## StepperClock

This project shows the current time using a stepper motor. An optical endstop sensor is used to find the 12 o'clock position.

Este projeto usa um motor de passos para mostrar a hora atual. Um sensor infravermelho é usado para determinar a posição de meio-dia.

