from flask import Blueprint, render_template, request, redirect, url_for
import requests
import datetime
import json
import os
from datagathering.accountData import account
from website.datagathering.call_database_data import headers
from datagathering.matchData import database_worker
from datagathering.match_grids import create_match_grids 

views = Blueprint("views", __name__)

# function to check if accountID is valid
def validate_accountID(account_id):
    """
    Make an attempt to call the api with the current account_id.
    If the call fails it means the account_id is invalid.
    """
    response = requests.get(f"https://api.stratz.com/api/v1/Player/{account_id}", headers=headers,)
    
    if response.status_code == 200:
        try:
            response = response.json()
            return True
        except json.JSONDecodeError as e:
            return False
    else:
        return False


# create view for the Home Page
@views.route("/")
def home():
    return render_template("home.html")


# view similar to the homepage just with adding a potential error message
# if the accountID is invalid. 
@views.route("/", methods=["POST"])
def process_input():
    dota2_account_id = request.form.get("dota2_account_id")
    error_message = None

    try:
        # check if accountID is valid
        if validate_accountID(dota2_account_id):
            return redirect(url_for("views.account_overview", account_id=dota2_account_id))
        else:
            # If accountID is invalid, set error message
            error_message = "Invalid Account ID."
    except Exception as e:
        # Handle exceptions if there is an issue with the API call
        error_message = f"Error: {str(e)}"

    # send error message to display on page
    return render_template("home.html", error_message=error_message)


# view for the main account page were we will display last 10 matches
@views.route("/account_overview/<account_id>")
def account_overview(account_id):
    account_data = account(int(account_id)) # general data/information on the account
    _,match_data = database_worker(int(account_id)) # data on the 10 most recent games of the account
    return render_template("account_overview.html", account_data=account_data, match_data=match_data)


# view for the specific match with analysis
@views.route("/account_overview/<account_id>/match_details/<match_id>")
def match_details(account_id, match_id):
    # make sure the grid_images folder is empty so the images dont stack up infinite
    folder_path = "static/images/grid_images"
    folder_contents = os.listdir(folder_path)
    for item in folder_contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)

    # Retrieve match details based on the account_id and match_id
    pick_bans, match_data  = database_worker(account_id)
    match_details = next((match for match in match_data if match["id"] == int(match_id)), None) # out of the 10 recent matches, find the right one
    match_details["endDateTime"] = datetime.datetime.utcfromtimestamp(match_details["endDateTime"]).strftime('%Y-%m-%d %H:%M') # converting time from unix to readable date
    create_match_grids(match_details, match_id) # creates grids of networth and experience from the game
    return render_template("match_details.html", match_details=match_details, pick_bans=pick_bans, match_id=int(match_id), str_matchId=str(match_id))