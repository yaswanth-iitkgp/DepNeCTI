#!/bin/bash

# Get the current working directory
current_dir=$(pwd)
# Directory path where you want to check for the 'Saved_Models' folder
directory="$current_dir/DepNeCTI-XLMR"

# Check if the 'Saved_Models' folder doesn't exist
if [ ! -d "$directory/Saved_Models" ]; then
    # Create the 'Saved_Models' folder
    mkdir -p "$directory/Saved_Models"
fi


###############################################################
# Running the base trankit model
echo "make sure you activated DepNeCTI-XLMR environment."
echo "#################################################################"
echo "Currently DepNeCTI-XLMR model in progress..."
echo "#################################################################"
cd DepNeCTI-XLMR
max_attempts = 3  # Set the maximum number of retry attempts
current_attempt = 1

while current_attempt <= max_attempts:
    try:
        # Your Python script here
        python DepNeCTI-XLMR.py
        # If an error occurs, it will raise an exception

        # If the script completes successfully, exit the loop
        break
    except Exception as e:
        print(f"Attempt {current_attempt} failed with the following error: {e}")
        current_attempt += 1

if current_attempt > max_attempts:
    print(f"Script failed after {max_attempts} attempts. Exiting.")
