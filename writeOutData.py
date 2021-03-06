import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pandas as pd

def writeOutTrainings(staff, conf, debug=False):
    outDir = "training"
    she_sheet_date = staff.SHE_spreadsheet_date
    totara_sheet_date = staff.Totara_spreadsheet_date
    for uid in staff.nList:
        ff = "index.html" # Keep the file name simple
        outSubdir = outDir + "/" + staff.person[uid]["Email"] # Person identified by email
        fname = outSubdir + "/" + ff
        # if uid != "Raja Nandakumar": continue

        pathlib.Path(outSubdir).mkdir(exist_ok=True) # Hope it does not crash?

        f = open(fname, "w")
        writeOutHeader(f, uid, totara_sheet_date)
        nOKTrs = writeOutTraining(f, conf, uid, staff.trainings_status[uid], staff.trainings_dueDate[uid])
        writeOutFooter(f)
        f.close()
        writeOKay(outSubdir)
        if nOKTrs == len(conf["she_trainings"]) - 1:
            writeOKay(outSubdir, okay=True)
        # print(uid, nOKTrs, len(conf["she_trainings"]))

def writeOKay(path, okay=False):
    fnam = path + "/ok"
    if not okay:
        if os.path.exists(fnam):
            os.unlink(fnam)
    else:
        open(fnam,'a').close() # Just need an empty file



def writeOutTraining(hOut, conf, uid, training_status, tr_dueDate):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write("""<p><table><tr><th>Mandatory SHE training</th><th> Status </th><th> Date last completed</th><th> Training expiry date</th></tr>\n""")

    nOKTrainings = 0

    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"): continue
        xURL = tr[2]
        # What training it is
        hOut.write("""<tr><td> <a href="%s">%s</a> </td>""" %(xURL, training))

        if training not in training_status.keys(): # Quickly write out no record and proceed
            col = "#FF9F00"
            col_date = "#FF9F00" # "#99ee99"
            status = "No Record"
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, " "))
            hOut.write("""</tr>\n""" )
            tr_dueDate[training] = ["No Record", col_date, "Due"]
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
                if not (training.startswith("Asbestos") or training.startswith("Electrical") or "BiteSize" in training):
                    col_date = "#ee9999"
        if s_date == "0/0/0": # Training not done / recorded
            col_date = "#ffa500"

        if s_date == "0/0/0":
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, "No Record"))
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, str(s_date)[:10]))

        #  Date training is due
        if training.startswith("Asbestos") or training.startswith("Electrical") or "BiteSize" in training:
            if str(s_date)[:2] == "20": # Has been done this century
                hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, "Does not expire"))
                tr_dueDate[training] = [str(s_date)[:10], col_date, "OK"]
            else:
                hOut.write("""<td style="background-color:%s"> %s</td>""" %("#FF7777", "Needed"))
                tr_dueDate[training] = [str(s_date)[:10], "#FF7777", "Due"]
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, str(dDue)[:10]))
            tr_dueDate[training] = [str(dDue)[:10], col_date, "...."]

        if tr_dueDate[training][1] == "#99ee99":
            nOKTrainings = nOKTrainings + 1 # The SHE spreadsheet is out of date. So cannot rely on it.

        hOut.write("""</tr>\n""" )
    hOut.write("</table>")
    return nOKTrainings

def writeOutHeader(hOut, uid, totara_date):
    hOut.write("""
<HEAD>
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
    hOut.write("""<p style="border: 1px solid lightgray; background: lightyellow; font-size:20px">
The links above will each take you directly to the relevant online training. Make sure you are logged
in first <a href="https://lmsweb.stfc.ac.uk/moodle/totara/dashboard/" target="_blank" rel="noopener noreferrer"> here in the totara portal </a>
(opens in separate tab). </p>""")
    hOut.write("\n")
    hOut.write("""
  </body>
</html>
""")
