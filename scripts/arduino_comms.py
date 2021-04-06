#!packages/bin/python3
import serial
import sqlite3
import time

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
# --------- '1' - peristaltic pump #1                                          #
# --------- '2' - peristaltic pump #2                                          #
# --------- '3' - peristaltic pump #3                                          #
#                                                                              #
# -----------------------------------------------------------------------------#
port = 'COM4'

class Database:
    def __init__(self, name):
        self.name = f'{name}.db'
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()

    def open(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()

    def createTable(self):
        self.open()
        try:
            self.cur.execute('''CREATE TABLE sensorData
                                (dt DATETIME, EC REAL, PH REAL,
                                Temp REAL, Humidity REAL, Water BOOLEAN)''')
            self.con.commit()
        except:
            print('Table exists. passing')
        self.close()

    def insertData(self, data):# data = [ec, ph, temp, hum, wat]
        self.open()
        tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data.insert(0, tim)
        self.cur.execute("INSERT INTO sensorData VALUES (?, ?, ?, ?, ?, ?)",
                        data)
        self.con.commit()
        self.close()

    def readLastTen(self):
        self.open()
        self.cur.execute('''SELECT * FROM sensorData
                            ORDER BY dt
                            DESC LIMIT 10''')
        data = self.cur.fetchall()
        self.con.commit()
        self.close()
        data = self.largeConvertToDict(data)
        return data

    def readLast(self):
        self.open()
        self.cur.execute('''SELECT * FROM sensorData
                            ORDER BY dt
                            DESC LIMIT 1''')
        data = self.cur.fetchone()
        self.con.commit()
        self.close()
        data = self.convertToDict(data)
        return data

    def largeConvertToDict(self, lst):
        names = ['time', 'EC', 'PH', 'temp', 'hum', 'wat']
        dict = {}
        for i in range(0, len(lst)):
            dict[i] = {names[j]: lst[i][j] for j in range(0, len(names))}
        return dict

    def convertToDict(self, lst):
        names = ['time', 'EC', 'PH', 'temp', 'hum', 'wat']
        dict = {}
        dict = {names[i]: lst[i] for i in range(0, len(lst))}
        return dict




class Monitor:
    def __init__(self, sPort):
        self.sPort = sPort
        self.tunnel = serial.Serial(sPort, 9600)
    # ---------------------------Sensor Reading -------------------------------#
    def ecSensor(self):
        self.tunnel.write(b'SE')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = data.decode()
        data = data.rstrip()
        data = float(data)
        return data

    def phSensor(self):
        self.tunnel.write(b'SP')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def tmpSensor(self):
        self.tunnel.write(b'ST')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def humSensor(self):
        self.tunnel.write(b'SH')
        time.sleep(.2)
        data = self.tunnel.readline()
        data = float(data.encode().rstrip())
        return data

    def watSensor(self):
        self.tunnel.write(b'SW')
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
        return data

    # -----------------------------System Control -----------------------------#
    def lightSwitch(self, state):
        time.sleep(.1)
        if state:
            self.tunnel.write(b'CFH')
        else:
            self.tunnel.write(b'CFL')

    def fanSwitch(self, state):
        time.sleep(.1)
        if state:
            self.tunnel.write(b'CLH')
        else:
            self.tunnel.write(b'CLL')

    def pumpSwitch(self, pump, state):
        time.sleep(.1)
        message = f'CU{pump}'
        if state:
            self.tunnel.write(bytes(f'{message}H', 'utf-8'))
        else:
            self.tunnel.write(bytes(f'{message}L', 'utf-8'))
