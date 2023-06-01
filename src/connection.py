from pymongo import MongoClient

client = MongoClient("mongodb://192.168.1.111:27017/")

db = client.twitter_api

trends_collection = db.trends

friends_collection = db.friends
