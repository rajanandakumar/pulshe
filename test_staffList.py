import os, sys, datetime
import pandas as pd
import numpy as np
import staff_training as st
from writeOutData import writeOutTrainings
from get_files import get_cdr_file, get_she_file, get_totara_file

debug = False
# debug = True

# First initialise the staff trainings class
cFile = sys.argv[1]
if cFile.endswith(".py"):
    cFile = cFile[:-3]
configuration = __import__(cFile)
if debug:
    print("Configuration used : ", configuration.config)
department = configuration.config["department"]
deptStaff = st.staffMember(department)
# deptStaff = st.staffMember("PPD")

# Get the list of members of the department.
cdr_file = "out_cdr.xls"
status = get_cdr_file(loc=cdr_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
cdrList = pd.read_excel(cdr_file, engine="xlrd", sheet_name="SearchResults")
deptStaff.addDepartment(cdrList, debug=debug)
os.unlink(cdr_file) # Clean up

# Get the SHE statuses
she_file = "SHETrainingRecords.xlsm"
status, she_time = get_she_file(loc=she_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
# she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Summary")
she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Master Data")
deptStaff.addSHERecords(she_table, configuration.config, fileTime=she_time, debug=debug)
os.unlink(she_file) # Clean up

# Get the totara statuses
# totara_file = "course_completion_report-6_3Sep21.xlsx"
# totara_file = "course_completion_report_26Feb22.xlsx"
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
deptStaff.addTotaraRecords(totara_table, configuration.config, fileTime=tot_time, debug=debug)
os.unlink(totara_file) # Clean up

writeOutTrainings(deptStaff, configuration.config)