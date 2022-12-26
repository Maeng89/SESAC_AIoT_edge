import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

# GPIO input number
coil_A_1_pin = 17 #1 GPIO17
coil_A_2_pin = 27 #2 GPIO27
coil_B_1_pin = 22 #3 GPIO22
coil_B_2_pin = 23 #4 GPIO23

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def forward(delay, steps):
    for i in range(steps):
        for j in range(step_count):
            setStep(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            time.sleep(delay)

def backward(delay, steps):
    for i in range(steps):
        for j in reversed(range(step_count)):
            setStep(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            time.sleep(delay)

step_count = 8
seq = list(range(0, step_count))
#        [A,B,C,D]
seq[0] = [1,0,0,0] #A
seq[1] = [1,1,0,0]
seq[2] = [0,1,0,0] #B
seq[3] = [0,1,1,0]
seq[4] = [0,0,1,0] #C
seq[5] = [0,0,1,1]
seq[6] = [0,0,0,1] #D
seq[7] = [1,0,0,1] 

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

if __name__ == '__main__':
    delay = 0.001 # ms
    steps = 500 # 500 1 cycle
    #forward(delay, int(steps))
    backward(delay, int(steps))