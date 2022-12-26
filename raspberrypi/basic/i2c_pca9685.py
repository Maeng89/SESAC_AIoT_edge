import RPi.GPIO as GPIO
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 60
LED = 0
R = 2
G = 3
B = 4
Servo = 8

def set_duty(c, duty):
	pul = duty * 16 *4096 // 100
	pca.channels[c].duty_cycle = pul


while True:
	m = input('mode')
	d = int(input('duty'))
	if m == 'l':
		set_duty(LED , d) # on LED
	elif m == 'r':
		set_duty(R, d)
	elif m == 'g':
		set_duty(G, d)
	elif m == 'b':
		set_duty(B, d)
	elif m == 's': # servo
		set_duty(Servo, d)
	elif m == 'q': # rgb and led quit
		break

set_duty(LED, 0)
set_duty(R, 0)
set_duty(G, 0)
set_duty(B, 0)
GPIO.cleanup()
