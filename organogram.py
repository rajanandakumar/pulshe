import ldap3, json

def makeOrganogram(staff):
    connection = make_connection()
    organogram = {}
    for uid in staff.nList:
        employees = query_cdr(connection, staff.person[uid]["Email"], "eMail")
        emList = []
        for employee in employees:
            ee = employee.decode()
            fID = ee.split(",")[0][3:]
            eem = query_cdr(connection, fID, "federalID")
            if len(eem) == 1: # Do they really exist in CDR?
                eMail = eem[0].decode()
                if eMail in staff.eList:
                    emList.append(eMail)
        if emList: organogram[staff.person[uid]["Email"]] = emList
    organogram["debbie.loader@stfc.ac.uk"] = staff.eList
    with open('ppd_organogram.json', 'w') as file:
        file.write(json.dumps(organogram))

def make_connection():
    server = ldap3.Server("ldaps://fed.cclrc.ac.uk:3269")
    connection = ldap3.Connection(server, client_strategy=ldap3.SAFE_SYNC, auto_bind=True)
    return connection

def query_cdr(conn, tag, type):
    if type == "eMail":
        filter = "(userPrincipalName=" + tag + ")"
        attribute = "directreports"
    else:
        filter = "(sAMAccountName=" + tag + ")"
        attribute = "userPrincipalName"
    status, result, response, _ = conn.search(
        "dc=FED,dc=CCLRC,dc=AC,dc=UK", filter, attributes=attribute
    )
    # For some reason the response is of class "bytes"
    if status:
        if attribute in response[0]["raw_attributes"]:
            feature = response[0]["raw_attributes"][attribute]
            return feature
    return []
