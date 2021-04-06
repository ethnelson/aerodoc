from arduino_comms import Database

import random
import time


def data_shuf(dbase):
    data = [random.randint(1100, 1400), # EC
            random.randrange(7, 8),     # PH
            random.randint(25, 30),     # Temp
            random.randint(40, 60),     # humidity
            1]                    # water level (low / high)

    dbase.insertData(data)

def inputData():
    db = Database('datadb')
    db.createTable()

    for i in range(0, 1):
        data_shuf(db)
        print('input into dabase')
        time.sleep(.1)






db = Database('datadb')

inputData()
data = db.readLast()
print(data)
