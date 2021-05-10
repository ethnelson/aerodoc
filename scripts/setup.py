#!packages/bin/python3
import sys
import os
import pickle
sys.path.append('scripts/')
from arduino_comms import Database, Monitor
from comms_emulate import EmuSystem

# EDIT ARDUINO PORT VALUE FOUND ON RPI
PORT = '/dev/ttyACM0'

# --------------------------- SETUP SYSTEM ----------------------------------- #
if __name__ == '__main__':
    # If built on Rpi, create RPi monitor class
    # Failed: Connect to simulator class
    try:
        mon = Monitor(PORT)
    except:
        mon = EmuSystem()

    # Create base objects for the system
    # & fill database with null values
    pickle.dump([], open('dbBuffer.p', 'wb'))
    db = Database('datadb')
    db.createTable()
    db.insertData([0,0,0,0,0,0,0,0,0,0])
    pickle.dump(mon, open('monitor.p', 'wb'))
    pickle.dump([], open('noteBuffer.p', 'wb'))
