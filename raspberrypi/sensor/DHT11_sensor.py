import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4)
num = 0
while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 /5)+32
        humidity=dhtDevice.humidity
        num += 1 
        print(
            "Num : {}, Temp: {:.1f}F / {:.1f}C , Humidity:{}%".format(
            num, temperature_f, temperature_c, humidity)
            )
        time.sleep(2)
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue