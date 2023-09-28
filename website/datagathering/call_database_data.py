import json
import requests
from filt_hero import hero

"""
    In this file we create multiple responses from the STRATZ api
    and saves the data to later insert into sqlite database
"""

# find your token at stratz.com/api
token = ""
headers = {"Authorization": f"Bearer {token}"}

# make a response with the input url. inlcudes error-handling
def make_response(url):
    response = requests.get(url, headers=headers,)

    if response.status_code == 200:
        try:
            response = response.json()
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("Error:", response.status_code)

    return response


def items():
    response = make_response(f"https://api.stratz.com/api/v1/Item")
    
    path = "http://cdn.dota2.com/apps/dota2/images/items/"
    # add the image path in every image value to make complete url
    for val in response.values():
        try:
            # update the image value to complete url
            temp = path + val["image"]
            val["image"] = temp
        except:
            continue

    return response



def region():
    response = make_response(f"https://api.stratz.com/api/v1/Region")
    del response[0] # 0th element does not contain any region
    return response


def patchnotes():
    response = make_response(f"https://api.stratz.com/api/v1/Patch/notes")
    return response


def lobbytype():
    response = make_response(f"https://api.stratz.com/api/v1/lobbyType")
    return response


def gamemode():
    response = make_response(f"https://api.stratz.com/api/v1/GameMode")
    response.pop("0") # 0th element does not contain any region
    return response

def gameversion():
    response = make_response(f"https://api.stratz.com/api/v1/GameVersion")
    return response


def matches(accId):
    response = make_response(f"https://api.stratz.com/api/v1/Player/{accId}/matches")
    return response


"""
Since the hero, account api contain many nested keys/values and we only want to keep a few,
they have comprehensive filtering in seperate files before its returned to this file.
The account api also needs to be called everytime a user uses the application
"""

# calling all api's
hero_data = hero(make_response(f"https://api.stratz.com/api/v1/Hero"))
items_data = items()
region_data = region()
patchnotes_data = patchnotes()
lobbytype_data = lobbytype()
gamemode_data = gamemode()
gameversion_data = gameversion()