import glob
target_folder = "data/persistent/weekly_uploads/diagon_alley_2"


def create_paths(target_folder):
    """Creates the initial path file, which is modified manually

    Args:
        target_folder (string): Folder that contains all files related to a specific video
    """

    video_paths = glob.glob1(f"{target_folder}/videos/raw_videos", "*")
    # print(video_paths)
    # video_paths_1 = ["file '" + target_folder + "/videos/raw_videos/" +
    #                  path + "'" + "\n" for path in video_paths]

    video_paths_1 = ["file '" + "videos/raw_videos_2/" +
                     path + "'" + "\n" for path in video_paths]
    # print(video_paths_1)

    with open(f"{target_folder}/video_paths.txt", "w") as f:
        f.writelines(video_paths_1)


if __name__ == "__main__":

    create_paths(target_folder)
