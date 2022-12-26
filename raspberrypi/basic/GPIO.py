import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 60)

p.start(99)

# exit
input('Press return to stop:')

p.stop()
GPIO.cleanup()