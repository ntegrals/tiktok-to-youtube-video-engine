
def remove_prev_production(path_production_file):
    """Transfer the current production vars from the production list to the env vars

    Args:
        path_production_file (string): Path to production list file
        path_env_file (string): Path to env var file
    """
    try:
        # Read production file
        with open(path_production_file) as f:

            lines = f.readlines()
            # Removes the whitespace chars
            lines = [x.strip() for x in lines]

        # Remove produced video file
        with open(path_production_file, "w") as f:
            f.writelines(lines[1:])

    except Exception as e:
        # print(e)
        pass


if __name__ == "__main__":
    remove_prev_production("data/static/production/production.txt")
