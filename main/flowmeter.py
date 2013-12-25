import time
from __future__ import print_function

class FlowMeter():
  PINTS_IN_A_LITER = 2.11338
  LITRES_IN_KEG = 58.6738827
  SECONDS_IN_A_MINUTE = 60
  MS_IN_A_SECOND = 1000.0
  displayFormat = 'metric'
  clicks = 0
  lastClick = 0
  clickDelta = 0
  hertz = 0.0
  flow = 0 # in Liters per second
  thisPour = 0.0 # in Liters
  totalPour = 0.0 # in Liters
  filename = "totalpour.dat"
  def __init__(self, displayFormat):
    self.displayFormat = displayFormat
    self.clicks = 0
    self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    self.clickDelta = 0
    self.hertz = 0.0
    self.flow = 0.0
    #open file
    file = open(self.filename, 'r')
    self.thisPour = float(file.readline())
    file.close()
    
    self.totalPour = 0.0

  def update(self, currentTime):
    self.clicks += 1
    # get the time delta
    self.clickDelta = max((currentTime - self.lastClick), 1)
    # calculate the instantaneous speed
    if (self.clickDelta < 1000):
      self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta
      self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)  # In Liters per second
      instPour = self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)  
      self.thisPour += instPour
      self.totalPour += instPour
    # Update the last click
    self.lastClick = currentTime
    file = open(self.filename, 'w')
    file.write(self.totalPour)
    file.close()

  
  
  def reset(self):
	self.clicks = 0
	self.lastClick=0
	self.hertz = 0.0
	self.flow = 0
	self.thisPour = 0
	self.totalPour = 0
		
  def getFormattedClickDelta(self):
     return str(self.clickDelta) + ' ms'
  
  def getFormattedHertz(self):
     return str(round(self.hertz,3)) + ' Hz'
  
  def getFormattedFlow(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.flow,3)) + ' L/s'
    else:
      return str(round(self.flow * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints/s'
  
  def getFormattedThisPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.thisPour,3)) + ' L'
    else:
      return str(round(self.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'
  
  def getFormattedTotalPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.totalPour,3)) + ' L'
    else:
      return str(round(self.totalPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'
