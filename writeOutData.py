import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pandas as pd

def writeOutTrainings(staff, conf, debug=False):
    outDir = "training"
    she_sheet_date = staff.SHE_spreadsheet_date
    totara_sheet_date = staff.Totara_spreadsheet_date
    for uid in staff.nList:
        outSubDir = uid
        ff = "index.html" # Keep the file name simple
        od = outDir + "/" + uid
        fname = od + "/" + ff
        # if uid != "Raja Nandakumar": continue

        pathlib.Path(od).mkdir(exist_ok=True) # Hope it does not crash?

        f = open(fname, "w")
        writeOutHeader(f, uid, totara_sheet_date)
        writeOutTraining(f, conf, uid, staff.trainings_status[uid])
        writeOutFooter(f)
        f.close()
        writeOutHTA(od, staff.person[uid]["federalID"])

def writeOutHTA(dOut, fID):
    htaFile = dOut + "/.htaccess"
    f = open(htaFile, "w")
    f.write("Require all denied\n")
    f.write("Require ldap-user %s\n" % fID)
    f.close()

def writeOutTraining(hOut, conf, uid, training_status):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write("""<p><table><tr><th>Mandatory SHE training</th><th> Status </th><th> Date last completed</th><th> Training expiry date</th></tr>\n""")

    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"): continue
        xURL = tr[2]
        # What training it is
        hOut.write("""<tr><td> <a href="%s">%s</a> </td>""" %(xURL, training))

        if training not in training_status.keys(): # Quickly write out no record and proceed
            col = "#FF9F00"
            col_date = "#99ee99"
            status = "No Record"
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, " "))
            hOut.write("""</tr>\n""" )
            continue

        # Training status
        statList = training_status[training]
        status = statList[0]
        col = "#f6566b" # Default to red
        if status in ["In date", "OK", "Complete", "Complete via rpl"]:
            col = "#52D017"
            status = "Up to date"
        elif status == "In progress": col = "yellow"
        hOut.write("""<td style="background-color:%s"> %s</td>""" %(col, status))

        s_date = statList[1]
        if isinstance(s_date, type(pd.NaT)):
            s_date = -1.0

        # The date of the training and its manipulations
        col_date = "#f6566b"
        dDue = "Unknown"
        dTrn = s_date
        col_date = "#115511"
        try:
            dTrn = parse(str(s_date))
        except:
            dTrn = "Unknown"

        if dTrn != "Unknown":
            dNow = datetime.datetime.now()
            col_date = "#99ee99"
            dDue = dTrn + relativedelta(years=+5)
            if  dDue < dNow:
                col_date = "#ee9999"
        if s_date == "0/0/0": # Training not done / recorded
            col_date = "#ffa500"

        if s_date == "0/0/0":
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, "No Record"))
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, str(s_date)[:10]))

        #  Date training is due
        if training.startswith("Asbestos") or training.startswith("Electrical"):
            if str(s_date)[:2] == "20": # Has been done this century
                hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, "Does not expire"))
            else:
                hOut.write("""<td style="background-color:%s"> %s</td>""" %("#FF7777", "Needed"))
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, str(dDue)[:10]))

        hOut.write("""</tr>\n""" )
    hOut.write("</table>")

def writeOutHeader(hOut, uid, totara_date):
    hOut.write("""
<HEAD>
    <meta http-equiv="refresh" content="1800">
    <TITLE>PPD SHE trainings record for %s</TITLE>
    """ % uid)
    hOut.write("""
    <style type="text/css">
    table {
        border-collapse: collapse;
        width: 70%;
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
    tr:nth-child(even) {
        background-color: #D6EEEE;
    }
</style>
</HEAD>
<BODY>
""")
    hOut.write("""<p style="font-size:25px">Mandatory training status for %s </p>""" % uid)
    hOut.write("""<p style="font-size:20px">Report preparation date: %s </p>\n"""%str(totara_date)[:10])
    hOut.write("\n")

def writeOutFooter(hOut):
    hOut.write("\n<p>\n")
    hOut.write("""<p style="font-size:20px">Note : If you want to update any of your trainings, they are now online\
        and available on the <a href="https://lmsweb.stfc.ac.uk/moodle/totara/dashboard/">\
        Totara portal </a> </p>""")
    hOut.write("\n")
    hOut.write("""
  </body>
</html>
""")