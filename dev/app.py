from flask import Flask, request
from flask import render_template, url_for, send_from_directory
import json
import os
# user email ID coming in from the login could be arbitrarily capitalised
# Manager emails should all be lower case by design of the programme
with open("/home/local/nraja/ppd/pulshe/ppd_organogram.json") as f:
    managers = json.load(f)

app = Flask(__name__)

@app.route("/")
def hello():
    user = request.authorization['username'].lower()
    if isManager():
        return render_template('manager.html', my_string=user, my_employees=myEmployees())
    # The user is not a manager - return just the page itself
    return onePerson(user=user)

@app.route("/<string:user>")
def onePerson(user):
    current_user = request.authorization['username'].lower()
    if user == current_user or isMyEmployee(user):
        localDir = "/home/local/nraja/ppd/pulshe/training/"
        fileName = "index.html"
        if os.path.isfile(os.path.join(localDir, user, fileName)):
            return send_from_directory(localDir + user, fileName)
        else:
            return "Wrong department? - 404 times sorry!", 404
    else:
        return "Not authorised - 401 times sorry!", 401

def isManager():
    current_user = request.authorization['username'].lower()
    for manager in managers.keys():
        if current_user == manager:
            return True
    return False

def myEmployees():
    if not isManager(): return []
    current_user = request.authorization['username'].lower()
    for manager in managers.keys():
        if current_user == manager:
            return managers[manager]

def isMyEmployee(user):
    if not isManager(): return False
    current_user = request.authorization['username'].lower()
    for manager in managers.keys():
        if current_user == manager:
            if user in managers[manager]: return True
    return False

if __name__ == "__main__":
    app.run()
