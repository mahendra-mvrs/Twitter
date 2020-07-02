from google.appengine.ext import ndb

class Tweet(ndb.Model):

    share_text = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    avatar = ndb.BlobKeyProperty()