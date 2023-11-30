import os
import shutil


def delete_temp_files():
    """Deletes the temporary files
    """
    folder = "data/temp"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    try:
        os.remove("videos.txt")
    except:
        pass


def create_temp_folders():
    """Creates a new temporary folder
    """
    os.makedirs("data/temp/images/thumbnails")
    os.makedirs("data/temp/images/final_thumbnails")
    os.makedirs("data/temp/images/qc_thumbnails")
    os.makedirs("data/temp/urls")
    os.makedirs("data/temp/videos")
    os.makedirs("data/temp/videos/concat_videos")
    os.makedirs("data/temp/videos/upload")
    os.makedirs("data/temp/videos/raw_videos")
    os.makedirs("data/temp/videos/raw_videos_2")


if __name__ == "__main__":
    # Deletes the temp files and recreates the folder structure
    delete_temp_files()
    create_temp_folders()
