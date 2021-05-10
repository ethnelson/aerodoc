#!packages/bin/python3
import serial
import sqlite3
import time
import configparser
import pickle

class Database:
    def __init__(self, name):
        self.name = f'{name}.db'
        self.con = None
        self.cur = None
        self.bufferFile = 'dbBuffer.p'
        self.collectionBuffer = []

    def open(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()

    def createTable(self):
        self.open()
        try:
            self.cur.execute("""CREATE TABLE sensorData
                                (time DATETIME, EC REAL, PH REAL,
                                Temp REAL, Humidity REAL, Water BOOLEAN,
                                Light BOOLEAN, Fan BOOLEAN, P1 BOOLEAN,
                                P2 BOOLEAN, P3 BOOLEAN)""")
            self.con.commit()
        except:
            print('Table exists. passing')
        self.close()

    # data = [ec, ph, temp, hum, wat, light, fan, p1, p2, p3]
    def insertData(self, data):
        self.open()
        tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data.insert(0, tim)
        self.cur.execute("""INSERT INTO sensorData
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            data)
        self.con.commit()
        self.close()
        self.addToBuffer(self.readLast())

    def readLast(self):
        self.open()
        self.cur.execute("""SELECT * FROM sensorData
                            ORDER BY time
                            DESC LIMIT 1""")
        data = self.cur.fetchone()
        self.con.commit()
        self.close()
        data = self.convertToDict(data)
        return data

    def readLastMult(self, num):
        self.open()
        self.cur.execute("""SELECT * FROM sensorData
                            ORDER BY time
                            DESC LIMIT ?""", (str(num),))
        data = self.cur.fetchall()
        self.con.commit()
        self.close()
        data = self.convertToDictLarge(data)
        return data

    def convertToDict(self, lst):
        names = ['time', 'EC', 'PH', 'temp', 'hum',
                    'wat', 'light', 'fan', 'p1', 'p2', 'p3']
        dict = {}
        dict = {names[i]: lst[i] for i in range(0, len(lst))}
        return dict

    def convertToDictLarge(self, lst):
        names = ['time', 'EC', 'PH', 'temp', 'hum',
                    'wat', 'light', 'fan', 'p1', 'p2', 'p3']
        dict = {}
        for i in range(0, len(lst)):
            dict[i] = {names[j]: lst[i][j] for j in range(0, len(names))}
        return dict

    def addToBuffer(self, data):
        self.collectionBuffer = pickle.load(open(self.bufferFile, 'rb'))
        self.collectionBuffer.append(data)
        pickle.dump(self.collectionBuffer, open(self.bufferFile, 'wb'))

    def getBuffer(self):
        self.collectionBuffer = pickle.load(open(self.bufferFile, 'rb'))
        package = {}
        if self.collectionBuffer:
            self.collectionBuffer.reverse()
            for i in range(0, len(self.collectionBuffer)):
                package[i] = self.collectionBuffer[i]

            self.collectionBuffer = []
            pickle.dump(self.collectionBuffer, open(self.bufferFile, 'wb'))

        return package



# ---------------------------------------------------------------------------- #
#                           COMMUNICATION METHOD                               #
# ---------------------------------------------------------------------------- #
# Sensor Data Requests                                                         #
# --- Start communication phrase with 'S', then add one of the following       #
# --- characters for specifying which type of sensor data to request.          #
# ------ 'E' - EC sensor                                                       #
# ------ 'P' - PH sensor                                                       #
# ------ 'T' - Temperature Sensor                                              #
# ------ 'H' - Humidity Sensor                                                 #
# ------ 'W' - Water level Sensor                                              #
#                                                                              #
#           EX: tunnel.write(b'SE')                                            #
#            - This sends a request for data on the                            #
#              EC Sensor(Electrical Conductivity)                              #
#                                                                              #
# Controller Action Requests                                                   #
# --- Start the phrase with 'C', then add any of the following characters for  #
# --- specifying which element to control.                                     #
# ------ 'L' - controls the light                                              #
# ------ 'F' - controls the fan                                                #
# ------ 'U' - controls the Peristaltic pumps                                  #
# --------- '1' - peristaltic pump #1 - PH Up                                  #
# --------- '2' - peristaltic pump #2 - PH Down                                #
# --------- '3' - peristaltic pump #3 - EC Up (Dispense Nutrient Solution)     #
#                                                                              #
# -----------------------------------------------------------------------------#
class Monitor:
    def __init__(self, sPort):
        self.sPort = sPort
        self.tunnel = serial.Serial(sPort, 9600)
        self.lightStatus = False
        self.fanStatus = False
        self.pStatus = [False, False, False]
    # ---------------------------Sensor Reading -------------------------------#
    def ecSensor(self):
        self.tunnel.write(b'SE\n')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = data.decode()
        data = data.rstrip()
        data = float(data)
        return data

    def phSensor(self):
        self.tunnel.write(b'SP\n')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def tmpSensor(self):
        self.tunnel.write(b'ST\n')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def humSensor(self):
        self.tunnel.write(b'SH\n')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def watSensor(self):
        self.tunnel.write(b'SW\n')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def getAllSensors(self):
        data = []
        data.append(self.ecSensor())
        data.append(self.phSensor())
        data.append(self.tmpSensor())
        data.append(self.humSensor())
        data.append(self.watSensor())
        data.append(self.lightStatus)
        data.append(self.fanStatus)
        data.extend(self.pStatus)
        return data

    # -----------------------------System Control -----------------------------#
    def lightSwitch(self, state):
        time.sleep(.1)
        if state:
            self.tunnel.write(b'CFH\n')
            self.lightStatus = True
        else:
            self.tunnel.write(b'CFL\n')
            self.lightStatus = False

    def fanSwitch(self, state):
        time.sleep(.1)
        if state:
            self.tunnel.write(b'CLH\n')
            self.fanStatus = True
        else:
            self.tunnel.write(b'CLL\n')
            self.fanStatus = False

    def pumpSwitch(self, pump, state):
        time.sleep(.1)
        message = f'CU{pump}'
        if state:
            self.tunnel.write(bytes(f'{message}\n', 'utf-8'))
            self.pStatus[pump - 1] = True
