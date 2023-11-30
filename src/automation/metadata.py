import os
import datetime
import json
import shutil
import random
from PIL import Image


# Is triggered when the production is happening

def create_folders(target_folder):

    os.makedirs(f"{target_folder}/upload")


def get_title(genre):

    # Get title & remove the title from the file
    with open(f"data/store/{genre}/titles.txt", "r") as f:
        lines = f.readlines()

    title = lines.pop(0)
    title = title.replace("\n", "")

    with open(f"data/store/{genre}/titles.txt", "w") as f:
        f.writelines(lines)

    return title


def get_description(genre):

    with open(f"data/store/{genre}/description.txt", "r") as f:
        description = f.read()

    return description


def get_account_data(account_id, video_type):

    with open("data/accounts/accounts.json") as f:
        account_data = json.load(f)[account_id]

    tags = account_data["video_types"][video_type]["keywords"]
    category_id = account_data["category_id"]
    channel_id = account_data["channel_id"]

    return tags, category_id, channel_id


# def calculate_publishing_date():
#     # I am going to base it on the production of the video
#     # The creation of the videos will be scheduled (e.g. via launchd)
#     # So I just need to add a bit of space in between (e.g. 7 days)
#     # format: YYYY-MM-DD

#     # Adds 7 days for quality control
#     date = str(datetime.datetime.now() + datetime.timedelta(7))
#     date = date.split(" ")[0]

#     return date


def copy_auth_files(folder_name, account_id):

    with open("data/accounts/accounts.json") as f:
        account_data = json.load(f)[account_id]

    # Copy client secret file
    shutil.copyfile(account_data["client_secret_file"],
                    f"{folder_name}/upload/client_secret.json")

    # Copy credentials file
    shutil.copyfile(account_data["credentials_file"],
                    f"{folder_name}/upload/credentials.json")


def get_thumbnail(folder_name, genre):
    # Randomly select a thumbnail from the store and store it in the upload folder

    base_path = f"data/store/{genre}/thumbnails"
    files = os.listdir(base_path)

    thumbnail_path = random.choice(files)
    full_thumbnail_path = f"{base_path}/{thumbnail_path}"

    # Convert image if it is png
    if "png" in thumbnail_path:

        im = Image.open(full_thumbnail_path)
        rgb_im = im.convert('RGB')
        rgb_im.save(f"{folder_name}/upload/thumbnail.jpg")

    else:
        os.replace(full_thumbnail_path,
                   f"{folder_name}/upload/thumbnail.jpg")


def create_metadata(folder_name, account_id, video_type, genre, publishing_date):

    get_thumbnail(folder_name, genre)

    title = get_title(genre)
    description = get_description(genre)
    tags, category_id, channel_id = get_account_data(account_id, video_type)
    #publishing_date = calculate_publishing_date()

    copy_auth_files(folder_name, account_id)

    metadata = {
        "title": title,
        "description": description,
        "tags": tags,
        "category_id": category_id,
        "publishing_date": publishing_date,
        "channel_id": channel_id,
    }

    with open(f"{folder_name}/upload/metadata.json", "w") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    return title

# Remove problematic videos


if __name__ == "__main__":

    create_metadata(os.environ["TARGET_FOLDER"], os.environ["ACCOUNT_ID"],
                    os.environ["VIDEO_TYPE"], os.environ["GENRE"], os.environ["PUBLISHING_DATE"])
