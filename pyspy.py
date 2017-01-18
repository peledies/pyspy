#!/usr/bin/python
# Written by Deac Karns
# License: GPL 2.0

import json
import os
from gps import *
from time import *
import time
import threading

path = os.path.dirname(os.path.realpath(__file__))
file = path,'/track.json'

gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      time.sleep(5) #set to whatever

      a_dict = {'latitude': gpsd.fix.latitude, 'longitude':gpsd.fix.longitude, 'time':gpsd.fix.time, 'altitude':gpsd.fix.altitude, 'speed_meters_per_second':gpsd.fix.speed}

      with open(file) as f:
          data = json.load(f)

      data.append(a_dict)

      with open(file, 'w') as f:
          json.dump(data, f)
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."

