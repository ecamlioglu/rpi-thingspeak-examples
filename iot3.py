import sys
import time
import board
import RPi.GPIO as GPIO
import adafruit_dht
import urllib.request
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


TRIG_pin = 23
ECHO_pin = 24

GPIO.setup(TRIG_pin,GPIO.OUT)
GPIO.setup(ECHO_pin,GPIO.IN)

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

        # hcsr-04 code block

        GPIO.output(TRIG_pin, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_pin, False)

        while GPIO.input(ECHO_pin)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO_pin)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        real_distance = 0.0
        if distance > 2 and distance < 400:
            real_distance = distance - 0.5
            print ("Mesafe:",distance - 0.5,"cm")
        else:
            real_distance = 0
            print ("Menzil asildi")
        conn = urllib.request.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s" % (temp, humi, real_distance))
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
