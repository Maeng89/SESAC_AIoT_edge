import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_noContact = 22


GPIO.setup(GPIO_noContact, GPIO.IN) 


def distance():
    result = GPIO.input(GPIO_noContact)
    time.sleep(1)

    return result

num = 0
while True:
    result = distance()
    num += 1
    print("non-contact water level {}".format(result)  )
    print(num, '=' * 50)
    time.sleep(1)

GPIO.cleanup()
