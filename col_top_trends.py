
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
  consumer_key = '' #Jamiah you need Yours here ( get in Twitter developer ) 
  consumer_secret = ''  #Jamiah you need Yours here ( get in Twitter developer ) 
  access_token = ''  #Jamiah you need Yours here ( get in Twitter developer )  
  access_token_secret = ''  #Jamiah you need Yours here ( get in Twitter developer )  

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
