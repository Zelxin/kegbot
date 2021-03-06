#!/usr/bin/python
import os
import time 
import math
import sys
import RPi.GPio as io

class FlowController:
  #Initialize GPIO pins
  SENSOR_PIN = -999
  boardRevision = GPIO.RPI_REVISION
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  #globals for keeping track of flow
  litresInKeg = 58.6738827
  lastPinState = False
  pouring = False
  pinState = 0
  lastPinChange = int(time.time() *1000)
  pourStart = 0
  pinChange = lastPinChange
  pinDelta = 0
  hertz = 0
  flow =0
  litresPoured = 0
  def __init__(self, pin):
    SENSOR_PIN = pin # Store the pin we are using to interface with our flow sensor
 
  '''
  This needs to be in a main loop to constantly check our flow rate.
  '''
  def MonitorFlow():
    currentTime = int(time.time() *1000)
    if(GPIO.input(22):
      pinState = True
    else
      pinSate = False
    #check if we have changed from low to high pinstate
    if(pinState != lastPinState and pinState == True):
      if(pouring ==False):
	pourStart = currentTime
      pouring =True
      #get time
      pinChange = currentTime
      pinDelta = pinChange - lastPinChange
      if (pinDelta < 1000):
	hertz = 1000.0000 / pinDelta
	flow = hertz/(60*7.5) #Litres/second
	litresPoured += flow * (pinDelta/1000.0000)

    if (pouring == True and pinSate == lastPinState and (currentTime - lastPinChange) > 3000):
    #not pouring anymore
      pouring=False
      
    lastpinChange = pinChange
    lastPinState = pinState
    


