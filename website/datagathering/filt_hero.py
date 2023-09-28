"""
    In hero.json we need to keep all keys. All keys have 1 value of type dict.
    Inside this dict there are a couple of keys we want to keep. 

    Most of these keys have value type str, but the key "stat" is another dict.
    From the "stat" dict we only want to keep specific keys and values. 
"""


# list of keys to keep from the nested dict "stat"
stats_to_keep = [
        "attackType", "startingArmor", "startingMagicArmor", "startingDamageMin",
        "startingDamageMax", "attackRate", "attackAnimationPoint", "attackAcquisitionRange",
        "attackRange", "AttributePrimary", "heroPrimaryAttribute", "strengthBase", "strengthGain",
        "intelligenceBase", "intelligenceGain", "agilityBase", "agilityGain", "hpRegen", "mpRegen",
        "moveSpeed", "moveTurnRate", "visionDaytimeRange", "visionNighttimeRange", "complexity"
]

                
# make a new dict with only the 3 keys we want to keep: "name", "displayName" and "stat"
def filter_keys(response):
    new_dict = {}
    for key, value in response.items():
        new_dict[key] = {
        "name": value.get("name", ""),
        "displayName": value.get("displayName", ""),
        "stat": value.get("stat", "")
    }
    return new_dict


# loop through dict and only keep the keys/values mention in our list "stats_to_keep"
def filter_stats(response):
    for value in response.values():
        if "stat" in value and isinstance(value["stat"], dict):
            new_stat_dict = {}
            for stat_key in stats_to_keep:
                if stat_key in value["stat"]:
                    new_stat_dict[stat_key] = value["stat"][stat_key]
            value["stat"] = new_stat_dict

    return response



# take account ID as input and runs the program
# when the api-response is filtered down it stores in .json file
def hero(hero_response):
    temp_hero_response = filter_keys(hero_response)
    temp_hero_response.pop("0") # remove because it doesn't contain data on hero
    new_hero_response = filter_stats(temp_hero_response)
    final_hero_resposne  = {key: val for key, val in new_hero_response.items() if "stat" in val and "attackType" in val["stat"]}

    return final_hero_resposne