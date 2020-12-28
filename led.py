import RPi.GPIO as GPIO
import sys
import urllib.request
from time import sleep

# Enter Your API key here
myAPI = 'QA2QAZKK8UVQPM02' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

try:
    while True:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(15,GPIO.OUT)
        GPIO.setup(16,GPIO.OUT)
        p=0
        # for i in range(0,5):
        #     p=p+LDR(11,13)
        p_avg = 600

        if p_avg > 500:
            #GPIO.output(18, GPIO.HIGH)
            #GPIO.output(15, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            value=1
            value_1=value
            value_2=value
            value_3=value
            conn = urllib.request.urlopen(baseURL + '&field5=%s&field6=%s&field7=%s&field8=%s' % (p_avg, value_1, value_2, value_3))
            conn.close()

        else:
            GPIO.output(18, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            value=0
            value_1=value
            value_2=value
            value_3=value
            conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' % (p_avg, value_1, value_2, value_3))
            conn.close()
    	
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)