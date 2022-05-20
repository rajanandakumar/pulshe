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
        ("Induction Refresher test", (22, 13), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=228"),
        ("STFC H&S BiteSize", (27, 19), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=46"),
        ("Fire test", (23,14), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=210"),
        ("DSE training test", (24, 15), "https://lmsweb.stfc.ac.uk/moodle/mod/scorm/view.php?id=534"),
        ("DSE self assessment  test", (25, 16), "https://uk.sheassure.net/stfc/Portal/Create/Portal/3f31848b-ae08-4dd5-970e-8efc4808362c#/information"),
        ("Man Hand test", (26, 17, 18), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=168"),
        ("Asbestos Essentials", (28, 20), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=158"),
        ("Electrical Safety Essentials", (29, 21), "https://lmsweb.stfc.ac.uk/moodle/course/view.php?id=181"),
        ("TEST for ALL Mandatory Training", (30,))
    ],
    "AllTraining" : "TEST for ALL Mandatory Training", # The test for all mandatory training

    # Totara configuration

}
