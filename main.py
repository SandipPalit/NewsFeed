from scripts.CustomFunctions import *
import json

with open("config/users.json", 'r') as users:
    userJson = json.load(users)
    for item in userJson:
        generateNewsFeed(item["topics"], item["language"], item["location"], item["receivers"])
