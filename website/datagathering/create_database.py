import sqlite3
import json
from call_database_data import hero_data, items_data, region_data, patchnotes_data, lobbytype_data, gamemode_data, gameversion_data


"""
    First we gather all the data from the STRATZ Api through 
    out call_database_data.py file. Then we insert all the data
    into a database.
"""


def error_convert(dict, val):
    """
    Convert the list to a string (JSON representation)
    this helps inserting list object to the database,
    aswell as it returns "None" if no value exists to prevent crash
    """
    if val in dict:
        if not dict[val]: # checks if empty list
            return "None"
        else:
            return json.dumps(dict[val]) 
    else:
        return "None"
    


# Create SQLite database
conn = sqlite3.connect("dota.db")
cursor = conn.cursor()



# -------------------------------
# Table of hero
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS hero (
        id INTEGER PRIMARY KEY,
        name TEXT,
        displayname TEXT,
        attackType TEXT,
        startingArmor REAL,
        startingMagicArmor REAL,
        startingDamageMin REAL,
        startingDamageMax REAL,
        attackRate REAL,
        attackAnimationPoint REAL,
        attackAcquisitionRange REAL,
        attackRange REAL,
        AttributePrimary TEXT,
        heroPrimaryAttribute INTEGER,
        strengthBase REAL,
        strengthGain REAL,
        intelligenceBase REAL,
        intelligenceGain REAL,
        agilityBase REAL,
        agilityGain REAL,
        hpRegen REAL,
        mpRegen REAL,
        moveSpeed REAL,
        moveTurnRate REAL,
        visionDaytimeRange REAL,
        visionNighttimeRange REAL,
        complexity INTEGER
    )
""")

for key, val in hero_data.items():
    # reach nested dict
    stat_data = val["stat"]
    
    cursor.execute("""
        INSERT INTO hero (
            id, name, displayname, attackType, startingArmor, startingMagicArmor,
            startingDamageMin, startingDamageMax, attackRate, attackAnimationPoint,
            attackAcquisitionRange, attackRange, AttributePrimary, heroPrimaryAttribute,
            strengthBase, strengthGain, intelligenceBase, intelligenceGain,
            agilityBase, agilityGain, hpRegen, mpRegen, moveSpeed, moveTurnRate,
            visionDaytimeRange, visionNighttimeRange, complexity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        int(key), val["name"], val["displayName"], stat_data["attackType"],
        stat_data["startingArmor"], stat_data["startingMagicArmor"],
        stat_data["startingDamageMin"], stat_data["startingDamageMax"],
        stat_data["attackRate"], stat_data["attackAnimationPoint"],
        stat_data["attackAcquisitionRange"], stat_data["attackRange"],
        stat_data["AttributePrimary"], stat_data["heroPrimaryAttribute"],
        stat_data["strengthBase"], stat_data["strengthGain"],
        stat_data["intelligenceBase"], stat_data["intelligenceGain"],
        stat_data["agilityBase"], stat_data["agilityGain"],
        stat_data["hpRegen"], stat_data["mpRegen"],
        stat_data["moveSpeed"], stat_data["moveTurnRate"],
        stat_data["visionDaytimeRange"], stat_data["visionNighttimeRange"],
        stat_data["complexity"]
    ])



# -------------------------------
# Table of items
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        displayName TEXT,
        shortName TEXT,
        lore BLOB,
        description BLOB,
        notes BLOB,
        castRange BLOB,
        castPoint BLOB,
        cooldown BLOB,
        manaCost BLOB,
        cost REAL,
        shopTags TEXT,
        aliases TEXT,
        quality TEXT,
        isSellable TEXT,
        isDroppable TEXT,
        isPurchaseable TEXT,
        isSecretShop TEXT,
        isSideShop TEXT,
        isStackable TEXT,
        isPermanent TEXT,
        isHideCharges TEXT,
        isRequiresCharges TEXT,
        isDisplayCharges TEXT,
        isSupport TEXT,
        isTempestDoubleClonable TEXT,
        stockMax REAL,
        initialCharges REAL,
        initialStock REAL,
        stockTime REAL,
        initialStockTime REAL,
        isRecipe TEXT,
        needsComponents TEXT,
        isFullItemHeroPurchaseItem TEXT,
        image TEXT
    )
""")

for key, val in items_data.items():
    # reach nested dicts
    language = val.get("language", {})  # Use a default empty dictionary if "language" key is missing
    stat = val.get("stat", {})
    
    cursor.execute("""
        INSERT INTO items (
            id, name, displayName, shortName, lore, description, notes,
            castRange, castPoint, cooldown, manaCost, cost, shopTags,
            aliases, quality, isSellable, isDroppable, isPurchaseable, 
            isSecretShop, isSideShop, isStackable, isPermanent, isHideCharges,
            isRequiresCharges, isDisplayCharges, isSupport, isTempestDoubleClonable,
            stockMax, initialCharges, initialStock, stockTime, initialStockTime,
            isRecipe, needsComponents, isFullItemHeroPurchaseItem, image
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        int(val["id"]), val["name"], val["displayName"], val["shortName"], error_convert(language, "lore"),
        error_convert(language, "description"), error_convert(language, "notes"), error_convert(stat, "castRange"), error_convert(stat, "castPoint"),
        error_convert(stat, "cooldown"), error_convert(stat, "manaCost"), error_convert(stat, "cost"), error_convert(stat, "shopTags"),
        error_convert(stat, "aliases"), error_convert(stat, "quality"), error_convert(stat, "isSellable"), error_convert(stat, "isDroppable"),
        error_convert(stat, "isPurchaseable"), error_convert(stat, "isSecretShop"), error_convert(stat, "isSideShop"), error_convert(stat, "isStackable"),
        error_convert(stat, "isPermanent"), error_convert(stat, "isHideCharges"), error_convert(stat, "isRequiresCharges"), error_convert(stat, "isDisplayCharges"),
        error_convert(stat, "isSupport"), error_convert(stat, "isTempestDoubleClonable"), error_convert(stat, "stockMax"), error_convert(stat, "initialCharges"),
        error_convert(stat, "initialStock"), error_convert(stat, "stockTime"), error_convert(stat, "initialStockTime"), error_convert(stat, "isRecipe"),
        error_convert(stat, "needsComponents"), val["isFullItemHeroPurchaseItem"], error_convert(val, "image")
    ])



# -------------------------------
# Table of Region
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS region (
        id INTEGER PRIMARY KEY,
        name TEXT,
        clientName TEXT,
        displayName TEXT,
        leaderboardDivision TEXT,
        langKey TEXT,
        latitude REAL,
        longitude REAL,
        code TEXT,
        matchGroup INTEGER
    )
""")

for key in region_data:
    cursor.execute("""
        INSERT INTO region (
            id, name, clientName, displayName, leaderboardDivision,
            langKey, latitude, longitude, code, matchGroup
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        error_convert(key, "id"), error_convert(key, "name"), error_convert(key, "clientName"),
        error_convert(key, "displayName"), error_convert(key, "leaderboardDivision"),
        error_convert(key, "langKey"), error_convert(key, "latitude"), error_convert(key, "longitude"),
        error_convert(key, "code"), error_convert(key, "matchGroup")
    ])



# -------------------------------
# Table of Patch notes
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patchnotes (
        id TEXT PRIMARY KEY,
        gameVersionId INTEGER,
        languageId INTEGER,
        slotIndex INTEGER,
        heroId INTEGER,
        text TEXT
    )
""")

for key in patchnotes_data:
    cursor.execute("""
        INSERT INTO patchnotes (
        id, gameVersionId, languageId,
        slotIndex, heroId, text
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        error_convert(key, "id"), error_convert(key, "gameVersionId"), error_convert(key, "languageId"),
        error_convert(key, "slotIndex"), error_convert(key, "heroId"), error_convert(key, "text")
    ])



# -------------------------------
# Table of Lobbytype
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS lobbytype (
        id INTEGER PRIMARY KEY,
        name TEXT,
        langKey TEXT
    )
""")

for val in lobbytype_data.values():
    cursor.execute("""
        INSERT INTO lobbytype (
            id, name, langKey
        )
        VALUES (?, ?, ?)
    """, [
    int(val["id"]), error_convert(val, "name"), error_convert(val, "langKey")
    ])



# -------------------------------
# Table of gamemode
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamemode (
        id INTEGER PRIMARY KEY,
        name TEXT,
        langKey TEXT
    )
""")

for key, val in gamemode_data.items():
    cursor.execute("""
        INSERT INTO gamemode (
            id, name, langKey
        )
        VALUES (?, ?, ?)
    """, [
        int(val["id"]), error_convert(val, "name"), error_convert(val, "langKey")
    ])



# -------------------------------
# Table of GameVersions
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gameversion (
        id INTEGER PRIMARY KEY,
        name TEXT,
        startDate TEXT
    )
""")

for key in gameversion_data:
    cursor.execute("""
        INSERT INTO gameversion (
            id, name, startDate
        )
        VALUES (?, ?, ?)
    """, [
        key["id"], error_convert(key, "name"), error_convert(key, "startDate")
    ])




# comming changes and close
conn.commit()
conn.close()