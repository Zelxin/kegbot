#!/usr/bin/python
import os
import sched, time 
import math
import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
from flowmeter import *
from TemperatureController import *
import threading

# ===========================================================================
# Define Pin setup
# ===========================================================================
FLOWSENSOR_PIN = 4
TEMPERATURESENSOR_PIN = 22
FRIDGEPOWER_PIN = 23
boardRevision = GPIO.RPI_REVISION
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOWSENSOR_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FRIDGEPOWER_PIN, GPIO.OUT)
GPIO.output(FRIDGEPOWER_PIN, GPIO.LOW)

# ===========================================================================
# Define Pin setup
# ===========================================================================
pygame.init()
VIEW_WIDTH = 1248
VIEW_HEIGHT = 688
BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.display.set_caption('')
windowSurface = pygame.display.set_mode([600,400])
windowInfo = pygame.display.Info()
FONTSIZE = 48
LINEHEIGHT = 28
basicFont = pygame.font.SysFont(None, FONTSIZE)

#set up flow meteru k 
fm = FlowMeter('metric')
#set up temperature controller
tc = TemperatureController(22)

bRun = True

#This gets run whenever an interrupt triggers it due to pin 4 being grounded.
def doAClick(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  fm.update(currentTime)
  print(fm.totalPour)

GPIO.add_event_detect(4, GPIO.RISING, callback=doAClick, bouncetime=20)

def render():
  windowSurface.fill(BLACK)
  
  text = basicFont.render('Temperature: ' + tc.GetFormattedTemperature(), True, WHITE, BLACK)
  textRect= text.get_rect()
  windowSurface.blit(text, (40,6*LINEHEIGHT))
  
  text = basicFont.render('Amount Poured(L)' + fm.getFormattedTotalPour(), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,7*LINEHEIGHT))
  
  
  text = basicFont.render('Current Pour' + fm.getFormattedThisPour() , True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,8*LINEHEIGHT))
  
  
  #Display everything
  pygame.display.flip()
  

# Operate the fridge based off the temp read
def FridgeControl(tc):
	if (tc.temperature >= 1):
		#Turn fridge On
		GPIO.output(FRIDGE_PIN, GPIO.HIGH)
		print ("ON")
		bFridgeOn = True
	elif (tc.temperature <= -1 ):
		#Turn fridge off
		GPIO.output(FRIDGE_PIN, GPIO.LOW)
		bFridgeOn = False


def WriteSpreadSheet(tc,sleepTime):
	while (bRun):
		try:
			gc = gspread.Client(auth=(email,password))
			gc.login()
			# Open a worksheet from your spreadsheet using the filename
			sht = gc.open(spreadsheet)
			# Get first sheet
			worksheet = sht.get_worksheet(0)
			# Create and insert values
			values = [datetime.datetime.now(), tc.temperature, tc.humidity,bFridgeOn]
			worksheet.append_row(values)
		except Exception:
			print ("Failed to connect to Google Spreadsheet")
		time.sleep(sleepTime)
		
def ReadTemp(tc,sleepTime):
	print('Sleeping TemperatureThread')
	while (bRun):
		tc.read_dht22()
		print('Sleeping TemperatureThread')
		time.sleep(sleepTime)

tTemp = threading.Timer(2,ReadTemp,(tc,15))
tTemp.start()
tSS = threading.Timer(2,WriteSpreadSheet,(tc,3600))
tSS.start()
#periodic(scheduler,30,ReadTemp,(tc,))
#periodic(scheduler,3600,WriteSpreadSheet,(tc,)) #set writespreadsheet to run every 3600 seconds(1 hour)


while True:
	if  ( tc.temperature > -254):
		FridgeControl(tc)
	for event in pygame.event.get():
	  if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
	    pygame.quit()
	    bRun = False
	    GPIO.cleanup()
	    sys.exit()
	render()
