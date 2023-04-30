import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import uuid

# Do the minimal outside of this place. All the needed manipulations of the rad data are here.


def okayToWrite(conf, uid, report, staff):
    oStatus = False
    rad_due = {}

    if report == "misc_trainings":
        radTr = staff.misc_training_status[uid]
    elif report == "coshh_trainings":
        radTr = staff.coshh_training_status[uid]
    elif report == "laser_trainings":
        radTr = staff.laser_training_status[uid]
    elif report == "rad_trainings":
        radTr = staff.rad_training_status[uid]

    for tr in conf[report]:
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


def writeOutNonMandReportHeader(hOut, conf, she_date, report):
    if report == "misc_trainings":
        myStr = "miscellaneous"
    elif report == "laser_trainings":
        myStr = "laser"
    elif report == "coshh_trainings":
        myStr = "COSHH"
    else:
        myStr = "UNKNOWN (error!)"
    hOut.write(f"<HEAD>\n    <TITLE>PPD SHE {myStr} trainings record for PPD</TITLE>\n")
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
    for tr in conf[report]:
        training = tr[0]
        hOut.write("""<th style="background-color:white"> %s</th>""" % training)
    hOut.write("\n")


def writeOutNonMandReportFooter(hOut):
    hOut.write("\n<p>\n")
    hOut.write(
        """
  </body>
</html>
"""
    )

def writeOutNonMandReport(staff, conf, report, debug=False):
    outDir = "training"
    file_ral = outDir + "/ppd-ral-" + report + "-" + str(uuid.uuid4()) + ".html"
    file_boulby = outDir + "/ppd-boulby-" + report + "-" + str(uuid.uuid4()) + ".html"
    SHE_sheet_date = staff.SHE_spreadsheet_date
    f_ral = open(file_ral, "w")
    f_boulby = open(file_boulby, "w")
    writeOutNonMandReportHeader(f_ral, conf, SHE_sheet_date, report)
    writeOutNonMandReportHeader(f_boulby, conf, SHE_sheet_date, report)

    for uid in staff.nList:
        if staff.person[uid]["Location"] != "RAL filtered":
            continue

        f = f_ral
        xl = staff.person[uid]['Exchange']
        if isinstance(xl, str) and xl.lower().startswith("boulby"):
            f = f_boulby

        status = okayToWrite(conf, uid, report, staff)

        if not status[0]:
            # Person has had no rad training ever
            continue
        radDue = status[1]
        p = staff.person[uid]
        pNN = p["Forename"] + " " + p["Surname"]
        f.write("""<tr><td style="background-color:white"> %s</td>""" % pNN)
        for tr in conf[report]:
            training = tr[0]
            if radDue[training] == "":
                f.write("""<td style="background-color:%s"> %s</td>""" % ("white", ""))
            else:
                rOut = str(radDue[training][0])[:10]
                f.write("""<td style="background-color:%s"> %s</td>""" % (radDue[training][1], rOut))
        f.write("</tr>\n")
    # print("\n")
    writeOutNonMandReportFooter(f_ral)
    writeOutNonMandReportFooter(f_boulby)
    f_ral.close()
    f_boulby.close()

