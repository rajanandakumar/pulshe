import os, sys, datetime, io
import pandas as pd
import numpy as np
import staff_training as st
from writeOutData import writeOutTrainings
from writeOutReport import writeOutReports
# from writeOutRadReport import writeOutRadReport
from writeOutNonMandReport import writeOutNonMandReport
from organogram import makeOrganogram
from get_files import get_cdr_file, get_she_file, get_totara_file

debug = False
# debug = True
sendEmail = True
# sendEmail = False

# First initialise the staff trainings class
cFile = sys.argv[1]
print("Loading configuration file %s" % cFile)
if cFile.endswith(".py"):
    cFile = cFile[:-3]
configuration = __import__(cFile)
if debug:
    print("Configuration used : ", configuration.config)
department = configuration.config["department"]
deptStaff = st.staffMember(configuration.config, department=department)
if not configuration.config["optionalTrainings"]:
    sendEmail = False

# Get the list of members of the department.
print("Contacting CDR for staff list information")
cdr_file = "out_cdr.xls"
status = get_cdr_file(loc=cdr_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
cdrList = pd.read_excel(cdr_file, engine="xlrd", sheet_name="SearchResults")
deptStaff.addDepartment(cdrList, debug=debug)

os.unlink(cdr_file)  # Clean up

print("Making Department organogram")
if sendEmail:
    leftStaff = makeOrganogram(deptStaff)
else:
    leftStaff = []
# print(deptStaff.eList)
# sys.exit()

# Capture the stdout to send as email. Also see
# https://stackoverflow.com/a/1218951
if sendEmail:
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

print("""
Note : The unique identification used is the STFC email address according to CDR as this
is (supposed to be) available now in CDR, the SHE spreadsheet and the totara spreadsheet.

First printout (CDR update needs) is of staff who have left but are still in various
linemanager chains in CDR.

Unidentified name in SHE spreadsheet used means that this name is a PPD staff member in
the SHE spreadsheet but is not in PPD according to CDR

addTotaraRecords - Unidentified (missing in CDR?): this means that there is a person in
Totara labelled as PPD staff but is not in PPD according to CDR

The list at the end: These names are flagged as having outstanding training in the SHE
spreadsheet but in Totara we find the training to be completed

======================
    """)

today = str(datetime.datetime.now())
print("\nTime of current run : ", today[:19])

# Organogram stuff
print(f"CDR update needs:")
for lStaff in leftStaff:
    print(f"{lStaff[0]:35s} {lStaff[1]:35s}  Manager : {lStaff[2]}")

# Get the SHE statuses
print("\nObtaining and processing SHE records")
she_file = configuration.config["she_filename"]
print("SHE spreadsheet used : ", she_file)
status, she_time = get_she_file(loc=she_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Master Data")
deptStaff.addSHERecords(she_table, configuration.config, fileTime=she_time, debug=debug)

# Get the totara statuses
print("\nObtaining and processing Totara records")
totara_file = "course_completion_report.csv"
status, tot_time = get_totara_file(loc=totara_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
if totara_file.endswith("csv"):
    dtypes = {"The completion date": "str"}
    # parse_dates = ["The completion date"]
    parse_dates = True
    totara_table = pd.read_csv(totara_file, dtype=dtypes, parse_dates=parse_dates)
    # print(totara_table.info())
else:
    totara_table = pd.read_excel(totara_file, engine="openpyxl")
print("Totara table obtained on ", tot_time)
deptStaff.addTotaraRecords(totara_table, configuration.config, fileTime=tot_time, debug=debug)
os.unlink(totara_file)  # Clean up

deptStaff.printTotaraUpates(configuration.config)
print("All Okay")

if sendEmail:
    sys.stdout = old_stdout
    eMailBody = mystdout.getvalue().split("\n")
    if eMailBody[-2] != "All Okay":
        print(eMailBody)
        print(eMailBody[-2])
        print("Something went wrong")
        sys.exit(-3)
    # Send email following https://docs.python.org/3/library/email.examples.html
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content("\n".join(eMailBody[:-2]))
    msg["Subject"] = f"Pulshe report - {today[:10]}"
    msg["From"] = "r.nandakumar@stfc.ac.uk"
    msg["To"] = "raja.nandakumar@stfc.ac.uk"
    # cc = ["joshua.davies@stfc.ac.uk", "andrew.j.smith@stfc.ac.uk", "maurits.van-der-grinten@stfc.ac.uk",
    cc = ["joshua.davies@stfc.ac.uk", "maurits.van-der-grinten@stfc.ac.uk", # Removed Andrew Smith on 13 Aug as per email from Katie Lamb
        "terry.cornford@stfc.ac.uk", "katie.lamb@stfc.ac.uk"]
    answer = input("Send wide? y/n: ")
    if answer == "y":
        msg["CC"] = ",".join(cc)
    try:
        s = smtplib.SMTP("localhost")
        s.send_message(msg)
        s.quit()
    except:
        pass

    for line in eMailBody:
        print(line)

print("All done")
print("\nWriting out html output files")
writeOutTrainings(deptStaff, configuration.config)
writeOutReports(deptStaff, configuration.config, workType="staff")
writeOutReports(deptStaff, configuration.config, workType="student")

if configuration.config["optionalTrainings"]:
    writeOutNonMandReport(deptStaff, configuration.config, "rad_trainings")
    writeOutNonMandReport(deptStaff, configuration.config, "misc_trainings")
    writeOutNonMandReport(deptStaff, configuration.config, "laser_trainings")
    writeOutNonMandReport(deptStaff, configuration.config, "coshh_trainings")
