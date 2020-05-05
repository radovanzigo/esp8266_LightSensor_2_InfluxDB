########################
#                      #
# 2020-05-05 by Zigi   #
########################

sleep_wifi_init=5
sleep_main_cycle=10

import network
import time

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect("Wifi", "Passwd")
    time.sleep(sleep_wifi_init) # waiting for wifi
    while not sta_if.isconnected():
        pass
print(sta_if.ifconfig())



import machine

led = machine.Pin(2, machine.Pin.OUT)

from machine import ADC

try:

    adc = ADC(0)

except:

    print ("Initial sensor timeout, continuing..") 

import urequests
import ubinascii

user_and_pass = str(ubinascii.b2a_base64("%s:%s" % ("InfluxDB_user", "InfluxDB_passwd"))[:-1], 'utf-8')
headers = {'Authorization': 'Basic %s' % user_and_pass}
#print (headers)

while True:

    try:

      led.value(0)  # LED ON
      esp8266_light = adc.read()


    except:

      print("Sensor timeout, retrying..")

      time.sleep(sleep_main_cycle)

      continue


    url_string = 'https://abc.com/write?db=db_name'
    data_string = 'metric=esp8266_light,host=sensor2 value=%s' % (esp8266_light)
    data_string = '%s\nmetric=esp8266_light,host=sensor2 value=%s' % (data_string, esp8266_light)

#        data_string = '%s\nmetric=esp8266_pin38,host=sensor1 value=%s' % (data_string, esp8266_temp_int)

    print(data_string)

    try:

      r = urequests.post(url_string, data=data_string, headers=headers)
      r.close()

    except:

      print("Unable to submit data to server")

    led.value(1)  # LED OFF
    time.sleep(sleep_main_cycle)
