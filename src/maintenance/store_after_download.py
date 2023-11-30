import os
import shutil
import datetime


def store():
    """Store the files for a video, to prevent deletion from the next video production.
    """
    target_path = f"data/persistent/weekly_uploads/video_{datetime.datetime.now().strftime('%d-%m-%Y.%H:%M:%S')}"
    os.makedirs(target_path)
    os.makedirs(target_path + "/videos")

    # Copy metadata
    # os.replace("data/temp/keywords.txt", f"{target_path}/keywords.txt")
    try:
        os.replace("data/temp/title.txt", f"{target_path}/title.txt")
    except:
        pass
    try:
        os.replace("data/temp/description.txt",
                   f"{target_path}/description.txt")
    except:
        pass

    try:
        os.replace("data/temp/tags.txt", f"{target_path}/tags.txt")
    except:
        pass

    # Copy video
    try:
        os.replace("data/temp/videos/upload/upload.mp4",
                   f"{target_path}/videos/upload/upload.mp4")
    except:
        pass
    # Copy images
    try:
        os.replace("data/temp/images", f"{target_path}/images")
    except:
        pass
    # Copy raw videos
    try:
        os.replace("data/temp/videos/raw_videos",
                   f"{target_path}/videos/raw_videos")
    except:
        pass

    os.makedirs(f"{target_path}/videos/raw_videos_2")
    os.makedirs(f"{target_path}/videos/concat")
    os.makedirs(f"{target_path}/videos/upload")
    os.makedirs(f"{target_path}/upload")


if __name__ == "__main__":
    store()
