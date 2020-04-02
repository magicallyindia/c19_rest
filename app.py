import flask
from flask import Flask, render_template, request
from flask_cors import CORS

from dal.datalayer import getgovcenters, getpricenters, addgovcenters, addpricenters
from global_bot import getglobdata
from india_bot import getcurrdata

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        result = flask.request.form
        user = ''
        passw = ''
        for key, value in result.items():
            # these are available to you:
            if key == 'username':
                user = value
            if key == 'password':
                passw = value

        if user == 'chandu' and passw == '1234':
            return flask.render_template('index.html')


@app.route('/govtestCenters', methods=['GET'])
def government():
    args = request.args
    try:
        j = getgovcenters(args)
        return j
    except NameError:
        print(NameError)
        return 'Error in API'


@app.route('/privatetestCenters', methods=['GET'])
def private():
    args = request.args
    try:
        j = getpricenters(args)
        return j
    except NameError:
        print(NameError)
        return 'Error in API'


@app.route('/quarantine', methods=['GET'])
def quarantine():
    data = getcurrdata()
    return data


@app.route('/helpline', methods=['GET'])
def helpline():
    return getglobdata()


@app.route('/redzone', methods=['GET'])
def redzone():
    return render_template('red_zone.html')


@app.route('/addgovernment', methods=['GET', 'POST'])
def insertgovuser():
    return render_template('newgovernmentcenter.html')


@app.route('/addgovtestcenters', methods=['POST'])
def addgovtestcenters():
    args = request.args
    try:
        j = addgovcenters(args)
        return j
    finally:
        return render_template('govlist.html')


@app.route('/addprivate', methods=['GET', 'POST'])
def insertpriuser():
    return render_template('newprivatecenter.html')


@app.route('/addpritestcenters', methods=['POST'])
def addpritestcenters():
    args = request.args
    try:
        j = addpricenters(args)
        return j
    finally:
        return render_template('prilist.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
