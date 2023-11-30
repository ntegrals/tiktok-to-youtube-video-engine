# Documentation

# Installation

### JavaScript

1. npm install (Install all packages in the root dir (Without puppeteer))
2. PUPPETEER_PRODUCT=firefox npm i puppeteer (Install puppeteer with Firefox Nightly)

### Python

1. pip3 install -r requirements.txt (Install all requirements)

### Shell

1. Install jq (https://stedolan.github.io/jq/download/)
   (Different path for different os)
2. Install brew
3. Install ffmpeg via brew

### Adding more accounts (The auto upload feature is experimental and only works if your account has the feature enabled)

1. Add the account to the "accounts.json" file
2. Registering the account for the Google API
3. Go to the credentials page (https://console.developers.google.com/apis/credentials)
4. Create a new OAuth2 client id for a "Desktop" application
5. Download the "Client Secret File"
6. Generate the refresh token via the Auth File
7. Rename the Refresh Token (examples in accounts.json)
8. Add the video types with urls

(Source: https://developers.google.com/youtube/v3/quickstart/python)

# Running the program

### Phase 1 - Getting the videos and images

1. Specify the production plan in production.txt (e.g. account_1;harry_malfoy_compilation). The format is derived from the name of the account and the video type name in the accounts.json file.

2. Run /src/main.py (This starts the production process for all videos in the production list)

### Phase 2 - Manual quality control

1. Rename the folder

2. Remove thumbnails that don´t fit the criteria

3. Create a thumbnail with src/metadata/thumbnail.py

4. Create a video path list with src/processing/create_paths.py

5. Delete videos that don´t fit the criteria (As files and in the video path file)

6. Select 3-5 videos for the start (Manual sorting in the video path file)

### Phase 3 - Producing the video to upload

1. Set the production list in src/prod_queue.sh (The target folder as an env var that is passed into src/processing/create_paths_prod.py and src/processing/processing.sh)

2. Run the production when the computer isn´t needed much (e.g. at night)

# FAQ

### How does the selection work?

We specify the accounts and topics in the production file (data/static/production/production.txt), which are then being translated into target urls, based on our account.json video types.
