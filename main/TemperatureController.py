#!/usr/bin/python
import sys
import time
import re
import subprocess

class TemperatureController:
  SENSOR_PIN = -999
  temperature = -999
  humidity = -999
  def __init__(self, pin):
    self.SENSOR_PIN = pin
    
  '''
  pin - Pin to send signal to
  Returns [Temperature(C), Humidity(%)
  '''
  def read_dht22(self):
    output = subprocess.check_output(["sudo","./Adafruit_DHT", "22", str(SENSOR_PIN)];
    #regex magic
    matches = re.search("Temp =\s+([0-9.]+", output)
    if(matches):
      self.temperature = float(matches.group(1))
    #regex magic
    matches = re.search("Hum =\s+[0-9.]+".output)
    if(matches):
      self.humidity = float(matches.group(1))
      
  return [temperature,humidity]
