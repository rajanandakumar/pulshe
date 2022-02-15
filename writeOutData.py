import os, time, datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def writeOutTrainings(staff, debug=False):
    outDir = "training/"
    for uid in staff.nList:
        fname = outDir + uid + ".html"
        f = open(fname, "w")
        writeOutHeader(f, uid)
        writeOutTraining(f, uid, staff.trainings_status[uid], staff.trainings_date[uid])
        writeOutFooter(f)
        f.close()

def writeOutTraining(hOut, uid, training_status, training_date):
    hOut.write("""<hr align="center" width="70%">\n""")
    hOut.write("""<p><table><tr><th> SHE training </th><th> Status, source </th><th> Date, source </th></tr>\n""")
    for training, statList in training_status.items():
        special = True
        col = "#fffafa"
        col_date = "#fffafa"
        status = statList[0]
        source = statList[1]
        if status in ["In date", "OK", "Complete", "Complete via rpl"]:
            col = "green"
        elif status == "In progress": col = "yellow"

        status_date = "Unknown"
        if training != "Fire test" and not training.startswith("TEST for ALL"):
            special = False
            if training in training_date:
                status_date = training_date[training][0]
                source_date = training_date[training][1]
            else : # No Totara records?
                special = True
        if not special and type(status_date) == type("str") and "/" in status_date: # probably date
            # dTrn = time.strptime(status, "%d/%m/%Y")
            # dNow = time.strptime(time.strftime("%d/%m/%Y",time.localtime()), "%d/%m/%Y")
            dTrn = parse(status_date)
            dNow = datetime.datetime.now()
            col_date = "green"
            if dTrn + relativedelta(years=+5) < dNow : col_date = "red"
        statOut = status + "," + source
        if special :
            hOut.write("""<tr><td> %s </td><td style="background-color:%s"> %s</td><td></td></tr>\n""" %(training, col, statOut))
        else:
            if type(status_date) == type(1.0):
                status_date = "Unknown"
            statOut_date = status_date + "," + source_date
            hOut.write("""<tr><td> %s </td><td style="background-color:%s"> %s</td><td style="background-color:%s"> %s</td></tr>\n""" %(training, col, statOut, col_date, statOut_date))
    hOut.write("</table>")

def writeOutHeader(hOut, uid):
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
    }
    th {
        padding: 6px;
        text-align: left;
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
    hOut.write(time.strftime("Date : %d %b %Y \nTime : %H:%M:%S\n", time.localtime()))
    hOut.write("""
This web page displays the SHE training information for %s from Totara and SHE
</pre>
""" % uid)

def writeOutFooter(hOut):
    hOut.write("""
  </body>
</html>
""")