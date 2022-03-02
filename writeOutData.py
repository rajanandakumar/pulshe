import os, time, datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pandas as pd

def writeOutTrainings(staff, debug=False):
    outDir = "training/"
    she_sheet_date = staff.SHE_spreadsheet_date
    totara_sheet_date = staff.Totara_spreadsheet_date
    for uid in staff.nList:
        fname = outDir + uid + ".html"
        # if uid != "Raja Nandakumar": continue
        f = open(fname, "w")
        writeOutHeader(f, uid, she_sheet_date, totara_sheet_date)
        writeOutTraining(f, uid, staff.trainings_status[uid])
        writeOutFooter(f)
        f.close()

def writeOutTraining(hOut, uid, training_status):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write("""<p><table><tr><th>Mandatory SHE training</th><th> Status </th><th> Date last completed</th><th> Training expiry date</th></tr>\n""")
    for training, statList in training_status.items():
        if training.startswith("TEST for ALL"): continue
        status = statList[0]
        s_date = statList[1]
        source = statList[2]
        if isinstance(s_date, type(pd.NaT)):
            s_date = -1.0

        # What training it is
        hOut.write("""<tr><td> %s </td>""" %training)

        # The status of the training. Colour can dominate?
        col = "#fffafa"
        if status in ["In date", "OK", "Complete", "Complete via rpl"]:
            col = "green"
            status = "Up to date"
        elif status == "In progress": col = "yellow"
        hOut.write("""<td style="background-color:%s"> %s</td>""" %(col, status))

        # The date of the training and its manipulations
        col_date = "#fffafa"
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
            hOut.write("""<td style="background-color:%s"> %s</td>""" %(col_date, "Not yet done?"))
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

def writeOutHeader(hOut, uid, she_date, totara_date):
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
<pre>
""")
    hOut.write("Report preparation and staff listing date and time: ")
    hOut.write(time.strftime(" %d %b %Y, %H:%M:%S\n", time.localtime()))
    hOut.write("\n")
    hOut.write("SHE spreadsheet dated : %s\n" % str(she_date)[:10])
    hOut.write("Totara spreadsheet dated : %s\n" % str(totara_date)[:10])
    hOut.write("\n")
    hOut.write("""
This web page displays the SHE training information for %s from Totara and SHE
</pre>
""" % uid)

def writeOutFooter(hOut):
    hOut.write("\n<p>\n")
    hOut.write("""Note : If you want to update any of your trainings, they are now online\
        and available on the <a href="https://lmsweb.stfc.ac.uk/moodle/totara/dashboard/">\
        Totara portal </a>""")
    hOut.write("\n")
    hOut.write("""
  </body>
</html>
""")