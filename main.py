from configparser import ConfigParser
import pymongo
from pymongo import MongoClient
import pprint
import requests
import json
import time
import random
from Atlas_Connection import Atlas_Connect
cluster = MongoClient(Atlas_Connect)
Itemdb = cluster["POE_DOCS"]
TestCollection = Itemdb["Test_1"]
CurrencyCollection = Itemdb["Currency"]
CardsCollection = Itemdb["Cards"]
AccessoriesCollection = Itemdb["accessories"]
GemsCollection = Itemdb["gems"]
JewelsCollection = Itemdb["Jewels"]
MapsCollection = Itemdb["Maps"]
WeaponsCollection = Itemdb["weapons"]
ArmourCollection = Itemdb["armour"]
HeistequipmentCollection = Itemdb["heistequipment"]
################
###Categories###
################
# Currency
# SubCat: resonator

# Cards
# No base Type

# accessories
# SubCat: ring, amulet, belt, trinket,

# gems
# SubCat: activegem, supportgem

# jewels
# SubCat: abyss, cluster,

# maps
# SubCat: fragment, scarab,

# weapons
# SubCat: staff, onesword, dagger, wand, twoaxe, twosword, twomace, bow, onemace, sceptre, claw, dagger, oneaxe, twoaxe,

# armour
# SubCat: chest, helmet, gloves, boots, quiver, shield

# heistequipment
# SubCat: heistreward, contract, heisttool, heistweapon, heistutility,


def currency(item_length, list_items):
    x = 0
    while x < item_length:
        items_in_index = list_items[x]
        Item_Base = items_in_index['typeLine']
        try:
            Item_Stack_Size = items_in_index['stackSize']
        except KeyError:
            Item_Stack_Size = "N/A"
        try:
            Item_Price = items_in_index['note']
        except KeyError:
            Item_Price = "N/A"
        extended = items_in_index["extended"]
        Category = extended['category']
        if Category == 'currency':
            # create a log file and write found currency
            for y in range(1):
                random_id = random.randint(1, 1000000000)
                id_random = str(random_id)
            currenyPost = {"_id": id_random,
                           "Item_Base": Item_Base, "Item_Price": Item_Price, "Item_Stack_Size": Item_Stack_Size}
            print("Found a Currency")
            CurrencyCollection.insert_one(currenyPost)
        x += 1
    return


def card(item_length, list_items):
    x = 0
    while x < item_length:
        items_in_index = list_items[x]
        Item_Base = items_in_index['typeLine']
        try:
            Item_Stack_Size = items_in_index['stackSize']
        except KeyError:
            Item_Stack_Size = 'N/A'
        try:
            Item_Price = items_in_index['note']
        except KeyError:
            Item_Price = "N/A"
        extended = items_in_index["extended"]
        Category = extended['category']
        if Category == 'cards':
            # create a log file and write found currency
            for y in range(1):
                random_id = random.randint(1, 1000000000)
                id_random = str(random_id)
            CardPost = {"_id": id_random,
                        "Item_Base": Item_Base, "Item_Price": Item_Price, "Item_Stack_Size": Item_Stack_Size}
            print("Found a Div Card")
            CardsCollection.insert_one(CardPost)
        x += 1

    return


while True:  # loops infinitely
    # stops for 600 milleseconds so app doest get rate limited
    time.sleep(.600)
    # opens txt file and reads change id
    with open("next_change_id.txt") as file:
        change_id = file.read()
        # api response with the change id
        response = requests.get(
            "http://www.pathofexile.com/api/public-stash-tabs?id=" + change_id)
        file.close()
        # reads the response and formats as json
        json_response = response.json()
        # gets the next change id
        next_change_id = json_response['next_change_id']
        # if the next change id is the same as the current if moves on so the app doesnt process the same data
        if next_change_id == change_id:
            continue
        # gets all the stash tab data from api response
        json_data = json_response["stashes"]
        list_length = len(json_data)
        # opens file and writes next change id to the file
        f = open("next_change_id.txt", "w")
        f.write(next_change_id)
        f.close()
        x = 0
        while x < list_length:
            # loops trough the stash data list
            list_index = json_data[x]
            # filters out anything but the league you are wanting data from
            # this can be anything before items in the json data or nothing at all it just makes the data alot smaller
            if list_index['league'] == 'Heist':
                # ETHICAL LEAGUE (PL12057)
                # grabs all the item data form the stashes in that what ever filter you set
                list_items = list_index['items']
                # gets length of the item data list
                item_length = len(list_items)
                # loops through the item list
                # currency(item_length=item_length, list_items=list_items)
                card(item_length=item_length, list_items=list_items)

            x += 1
        # writes next change id to the file so it can be on the current shard
        with open('next_change_id.txt', 'w') as file:
            file.write(next_change_id)
