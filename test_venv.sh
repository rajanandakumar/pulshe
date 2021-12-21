#!/bin/bash

# Directory for virtual environment
DIRECTORY="she"
DEPARTMENT="PPD"

# If the venv is not available, create it
if [[ -d "$DIRECTORY" ]]
then
    echo "Virtual environment \"$DIRECTORY\" exists on your filesystem. Activating it."
    source she/bin/activate
else
    echo "Setting up environment. This will take some time."
    python3 -m venv $DIRECTORY
    source $DIRECTORY/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install requests pandas openpyxl xlrd
    echo "Finished setting up environment. Next : SHE processing"
fi

python3 test_staffList.py $DEPARTMENT

deactivate
