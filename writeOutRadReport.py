import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import uuid

# Do the minimal outside of this place. All the needed manipulations of the rad data are here.


def okayToWrite(conf, uid, radTr):
    oStatus = False
    rad_due = {}
    for tr in conf["rad_trainings"]:
        training = tr[0]
        dTrn = radTr[training]
        rad_due[training] = dTrn
        if type(dTrn) == type("a"):
            continue
        oStatus = True
        dDue = dTrn + relativedelta(years=+5)
        dNow = datetime.datetime.now()
        colour = "#f6566b"
        if dDue > dNow:
            colour = "#99ee99"
        rad_due[training] = (dDue, colour)
    return (oStatus, rad_due)


def writeOutRadReport(staff, conf, debug=False):
    outDir = "training"
    fileName = outDir + "/ppd-rad-" + str(uuid.uuid4()) + ".html"
    sheet_date = staff.Totara_spreadsheet_date
    f = open(fileName, "w")
    writeOutRadReportHeader(f, conf, sheet_date)

    for uid in staff.nList:
        if staff.person[uid]["Location"] != "RAL filtered":
            continue

        status = okayToWrite(conf, uid, staff.rad_training_status[uid])
        if not status[0]:
            # Person has had no rad training ever
            continue
        radDue = status[1]
        p = staff.person[uid]
        pNN = p["Forename"] + " " + p["Surname"]
        f.write("""<tr><td style="background-color:white"> %s</td>""" % pNN)
        for tr in conf["rad_trainings"]:
            training = tr[0]
            if radDue[training] == "":
                f.write("""<td style="background-color:%s"> %s</td>""" % ("white", ""))
            else:
                rOut = str(radDue[training][0])[:10]
                f.write("""<td style="background-color:%s"> %s</td>""" % (radDue[training][1], rOut))
        f.write("</tr>\n")
    print("\n")
    writeOutRadReportFooter(f)
    f.close()


def writeOutRadReportHeader(hOut, conf, she_date):
    hOut.write(
        """
<HEAD>
    <TITLE>PPD SHE radiation trainings record for PPD</TITLE>
"""
    )
    hOut.write(
        """
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
"""
    )
    hOut.write("""<p style="font-size:20px">Report preparation date: %s </p>\n""" % str(she_date)[:10])
    hOut.write("""<p><table><tr><th style="background-color:white">Name</th>""")
    for tr in conf["rad_trainings"]:
        training = tr[0]
        hOut.write("""<th style="background-color:white"> %s</th>""" % training)
    hOut.write("\n")


def writeOutRadReportFooter(hOut):
    hOut.write("\n<p>\n")
    hOut.write(
        """
  </body>
</html>
"""
    )
