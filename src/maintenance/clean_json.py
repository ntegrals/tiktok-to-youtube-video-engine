import json


def clean_json(path):
    """Cleans up the json files that were concatenated

    Args:
        path (string): Path to json file
    """

    with open(path, "r") as f:
        result = f.readline().replace("[", "").replace("]", "")
        result = "[" + result + "]"
        result = result.replace('""', '","')
        result = result.replace("}{", "},{")
        result = result.replace("}}", "}]}")
        result = result.replace('cookie":{', 'cookie":[{')

    with open(path, "w") as f:
        f.write(result)


if __name__ == "__main__":

    file_list = ["data/temp/urls/urls.json",
                 "data/temp/urls/download_urls.json"]

    for n in file_list:
        clean_json(n)
