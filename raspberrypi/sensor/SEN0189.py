import spidev
from time import sleep
import os
import sys

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def adc_read(channel):
    r = spi.xfer2([1, (0x08+channel)<<4, 0])
    adc_out = ((r[1]&0x03)<<8) + r[2]
    return adc_out

def turbidity_read(channel):
    adc = adc_read(channel)
    
    voltage = adc*(5.0/1024.0)
    print(" turbidity : ", voltage, "V", "4.5V is MAX")

try:
    while True:
        turbidity_read(17)
except keyboardInterrupt:
    sleep(1)
    io.cleanup()
