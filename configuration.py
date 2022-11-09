config = {
    "department": "PPD",  # Capitalisation matters

    # SHE spreadsheet columns we are interested in to select and identify staff
    "she_numColumns" : 30, # Minimum number of visible columns to be a valid row
    "she_forename" : 4,
    "she_lastname" : 3,
    "she_department" : 9,
    "she_type" : 1,
    "she_status" : 0,# Want only "Live" people
    # SHE trainings
    "she_trainings" : [
        ("Induction Refresher test", (22, 13), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=228"), # W N
        ("STFC H&S BiteSize", (27, 19), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=46"), #  AB T
        ("Fire test", (23,14), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=210"), # X O
        ("DSE training test", (24, 15), "https://lmsweb.stfc.ac.uk/moodle/mod/scorm/view.php?id=534"), # Y P
        ("DSE self assessment  test", (25, 16), "https://uk.sheassure.net/stfc/Portal/Create/Portal/3f31848b-ae08-4dd5-970e-8efc4808362c#/information"), # Z Q
        ("Man Hand test", (26, 17, 18), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=168"), # AA R S
        ("Asbestos Essentials", (28, 20), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=158"), # AC  U
        ("Electrical Safety Essentials", (29, 21), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=181"), # AD V
        ("TEST for ALL Mandatory Training", (30,)) # AE
    ],
    "AllTraining" : "TEST for ALL Mandatory Training", # The test for all mandatory training

    # People left but still in SHE spreadsheet
    "she_leftDept" : [
        "Josephine Jones", "Asher Kaboth", # To be removed in 2021
        "Divyatharsshni Sekar", # yini  left in July 2022
    ],

    "she_nameMismatch" : {
        "Atanu Modal": "Atanu Modak",
        "Sandeep Rao Gopalam": "Sandeep Gopalam",
        "Nicholas Jones": "Nicholas Cleverly-Jones",
        "Calum Cox": "Callum Cox",
    },

    # People left but still in Totara spreadsheet
    "totara_leftDept" : [
        "Alfons Weber", # Has left for Germany in 2021
    ],

}
