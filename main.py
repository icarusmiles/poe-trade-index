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


def post(item_length, list_items):
    y = 0
    while y < item_length:
        # gets all the item data
        items_in_index = list_items[y]
        # sometimes certian dicts of json dont have a certian key so this gets around that so the app can run for ever
        try:
            Item_Name = items_in_index['name']
            Item_Type = items_in_index['typeLine']
            Item_Ident = items_in_index['identified']
            Item_desc = items_in_index['descrText']
            Item_level = items_in_index['ilvl']
            Item_Explicit = items_in_index['explicitMods']
            Item_implicit = items_in_index['implicitMods']
            for x in range(1):
                random_id = random.randint(1, 1000000000)
                id_random = str(random_id)
            Post = {
                "_id": id_random, "Item_Name": Item_Name, "Item_Base": Item_Type, "Item_Ident": Item_Ident, "Item_desc": Item_desc, "Item_level": Item_level, "Item_Explicit": Item_Explicit, "Item_implicit": Item_implicit}
            print("Inscerting")
            TestCollection.insert_one(Post)
            # print(Explicit)
        except KeyError:
            null = "null"
        y += 1
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
            if list_index['league'] == 'ETHICAL LEAGUE (PL12057)':
                print("FOUND IT ")
                # grabs all the item data form the stashes in that what ever filter you set
                list_items = list_index['items']
                # gets length of the item data list
                item_length = len(list_items)
                # loops through the item list
                post(item_length=item_length, list_items=list_items)
            x += 1
        # writes next change id to the file so it can be on the current shard
        with open('next_change_id.txt', 'w') as file:
            file.write(next_change_id)
