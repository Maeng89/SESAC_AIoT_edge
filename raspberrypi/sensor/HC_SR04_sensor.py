import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 22
GPIO_ECHO = 27

GPIO.setup(GPIO_TRIGGER, GPIO.OUT) 
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, 1)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, 0)

    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1: #
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime #
    distance = (TimeElapsed * 34300) / 2

    return distance

while True:
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist) 
    time.sleep(1)

GPIO.cleanup()