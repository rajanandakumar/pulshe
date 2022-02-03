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
        ("SHE Induction / Refresher", 12),
        ("Display Screen Equipment", 13),
        ("DSE Workstation Self Assessment (office PC)", 14),
        ("SMH - HandleRite", 15),
        ("Safe Manual Handling", 16),
        ("Asbestos Essentials", 17),
        ("Electrical Safety Essentials", 18),
        ("Induction Refresher test", 19),
        ("Fire test", 20),
        ("DSE training test", 21),
        ("DSE self assessment  test", 22),
        ("Man Hand test", 23),
        ("Asbestos Essentials", 24),
        ("Electrical Safety Essentials", 25),
        ("TEST for ALL Mandatory Training", 26)],
    "AllTraining" : "TEST for ALL Mandatory Training", # The test for all mandatory training

    # Totara configuration

}
