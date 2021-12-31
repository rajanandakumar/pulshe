import pandas as pd

class staffMember:
    def __init__(self):
        self.nStaff = 0
        self.person = {}
        self.trainings = {}
        self.eList = []

    def addPerson(self, person):
        eMail = person["Email"]
        if type(eMail) != type("") : return -1 # Critical error. Do not add this person.
        if len(eMail) < 5 : return -2 # Critical error. Do not add this person.
        if eMail in self.eList:
            # print("Person already added? : ", person["Title"], person["Forename"], person["Initials"],
            #      person["Surname"], person["Email"])
            return -3
        else:
            self.eList.append(eMail)
        # self.person.insert(self.nStaff, person)
        self.person[eMail] = person
        self.trainings[eMail] = {}
        self.nStaff = self.nStaff + 1
        return 0

    def myPrint(self):
        print("Number of staff : ", self.nStaff)
        for i in range(self.nStaff):
            print(i, self.person[i]["Title"], self.person[i]["Forename"], self.person[i]["Initials"],
                 self.person[i]["Surname"], self.person[i]["Email"])

    def addDepartment(self, cdrList, debug=False):
        for index,bx in cdrList.iterrows():
            person = bx.to_dict()
            status = self.addPerson(person)
            if debug:
                if status == -3:
                    continue
                    # print("Duplicate emaild ID - person not added:", person["Email"])
                elif status != 0:
                    print(person["Title"], person["Forename"], person["Surname"], "Was not added because email ID was bad:", person["Email"])
