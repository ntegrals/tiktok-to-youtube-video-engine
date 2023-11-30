
def read_production_file(path_production_file, path_env_file):
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

        # print(lines)

        # Process content
        account = lines[0].split(";")[0]
        video_type = lines[0].split(";")[1]

        # Write env file
        with open(path_env_file, "w") as f:
            f.write(f"ACCOUNT_ID={account}\nVIDEO_TYPE={video_type}")

        # # Remove produced video file
        # with open(path_production_file, "w") as f:
        #     f.writelines(lines[1:])

    except Exception as e:
        # print(e)
        pass


if __name__ == "__main__":
    read_production_file("data/static/production/production.txt", "src/.env")
