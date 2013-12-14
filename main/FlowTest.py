#!/usr/bin/python
import os
import time 
import math
import sys
import RPi.GPIO as GPIO

#globals for keeping track of flow
litresInKeg = 58.6738827
lastPinState = False
pouring = False
pinState = False
lastPinChange = int(time.time() *1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0
hertz = 0
flow =0
litresPoured = 0
#Initialize GPIO pins
SENSOR_PIN = 4
boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
while True:
  currentTime = int(time.time() *1000)
  if(GPIO.input(4)):
    pinState = True
  else:
    pinSate = False
    #check if we have changed from low to high pinstate
  if(pinState != lastPinState and pinState == True):
    if(pouring ==False):
      pourStart = currentTime
    #endif
    pouring =True
    #get time
    pinChange = currentTime
    pinDelta = pinChange - lastPinChange
    if (pinDelta < 1000 and pinDelta != 0):
      hertz = 1000.0000 / pinDelta
      flow = hertz/(60*7.5) #Litres/second
      litresPoured += flow * (pinDelta/1000.0000)
    #endif
    if (pouring == True and pinState == lastPinState and (currentTime - lastPinChange) > 3000):
    #not pouring anymore
      pouring=False
    #endif
  lastpinChange = pinChange
  lastPinState = pinState
  print (pinChange)
  print (pinState)
  print(pouring)
  print (litresPoured)


