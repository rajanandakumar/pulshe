import os, sys, datetime
import pandas as pd
import numpy as np
import staff_training as st
from writeOutData import writeOutTrainings
from writeOutReport import writeOutReports
from organogram import makeOrganogram
from get_files import get_cdr_file, get_she_file, get_totara_file

debug = False
# debug = True

# First initialise the staff trainings class
cFile = sys.argv[1]
print("Loading configuration file %s" % cFile)
if cFile.endswith(".py"):
    cFile = cFile[:-3]
configuration = __import__(cFile)
if debug:
    print("Configuration used : ", configuration.config)
department = configuration.config["department"]
deptStaff = st.staffMember(department)
# deptStaff = st.staffMember("PPD")

# Get the list of members of the department.
print("Contacting CDR for staff list information")
cdr_file = "out_cdr.xls"
status = get_cdr_file(loc=cdr_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
cdrList = pd.read_excel(cdr_file, engine="xlrd", sheet_name="SearchResults")
deptStaff.addDepartment(cdrList, debug=debug)
os.unlink(cdr_file) # Clean up

print("Making Department organogram")
makeOrganogram(deptStaff)
# print(deptStaff.eList)
# sys.exit()

print("\nTime of current run : ", str(datetime.datetime.now())[:19])

# Get the SHE statuses
print("\nObtaining and processing SHE records")
# she_file = "SHETrainingRecords.xlsm"
she_file = "SHETrainingRecords-31May2022.xlsm"
print("SHE spreadsheet used : ", she_file)
status, she_time = get_she_file(loc=she_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
# she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Summary")
she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Master Data")
# she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Sheet1")
deptStaff.addSHERecords(she_table, configuration.config, fileTime=she_time, debug=debug)
os.unlink(she_file) # Clean up

# Get the totara statuses
print("\nObtaining and processing Totara records")
totara_file = "course_completion_report.csv"
status, tot_time = get_totara_file(loc=totara_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
if totara_file.endswith("csv"):
    dtypes = {"The completion date":"str"}
    parse_dates = ["The completion date"]
    totara_table = pd.read_csv(totara_file, dtype=dtypes, parse_dates=parse_dates)
    # print(totara_table.info())
else:
    totara_table = pd.read_excel(totara_file, engine="openpyxl")
print("Totara table obtained on ", tot_time)
deptStaff.addTotaraRecords(totara_table, configuration.config, fileTime=tot_time, debug=debug)
os.unlink(totara_file) # Clean up

print("\nWriting out html output files")
writeOutTrainings(deptStaff, configuration.config)
writeOutReports(deptStaff, configuration.config)
