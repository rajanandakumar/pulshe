import sys
import pandas as pd
import staff_training as st
from get_files import get_cdr_file

debug = False
# debug = True

# First get the list of members of the department.
cdr_file = "out_cdr.xls"
department = sys.argv[1]
status = get_cdr_file(loc=cdr_file, department=department)
if not status:
    print("Could not access CDR. Cannot create list of staff in ", department)
    print("Exiting")
    sys.exit(-2)

cdrList = pd.read_excel(cdr_file, engine='xlrd', sheet_name="SearchResults")
deptStaff = st.staffMember()
deptStaff.addDepartment(cdrList, debug=debug)

# excel_file = "course_completion_report-6_3Sep21.xlsx"
# # help(pd.read_excel)
# aa = pd.read_excel(excel_file, engine='openpyxl')
# # print(type(aa))
# # print(dir(aa))
# print(aa.head)
# print(aa["User Last Name"])
# # for index,a in aa.iterrows():
# #     print(a["User Last Name"], a["User First Name"])
# # print(aa.shape)
# print(aa)

