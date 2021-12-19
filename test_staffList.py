import requests
# --data-raw 'method=advancedSearch&department=PPD&outputForm=EXCEL' --output test5.xls

def get_file(loc="out.xls"):
    url = 'https://cdr.stfc.ac.uk/siteDirectory/adSearch.do'
    data = {'method': 'advancedSearch',
    'department':'PPD',
    'outputForm':'EXCEL'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data = data, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        file = open("out.xls", "wb")
        file.write(response.content)
        file.close()
        return True
    else:
        print("Problem accessing CDR data")
        return False

if __name__ == 'main':
    get_file()