
import sys
import tweepy
import json
from datetime import datetime
from pymongo import MongoClient

connMongo = MongoClient('mongodb://192.168.100.15:27017')
db = connMongo.TweetData
arg = int(sys.argv[1])



if arg == 1:

  #Autenticações
  consumer_key = '1mvb006pw6l8mkedDTeqE8UOw'
  consumer_secret = 'dOgONpX9mlIgW4lcHnmBgRx4KTxn5ILiK1TH4hWQz1DuqP2hP8'
  access_token = '237450282-x8x7SWNxcCmB7yRXNi5nFoGHEyRiJBFOddujx0vH'
  access_token_secret = 'TZdyqlidRQkl3vH4xLAyN35Tf1K9S5IYMhkZ2yWfK75xI'

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  # O Yahoo! Where On Earth ID para o Brasil é 23424768.
  # Veja mais em https://dev.twitter.com/docs/api/1.1/get/trends/place e http://developer.yahoo.com/geo/geoplanet/
  BRAZIL_WOE_ID = 23424768

  brazil_trends = api.trends_place(BRAZIL_WOE_ID)

  trends = json.loads(json.dumps(brazil_trends, indent=1))


  for trend in trends[0]["trends"]:
    doc = {}
    for k,v in trend.items():
      doc[''+ k + ''] = v
      doc['datetime'] = datetime.today()
    print(doc)
    db.toptrends.insert_one(doc)

if arg == 2:

  result  = db.toptrends.aggregate([
    {"$match": {"name": {"$regex": "#"}}},
                        {"$group": {"_id": {"name": "$name"},
                "datetime": {"$max": "$datetime"}}},
    {"$project": {"name": "$_id.name", "_id": 0}},
    {"$limit": 3}])
  for res in result:
    print(res['name'])
