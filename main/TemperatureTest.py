#!/usr/bin/env python
import os
import glob
import time
import RPi.GPIO as GPIO
import re
import subprocess
import gspread
import datetime
import math
import sys
import sched
# ===========================================================================
# Define Scheduler
# ===========================================================================
scheduler = sched.scheduler(time.time, time.sleep)
def periodic(scheduler, interval, action,actionargs=()):
  scheduler.enter(interval,1, periodic, (scheduler,interval,action,actionargs))
  action(*actionargs)
# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email       = 'fenix.jyinaer@gmail.com'
password    = 'Vassallo4460'
spreadsheet = 'Keg Temperatures'

# ===========================================================================
# Pin Information
# ===========================================================================
TEMPERATURE_PIN = 22 #Temperature Sensor
FRIDGE_PIN = 23 #Relay controling Fridge
#Setup GPIO on fridge pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(FRIDGE_PIN, GPIO.OUT)
GPIO.output(FRIDGE_PIN, GPIO.LOW)

# ===========================================================================
# Global Information
# ===========================================================================
# stores whether the fridge is turned on or not.
bFridgeOn = False
temperature = -999.9
humidity = -999.9
def WriteSpreadSheet(temperature, humidity):
	try:
		gc = gspread.Client(auth=(email,password))
		gc.login()
		# Open a worksheet from your spreadsheet using the filename
		sht = gc.open(spreadsheet)
		# Get first sheet
		worksheet = sht.get_worksheet(0)
		# Create and insert values
		values = [datetime.datetime.now(), temperature, humidity,bFridgeOn]
		worksheet.append_row(values)
	except Exception:
		print ("Failed to connect to Google Spreadsheet")

# Read data off dht22 using c driver
def read_dht22( pin ):
	temp = -999.9
	hum = -999.9
	output = subprocess.check_output(["sudo","./Adafruit_DHT", "22", str(SENSOR_PIN)])
	
	matches = re.search("Temp =\s+(.[0-9.]+)", output)	
	print(output)
	if ( matches ):
		temp = float(matches.group(1))
		
	matches = re.search("Hum =\s+(.[0-9.]+)", output)	
	if ( matches ):
	  hum = float(matches.group(1))
	  
	result = {'temp': temp, 'hum': hum}
	return result

# Operate the fridge based off the temp read
def FridgeControl(temp):
	global bFridgeOn
	if (temp >= 1):
		#Turn fridge On
		GPIO.output(FRIDGE_PIN, GPIO.HIGH)
		print ("ON")
		bFridgeOn = True
	elif (temp <= -1 ):
		#Turn fridge off
		GPIO.output(FRIDGE_PIN, GPIO.LOW)
		bFridgeOn = False
		
while True:
	results =read_dht22(22)
	if  ( results['temp'] > -254):
		FridgeControl(results['temp'])
		WriteSpreadSheet(results['temp'],results['hum'])
	time.sleep(20)
