config = {
    "department": "PPD",  # Capitalisation matters
    "optionalTrainings": True,
    # SHE spreadsheet columns we are interested in to select and identify staff
    "she_filename": "SHETrainingRecords-31Aug2024.xlsm",
    "she_numColumns": 110,  # Minimum number of visible columns to be a valid row
    "she_forename": 4,
    "she_lastname": 3,
    "she_department": 9,
    "she_type": 1,
    "she_email": 12,
    "she_status": 0,  # Want only "Live" people
    # SHE trainings
    "she_trainings": [
        ("Induction Refresher test", (22, 13), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=228"),  # W N
        ("STFC H&S BiteSize", (27, 19), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=46"),  #  AB T
        # ("SC0501 - BiteSize SHE for Incident reporting and investigation code", "","https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=53"), # Totara only
        # ("SC0601 - BiteSize SHE for Risk management code", (45),"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=54"), # AT
        ("Fire test", (23, 14), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=210"),  # X O
        ("DSE training test", (24, 15), "https://lmsweb.stfc.ac.uk/moodle/mod/scorm/view.php?id=534"),  # Y P
        # ("DSE self assessment  test", (25, 16), "https://app.uk.sheassure.net/ukri/p/STFC_Open_Z7GHXvqMA5/forms/7182"),  # Z Q
        ("DSE self assessment  test", (25, 16), "https://lmsweb.stfc.ac.uk/moodle/course/index.php?categoryid=107"),  # Z Q
        ("Man Hand test", (26, 17, 18), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=168"),  # AA R S
        ("Asbestos Essentials", (28, 20), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=158"),  # AC  U
        ("Electrical Safety Essentials", (29, 21), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=181"),  # AD V
        ("TEST for ALL Mandatory Training", (30,)),  # AE
    ],
    "AllTraining": "TEST for ALL Mandatory Training",  # The test for all mandatory training
    # Non-mandatory radiation trainings as requested by Jens Dopke, Gary Zhang
    "rad_trainings": [
        ("Radioactive Materials (RAM)", 82, ""), # CE
        ("STFC General Radiation Awareness (online)", 85, ""), # CH
        ("Working with ionising radiation (1 day)", 86, ""), # CI
        ("Working with ionising radiation (refresher, online)", 87, ""), # CJ
        ("RPS (RAL / DL)", 88, ""), # CK
    ],
    # Non-mandatory miscellaneous trainings
    "misc_trainings": [
        ("Cryogenics (SHE Code 3 - SC0302)", 32, ""), # AG
        ("SC0501 - BiteSize SHE for Incident reporting and investigation code", -1,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=53"), # Totara only
        ("SC0601 - BiteSize SHE for Risk management code", 45,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=54"), # AT
        ("STFC SHE Training for Non-Technical Managers (SHE Code 10 - SC1004)", 55,""), # BD
        ("SC1701 - BiteSize SHE for Inspection and testing of electrical equipment code", 67,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=178"), # BP
        ("SC3201ral - RAL Fire Warden (Refresher)", 93,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=227"), # CP
        ("Building Warden (Refresher) (SHE Code 32 - SC3202)", 94,""), # CQ
        ("SC3301 - BiteSize SHE for Pressure and Vacuum code", 99,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=161"), # CV # Gas cylinder safety awareness
        ("First Aid at Work (Initial) (SHE Code 36)", 106,"https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=179"), # DC
        ("First Aid at Work Refresher (Requalification) (SHE Code 36)", 107,""), # DD
        ("Annual Skills/Defib Refresher (SHE Code 36)", 108,""), # DE
    ],
    # Non-mandatory chemical safety training
    "coshh_trainings":[
        ("Basic COSHH Awareness (on-line) (SHE Code 37 - SC3701)", 110,""), # DG
        ("COSHH Assessor (SHE Code 37 - SC3702)", 111,""), # DH
    ],
    # Non-mandatory laser safety training
    "laser_trainings":[
        ("Laser Safety Hazard Awareness (SHE Code 22 - SC2202)", 69,""), # BR
        ("SC2201 - BiteSize SHE for Laser Safety code", -1, "https://lmsweb.stfc.ac.uk/moodle/enrol/index.php?id=62"), # Totara only
        ("Laser Responsible / Safety Officer (OLRO/LRO/LSO) (SHE Code 22 - SC2203)", 70,""), # BS
        ("Laser Nominated Person (LNP) Briefing (SHE Code 22)", 71,""), # BT
    ],
    # Trainings that do not expire
    "always_valid_trainings":[
        "STFC H&S BiteSize", "Asbestos Essentials", "Electrical Safety Essentials",
    ],
    # People left but still in SHE spreadsheet
    "she_leftDept": [
    ],
    # People left but still in Totara spreadsheet
    "totara_leftDept": [
    ],
}
