from google.appengine.api import users
from google.appengine.ext import ndb

from tweet import Tweet
from myuser import MyUser

class Services(object):

    def create_user(self,user_id):

        myuser = MyUser(id=user_id, user_id=str(user_id))
        myuser.user_name = ""
        myuser.user_following = []
        myuser.put()
        return myuser

    def get_current_user(self):
        return users.get_current_user()


    def get_current_user_id(self):
        return users.get_current_user().user_id()


    def get_login_user(self):
        myuser_key = ndb.Key("MyUser", Services().get_current_user_id())
        return  myuser_key.get()

    def search_by_tweet(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Tweet.query(Tweet.share_text >= text, Tweet.share_text < limit)

    def search_by_user(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Tweet.query(Tweet.user_name >= text, Tweet.user_name < limit)

    def delete_tweet(self,tweet_id):

        myuser = Services().get_login_user()
        tweet_ids = myuser.tweet_ids
        tweet_ids.remove(int(tweet_id))
        myuser.tweet_ids = tweet_ids
        myuser.put()

        tweet_key = ndb.Key("Tweet", int(tweet_id))
        tweet = tweet_key.get()
        tweet.key.delete()


    def get_tweet(self,tweet_id):

        tweet_key = ndb.Key("Tweet", int(tweet_id))
        tweet = tweet_key.get()
        return tweet

    def get_all_user_tweets(self):

        myuser = Services().get_login_user()
        tweets = []
        for tweet in Tweet.query().order(-Tweet.time).fetch():
            if tweet.user_id in myuser.user_following or tweet.user_id == myuser.key.id():
                tweets.append(tweet)
        return tweets


