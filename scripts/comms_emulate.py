#!packages/bin/python3
import random


class EmuSystem:
    def __init__(self, data={'time': '0000-00-00 00:00:00', 'EC':1.2, 'PH':6,
                                'temp':23, 'hum':30, 'wat':1, 'light':1, 'fan':0,
                                'p1':0, 'p2':0,'p3':0}):
        self.lightStatus = data['light']
        self.fanStatus = data['fan']
        self.pStatus = [data['p1'], data['p2'], data['p3']]
        self.sensors = {
                        'ec'    : float(data['EC']),
                        'ph'    : float(data['PH']),
                        'temp'  : float(data['temp']),
                        'hum'   : float(data['hum']),
                        'wat'   : float(data['wat'])
        }
        self.ranges = {
                        'ec'    : [1, 2.4, 0.1],
                        'ph'    : [4, 11, .25],
                        'temp'   : [20, 30, 0.5],
                        'hum'   : [20, 70, 2],
                        'wat'   : [0, 1, 1]
        }

    def updateData(self):
        for sensor in self.sensors:
            if random.randint(0, 5) == 0:
                stepValue = self.ranges[sensor][2]
                if (sensor == 'ec' and self.pStatus[2]):
                    print('increasing ec')
                    step = stepValue
                elif sensor == 'ec':
                    step = -stepValue
                elif (sensor == 'ph' and self.pStatus[0]):
                    print('increasing ph')
                    step = stepValue
                elif (sensor == 'ph' and self.pStatus[1]):
                    print('decreasing ph')
                    step = -stepValue
                elif (sensor == 'temp' or sensor == 'hum') and self.fanStatus:
                    print('decreasing hum and temp')
                    step = -stepValue
                else:
                    print('random choice selected')
                    step = random.choice([stepValue, -stepValue])

                oldValue = self.sensors[sensor]
                newValue = round(oldValue + step, 2)
                if self.ranges[sensor][0] <= newValue <= self.ranges[sensor][1]:
                    self.sensors[sensor] = newValue
                print(f'Changed {sensor} from {oldValue} => {self.sensors[sensor]}')

    def displaySensors(self):
        for sensor in self.sensors:
            print(f'{sensor} : {self.sensors[sensor]}')

    def getAllSensors(self):
        self.updateData()
        data = []
        for sensor in self.sensors:
            data.append(self.sensors[sensor])
        data.append(self.lightStatus)
        data.append(self.fanStatus)
        data.extend(self.pStatus)
        return data

    def lightSwitch(self, state):
        self.lightStatus = state

    def fanSwitch(self, state):
        self.fanStatus = state

    def pumpSwitch(self, pump, state):
        self.pStatus[pump -1] = state
