
export QC_FOLDER="/Users/julian/Dropbox/coding/yt-uploader/data/quality_control"

# # Video 1
# # Upload date should be checked - Format: YYYY-MM-DDhogwarts_letter_1
# export TARGET_FOLDER="data/persistent/weekly_uploads/hogwarts_letter_1"
# export ACCOUNT_ID="account_1" 
# export VIDEO_TYPE="harry_malfoy_compilation" 
# export GENRE="harrypotter" 
# export PUBLISHING_DATE="2021-01-13"

# sh src/processing/processing.sh && python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER

# # Video 1
# # Upload date should be checked - Format: YYYY-MM-DD
# export TARGET_FOLDER="data/persistent/weekly_uploads/diagon_alley_1"
# export ACCOUNT_ID="account_2" # Needs to be changed for each account
# export VIDEO_TYPE="harry_malfoy_compilation" 
# export GENRE="harrypotter" 
# export PUBLISHING_DATE="2021-02-05"

# sh src/processing/processing.sh && python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER

# Video 1
# Upload date should be checked - Format: YYYY-MM-DD
export TARGET_FOLDER="data/persistent/weekly_uploads/diagon_alley_1"
export ACCOUNT_ID="account_1" # Needs to be changed for each account
export VIDEO_TYPE="harry_malfoy_compilation" 
export GENRE="harrypotter" 
export PUBLISHING_DATE="2021-02-05"

sh src/processing/processing.sh && python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER

# Video 2
# Upload date should be checked - Format: YYYY-MM-DD
export TARGET_FOLDER="data/persistent/weekly_uploads/diagon_alley_2"
export ACCOUNT_ID="account_1" # Needs to be changed for each account
export VIDEO_TYPE="harry_malfoy_compilation" 
export GENRE="harrypotter" 
export PUBLISHING_DATE="2021-02-08"

sh src/processing/processing.sh && python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER

# Video 3
# Upload date should be checked - Format: YYYY-MM-DD
export TARGET_FOLDER="data/persistent/weekly_uploads/diagon_alley_3"
export ACCOUNT_ID="account_1" # Needs to be changed for each account
export VIDEO_TYPE="harry_malfoy_compilation" 
export GENRE="harrypotter" 
export PUBLISHING_DATE="2021-02-11"

sh src/processing/processing.sh && python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER




# # python3 src/automation/metadata.py && mv $TARGET_FOLDER $QC_FOLDER

# # TARGET_FOLDER="data/persistent/weekly_uploads/hogwarts_letter_2" sh src/processing/processing.sh
# # TARGET_FOLDER="data/persistent/weekly_uploads/hogwarts_letter_3" sh src/processing/processing.sh
# # TARGET_FOLDER="data/persistent/weekly_uploads/cutest_doggies_1" sh src/processing/processing.sh


# # # Invoking sleep mode on the mac
# # # (For doing the production at night)
# # pmset sleepnow