import sys
import time
import board
import adafruit_dht
import urllib.request

mySecretApi = "QA2QAZKK8UVQPM02"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % mySecretApi 
# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D18)
dhtDevice = adafruit_dht.DHT11(board.D18)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        temp = "%.2f" % temperature_c
        humi = "%.2f" % humidity
        conn = urllib.request.urlopen(baseURL + "&field1=%s&field2=%s" % (temp, humi))
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            ) 
        )
        conn.close()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(0.2)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(0.2)
