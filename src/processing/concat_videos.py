from moviepy.video.VideoClip import ImageClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import resize
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

import glob

from datetime import datetime
import sys
import random

# Potential Performance Upgrade (Example)
# https://stackoverflow.com/questions/37317140/cutting-out-a-portion-of-video-python

# Settings
shuffle = True

def count_json_files():
    other_json_files = 2
    count = len(glob.glob1("data/temp/urls","*.json"))
    count = count - other_json_files
    return count

def count_mp4s():
    count = len(glob.glob1(f"data/temp/videos/raw_videos_{video_count}","*.mp4"))
    return count

def str_to_class(str):
    return getattr(sys.modules[__name__], str)

def generate_bg_video():

    duration_bg = 1200 # In seconds (1200 = 20 min)

    bg_img = ImageClip("data/static/images/video_background.png", duration=duration_bg)

    bg_img.write_videofile("data/static/videos/background.mp4", fps=24)

    bg_img.close()


def concat_vids():

    # Generates a list with all videos names based on the number of videos
    video_list = []
    for n in range(count_mp4s()):
        # Starts with 0, thats why it´s n+1
        instance_object = f"data/temp/videos/raw_videos/video_{n+1}.mp4"
        video_list.append(instance_object)
    # print(video_list)

    # Instanciates classes from all the video files
    video_object_list = []

    x,y = 544, 977

    for i,n in enumerate(video_list):
        i = globals()["VideoFileClip"](n)

        # Adjustments to the video clips
        i = i.resize((x,y))

        video_object_list.append(i)
    
    # Shuffleing the video
    # Should avoid the duplication problem
    # Most people shouldn´t be able to notice, hence I shouldn´t be that much worried
    # about producing videos about the same person several times in a short timeframe.
    if shuffle == True:
        random.shuffle(video_object_list)
        
    final_clip = concatenate_videoclips(video_object_list,method="compose")
    # # The details fix the "no audio" issue - seemed to have been in the wrong format for QuickTime to read (VLC had sound the whole time)
    final_clip.write_videofile(f"data/temp/videos/concat_videos/concat_{video_count}.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    
    # Releasing all video resources
    for video in video_object_list:
        video.close()
    
    final_clip.close()


def add_background_video():

    clip_bg = VideoFileClip("data/static/videos/background.mp4")
    clip_tt_comp = VideoFileClip(f"data/temp/videos/concat_videos/concat_{video_count}.mp4").resize((607.5, 1080))
    
    duration_calc = clip_tt_comp.duration # In seconds (1200 = 20 min)

    comp_clip = CompositeVideoClip([clip_bg.set_position("center").subclip(0,duration_calc),clip_tt_comp.set_position("center")])
    # comp_clip = CompositeVideoClip([clip_bg.set_position("center"),clip_tt_comp.set_position("center")])
    comp_clip.write_videofile(f"data/temp/videos/upload/upload_{video_count}.mp4", fps=24, threads=8) # The thread effect doesn´t seem significant
    
    # Releasing all video resources
    clip_bg.close()
    clip_tt_comp.close()
    comp_clip.close()


if __name__ == "__main__":

    # generate_bg_video()
    # video_count=0
    # concat_vids()
    # add_background_video()

    # Download raw videos for all 3 videos

    video_count = 0
    for n in range(count_json_files()):
        print(f"Producing video {video_count+1}")
        concat_vids()
        add_background_video()
        video_count += 1