from flask import Flask, request, g
from flask import render_template, url_for, send_from_directory
import json
import os
# user email ID coming in from the login could be arbitrarily capitalised
# Manager emails should all be lower case by design of the programme
with open("/data/pulshe/dev/ppd/ppd_organogram.json") as f:
    workers = json.load(f)

app = Flask(__name__)

@app.route("/")
def hello():
    user = request.authorization['username'].lower()
    if isManager():
        return render_template('manager.html', me=user, organogram=myEmployees())
        # print(myEmployees())
    # The user is not a manager - return just the page itself
    print(user, "is not a manager?")
    return onePerson(user=user)

@app.route("/<string:user>")
def onePerson(user):
    current_user = request.authorization['username'].lower()
    if user == current_user or isMyEmployee(user):
        localDir = "/data/pulshe/training/ppd/"
        fileName = "index.html"
        if os.path.isfile(os.path.join(localDir, user, fileName)):
            return send_from_directory(localDir + user, fileName)
        else:
            return "Wrong department? - 404 times sorry!", 404
    else:
        return "Not authorised - 401 times sorry!", 401

def isManager():
    current_user = request.authorization['username'].lower()
    if workers.get(current_user, []):
        return True
    return False

def myEmployees():
    if not isManager(): return []
    current_user = request.authorization['username'].lower()
    thisGram = {}
    if workers.get(current_user, []):
        thisGram = get_all_my_workers(current_user)
    return thisGram

def get_all_my_workers(user):
    all_my_workers = {}
    immediate_workers = workers.get(user, [])
    for worker in immediate_workers:
        all_my_workers[worker] = get_all_my_workers(worker)
    return all_my_workers

def list_all_my_workers(user, all_my_workers=[]):
    immediate_workers = workers.get(user, [])
    for worker in immediate_workers:
        all_my_workers.append(worker)
        list_all_my_workers(worker, all_my_workers)
    return all_my_workers

def isMyEmployee(user):
    if not isManager(): return False
    current_user = request.authorization['username'].lower()
    if user in list_all_my_workers(current_user):
        return True
    return False

if __name__ == "__main__":
    app.run()
