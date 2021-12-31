import sys
import pandas as pd
import staff_training as st
from get_files import get_cdr_file, get_she_file, get_totara_file

debug = False
# debug = True

# First get the list of members of the department.
cdr_file = "out_cdr.xls"
department = sys.argv[1]
status = get_cdr_file(loc=cdr_file, department=department)
if not status:
    print("Exiting")
    sys.exit(-2)
cdrList = pd.read_excel(cdr_file, engine='xlrd', sheet_name="SearchResults")
deptStaff = st.staffMember()
deptStaff.addDepartment(cdrList, debug=debug)

# Get the SHE statuses
she_file = "course_completion_report-6_3Sep21.xlsx"
status = get_she_file(loc=she_file, department=department)
if not status:
    print("Exiting")
    sys.exit(-2)
# she_table = pd.read_excel(she_file, engine='openpyxl')

# Get the totara statuses
totara_file = "course_completion_report-6_3Sep21.xlsx"
status = get_totara_file(loc=totara_file, department=department)
if not status:
    print("Exiting")
    sys.exit(-2)
# totara_table = pd.read_excel(totara_file, engine='openpyxl')
