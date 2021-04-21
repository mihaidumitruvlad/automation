import os
import sys
import time
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
if humidity is not None and temperature is not None:
  with open(sys.argv[1], 'w') as f:
    f.write('{{"timestamp": "{0} {1}", "temperature": "{2:0.1f}", "humidity": "{3:0.1f}"}}'.format(time.strftime('%d-%b-%Y'), time.strftime('%H:%M'), temperature, humidity))
    f.close
  print("Sensor humidity: {0:.2f}%, temperature: {1:.2f}*C".format(humidity,temperature))
