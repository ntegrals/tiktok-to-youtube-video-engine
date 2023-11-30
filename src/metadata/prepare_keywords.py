import json


def prepare_keywords(kw_file_path, json_path, account_id, video_type, character_limit):

    with open(kw_file_path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    charcount = 0
    last_index = 0

    # Cap the keywords at the 500 chars

    for i, line in enumerate(lines):

        if charcount >= character_limit:
            last_index = i - 1
            break
        charcount += len(line)

    if last_index != 0:
        lines = lines[:last_index]

    # Add the keywords to the json file

    with open(json_path) as f:
        data = json.load(f)

    data[account_id]["video_types"][video_type]["keywords"] = lines

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2,)


if __name__ == "__main__":

    prepare_keywords("src/test.txt", "data/accounts/accounts.json",
                     "account_1", "slytherin_compilation", 500)
