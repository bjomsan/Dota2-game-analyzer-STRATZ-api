import datetime
from datetime import datetime
from datagathering.call_database_data import make_response

"""
    This file calls the Player/{accountId} api from Stratz with data on the specified
    account, including e.g. accountname, total games played, last time active, if account is smurfflagged...

    After gathering the data we filter out everything we dont need.
"""


# converting Unix timestamps
def convert_time(timestamp):
    conv = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    return conv

# checks if number is unix timestamp
def is_unix_timestamp(timestamp):
    # Define reasonable boundaries for Unix timestamps
    current_date = datetime.now() # find current date
    current_date = int(current_date.timestamp())

    min_unix_timestamp = 1356998400  # January 1., 2013 (the year Dota2 was released)
    max_unix_timestamp = current_date

    # check if time is between min and max
    if isinstance(timestamp, int) and timestamp > min_unix_timestamp and timestamp < max_unix_timestamp:
        return True
    else:
        return False
    

# list of keys we want to keep
keys_to_keep = [
        "steamAccount", "battlePass", "firstMatchDate",
        "matchCount", "winCount", "names"
]

# list of values we want to keep
values_to_keep = [
        "lastActiveTime", "realName", "timeCreated", "name",
        "isDotaPlusSubscriber", "dotaPlusIriginalStartDate",
        "smurfFlag", "smurfCheckDate", "lastMatchDateTime",
        "lastMatchRegionId", "dotaAccountLevel", "evendId", "level"
]

    
# first we remove the keys we don't want to keep
def del_keys(response):
    keys_to_delete = []
    for key in response.keys():
        if key not in keys_to_keep:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del response[key]
    return response


# new dict with the filtered response 
filt_response = {}


# when the value is a list with dict
def list_with_dict(input):
    """
        There are 2 values that are a list with dicts - "name" and "battlePass".
        In these two we also want to filter out just 2 of the neste values.
    """
    if "name" in input[0]:
        output_dict = {'names': []}
        for d in input:
            time = d["lastseendatetime"]
            if is_unix_timestamp(time):
                conv_time = convert_time(d['lastseendatetime'])
                output_dict['names'].append([d['name'], conv_time])
                filt_response.update(output_dict)
    elif "battlePass":
        output_dict = {"battlePassLevel": []}
        for d in input:
            output_dict["battlePassLevel"].append(d["level"])
            filt_response.update(output_dict)
         

# when value is a dict
def dict_only(input):
    for key, val in input.items():
        if key in values_to_keep:
            filt_response[key] = val


# when value is int
def int_only(input):
    if is_unix_timestamp(input):
        return convert_time(input)
    else:
        return input


# find out what type the value is and call the suited function
def filter_keys_and_values(response):
    for key, value in response.items():
        if type(value) is dict:
            dict_only(value)
        elif type(value) is list:
            list_with_dict(value)
        elif type(value) is int:
            value = int_only(value)
            filt_response[key] = value
    return filt_response


# take account ID as input and runs the program.
# when the api-response is filtered down it returns the new response
def account(accId):
    url = f"https://api.stratz.com/api/v1/Player/{accId}"
    response = make_response(url)
    temp_response = del_keys(response)
    new_response = filter_keys_and_values(temp_response)
    
    return new_response
