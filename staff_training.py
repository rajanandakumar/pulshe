import pandas as pd
from dateutil.parser import parse

class staffMember:
    def __init__(self, department="PPD"):
        self.nStaff = 0
        self.department = department
        self.person = {} # The identifying details of the person
        self.trainings_status = {} # The trainings associated to person
        self.trainings_dueDate = {} # The trainings associated to person
        self.eList = []  # List of all email addresses (sanity check for duplication)

        # List of all "names" = Forename Surname (Totara does not return initials?)
        self.nList = [] # This is the list of all the Unique IDs (UID) as defined in addPerson
        self.SHE_spreadsheet_date = ""
        self.Totara_spreadsheet_date = ""

    def addPerson(self, person):
        eMail = person["Email"]
        nName = person["Forename"] + " " + person["Surname"]
        # Specific exception
        if person["Surname"] == "Buttinger":
            nName = "Will Buttinger"
        if person["Surname"] == "Rao Gopalam":
            nName = "Sandeep Gopalam"
        if person["Surname"] == "Richards" and person["Forename"] == "Kate":
            nName = "Katherine (Kate) Richards"
        if person["Surname"] == "Whalen" and person["Forename"] == "Kate":
            nName = "Kathleen (Kate) Whalen"
        #
        if type(eMail) != type(""):
            return -1  # Critical error. Do not add this person.
        eMail = eMail.lower() # It is a string
        person["Email"] = person["Email"].lower()
        if len(eMail) < 5:
            return -2  # Critical error. Do not add this person.
        if eMail in self.eList:
            # Person already added?
            return -3
        self.eList.append(eMail)
        # The Unique Identifier of the person - eMail is not stored in the spreadsheets.
        # UID = eMail
        UID = nName
        # person["federalID"] = "rn37"
        self.person[UID] = person
        self.person[UID]["Location"] = "Unknown"
        self.trainings_status[UID] = {}
        self.trainings_dueDate[UID] = {}
        self.nList.append(nName)
        self.nStaff = self.nStaff + 1
        return 0

    def myPrint(self):
        print("Number of staff : ", self.nStaff)
        for i in range(self.nStaff):
            print(i, self.person[i]["Title"], self.person[i]["Forename"], self.person[i]["Initials"],
                self.person[i]["Surname"], self.person[i]["Email"])

    def addDepartment(self, cdrList, debug=False):
        for index, bx in cdrList.iterrows():
            person = bx.to_dict()
            status = self.addPerson(person)
            if debug:
                if status == -3:
                    continue
                    # print("Duplicate emaild ID - person not added:", person["Email"])
                elif status != 0:
                    print(person["Title"], person["Forename"], person["Surname"],
                        "Was not added because email ID was bad:", person["Email"],)
        # print(self.nList)

    def addSHERecords(self, sheRecords, conf, fileTime, debug=False):
        # print(sheRecords) # Generic summary
        # SHE records are written by hand
        self.SHE_spreadsheet_date = fileTime 
        trs = conf["she_trainings"]
        kount = 0
        for index, sR in sheRecords.iterrows():
            kount = kount + 1
            srv = sR.values
            # for iii in range(len(srv)):
            #     print(iii,srv[iii])
            # if kount >= 5 :
            #     import sys
            #     sys.exit()
            if len(srv) < conf["she_numColumns"] : continue #Record not complete

            # Select only "live" and "staff / fixed term" from the configured department
            if srv[conf["she_department"]] != conf["department"]: continue
            if srv[conf["she_status"]] != "Live": continue
            # if srv[conf["she_type"]] not in {"Staff", "Fixed Term", "Agency"} : continue  # Bug?
            # if srv[conf["she_type"]] not in ["Staff", "Fixed Term", "Agency"] : continue
            if srv[conf["she_type"]].strip().lower() not in ["staff", "fixed term", "agency"] : continue

            nName = srv[conf["she_forename"]] + " " + srv[conf["she_lastname"]] # UID : Same algorithm as in line 14/15, 33/34 above
            # print(nName)
            if nName in conf["she_leftDept"]: # Has left for Germany
                print("Still encountering %s ..." %nName)
                continue
            if nName == "Atanu Modal":
                nName = "Atanu Modak"
                print("Still encountering Atanu Modal ...")
            if nName == "Sandeep Rao Gopalam":
                nName = "Sandeep Gopalam"
            if nName == "Nicholas Jones":
                nName = "Nicholas Cleverly-Jones"
            if nName == "Calum Cox":
                nName = "Callum Cox"
                print("Still encountering Calum Cox ...")
            self.person[nName]["Location"] = "RAL filtered"
            if nName not in self.nList:
                if nName not in self.nList:
                    print("addSHERecords - Unidentified name :", nName)
                    continue

            # Add in the training records
            for tr in trs:
                if tr[0].startswith("TEST for ALL"): # Only in SHE spreadsheet
                    self.trainings_status[nName][tr[0]] = (srv[tr[1][0]], "Not needed", "SHE")
                else:
                    self.updateTraining(nName, tr[0], srv[tr[1][0]], srv[tr[1][1]], "SHE")
                    if tr[0].startswith("Man Hand"):
                        self.updateTraining(nName, tr[0], srv[tr[1][0]], srv[tr[1][2]], "SHE")
        return 0

    def addTotaraRecords(self, totaraRecords, conf, fileTime, debug=False):
        self.Totara_spreadsheet_date = fileTime
        index = 0
        # new_header = totaraRecords.iloc[index]
        # totaraRecords = totaraRecords[index+1:]
        # totaraRecords.columns = new_header
        kount = 0
        for index, tR in totaraRecords.iterrows():
            kount = kount + 1
            trd = tR.to_dict() # This works because apparently Totara records have a decent first row
            # print(trd)

            # Hopefully this takes care of ensuring that the person is in the department
            if trd["Active/Deleted"] == "Deleted" : continue
            if conf["department"] not in trd["User's Fullname"] and \
               conf["department"] != trd["Department"]: continue

            nName = trd["User First Name"] + " " + trd["User Last Name"]
            if nName in conf["totara_leftDept"]: # Has left for Germany
                continue
            if nName == "Kate Richards":
                nName = "Katherine (Kate) Richards"
            if nName == "Sandeep Rao Gopalam":
                nName = "Sandeep Gopalam"
            if nName == "William Buttinger":
                nName = "Will Buttinger"
            if nName == "Kate Whalen":
                nName = "Kathleen (Kate) Whalen"
            if nName == "Nicholas Jones":
                nName = "Nicholas Cleverly-Jones"
            if nName not in self.nList:
                print("addTotaraRecords - Unidentified name :", nName)
                continue

            if self.person[nName]["Location"] == "Unknown":
                ufn = trd["User's Fullname"]
                loc = "Unknown"
                if "(" in ufn:
                    ulo = ufn[ufn.index("(")+1:-1]
                    loc = ulo.split(",")[1]
                self.person[nName]["Location"] = loc

            # Some clean up of the course names
            course = trd['Course Name']
            # if course not in c2:
            #     c2.append(course)
            if course.lower().startswith("sc") or course.startswith("Restored"):
                course = course.split("-")[1].strip()
            if "BiteSize SHE for " in course:
                course = course.split("BiteSize SHE for")[-1].strip()

            okay = False
            if course == "Asbestos Essentials":
                trg = course
                okay = True
            elif course == "Manual Handling":
                trg = "Man Hand test"
                okay = True
            elif course == "STFC Fire Safety Training":
                trg = "Fire test"
                okay = True
            elif course == "RAL SHE Induction (Refresher)":
                trg = "Induction Refresher test"
                okay = True
            elif course == "Display screen Equipment":
                trg = "DSE training test"
                okay = True
            elif course == "Electrical Safety Essentials":
                trg = "Electrical Safety Essentials"
                okay = True
            elif course == "STFC Health and Safety Arrangements BiteSize":
                trg = "STFC H&S BiteSize"
                okay = True
            if okay:
                self.updateTraining(nName, trg, trd['Completion Status'], trd['The completion date'], "Totara")
        return 0

    def updateTraining(self, uid, training, stat, date, info):
        if training not in self.trainings_status[uid]: # new record
            if type(date) == type(1.0) or isinstance(date, type(pd.NaT)) or isinstance(date, type(None)): # Invalid date - enter a simple default
                self.trainings_status[uid][training] = (stat, "0/0/0", info)
            elif type(date) == type("a") and "/" not in date:
                self.trainings_status[uid][training] = (stat, date, info)
            else:
                # print(date, type(date))
                self.trainings_status[uid][training] = (stat, parse(str(date)), info)
            return

        # Is the new date valid?
        try:
            dnew = parse(str(date))
        except:
            return # Nothing to do - new date is crappy

        # Bad old date - but good new date!
        try:
            dold = parse(str(self.trainings_status[uid][training][1]))
        except: #Hmmm - new date is okay (hopefully)
            self.trainings_status[uid][training] = (stat, dnew, info)
            return

        # Good new and old dates - Update only if it is a newer record
        if dnew > dold:
            self.trainings_status[uid][training] = (stat, dnew, info)
        return
