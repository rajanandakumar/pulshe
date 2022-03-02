config = {
    "department": "PPD",  # Capitalisation matters

    # SHE spreadsheet columns we are interested in to select and identify staff
    "she_numColumns" : 27, # Minimum number of visible columns to be a valid row
    "she_forename" : 4,
    "she_lastname" : 3,
    "she_department" : 9,
    "she_type" : 1,
    "she_status" : 0,# Want only "Live" people
    # SHE trainings
    "she_trainings" : [
        ("Induction Refresher test", (21, 12)), # For the master data sheet
        ("Fire test", (22,13)),
        ("DSE training test", (23, 14)),
        ("DSE self assessment  test", (24, 15)),
        ("Man Hand test", (25, 16)),
        ("Asbestos Essentials", (27, 19)),
        ("Electrical Safety Essentials", (28, 20)),
        ("TEST for ALL Mandatory Training", (29,))],
    "AllTraining" : "TEST for ALL Mandatory Training", # The test for all mandatory training

    # Totara configuration

}
