# Processing in one specific folder

# TARGET_FOLDER is passed in as an env var

# Measure start time
res1=$(date +%s)

# check the video details
TARGET_FPS="30"
TARGET_RES="608x1080"

# count the lines of the file (video count)
# VIDEO_COUNT="$(grep -c . ${TARGET_FOLDER}/video_paths.txt)"
# echo $VIDEO_COUNT

FILES=$TARGET_FOLDER/videos/raw_videos/*

# for n in $(seq 1 $VIDEO_COUNT);
for f in $FILES;

    do 
    VIDEO_PATH=$f
    NEW_VIDEO_PATH=${VIDEO_PATH/"raw_videos"/"raw_videos_2"}

    RESOLUTION="$(ffprobe -v error -select_streams v:0 -show_entries stream=height,width -of csv=s=x:p=0 $VIDEO_PATH)"
    echo $RESOLUTION

    FRAME_RATE="$(ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 $VIDEO_PATH)"
    echo $FRAME_RATE

    IFS='/' read -r -a FRAME_RATE_LIST <<< "$FRAME_RATE"
    REAL_FRAME_RATE=$(expr ${FRAME_RATE_LIST[0]} / ${FRAME_RATE_LIST[1]})

    # echo "Checking Video [$n/$VIDEO_COUNT]";

    if [ "$REAL_FRAME_RATE" != "$TARGET_FPS" ] || [ "$RESOLUTION" != "$TARGET_RES" ]; then

        ffmpeg -y -i $VIDEO_PATH -vf scale=$TARGET_RES,setsar=1,fps=$TARGET_FPS $NEW_VIDEO_PATH

    else
        #copy file to next folder if it doesn´t already exist
        cp -n $VIDEO_PATH $NEW_VIDEO_PATH

    fi

done

# Concat video files

# Important note:
# FFMPEG concat interprets the file paths as relative to the location of the text file
# https://superuser.com/questions/718027/ffmpeg-concat-doesnt-work-with-absolute-path
# To fix this we just need to fix the paths in the second file (Make them relative to the video_paths.txt file)

ffmpeg -y -f concat -safe 0 -i ${TARGET_FOLDER}/video_paths.txt -c copy "${TARGET_FOLDER}/videos/concat/concat.mp4"

# Background file needs an even resolution (1980x1280)
ffmpeg -y -loop 1 -i "data/static/images/video_background.png" -i "${TARGET_FOLDER}/videos/concat/concat.mp4" -filter_complex \
"[0:v][1:v]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p[v]" \
-map "[v]" -map 1:a -c:a copy -movflags +faststart "${TARGET_FOLDER}/videos/upload/upload.mp4" #upload_${res1}.mp4"
 
## Motion Graphics

# Add the subscribe button
# Very slow currently
# To split and concat might work way better

ffmpeg -y -i $TARGET_FOLDER/videos/upload/upload.mp4 -i data/static/videos/subscribe.mov  -filter_complex \
        "[1]setpts=PTS-STARTPTS+10/TB[top];
        [0:0][top]overlay=enable='between(t\,5,15)'[out]" \
       -shortest -map [out] -map 0:1 \
       -pix_fmt yuv420p -c:a copy -c:v libx264 -crf 18  $TARGET_FOLDER/videos/upload/upload_2.mp4

# Replaces the previous upload video with the output video with the subscribe button
rm $TARGET_FOLDER/videos/upload/upload.mp4 && mv $TARGET_FOLDER/videos/upload/upload_2.mp4 $TARGET_FOLDER/upload/upload.mp4

# # Create metadata
# python3 src/automation/metadata.py

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