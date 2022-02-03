import os, sys
import pandas as pd
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
status = get_she_file(loc=she_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
she_table = pd.read_excel(she_file, engine="openpyxl", sheet_name="Summary")
deptStaff.addSHERecords(she_table, configuration.config, debug=debug)
os.unlink(she_file) # Clean up

# Get the totara statuses
totara_file = "course_completion_report-6_3Sep21.xlsx"
status = get_totara_file(loc=totara_file, department=department, debug=debug)
if not status:
    print("Exiting")
    sys.exit(-2)
totara_table = pd.read_excel(totara_file, engine="openpyxl")
deptStaff.addTotaraRecords(totara_table, configuration.config, debug=debug)
os.unlink(totara_file) # Clean up

writeOutTrainings(deptStaff)