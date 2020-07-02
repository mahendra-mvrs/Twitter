from google.appengine.ext import ndb
from tweet import Tweet

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    bio_text = ndb.StringProperty()

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    dob = ndb.DateProperty()

    tweet_ids = ndb.IntegerProperty(repeated=True)
    user_following = ndb.StringProperty(repeated=True)
