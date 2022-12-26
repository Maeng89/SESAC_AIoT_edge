import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

CW_PIN = 23 
VOL_PIN = 24

GPIO.setup(CW_PIN, GPIO.OUT)
GPIO.setup(VOL_PIN, GPIO.OUT)

# direction
GPIO.output(CW_PIN, 1)

# speed
p = GPIO.PWM(VOL_PIN, 1000)

p.start(0)
time.sleep(1)

p.start(20)
time.sleep(1)

p.start(100) #duty
time.sleep(10)
p.start(0)

input()
GPIO.cleanup()