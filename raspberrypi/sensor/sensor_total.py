## turbidity, ph sensor
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
    return voltage


## sampling
sample = 10
sampleValue = []

def phSensor_read(channel):
    for i in range(sample):
        adc = adc_read(channel)
        sampleValue.append(adc)
        sleep(0.10)

    sampleValue.sort()

    avg = 0
    for i in range(2, 8):
        avg += sampleValue[i]
    
    phValue = float(avg * 5 / 1024 /6)
    phValue = float(3.5 * phValue)
    
    return phValue

    sampleValue.clear()
    

## non-contact water level sensor
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_nonContact = 22

GPIO.setup(GPIO_nonContact, GPIO.IN) 


def ncLevel():
    result = GPIO.input(GPIO_nonContact)
    return result


## dht sensor ##
#import time
import board
import adafruit_dht


dhtDevice = adafruit_dht.DHT22(board.D27)

def dht():
    try:
        # Print the values to the serial port        
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        return temperature_f, temperature_c, humidity

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        #time.sleep(2)        
        #continue
        return 0,0,0

    except Exception as error:
        dhtDevice.exit()
        raise error



# excute
num = 0
try:
    while True:
        time.sleep(2)
        
        num += 1
        print(num, "="*50)
        

        
        temperature_f, temperature_c, humidity = dht() # 27
        print("Temp : {:.1f}F / {:.1f}C    Humidity: {}%".format(temperature_f, temperature_c, humidity))
        
        turbidity = turbidity_read(17) #17
        print("Turbidity : {:.1f}V  (4.5V is MAX)".format(turbidity))
        
        phValue = phSensor_read(1)  
        print("PHvalue : {:.1f}(acid)".format(phValue) )
        
        ncLevel2 = ncLevel() # 22
        print("non-contact water level : {}".format(ncLevel2) )
        
        
                             
except KeyboardInterrupt:
    sleep(10)
    io.cleanup()

GPIO.cleanup()
