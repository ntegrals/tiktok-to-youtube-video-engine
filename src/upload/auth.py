# Source: https://stackoverflow.com/questions/27771324/google-api-getting-credentials-from-refresh-token-with-oauth2client-client

# We only need to get the refresh token manually
# This auth script gets new access tokens based on the refresh tokens then
# Refresh tokens are very rarely expiring

import os
import json
import os.path
import requests
from dotenv import load_dotenv
import google.oauth2.credentials
from datetime import datetime, date, timedelta, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.http import MediaFileUpload

import dateutil.parser

# Read ENV var file
load_dotenv()


# Local Methods
def read_title():
    with open("data/metadata/title.txt", "r") as f:
        return f.read()


def read_description():
    with open("data/metadata/description.txt", "r") as f:
        return f.read()


def read_tags():
    with open("data/metadata/tags.txt", "r") as f:
        return f.read()


def read_account_data(account_id=os.getenv("ACCOUNT_ID")):
    with open("data/accounts/accounts.json") as f:
        account = json.load(f)[account_id]

    return account

# API Auth Vars & Methods


CLIENT_SECRETS_FILE = read_account_data()["client_secret_file"]
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def refreshToken(client_id, client_secret, refresh_token):
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    authorization_url = "https://www.googleapis.com/oauth2/v4/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        return r.json()['access_token']
    else:
        return None


def get_authenticated_service(cred_file):

    # we are just going to refresh every single time

    if os.path.isfile(cred_file):

        with open(cred_file, 'r') as f:
            creds_data = json.load(f)

        # generates a new access_token every time
        access_token = refreshToken(
            creds_data["client_id"], creds_data["client_secret"], creds_data["refresh_token"])

        creds = Credentials(access_token)

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_console()
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        # print(creds_data)
        with open(cred_file, 'w') as outfile:
            json.dump(creds_data, outfile)
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

# API Methods


def list_channel_videos(service, **kwargs):
    results = service.videos().list(**kwargs).execute()
    # print(results)
    return results


def list_all_channel_videos(service, **kwargs):
    results = service.search().list(**kwargs).execute()
    # print(results)
    return results


def upload_video(service, **kwargs):
    results = service.videos().insert(**kwargs).execute()
    print(results)
    return results


def set_thumbnail(service, **kwargs):
    results = service.thumbnails().set(**kwargs).execute()
    print(results)


def set_upload_time(service, **kwargs):

    videos = list_all_channel_videos(service, part='snippet', channelId=read_account_data()[
                                     "youtube_channel_id"], maxResults=20)


def get_subscribers(service, **kwargs):
    results = service.channels().list(
        **kwargs).execute()["items"][0]["statistics"]["subscriberCount"]
    print(results)


def get_publishing_time(service, **kwargs):
    """
    Checks if one of the current videos is scheduled for a day of the next week.
    If that is the case, the day is deleted from the scheduling dates.
    If there is a free date, it will print the free date.

    Is the order correct? (Do we always get the latest videos?)
    """

    # The channel id needs to be adjusted

    video_id_list = []
    publishing_times = []

    """ To get the scheduled times we have to get all videos with the forMine parameter and then query status of each video individually"""
    videos = list_all_channel_videos(
        service, part='snippet', forMine=True, type="video", maxResults=25, order="date")

    for item in videos["items"]:
        video_id_list.append(item["id"]["videoId"])

    video_id_list = video_id_list[0:7]  # checks only the last 7 entries

    # get the publishing times
    for video_id in video_id_list:
        result = list_channel_videos(service, part='status', id=video_id)
        try:
            publishing_times.append(result["items"][0]["status"]["publishAt"])
        except:
            pass

    # Index for the first day of the week (Monday) referring to dates (list)
    publishing_date = 0

    # get the dates for the next week

    # timedelta with 7 days gets us to the next week
    theday = date.today() + timedelta(days=7)
    # -1 necessary, otherwhise the week starts on Sunday
    weekday = theday.isoweekday() - 1
    # The start of the week
    start = theday - timedelta(days=weekday)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(7)]

    for item in publishing_times:

        if publishing_date >= 7:
            break

        if not dates:
            break

        vid_date = dateutil.parser.parse(item)

        # deletes the matched date from the list of dates
        for i, item in enumerate(dates):

            if vid_date.date() == item:

                del dates[i]

                publishing_date += 1  # Moves one day further each loop

    # Choose the next publishing date

    #!!!!!!!#
    # Account 1 muss noch geändert werden
    try:
        next_publishing_date = dates[0].strftime(
            "%Y-%m-%d" + read_account_data()["publishing_time"])  # + time + timezone from accounts
        print(next_publishing_date)
        return next_publishing_date

    except:
        print("All dates are already allocated")


def check_production_load(service, **kwargs):
    """
    Checks if there is still production that needs to be done.
    """
    video_id_list = []
    publishing_times = []

    """ To get the scheduled times we have to get all videos with the forMine parameter and then query status of each video individually"""
    videos = list_all_channel_videos(
        service, part='snippet', forMine=True, type="video", maxResults=25, order="date")

    for item in videos["items"]:
        video_id_list.append(item["id"]["videoId"])

    video_id_list = video_id_list[0:7]  # checks only the last 7 entries

    # get the publishing times
    for video_id in video_id_list:
        result = list_channel_videos(service, part='status', id=video_id)
        try:
            publishing_times.append(result["items"][0]["status"]["publishAt"])
        except:
            pass

    # Index for the first day of the week (Monday) referring to dates (list)
    publishing_date = 0

    # get the dates for the next week

    # timedelta with 7 days gets us to the next week
    theday = date.today() + timedelta(days=7)
    # -1 necessary, otherwhise the week starts on Sunday
    weekday = theday.isoweekday() - 1
    # The start of the week
    start = theday - timedelta(days=weekday)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(7)]

    for item in publishing_times:

        if publishing_date >= 7:
            break

        if not dates:
            break

        vid_date = dateutil.parser.parse(item)

        # deletes the matched date from the list of dates
        for i, day in enumerate(dates):

            if vid_date.date() == day:

                del dates[i]

                publishing_date += 1  # Moves one day further each loop

    if not dates:
        # returns False if all videos for this account are already scheduled (list is empty)
        return False
    else:
        # returns True if there is still space for a new video
        return True


if __name__ == '__main__':

    # Authentication YouTube API
    # gets the name of the credentials from the accounts files
    cred_file = read_account_data()["credentials_file"]

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    service = get_authenticated_service(cred_file)

    # Get metadata
    title = read_title()
    desc = read_description()
    tags = read_tags()
    channelId = read_account_data()["youtube_channel_id"]
    # category_id = read_account_data()[]

    publishing_time = get_publishing_time(service)
    print(publishing_time)

    # get_subscribers(service, part='statistics', id='UCmi_GwnNxFdzCsxb9oiqw9Q')

    upload_res = upload_video(service, part='snippet, status',
                              body={
                                  "snippet": {
                                      "channelId": channelId,
                                      "categoryId": "22",
                                      "description": desc,
                                      "title": title,
                                      "tags": tags,
                                  },
                                  "status": {
                                      "privacyStatus": "private",
                                      "publishAt": publishing_time,
                                  }
                              },
                              media_body=MediaFileUpload(
                                  "data/temp/videos/upload/upload.mp4", resumable=True)
                              )

    # He currently always uses the first image - is this the best approach?
    set_thumbnail(service, videoId=upload_res["id"], media_body=MediaFileUpload(
        "data/temp/images/final_thumbnails/yt_thumbnail_1.png"))
