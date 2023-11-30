import subprocess


def main(production_file_path):
    # read len of production file
    with open(production_file_path) as f:
        lines = f.readlines()

    video_count = len(lines)

    for index in range(video_count):

        print(f"Production: {lines[index].split(';')[1]}")
        subprocess.run("src/production.sh")


if __name__ == "__main__":
    main("data/static/production/production.txt")
