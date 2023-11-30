import os
import glob
from auth_test import complete_video_upload


# Thumbnail needs to have the name thumbnail.png

def upload(state, publishing_date):
    """Uploads either single, multiple or all videos

    Args:
        state (string): Specifies the amount of videos to upload
    """

    if state == "Single":
        # Upload a single file in the folder
        complete_video_upload(video, publishing_date)

    elif state == "Multiple":
        # Upload multiple files in the folder
        video_paths = []

        for video in video_paths():
            complete_video_upload(video, publishing_date)

    elif state == "All":
        # Upload all videos in the folder
        # More than 5-6 videos won´t work due to the Youtube API quota

        video_paths = glob.glob1("data/persistent/weekly_uploads", "*")

        for video in video_paths:
            video = f"data/persistent/weekly_uploads/{video}"
            complete_video_upload(video, publishing_date)


if __name__ == "__main__":

    upload("All", "2020-11-02")
