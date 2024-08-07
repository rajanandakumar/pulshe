import os, time, datetime, pathlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pandas as pd

def okayToWrite(conf, uid, staff):
    oStatus = False
    rad_due = {}

    report_list = ["misc_trainings", "coshh_trainings", "laser_trainings", "rad_trainings"]
    for report in report_list:    
        if report == "misc_trainings":
            radTr = staff.misc_training_status[uid]
        elif report == "coshh_trainings":
            radTr = staff.coshh_training_status[uid]
        elif report == "laser_trainings":
            radTr = staff.laser_training_status[uid]
        elif report == "rad_trainings":
            radTr = staff.rad_training_status[uid]

        if not radTr: # Not a staff, fixed term or agency
            continue

        for tr in conf[report]:
            training = tr[0]
            if training not in radTr.keys():
                continue
            dTrn = radTr[training]
            rad_due[training] = dTrn

            if isinstance(dTrn, type(())):
                dDue = dTrn[1] + relativedelta(years=+5)
            elif isinstance(dTrn, type(datetime.datetime(1,1,1))):
                dDue = dTrn + relativedelta(years=+5)
            else: # This training has not been done
                continue
            oStatus = True
            dNow = datetime.datetime.now()
            colour = "#f6566b"
            if dDue > dNow:
                colour = "#99ee99"
            rad_due[training] = (dDue, colour)
    return (oStatus, rad_due)

def writeOutTrainings(staff, conf, debug=False):
    outDir = "training"
    she_sheet_date = staff.SHE_spreadsheet_date
    totara_sheet_date = staff.Totara_spreadsheet_date
    for uid in staff.nList:
        ff = "index.html"  # Keep the file name simple
        outSubdir = outDir + "/" + staff.person[uid]["Email"]  # Person identified by email
        fname = outSubdir + "/" + ff

        pathlib.Path(outSubdir).mkdir(exist_ok=True)  # Hope it does not crash?
        # print(f"Writing information for ... {fname}")
        f = open(fname, "w")
        writeOutHeader(f, uid, staff.person[uid], totara_sheet_date)
        nOKTrs = writeOutTraining(f, conf, uid, staff.trainings_status[uid], staff.trainings_dueDate[uid])
        writeOutFooter(f)

        # Write out the miscellaneous trainings if they exist
        if conf["optionalTrainings"]:
            status = okayToWrite(conf, uid, staff)
            if status[0]:
                writeOutNonMandTraining(f, conf, status[1])
        writeOutFooter(f, non_mand=True)
        f.close()

        # A status flag in the directory for flask
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
        open(fnam, "a").close()  # Just need an empty file

def writeOutNonMandTraining(hOut, conf, training_status):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write(
        """<p><table><tr><th>Non-mandatory SHE training</th><th> Status </th><th> Training expiry date</th></tr>\n"""
    )
    for k, v in training_status.items():
        if v:
            col = v[1]
            dat = v[0]
            status = "Expired"
            if col == '#99ee99':
                status = "OK"
            xURL = ""
            for tr in conf["misc_trainings"]:
                if k == tr[0]:
                    xURL = tr[2]
            if len(xURL) > 2:
                hOut.write(f"<tr><td> <a href={xURL}>{k}</a> </td> <td  style='background-color:{col}'> {status} </td> <td> {dat} </td>")
            else:
                hOut.write(f"<tr><td> {k} </td> <td  style='background-color:{col}'> {status} </td> <td> {dat} </td>")
    hOut.write("</table>")


def writeOutTraining(hOut, conf, uid, training_status, tr_dueDate):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write(
        """<p><table><tr><th>Mandatory SHE training</th><th> Status </th><th> Date last completed</th><th> Training expiry date</th></tr>\n"""
    )

    nOKTrainings = 0

    for tr in conf["she_trainings"]:
        training = tr[0]
        if training.startswith("TEST for ALL"):
            continue
        xURL = tr[2]
        # What training it is
        hOut.write("""<tr><td> <a href="%s">%s</a> </td>""" % (xURL, training))

        if training not in training_status.keys():  # Quickly write out no record and proceed
            col = "#FF9F00"
            col_date = "#FF9F00"  # "#99ee99"
            status = "No Record"
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, status))
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, " "))
            hOut.write("""</tr>\n""")
            tr_dueDate[training] = ["No Record", col_date, "Due"]
            continue

        # Training status
        statList = training_status[training]
        status = statList[0]
        col = "#f6566b"  # Default to red
        if status in ["In date", "OK", "Complete", "Complete via rpl"]:
            col = "#52D017"
            status = "Up to date"
        elif status == "In progress":
            col = "yellow"

        s_date = statList[1]
        if isinstance(s_date, type(pd.NaT)):
            s_date = -1.0
        if s_date == "":
            s_date = "0/0/0"

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
            if dDue < dNow:
                if not (training.startswith("Asbestos") or training.startswith("Electrical") or "BiteSize" in training):
                    col_date = "#ee9999"
                    if col == "#52D017":
                        # Training was only from Totara information
                        # print("Error in status from SHE table - reset colour.", uid, training)
                        col = "#f6566b"
                        status = "Out of date"
        if s_date == "0/0/0":  # Training not done / recorded
            col_date = "#ffa500"

        hOut.write("""<td style="background-color:%s"> %s</td>""" % (col, status))

        if s_date == "0/0/0":
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, "No Record"))
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, str(s_date)[:10]))

        #  Date training is due
        # if training.startswith("Asbestos") or training.startswith("Electrical") or "BiteSize" in training:
        if training in conf["always_valid_trainings"]:
            if str(s_date)[:2] == "20":  # Has been done this century
                hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, "Does not expire"))
                tr_dueDate[training] = [str(s_date)[:10], col_date, "OK"]
            else:
                hOut.write("""<td style="background-color:%s"> %s</td>""" % ("#FF7777", "Needed"))
                tr_dueDate[training] = [str(s_date)[:10], "#FF7777", "Due"]
        else:
            hOut.write("""<td style="background-color:%s"> %s</td>""" % (col_date, str(dDue)[:10]))
            tr_dueDate[training] = [str(dDue)[:10], col_date, "...."]

        if tr_dueDate[training][1] == "#99ee99":
            nOKTrainings = nOKTrainings + 1  # The SHE spreadsheet is out of date. So cannot rely on it.

        hOut.write("""</tr>\n""")
    hOut.write("</table>")
    return nOKTrainings


def writeOutHeader(hOut, uid, person, totara_date, non_mand=False):
    pNN = person["Forename"] + " " + person["Surname"]
    if non_mand:
        hOut.write(f"<HEAD>\n  <TITLE>PPD non mandatory trainings record for {pNN}</TITLE>")
    else:
        hOut.write(f"<HEAD>\n  <TITLE>PPD SHE trainings record for {pNN}</TITLE>")
    hOut.write(
        """
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
"""
    )
    if non_mand:
        hOut.write("""<p style="font-size:25px">Non-Mandatory training status for %s </p>""" % pNN)
    else:
        hOut.write("""<p style="font-size:25px">Mandatory training status for %s </p>""" % pNN)
        hOut.write("""<p style="font-size:20px">Report preparation date: %s </p>\n""" % str(totara_date)[:10])
    hOut.write("\n")

def writeOutFooter(hOut, non_mand=False):
    hOut.write("\n<p>\n")
    if not non_mand:
        hOut.write(
        """<p style="border: 1px solid lightgray; background: lightyellow; font-size:20px">
The links above will each take you directly to the relevant online training. Make sure you are logged
in first <a href="https://lmsweb.stfc.ac.uk/moodle/totara/dashboard/" target="_blank" rel="noopener noreferrer"> here in the totara portal </a>
(opens in separate tab). </p>\n\n"""
    )
    else:
        hOut.write("\n")
        hOut.write(f"    </body>\n  </html>\n")
