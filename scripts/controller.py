import sys
import os
sys.path.append('scripts/')
from arduino_comms import Database, Monitor
from comms_emulate import EmuSystem
import configparser
from time import strftime, localtime, sleep
import threading
import pickle
import ast

class aeroD:
    def __init__(self, interval=8):
        self.interval = interval
        self._running = True

        file = open('scripts/notes.txt', 'r')
        contents = file.read()
        self.noteTemplates = ast.literal_eval(contents)
        self.noteBuffer = []

        self.mon = pickle.load(open('monitor.p', 'rb'))
        self.conf = configparser.ConfigParser()
        self.db = Database('datadb')

        self.thread = threading.Thread(target=self.startThread, args=())
        self.thread.setDaemon(True)
        self.thread.start()

    def startThread(self):
        while self._running:
            self.updateDB()
            sleep(self.interval)
        print("Exiting Thread")
        pickle.dump(self.mon, (open('monitor.p', 'wb')))

    def stop(self):
        self._running = False
        self.thread.join()

    def updateDB(self):
        data = self.mon.getAllSensors()
        self.db.insertData(data)
        lastpoint = self.db.readLast()
        self.sysCheckup(lastpoint)

    def sysCheckup(self, data):
        timeNow = strftime('%H:%M', localtime())
        self.conf.read('aerodoc.ini')
        if float(data['PH']) <= float(self.conf['CONTROLLER']['ph_low']):
            self.mon.pumpSwitch(1, True)
            print("PH Up Activated")
            self.createNote('ph_low')
        elif float(self.conf['CONTROLLER']['ph_up']) <= float(data['PH']):
            self.mon.pumpSwitch(2, True)
            print("PH Down Activated")
            self.createNote('ph_up')
        elif (float(self.conf['CONTROLLER']['ph_low']) <= float(data['PH']) <=
            float(self.conf['CONTROLLER']['ph_up'])):
            self.mon.pumpSwitch(1, False)
            self.mon.pumpSwitch(2, False)

        if float(data['EC']) <= float(self.conf['CONTROLLER']['ec_low']):
            self.mon.pumpSwitch(3, True)
            print("Activating EC Up")
            self.createNote('ec_low')
        else:
            self.mon.pumpSwitch(3, False)
            print("EC deactivated")

        if (not self.mon.fanStatus) and (float(self.conf['CONTROLLER']['temp_up']) <= float(data['temp']) or
                                    float(self.conf['CONTROLLER']['hum_up']) <= float(data['hum'])):
            self.mon.fanSwitch(True)
            print("Fan Activated")
            self.createNote('temp_up')

        if ((not self.mon.fanStatus) and float(self.conf['CONTROLLER']['hum_up']) <= float(data['hum'])):
            self.createNote('hum_up')

        if (not self.mon.lightStatus) and (self.conf['CONTROLLER']['light_start'] <= timeNow <=
                                        self.conf['CONTROLLER']['light_stop']):
            self.mon.lightSwitch(True)
            print("Light Activated")
            self.createNote('light_on')
        elif (self.mon.lightStatus and
                (timeNow <= self.conf['CONTROLLER']['light_start'] or
                 self.conf['CONTROLLER']['light_stop'] <= timeNow)):
            self.mon.lightSwitch(False)
            print("Light Deactivated")
            self.createNote('light_off')

    def createNote(self, type):
        try:
            self.noteBuffer = pickle.load(open('noteBuffer.p', 'rb'))
            note = self.noteTemplates[type]
            note['time'] = strftime('%Y-%m-%d %H:%M', localtime())
            self.noteBuffer.append(self.noteTemplates[type])
            pickle.dump(self.noteBuffer, open('noteBuffer.p', 'wb'))
        except:
            print('Error grabbing note')
