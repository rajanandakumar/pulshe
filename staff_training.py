import pandas as pd
from dateutil.parser import parse
import math

class staffMember:
    def __init__(self, conf, department="PPD"):
        self.nStaff = 0
        self.department = department
        self.person = {}  # The identifying details of the person
        self.trainings_status = {}  # The trainings associated to person
        self.trainings_dueDate = {}  # The trainings associated to person
        self.eList = []  # List of all email addresses (sanity check for duplication)

        # Non-mandatory trainings
        self.rad_training_status = {} # Radiation
        self.laser_training_status = {} # Lasers
        self.coshh_training_status = {} # Chemicals
        self.misc_training_status = {} # Other "stuff"

        # List of all "names" = Forename Surname (Totara does not return initials?)
        self.nList = []  # This is the list of all the Unique IDs (UID) as defined in addPerson
        self.SHE_spreadsheet_date = ""
        self.Totara_spreadsheet_date = ""

        # Just the courses in a listing
        self.optional_courses = []
        self.misc_courses = []
        self.rad_courses = []
        self.coshh_courses = []
        self.laser_courses = []
        for item in conf["misc_trainings"]:
            self.optional_courses.append(item[0])
            self.misc_courses.append(item[0])
        for item in conf["rad_trainings"]:
            self.optional_courses.append(item[0])
            self.rad_courses.append(item[0])
        for item in conf["coshh_trainings"]:
            self.optional_courses.append(item[0])
            self.coshh_courses.append(item[0])
        for item in conf["laser_trainings"]:
            self.optional_courses.append(item[0])
            self.laser_courses.append(item[0])


    def addPerson(self, person):
        eMail = person["Email"]
        # nName = person["Forename"] + " " + person["Surname"]
        # # Specific exception
        # if person["Surname"] == "Buttinger":
        #     nName = "Will Buttinger"
        # if person["Surname"] == "Rao Gopalam":
        #     nName = "Sandeep Gopalam"
        # if person["Surname"] == "Richards" and person["Forename"] == "Kate":
        #     nName = "Katherine (Kate) Richards"
        # if person["Surname"] == "Whalen" and person["Forename"] == "Kate":
        #     nName = "Kathleen (Kate) Whalen"
        #
        if type(eMail) != type(""):
            return -1  # Critical error. Do not add this person.
        eMail = eMail.lower()  # It is a string
        nName = eMail
        person["Email"] = person["Email"].lower()
        if len(eMail) < 5:
            return -2  # Critical error. Do not add this person.
        if eMail in self.eList:
            # Person already added?
            return -3
        self.eList.append(eMail)
        # The Unique Identifier of the person - eMail is not stored in the spreadsheets.
        UID = eMail
        # UID = nName
        # person["federalID"] = "rn37"
        self.person[UID] = person
        self.person[UID]["Location"] = "Unknown"
        self.person[UID]["work_type"] = "Unknown"
        self.trainings_status[UID] = {}
        self.trainings_dueDate[UID] = {}
        self.rad_training_status[UID] = {}
        self.laser_training_status[UID] = {} # Lasers
        self.coshh_training_status[UID] = {} # Chemicals
        self.misc_training_status[UID] = {} # Other "stuff"
        self.nList.append(nName)
        self.nStaff = self.nStaff + 1
        return 0

    def myPrint(self):
        print("Number of staff : ", self.nStaff)
        for i in range(self.nStaff):
            print(
                i,
                self.person[i]["Title"],
                self.person[i]["Forename"],
                self.person[i]["Initials"],
                self.person[i]["Surname"],
                self.person[i]["Email"],
            )

    def getRDate(self, rTr="", srv=""):
        rDate = ""
        if type(srv) == type(0.0) and math.isnan(srv):
            return rDate
        if rTr >= 0 and srv != None and srv != "NR":
            rDate = parse(str(srv))
        return rDate


    def addDepartment(self, cdrList, debug=False):
        for index, bx in cdrList.iterrows():
            person = bx.to_dict()
            status = self.addPerson(person)
            if debug:
                if status == -3:
                    continue
                    # print("Duplicate emaild ID - person not added:", person["Email"])
                elif status != 0:
                    print(
                        person["Title"],
                        person["Forename"],
                        person["Surname"],
                        "Was not added because email ID was bad:",
                        person["Email"],
                    )
        # print(self.nList)

    def addSHERecords(self, sheRecords, conf, fileTime, debug=False):
        # print(sheRecords) # Generic summary
        # SHE records are written by hand
        self.SHE_spreadsheet_date = fileTime
        trs = conf["she_trainings"]
        kount = 0
        messages_leftPPD = []
        for index, sR in sheRecords.iterrows():
            kount = kount + 1
            srv = sR.values
            if len(srv) < conf["she_numColumns"]:
                continue  # Record not complete

            # Select only "live" and "staff / fixed term" from the configured department
            if srv[conf["she_department"]] != conf["department"]:
                continue
            if srv[conf["she_status"]] != "Live":
                continue

            # UID : Same algorithm as in line 14/15, 33/34 above
            # nName = srv[conf["she_forename"]].strip() + " " + srv[conf["she_lastname"]].strip()
            if isinstance(srv[conf["she_email"]], type("")):
                nName = srv[conf["she_email"]].strip().lower()
            else:
                # print("Ignoring person with no email ID: ",srv[conf["she_forename"]].strip() + " " + srv[conf["she_lastname"]].strip())
                continue

            # if srv[conf["she_type"]] not in {"Staff", "Fixed Term", "Agency"} : continue  # Bug?
            # if srv[conf["she_type"]] not in ["Staff", "Fixed Term", "Agency"] : continue
            # if srv[conf["she_type"]].strip().lower() not in [
            #     "staff",
            #     "fixed term",
            #     "agency",
            # ]:
            #     print("email:", srv[conf["she_email"]], " type:", srv[conf["she_type"]].strip())
            #     continue

            # print(conf["she_email"], srv[conf["she_email"]])
            if isinstance(srv[conf["she_email"]], type("")):
                nName = srv[conf["she_email"]].strip().lower()
            else:
                print("Ignoring person with no email ID: ",srv[conf["she_forename"]].strip() + " " + srv[conf["she_lastname"]].strip())
                continue
            if nName in conf["she_leftDept"]:
                print(f"Still encountering {nName} ... (left?)")
                continue
            if nName not in self.nList:
                messages_leftPPD.append(f"addSHERecords - Unidentified name (left?) :{nName}")
                continue
            self.person[nName]["Location"] = "RAL filtered"
            self.person[nName]["work_type"] = srv[conf["she_type"]].strip().lower()

            # Add in the training records
            for tr in trs:
                if tr[0].startswith("TEST for ALL"):  # Only in SHE spreadsheet
                    self.trainings_status[nName][tr[0]] = (
                        srv[tr[1][0]],
                        "Not needed",
                        "SHE",
                    )
                else:
                    if isinstance(tr[1], type(())):
                        if len(tr[1]) == 1: # Is this mandatory?
                            self.updateTraining(nName, tr[0], srv[tr[1][0]], "0/0/0", "SHE")
                        else: # Standard mandatory training
                            self.updateTraining(nName, tr[0], srv[tr[1][0]], srv[tr[1][1]], "SHE")
                            if tr[0].startswith("Man Hand"):
                                self.updateTraining(nName, tr[0], srv[tr[1][0]], srv[tr[1][2]], "SHE")
                    else: # Information only in Totara
                        self.updateTraining(nName, tr[0], "0/0/0", "", "SHE")

            # Do only if requested in the configuration
            if conf["optionalTrainings"]:
                for rTr in conf["rad_trainings"]:
                    rDate = self.getRDate(rTr[1], srv[rTr[1]])
                    self.rad_training_status[nName][rTr[0]] = rDate
                for rTr in conf["coshh_trainings"]:
                    rDate = self.getRDate(rTr[1], srv[rTr[1]])
                    self.coshh_training_status[nName][rTr[0]] = rDate
                for rTr in conf["laser_trainings"]:
                    rDate = self.getRDate(rTr[1], srv[rTr[1]])
                    self.laser_training_status[nName][rTr[0]] = rDate
                for rTr in conf["misc_trainings"]:
                    rDate = self.getRDate(rTr[1], srv[rTr[1]])
                    self.misc_training_status[nName][rTr[0]] = rDate
        uniq_leftPPD = set(messages_leftPPD)
        leftPPD = list(uniq_leftPPD)
        for mess in leftPPD:
            print(mess)
        return 0

    def addTotaraRecords(self, totaraRecords, conf, fileTime, debug=False):
        self.Totara_spreadsheet_date = fileTime
        index = 0
        # new_header = totaraRecords.iloc[index]
        # totaraRecords = totaraRecords[index+1:]
        # totaraRecords.columns = new_header
        kount = 0
        messages_missCDR = []

        for index, tR in totaraRecords.iterrows():
            kount = kount + 1
            trd = tR.to_dict()  # This works because apparently Totara records have a decent first row
            # print(trd)

            # Hopefully this takes care of ensuring that the person is in the department
            if trd["Active/Deleted"] == "Deleted":
                continue
            if type(trd["Department"]) != type(" "): # Department is not filled for this user
                # print(trd["User's Fullname"], trd["Department"])
                continue
            if conf["department"] not in trd["User's Fullname"] and conf["department"] != trd["Department"]:
                continue

            nName = trd["Username"].strip().lower()
            # nName = trd["User First Name"] + " " + trd["User Last Name"]
            if nName in conf["totara_leftDept"]:
                continue
            if nName not in self.nList:
                messages_missCDR.append(f"addTotaraRecords - Unidentified (missing in CDR?) :{nName}")
                continue

            if self.person[nName]["Location"] == "Unknown":
                ufn = trd["User's Fullname"]
                loc = "Unknown"
                if "(" in ufn:
                    ulo = ufn[ufn.index("(") + 1 : -1]
                    loc = ulo.split(",")[1]
                self.person[nName]["Location"] = loc

            # Some clean up of the course names
            course = trd["Course Name"]
            # print(course)
            if course.lower().startswith("sc") or course.startswith("Restored"):
                if "-" in course:
                    course = course.split("-")[1].strip()
                else:
                    course = course.split(" ", 1)[1].strip()
            if "BiteSize SHE for " in course:
                course = course.split("BiteSize SHE for")[-1].strip()

            if course == "Asbestos Essentials":
                trg = course
            elif course == "Manual Handling":
                trg = "Man Hand test"
            elif course == "STFC Fire Safety Training":
                trg = "Fire test"
            elif course == "RAL SHE Induction (Refresher)":
                trg = "Induction Refresher test"
            elif course == "Display screen Equipment":
                trg = "DSE training test"
            elif course == "Electrical Safety Essentials":
                trg = "Electrical Safety Essentials"
            elif course == "STFC Health and Safety Arrangements BiteSize":
                trg = "STFC H&S BiteSize"
            elif course.startswith("Workstation Risk Assessment"):
                trg = "DSE self assessment test"
            else: # Course name is same as in Totara systems
                trg = trd["Course Name"]
            self.updateTraining(nName, trg, trd["Completion Status"], trd["The completion date"], "Totara")

            course = trd["Course Name"]
            if conf["optionalTrainings"] and course in self.optional_courses:
                self.updateTraining_misc(conf, nName, course, trd["Completion Status"], trd["The completion date"], "Totara")
        uniq_missCDR = set(messages_missCDR)
        missCDR = list(uniq_missCDR)
        for mess in missCDR:
            print(mess)
        return 0

    def printTotaraUpates(self, conf, debug=False):
        for uid in self.nList:
            if self.person[uid]["Location"] != "RAL filtered":
                continue
            for tr in conf["she_trainings"]:
                training = tr[0]
                if training not in self.trainings_status[uid].keys():
                    continue
                if training.startswith("TEST for ALL"):
                    continue
                if self.trainings_status[uid][training][2] == "Totara":
                    print(f"{uid:20s} {training:25s} {str(self.trainings_status[uid][training][1])[:10]}")

    def updateTraining_misc(self, conf, uid, training, stat, date, info):
        if stat == "Not yet started":
            return # Do not update the information from the SHE table
        dnew = parse(str(date))
        if training in self.misc_courses:
            self.misc_training_status[uid][training] = (stat, dnew, info)
        elif training in self.laser_courses:
            self.laser_training_status[uid][training] = (stat, dnew, info)
        elif training in self.rad_courses:
            self.rad_training_status[uid][training] = (stat, dnew, info)
        elif training in self.coshh_courses:
            self.coshh_training_status[uid][training] = (stat, dnew, info)
        else:
            print(f"Unknown source of training {training} : No update")
        return


    def updateTraining(self, uid, training, stat, date, info):
        if stat == "Not yet started":
            return # Do not update the information from the SHE table

        if training not in self.trainings_status[uid]:  # new record
            if (
                type(date) == type(1.0) or isinstance(date, type(pd.NaT)) or isinstance(date, type(None))
            ):  # Invalid date - enter a simple default
                self.trainings_status[uid][training] = (stat, "0/0/0", info)
            # elif type(date) == type("a") and "/" not in date:
            #     print("Parsing .....", parse(str(date)))
            #     self.trainings_status[uid][training] = (stat, date, info)
            else:
                self.trainings_status[uid][training] = (
                    stat,
                    parse(str(date)),
                    info,
                )
            return

        # Is the new date valid?
        try:
            dnew = parse(str(date))
        except:
            return  # Nothing to do - new date is crappy

        # Bad old date - but good new date!
        try:
            dold = parse(str(self.trainings_status[uid][training][1]))
        except:  # Hmmm - new date is okay (hopefully)
            self.trainings_status[uid][training] = (stat, dnew, info)
            return

        # Good new and old dates - Update only if it is a newer record
        if dnew > dold:
            self.trainings_status[uid][training] = (stat, dnew, info)
        return
