import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

p=GPIO.PWM(13,60)
p.start(15)#duty6~15 anglue only00

while True:
    d=input('Pressreturntostop:')
    if d=='s':
        break
    d=int(d)
    if d >=6 and d<=15:
        p.start(d)

p.stop()
GPIO.cleanup()