#!/usr/bin/env bash

# Measure start time
res1=$(date +%s)

# Reads the production plan to the env vars
echo "Selecting target material"
python3 src/maintenance/production_plan.py

### Video Production ###
echo "Removing Temp Files..."
# Delete the old temp files
python3 src/maintenance/remove_temp.py

echo "Retrieving the links from TikTok..."
# Get the video and thumbnail links
node src/selection/link_finder.js

echo "Cleaning the JSON files for downloading..."
python3 src/maintenance/clean_json.py

echo "Downloading Thumbnails..."
# Downloads necessary files
python3 src/downloads/thumbnail_downloader.py

echo "Downloading Videos..."
python3 src/downloads/video_downloader.py

### Manual QC Step
# Store for Quality Control
python3 src/maintenance/store_after_download.py

# Removes video from production list
python3 src/maintenance/remove_prev_production.py


echo "Video Production finished."

# if we are on EC2 - shut down after completion
# sudo shutdown now -h

# Measure end time

res2=$(date +%s)
dt=$(echo "$res2 - $res1" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)

printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds