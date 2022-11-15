from flask import Flask, request, g
from flask import render_template, url_for, send_from_directory
import json
import os, sys

# user email ID coming in from the login could be arbitrarily capitalised
# Manager emails should all be lower case by design of the programme
# with open("/home/nraja/my_heplnv116/dev/ppd/ppd_organogram.json") as f:
with open("/data/pulshe/dev/ppd/ppd_organogram.json") as f:
    workers = json.load(f)

app = Flask(__name__)

sheResponsibles = [
    "dave.newbold@stfc.ac.uk",
    "debbie.loader@stfc.ac.uk",
    "maurits.van-der-grinten@stfc.ac.uk",
    "raja.nandakumar@stfc.ac.uk",
    "chris.brew@stfc.ac.uk",
]

# Overall manager!
specialViewers = ["debbie.loader@stfc.ac.uk",
"raja.nandakumar@stfc.ac.uk"]


@app.route("/")
def hello():
    user = request.authorization["username"].lower()
    if isManager():
        sheTable = False
        if user in sheResponsibles:
            sheTable = True
        if user in specialViewers:
            theEmployees = workers
        else:
            theEmployees = myEmployees()
        return render_template("manager3.html", dept="ppd", me=user, organogram=theEmployees, showTable=sheTable)
    # The user is not a manager - return just the page itself
    print(user, "is not a manager?")
    return onePerson(dept="ppd", user=user)


@app.route("/<string:dept>/<string:user>")
def onePerson(dept, user):
    current_user = request.authorization["username"].lower()
    if user == current_user or isMyEmployee(user) or current_user in specialViewers:
        localDir = "/data/pulshe/training/ppd/"
        fileName = "index.html"
        if os.path.isfile(os.path.join(localDir, user, fileName)):
            return send_from_directory(localDir + user, fileName)
        else:
            return "Wrong department? - 404 times sorry!", 404
    else:
        return "Not authorised - 401 times sorry!", 401


@app.route("/<string:dept>/<int:type>")
def summaryTable(dept, type):
    current_user = request.authorization["username"].lower()
    if current_user not in sheResponsibles:
        return "Not authorised - please shout even louder.", 401
    localDir = "/data/pulshe/training/ppd/"
    prefix = "temp"
    if dept == "ppd":
        if type == 1:
            prefix = "ppd-0t-"
        else:
            prefix = "ppd-1t-"
    pfile = [filename for filename in os.listdir(localDir) if filename.startswith(prefix)]
    if len(pfile) <= 0:
        return "Could not find Summary Table - sorry!", 202
    return send_from_directory(localDir, pfile[0])


@app.context_processor
def handle_context():
    return dict(os=os)


def isManager():
    current_user = request.authorization["username"].lower()
    if current_user in specialViewers or workers.get(current_user, []):
        return True
    return False


def myEmployees():
    if not isManager():
        return []
    current_user = request.authorization["username"].lower()
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
    if not isManager():
        return False
    current_user = request.authorization["username"].lower()
    if user in list_all_my_workers(current_user):
        return True
    return False


if __name__ == "__main__":
    app.run()
