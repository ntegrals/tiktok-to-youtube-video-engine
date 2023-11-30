
# A smarter way might be to cut out a certain part of the final video and concatenate it back together afterwards
# That would probably be way faster

TARGET_FOLDER=data/persistent/weekly_uploads/hogwarts_letter_3

ffmpeg -y -i $TARGET_FOLDER/videos/upload/upload.mp4 -i data/static/videos/subscribe.mov  -filter_complex \
        "[1]setpts=PTS-STARTPTS+10/TB[top];
        [0:0][top]overlay=enable='between(t\,5,15)'[out]" \
       -shortest -map [out] -map 0:1 \
       -pix_fmt yuv420p -c:a copy -c:v libx264 -crf 18  $TARGET_FOLDER/videos/upload/upload_2.mp4

rm $TARGET_FOLDER/videos/upload/upload.mp4 && mv $TARGET_FOLDER/videos/upload/upload_2.mp4 $TARGET_FOLDER/videos/upload/upload.mp4
