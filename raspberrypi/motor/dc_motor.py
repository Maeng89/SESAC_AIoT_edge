import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
IN1 = 13
IN2 = 6

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm = GPIO.PWM(IN1, 40)

GPIO.output(IN2, 0)
pwm.start(30)

sleep(5)
pwm.start(0)

sleep(1)
GPIO.output(IN2, 1)
pwm.start(70)

sleep(5)
pwm.start(0)

GPIO.cleanup()