from flask import Flask, render_template, request
import sys
sys.path.append('scripts/')
from arduino_comms import Database
import json

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    return ender_template('template.html')

@app.route('/sensors')
def sensors():
    return render_template('sensors.html')


@app.route('/sensors/data', methods=['GET'])
def getData():
    try:
        db = Database('datadb')
        data = db.readLastTen()
        as_json = json.dumps(data)
        return as_json
    except:
        return "Error reading database"
    finally:
        db.close()

@app.route('/sensors/dataUpdate', methods=['GET'])
def getDataUpdate():
    try:
        db = Database('datadb')
        data = db.readLast()
        as_json = json.dumps(data)
        return as_json
    except:
        return "Error reading database"
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
