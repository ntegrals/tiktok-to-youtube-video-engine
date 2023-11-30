import json


def channel_keywords(kw_file_path):

    with open(kw_file_path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        for line in lines:

            if "," in line:
                print("Yes")

                line = line.replace(",", "")

        lines = [line + "," for line in lines]

    print(lines)

    with open(kw_file_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":

    channel_keywords("data/static/texts/keywords.txt")
