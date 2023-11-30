from auth import *

if __name__ == '__main__':

    ###### Authentication YouTube API
    # gets the name of the credentials from the accounts files
    cred_file = read_account_data()["credentials_file"]

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    service = get_authenticated_service(cred_file)

    ###### Get metadata
    # title = read_title()
    # desc = read_description()
    # tags = read_tags()
    # publishing_time = get_publishing_time(service)

    # category_id = read_account_data()[]

    production_load = check_production_load(service)
    print(production_load)