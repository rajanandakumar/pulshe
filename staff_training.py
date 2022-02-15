import pandas as pd
class staffMember:
    def __init__(self, department="PPD"):
        self.nStaff = 0
        self.department = department
        self.person = {} # The identifying details of the person
        self.trainings_status = {} # The trainings associated to person
        self.trainings_date = {} # The last completed date of trainings if available
        self.eList = []  # List of all email addresses (sanity check for duplication)

        # List of all "names" = Forename Surname (Totara does not return initials?)
        self.nList = [] # This is the list of all the Unique IDs (UID) as defined in addPerson

    def addPerson(self, person):
        eMail = person["Email"]
        nName = person["Forename"] + " " + person["Surname"]
        if type(eMail) != type(""):
            return -1  # Critical error. Do not add this person.
        if len(eMail) < 5:
            return -2  # Critical error. Do not add this person.
        if eMail in self.eList:
            # Person already added?
            return -3
        else:
            self.eList.append(eMail)
        # The Unique Identifier of the person - eMail is not stored in the spreadsheets.
        # UID = eMail
        UID = nName
        self.person[UID] = person
        self.trainings_status[UID] = {}
        self.trainings_date[UID] = {}
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

    def addSHERecords(self, sheRecords, conf, debug=False):
        # print(sheRecords) # Generic summary
        # SHE records are written by hand
        trs = conf["she_trainings"]
        for index, sR in sheRecords.iterrows():
            srv = sR.values
            if len(srv) < conf["she_numColumns"] : continue #Record not complete

            # Select only "live" and "staff / fixed term" from the configured department
            if srv[conf["she_department"]] != conf["department"]: continue
            if srv[conf["she_status"]] != "Live": continue
            if srv[conf["she_type"]] not in {"Staff", "Fixed Term"} : continue

            nName = srv[conf["she_forename"]] + " " + srv[conf["she_lastname"]] # UID : Same algorithm as in line 14/15, 33/34 above
            if nName not in self.nList:
                if debug:
                    print("addSHERecords - Unidentified name :", nName)
                continue

            # Add in the training records
            for tr in trs:
                self.trainings_status[nName][tr[0]] = [srv[tr[1][0]], "SHE"]
                if tr[0] != "Fire test" and not tr[0].startswith("TEST for ALL"):
                    if len(tr[1]) == 2:
                        self.trainings_date[nName][tr[0]] = [srv[tr[1][1]], "SHE"]
                    else:
                        print("Configuration Error : trainings list incorrect")

            # if self.trainings_she[nName][conf["AllTraining"]] != "OK":
            #     print(nName)
            #     for tr, value in self.trainings_she[nName].items():
            #         if tr.startswith("TEST for ALL Mandatory"): continue
            #         if value != "In date":
            #             print("    ", tr, value)
        return 0

    def addTotaraRecords(self, totaraRecords, conf, debug=False):
        # courses = []
        # c2 = []
        kount = 0
        for index, tR in totaraRecords.iterrows():
            kount = kount + 1
            trd = tR.to_dict() # This works because apparently Totara records have a decent first row
            # print(index, trd)

            if conf["department"] not in trd["User's Fullname"]: continue

            nName = trd["User First Name"] + " " + trd["User Last Name"]
            if nName not in self.nList:
                if debug:
                    print("addSHERecords - Unidentified name :", nName)
                continue

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
            # print("Name : %s, Course : %s, Status : %s" %(nName, course, trd['Completion Status']))
            if okay: self.trainings_status[nName][trg] = [trd['Completion Status'], "Totara"]
            # if course not in courses:
            #     courses.append(course)
        # for course in courses:
        #     print(course)
        # for course in c2:
        #     print(course)
        return 0
