config = {
    "department": "PPD",  # Capitalisation matters
    # SHE spreadsheet columns we are interested in to select and identify staff
    "she_filename": "SHETrainingRecords-09Mar2023.xlsm",
    "she_numColumns": 110,  # Minimum number of visible columns to be a valid row
    "she_forename": 4,
    "she_lastname": 3,
    "she_department": 9,
    "she_type": 1,
    "she_status": 0,  # Want only "Live" people
    # SHE trainings
    "she_trainings": [
        ("Induction Refresher test", (22, 13), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=228"),  # W N
        ("STFC H&S BiteSize", (27, 19), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=46"),  #  AB T
        ("Fire test", (23, 14), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=210"),  # X O
        ("DSE training test", (24, 15), "https://lmsweb.stfc.ac.uk/moodle/mod/scorm/view.php?id=534"),  # Y P
        ("DSE self assessment  test", (25, 16), "https://app.uk.sheassure.net/ukri/p/STFC_Open_Z7GHXvqMA5/forms/7182"),  # Z Q
        ("Man Hand test", (26, 17, 18), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=168"),  # AA R S
        ("Asbestos Essentials", (28, 20), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=158"),  # AC  U
        ("Electrical Safety Essentials", (29, 21), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=181"),  # AD V
        ("TEST for ALL Mandatory Training", (30,)),  # AE
    ],
    "AllTraining": "TEST for ALL Mandatory Training",  # The test for all mandatory training
    # Non-mandatory radiation trainings as requested by Jens Dopke, Gary Zhang
    "rad_trainings": [
        ("Radioactive Materials (RAM)", 81, ""), # CD
        ("STFC General Radiation Awareness (online)", 84, ""), # CG
        ("Working with ionising radiation (1 day)", 85, ""), # CH
        ("Working with ionising radiation (refresher, online)", 86, ""), # CI
        ("RPS (RAL / DL)", 87, ""), # CJ
    ],
    # Non-mandatory miscellaneous trainings
    "misc_trainings": [
        ("Cryogenics (SHE Code 3 - SC0302)", 32, ""), # AG
        ("Risk Assessment (SHE Code 6 - SC0601)", 45,""), # AT
        ("STFC SHE Training for Non-Technical Managers (SHE Code 10 - SC1004)", 55,""), # BD
        ("PAT Testing (SHE Code 17 - SC1701)", 66,""), # BO

        ("Building Warden (SHE Code 32 - SC3201)", 92,""), # CO
        ("Building Warden (Refresher) (SHE Code 32 - SC3202)", 93,""), # CP

        ("Gas Cylinder Safety Awareness (SHE Code 33 - SC3301)", 98,""), # CU

        ("First Aid at Work (Initial) (SHE Code 36)", 105,""), # DB
        ("First Aid at Work Refresher (Requalification) (SHE Code 36)", 106,""), # DC
        ("Annual Skills/Defib Refresher (SHE Code 36)", 107,""), # DD
    ],
    # Non-mandatory chemical safety training
    "coshh_trainings":[
        ("Basic COSHH Awareness (on-line) (SHE Code 37 - SC3701)", 109,""), # DF
        ("COSHH Assessor (SHE Code 37 - SC3702)", 110,""), # DG
    ],
    # Non-mandatory laser safety training
    "laser_trainings":[
        ("Laser Safety Hazard Awareness (SHE Code 22 - SC2202)", 68,""), # BQ
        ("Laser Responsible / Safety Officer (OLRO/LRO/LSO) (SHE Code 22 - SC2203)", 69,""), # BR
        ("Laser Nominated Person (LNP) Briefing (SHE Code 22)", 70,""), # BS
    ],
    # People left but still in SHE spreadsheet
    "she_leftDept": [
        "Josephine Jones",
        "Asher Kaboth",  # To be removed in 2021
        "Divyatharsshni Sekar",  # yini  left in July 2022
    ],
    "she_nameMismatch": {
        "Atanu Modal": "Atanu Modak",
        "Sandeep Rao Gopalam": "Sandeep Gopalam",
        "Nicholas Jones": "Nicholas Cleverly-Jones",
        "Calum Cox": "Callum Cox",
        "Thomas Longman": "Tom Longman",
    },
    # People left but still in Totara spreadsheet
    "totara_leftDept": [
        "Alfons Weber",  # Has left for Germany in 2021
    ],
}
