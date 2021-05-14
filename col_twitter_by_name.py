import sys
import tweepy
import json
from pymongo import MongoClient
from bson import json_util
import sys


connMongo = MongoClient('mongodb://192.168.100.15:27017')
db = connMongo.TweetData
print(sys.argv[1])

#Autenticações
consumer_key = #Jamiah you need Yours here ( get in Twitter developer ) 
consumer_secret = #Jamiah you need Yours here ( get in Twitter developer ) 
access_token = #Jamiah you need Yours here ( get in Twitter developer ) 
access_token_secret = #Jamiah you need Yours here ( get in Twitter developer ) 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #print(status)
        doc = {}
        doc['geo'] = status.geo
        doc['created_at'] = status.created_at
        if status.place:
            doc['place_country'] = status.place.country
        doc['lang'] = status.lang
        doc['user_location'] = status.user.location
        doc['user_name'] = status.user.name
        doc['friends_count'] = status.user.friends_count
        doc['followers_count'] = status.user.followers_count
        doc['user_lang'] = status.user.lang
        #print("------------------------------------------")
        #print(doc)
        db.twitter.insert_one(doc)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

#recebe o argumento passado
myStream.filter(track=sys.argv[1], is_async=True)


