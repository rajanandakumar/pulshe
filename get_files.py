import requests

def get_cdr_file(loc="out.xls", department="PPD"):
    # Contact CDR and obtain the spreadsheet of the people in the department.
    # This is the definitive source of this list and will be kept up to date by the secretaries.
    url = 'https://cdr.stfc.ac.uk/siteDirectory/adSearch.do'
    data = {'method': 'advancedSearch', 'department':department, 'outputForm':'EXCEL'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data = data, headers=headers)
    if response.status_code == 200:
        file = open(loc, "wb")
        file.write(response.content)
        file.close()
        return True
    else:
        print("Problem accessing CDR data. Request (https) response code :", response.status_code)
        return False


def get_she_file(loc="", department="PPD"):
    # Holding code for obtaining the spreadsheet from SHE in "some way". Probably dropped in place by Mauritz?
    return True

def get_totara_file(loc="", department="PPD"):
    # Holding function for obtaining the spreadsheet from Totara.
    # Apparently using sftp in some manner - to be understood over the meetings with DI.
    return True
