import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pandas as pd
import uuid
def writeOutReports(staff, conf, workType="Unknown", debug=False):
    outDir = "training"
    if workType == "staff":
        fileName = outDir + "/ppd-0t-" + str(uuid.uuid4()) + ".html"
    else:
        fileName = outDir + "/ppd-3t-" + str(uuid.uuid4()) + ".html"
    totara_sheet_date = staff.Totara_spreadsheet_date
    f = open(fileName, "w")
    writeOutReportHeader(f, conf, totara_sheet_date)

    #stats
    nTot = 0
    nUpToDate = {}
    for tr in conf["she_trainings"]:
        nUpToDate[tr[0]] = 0

    if debug:
        print("\nRecords updated from Totara ...")
        print(f"Name                 Training               DateOfCompletion")
    work_type = ["staff", "fixed term", "agency"]
    for uid in staff.nList:
        if workType == "staff":
            if not staff.person[uid]["work_type"] in work_type:
                continue
        else:
            if staff.person[uid]["work_type"] in work_type:
                continue
        # print("Before filter ...", uid, staff.person[uid])
        if conf["optionalTrainings"]:
            if staff.person[uid]["Location"] != "RAL filtered" : continue
        else:
            if staff.person[uid]["Location"] != "RAL" : continue
        # if staff.person[uid]["Building"] == "Remote working" : continue
        # if type(staff.person[uid]["Band"]) != type("abc") : continue

        p = staff.person[uid]
        pNN = p["Forename"] + " " + p["Surname"]
        f.write("""<tr><td style="background-color:white"> %s</td>""" % pNN)
        nTot = nTot + 1
        # print(uid, staff.person[uid])
        for tr in conf["she_trainings"]:
            training = tr[0]
            if training.startswith("TEST for ALL"): continue
            f.write("""<td style="background-color:%s"> %s</td>""" %(staff.trainings_dueDate[uid][training][1],
                staff.trainings_dueDate[uid][training][0]))
            if staff.trainings_dueDate[uid][training][1] == "#99ee99":
                nUpToDate[training] = nUpToDate[training] + 1
            if training in staff.trainings_status[uid].keys() and staff.trainings_status[uid][training][2] == "Totara":
                if debug:
                    print(f"{uid:20s} {training:25s} {str(staff.trainings_status[uid][training][1])[:10]}")
            # print(staff.trainings_status[uid][training][2])
        # writeOutTraining(f, conf, uid, staff.trainings_status[uid])
        f.write("</tr>\n")
    writeOutReportFooter(f)
    f.close()

    # The stats page only for staff. Not visitors / students
    if workType != "staff":
        return

    # The stats page
    fileName = outDir + "/ppd-1t-" + str(uuid.uuid4()) + ".html"
    totara_sheet_date = staff.Totara_spreadsheet_date
    f = open(fileName, "w")
    writeOutReportHeader(f, conf, totara_sheet_date)
    # The basic totals
    f.write("""<tr><td> %s</td>""" % nTot)
    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"): continue
        f.write("""<td> %s</td>""" % nUpToDate[training])
    # The fractions
    # f.write("""\n<tr><td style="background-color:white"> %</td>""")
    f.write("""\n<tr><td> %</td>""")
    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"): continue
        f.write("""<td style="background-color:light-green"> %.2f</td>""" % (100.0*nUpToDate[training]/nTot))
    writeOutReportFooter(f)
    f.close()


def writeOutReportHeader(hOut, conf, totara_date):
    hOut.write("""
<HEAD>
    <TITLE>PPD SHE trainings record for PPD</TITLE>
""")
    hOut.write("""
    <style type="text/css">
    table {
        border-collapse: collapse;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
    }
    td {
        padding: 3px;
        text-align: center;
    }
    th {
        padding: 6px;
        text-align: center;
        border: 1px solid black;
    }
    tr {
        background-color: #EEEED6;
    }
    tr:nth-child(even) {
        background-color: #D6EEEE;
    }
    </style>
</HEAD>
<BODY>
""")
    hOut.write("""<p style="font-size:20px">Report preparation date: %s </p>\n"""%str(totara_date)[:10])
    hOut.write("""<p><table><tr><th style="background-color:white">Name</th>""")
    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"): continue
        hOut.write("""<th style="background-color:white"> %s</th>""" % training)
    hOut.write("\n")

def writeOutReportFooter(hOut):
    hOut.write("\n<p>\n")
    hOut.write("""
  </body>
</html>
""")
