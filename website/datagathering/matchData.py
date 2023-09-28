from website.datagathering.call_database_data import make_response
import sqlite3

database = "datagathering/dota.db"
string_remove = "npc_dota_hero_"

def database_worker(accId):
    # this api gives a response of data on the 10 most recent games of an account
    response = make_response(f"https://api.stratz.com/api/v1/Player/{accId}/matches")

    """
    First we connect to out database and make functions
    to access the different data we need from out database.

    In many cases the data from our response(matches api) is just numbers.
    We use the database to make sense of these different number so that
    they can be more presentable in the application
    """

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # query to find the name of the heroId
    def hero_query(id):
        query_heroId = f"SELECT * FROM hero WHERE id = ?"
        cursor.execute(query_heroId, (id,))
        result = cursor.fetchone()
        if result:
            hero_name, hero_displayName = result[1], result[2]
            return hero_name, hero_displayName
        else:
            return None

    # query to find lobbytype name
    def lobbytype_query(id):
        query_lobbytype = f"SELECT * FROM lobbytype WHERE id = ?"
        cursor.execute(query_lobbytype, (id,))
        result = cursor.fetchone()
        if result:
            lobbytype = result[1]
            return lobbytype
        else:
            return None

    # query to find gamemode type
    def gamemode_query(id):
        query_gamemode = f"SELECT * FROM gamemode WHERE id = ?"
        cursor.execute(query_gamemode, (id,))
        result = cursor.fetchone()
        if result:
            gamemode = result[1]
            return gamemode
        else:
            return None
    
    # query to find name of region
    def region_query(id):
        query_gamemode = f"SELECT * FROM region WHERE id = ?"
        cursor.execute(query_gamemode, (id,))
        result = cursor.fetchone()
        if result:
            gamemode = result[2]
            return gamemode
        else:
            return None

    # update certain values in the response
    def update_response():
        for i in response:
            # find the name of the hero based on heroId
            code_name, display_name = hero_query(i["players"][0]["heroId"])
            temp = code_name.replace(string_remove, "")

            # add url to the hero icon image
            i["players"][0]["heroId"] = f"https://cdn.stratz.com/images/dota2/heroes/{temp}_icon.png"
            i["players"][0]["heroName"] = display_name

            # find name of bracket and add url to the bracket icon image
            temp = i["bracket"]
            i["bracket"] = f"https://cdn.stratz.com/images/dota2/seasonal_rank/medal_{temp}.png"

            # swap lobbytype id with name of lobbytype
            i["lobbyType"] = lobbytype_query(i["lobbyType"])

            # swap gamemode id with name of gamemode
            i["gameMode"] = gamemode_query(i["gameMode"])

            # swap region id with name of region
            i["regionId"] = region_query(i["regionId"])
    

    result_dict = {}
    """
    Now we want to find the hero draft from the game, and we want it sorted into:
    Radiant team, Dire team and banned heroes.

    We need to check every hero in the dataset if its a Picked hero or a banned hero.
    If the hero is picked we also need to check if its in Radiant or Dire team.
    On every hero we also add url to the "profile-picture" of the hero
    """
    for match in response:
        match_id = str(match["id"])
        radiant_picks = []
        dire_picks = []
        bans = []
        try: 
            # loop through all the heroes in the match that was either picked or tried banned
            for pickBan in match["pickBans"]:
                is_pick = pickBan["isPick"]
                
                # if hero was picked / if hero is NOT banned
                if is_pick:
                    hero_id = pickBan["heroId"]
                    is_radiant = pickBan["isRadiant"]

                    # if hero is on Radiant team
                    if is_radiant:
                        code_name, display_name = hero_query(hero_id)
                        temp = code_name.replace(string_remove, "")
                        hero_image = f"https://cdn.stratz.com/images/dota2/heroes/{temp}_horz.png" # img url for hero
                        radiant_picks.append([display_name, hero_image])

                    # if hero is on Dire team
                    else: 
                        code_name, display_name = hero_query(hero_id)
                        temp = code_name.replace(string_remove, "")
                        hero_image = f"https://cdn.stratz.com/images/dota2/heroes/{temp}_horz.png" # img url for hero
                        dire_picks.append([display_name, hero_image])

                # if hero was banned / not picked
                elif not is_pick: 
                    if pickBan["wasBannedSuccessfully"]: # if the ban was successful (this is not always the case)
                        banned_hero_id = pickBan["bannedHeroId"]
                        code_name, display_name = hero_query(banned_hero_id)
                        temp = code_name.replace(string_remove, "")
                        hero_image = f"https://cdn.stratz.com/images/dota2/heroes/{temp}_horz.png" # img url for hero
                        bans.append([display_name, hero_image])
        except:
            pass
        
        # set the structure of the result_dict
        result_dict[int(match_id)] = {
            "radiant": radiant_picks,
            "dire": dire_picks,
            "bans": bans
        }


    update_response()
    conn.close()
    return result_dict, response