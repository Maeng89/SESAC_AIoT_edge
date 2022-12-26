import RPi.GPIO as GPIO
import spidev
import board
import adafruit_dht
import digitalio
from time import sleep

######## fire base ########
        
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Use a service account.
cred = credentials.Certificate('./nugunaaiot-maeng-1004a11a5af7.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


d_id = 'd0000001'

def create_device(d_id):
    doc_ref = db.collection('converea').document(d_id)
    doc = doc_ref.get()
    if doc.exists :
        pass
    else:
        doc_ref.set({
            'id': d_id,
             'is_running': True,
             'manufacture_date': datetime.now(),
            'sensor':[]
        })        
       
  

def upload_sensor(sensor):
    doc_ref = db.collection('converea').document(d_id)
    doc_ref.update({'sensor': firestore.ArrayUnion([sensor])})
    



GPIO.setmode(GPIO.BCM)
WL = 22
GPIO.setup(WL, GPIO.IN)
pin = digitalio.DigitalInOut(board.D27)

print("Digital IO ok!")
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D27)



sample = 10

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


def temp_read():
    
    temperature_c = dhtDevice.temperature
#     temperature_f = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    if temperature_c is None:
        temperature_c = 0
    elif humidity is None:
        humidity = 0
    return temperature_c, humidity


def water_level_read_digital():
    water_level = GPIO.input(WL)
    if (water_level == 0):
        return 1
    elif (water_level == 1):
        return 0
    else:
        raise Exception()


def adc_read(channel):
    r = spi.xfer2([1, (0x08 + channel) << 4, 0])
    adc_out = ((r[1] & 0x03) << 8) + r[2]
    return adc_out


def phSensor_read(channel):
    sampleValue = []
    for i in range(sample):
        adc = adc_read(channel)
        sampleValue.append(adc)

    sampleValue.sort()

    avg = 0
    for i in range(2, 8):
        avg += sampleValue[i]

    phValue = float(avg * 5 / 1024 / 6)
    phValue = float(3.5 * phValue)
    return phValue


def turbidity_read(channel):
    sampleValue = []
    for i in range(sample):
        adc = adc_read(channel)
        voltage = adc * (5.0 / 1024.0)
        sampleValue.append(voltage)

    sampleValue.sort() # 왜 정렬하지?
    avg = 0
    for i in range(2, 8):
        avg += sampleValue[i]
    voltage = avg / 6
    return voltage


def avg_sensor(sensors):
    s_len = len(sensors)
    sd = {'water_levle': 0,
          'ph': 0, 'turbidity': 0, 'temp': 0, 'humidity': 0, 'update_time' : 0}
    for s in sensors:
        sd['water_levle'] += s[0]
        sd['ph'] += s[1]
        sd['turbidity'] += s[2]
        sd['temp'] += s[3]
        print(s)
        sd['humidity'] += s[4]
        
#     sd['water_levle']
    
    if sd['water_levle'] >= s_len / 2:
        sd['water_levle'] = 1
    else:
        sd['water_levle'] = 0

    sd['ph'] = sd['ph'] / s_len
    sd['turbidity'] = sd['turbidity'] / s_len
    sd['temp'] = sd['temp'] / s_len
    sd['humidity'] = sd['humidity'] / s_len
    sd['update_time'] = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    return sd

#  fancode

# fan
fan_ch = 5
GPIO.setup(fan_ch, GPIO.OUT)
# sensor input data is GPIO.IN, electric output is GPIO.OUT

def fan(tp):

    if tp >= 24.0:
        GPIO.output(fan_ch, GPIO.LOW) # 
        print('fan off')
    else:
        GPIO.output(fan_ch, GPIO.HIGH)
        print('fan on')


# excute
if __name__ == '__main__':
    sensors = []
    create_device(d_id)
    
    doc_ref = db.collection('converea').document(d_id)
    doc_ref.update({'is_running': True})
    while True:
        try:
            wl = water_level_read_digital()
            ph = phSensor_read(1)
            tb = turbidity_read(17)
            tp, hd = temp_read()
            upt = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                 
            print('waterL ={}, ph = {}, turbidity= {}, temp = {}, humidity = {}, update_time = {}'.format(wl, ph, tb, tp, hd, upt))
            sensors.append([wl, ph, tb, tp, hd, upt])
          
#             if tp == None:
#                 pass
#             else:
            fan(tp)
                      
            if len(sensors) >= 10:
                sensor_data = avg_sensor(sensors)
                print(sensor_data)
                print('='*50)
                upload_sensor(sensor_data)
                sensors = []
            
            sleep(2.0)
            

        except KeyboardInterrupt:
            GPIO.cleanup()
            dhtDevice.exit()
            doc_ref.update({'is_running': False})
            break
        except RuntimeError:
            print('runtime error pass')
            pass  


