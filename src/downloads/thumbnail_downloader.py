import urllib.request
import requests
import json
from time import sleep
import os
import shutil


def remove_duplicates(list_of_dicts):
    """Removes duplicates from a list of dicts

    Args:
        list_of_dicts (list): List that contains dicts with a url key

    Returns:
        list: List of dicts that without duplicates
    """
    duplicate_list = []

    for i, n in enumerate(list_of_dicts):

        if n["url"] in duplicate_list:
            del list_of_dicts[i]
            # print("Entry removed")

        else:
            duplicate_list.append(n["url"])

    return list_of_dicts


def read_cookies(url_object):
    """Reads the cookies from a given url object that contains the cookies

    Args:
        url_object (json): Contains the url, the referrer and the cookies

    Returns:
        dict: Dict that contains all the cookies for downloading a video
    """

    cookie_dict = {}

    cookies = url_object["cookie"]

    for cookie in cookies:
        # print(cookie["name"], cookie["value"])

        cookie_dict[cookie["name"]] = cookie["value"]

    return cookie_dict


def download_thumbnails():
    """Downloads multiple thumbnails from TikTok
    """

    with open(f'data/temp/urls/download_urls.json', 'r') as f:
        video_urls = json.load(f)

    # removes duplicates
    # video_urls = [dict(t) for t in {tuple(d.items()) for d in video_urls}]
    remove_duplicates(video_urls)

    idx = 1

    for url in video_urls:

        try:

            # Read cookies from file
            cookies = read_cookies(url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
                'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                'Range': 'bytes=0-',
                'Referer': url["ref"],
                'Connection': 'keep-alive',
            }

            response = requests.get(url["bgurl"],
                                    headers=headers, cookies=cookies)

            with open(f"data/temp/images/thumbnails/thumbnail_{idx}.jpg", 'wb') as f:
                f.write(response.content)

            sleep(0.5)

        except Exception as e:
            print(e)

        finally:
            print(f"BG-IMG {idx} - Download Completed")
            idx += 1


if __name__ == "__main__":

    download_thumbnails()
