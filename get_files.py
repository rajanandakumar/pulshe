import os, sys, shutil, requests, datetime


def get_cdr_file(loc="out.xls", department="PPD", debug=False):
    # Contact CDR and obtain the spreadsheet of the people in the department.
    # This is the definitive source of this list and will be kept up to date by the secretaries.
    if debug:
        print("Getting the staff list from CDR as file name ", loc)
    url = "https://cdr.stfc.ac.uk/siteDirectory/adSearch.do"
    data = {"method": "advancedSearch", "department": department, "outputForm": "EXCEL"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        file = open(loc, "wb")
        file.write(response.content)
        file.close()
        return True
    else:
        print(
            "Problem accessing CDR data. Request (https) response code :",
            response.status_code,
        )
        return False


def get_she_file(loc="", department="PPD", debug=False):
    if debug:
        print("Getting the SHE trainings as file name ", loc)
    # Holding code for obtaining the spreadsheet from SHE in "some way". Probably dropped in place by Mauritz?
    # path = "/data/pulshe/she/"
    #
    # If needed, fix the time using the command
    #      touch -c -m --date="2022-10-31 0:00" /data/pulshe/she/SHETrainingRecords-31Oct2022.xlsm
    # Following on from the example at
    #   https://stackoverflow.com/questions/40630695/linux-modify-file-modify-access-change-time
    path = "../she/"
    shutil.copy2(path + loc, ".")
    she_time = datetime.datetime.fromtimestamp(os.path.getmtime(path + loc)).strftime("%Y-%m-%d")
    return (True, she_time)


def get_totara_file(loc="", department="PPD", debug=False):
    if debug:
        print("Getting the Totara trainings as file name ", loc)
    # Holding function for obtaining the spreadsheet from Totara.
    # Apparently using sftp in some manner - to be understood over the meetings with DI.
    # path = "/data/pulshe/she/"
    path = "../she/"
    shutil.copy2(path + loc, ".")
    tot_time = datetime.datetime.fromtimestamp(os.path.getmtime(path + loc)).strftime("%Y-%m-%d")
    return (True, tot_time)
