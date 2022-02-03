import os, time

def writeOutTrainings(staff, debug=False):
    outDir = "training/"
    for uid in staff.nList:
        fname = outDir + uid + ".html"
        f = open(fname, "w")
        writeOutHeader(f, uid)
        writeOutTraining_SHE(f, uid, staff.trainings_she[uid])
        writeOutTraining_Totara(f, uid, staff.trainings_totara[uid])
        writeOutFooter(f)

def writeOutTraining_SHE(hOut, uid, trainings):
    hOut.write("""<p><table style="width:100%"><tr><th> SHE training </th><th> Status </th></tr>
<tr><td>""")

    for training, status in trainings.items():
        col = "#fffafa"
        if status == "In date": col = "green"
        elif status == "OK": col = "green"
        else :
            if type(status) == type("str") and "/" in status: # probably date
                dTrn = time.strptime(status, "%d/%m/%Y")
                dNow = time.strptime(time.strftime("%d/%m/%Y",time.localtime()), "%d/%m/%Y")
                if dTrn < dNow : col = "red"
                else: col = "green"

        hOut.write("""<tr><td> %s </td><td style="background-color:%s"> %s</td></tr>\n""" %(training, col, status))
    hOut.write("</table>")

def writeOutTraining_Totara(hOut, uid, trainings):
    hOut.write("""<p><table style="width:100%"><tr><th> Training training </th><th> Status </th></tr>
<tr><td>""")

    for training, status in trainings.items():
        col = "#fffafa"
        if status.startswith("Complete"): col = "green"
        elif status == "In progress": col = "orange"
        elif status == "Not yet started": col = "grey"
        hOut.write("""<tr><td> %s </td><td style="background-color:%s"> %s</td></tr>\n""" %(training, col, status))
    hOut.write("</table>")


def writeOutHeader(hOut, uid):
    hOut.write("""
<HEAD>
    <meta http-equiv="refresh" content="1800">
    <TITLE>PPD SHE trainings record for %s</TITLE>
    <style type="text/css">
    div.white {
        background-color: #fffafa;
    }
    div.red {
        background-color: red;
    }
    div.cyan {
        background-color: cyan;
    }
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 5px;
    }
    th {
    text-align: left;
    }
</style>
</HEAD>
<BODY>
<pre>
%s
This web page displays the SHE training information for %s from Totara and SHE
</pre>
"""
    %(uid, time.strftime("Date : %d %b %Y \nTime : %H:%M:%S\n", time.localtime()), uid))

def writeOutFooter(hOut):
    hOut.write("""
  </body>
</html>
""")