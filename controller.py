import sys
sys.path.append('scripts/')
from arduino_comms import Database, Monitor
import time

DATABASE_NAME = 'datadb'
port = '/dev/ttyACM0'
mon = Monitor(port)
db = Database(DATABSE_NAME)

#-------------------------------- UPDATE DB -----------------------------------#
if __name__ == '__main__':
    while (True):
        data = mon.getAllSensors()
        db.createTable()
        db.insertData(data)
        time.sleep(15)
