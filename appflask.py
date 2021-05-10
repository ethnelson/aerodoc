#!packages/bin/python3
from flask import Flask, render_template, request, Response, url_for, send_file
from time import strftime, localtime
import sys
import os
import pickle
sys.path.append('scripts/')
from arduino_comms import Database
from controller import aeroD
import json
import configparser

app = Flask(__name__)

# ---------------------------------------------------------------------------- #
#                              HELPER FUNCTIONS                                #
# ---------------------------------------------------------------------------- #
# ------------------------------ CONFIGURATION ------------------------------- #

def getConf():
    systemConf = configparser.ConfigParser()
    systemConf.read('aerodoc.ini')
    data = {}
    for section in systemConf.sections():
        for key, value in systemConf.items(section):
            data[key] = value
    return data

def updateConf(data):
    systemConf = configparser.ConfigParser()
    systemConf.read('aerodoc.ini')
    for section in systemConf.sections():
        for key, value in systemConf.items(section):
            systemConf[section][key] = data[key]

    with open('aerodoc.ini', 'w') as configFile:
        systemConf.write(configFile)

# ----------------------------- NOTIFICATIONS -------------------------------- #
def getNote():
    noteBuffer = pickle.load(open('noteBuffer.p', 'rb'))
    noteBuffer.reverse()
    noteDict = {}
    for i in range(0, len(noteBuffer)):
        noteDict[i] = noteBuffer[i]
    noteBuffer = []
    pickle.dump(noteBuffer, open('noteBuffer.p', 'wb'))
    return noteDict


# ----------------------------- CAMERA STREAMING ----------------------------- #
# TO BE DEVELOPED

# ---------------------------------------------------------------------------- #
#                                 WEB PAGES                                    #
# ---------------------------------------------------------------------------- #
# ------------------------------- HOME PAGE ---------------------------------- #
@app.route('/')
@app.route('/index')
def index():
    conf_data = getConf()
    return render_template('template.html', conf=conf_data)

@app.route('/noteUpdate')
def noteUpdate():
    noteDict = getNote()
    as_json = json.dumps(noteDict)
    return as_json
# ------------------------------ SENSORS PAGE -------------------------------- #

@app.route('/sensors')
def sensors():
    conf_data = getConf()
    return render_template('sensors.html', conf=conf_data)

@app.route('/sensors/data', methods=['GET'])
def getData():
    conf_data = getConf()
    range = int(conf_data['chart_range'])
    try:
        db = Database('datadb')
        data = db.readLastMult(range)
    except:
        return "Error reading database"
    if data:
        as_json = json.dumps(data)
        return as_json
    else:
        return None

@app.route('/sensors/dataUpdate', methods=['GET'])
def getDataUpdate():
    try:
        db = Database('datadb')
        data = db.getBuffer()
    except:
        return "Error getting data buffer"

    if data:
        as_json = json.dumps(data)
        return as_json
    else:
        return None
# ------------------------------- CAMERA PAGE -------------------------------- #
@app.route('/camera')
def camera():
    conf_data = getConf()
    return render_template('camera.html', conf=conf_data)

@app.route('/camera_feed')
def camera_feed():
    file = 'static/img/501_error.png'
    return send_file(file, mimetype='image/png')

# ------------------------------ SETTINGS PAGE ------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        data = request.form
        updateConf(data)
        return render_template("settings.html", conf=data)
    else:
        data = getConf()
        return render_template('settings.html', conf=data)

if __name__ == '__main__':
    try:
        daemon = aeroD()
        app.run(debug=False)
    except KeyboardInterrupt:
        daemon.stop()
        sys.exit(0)
