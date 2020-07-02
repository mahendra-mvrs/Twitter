

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import  datetime

from services import Services
from tweet import Tweet

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        blobinfo = None
        if len(self.get_uploads()) > 0:
            upload_file = self.get_uploads()[0]
            blobinfo = blobstore.BlobInfo(upload_file.key())

        share_text = self.request.get("share_text")
        share_type = self.request.get("share_type")

        if share_type == "Update":

            edit_tweet_id = self.request.get("edit_tweet_id")
            edit_tweet = Services().get_tweet(tweet_id=edit_tweet_id)
            edit_tweet.share_text = share_text
            edit_tweet.time = datetime.datetime.now()
            if blobinfo != None:
                edit_tweet.avatar = upload_file.key()
            edit_tweet.put()

        else:

            myuser = Services().get_login_user()
            tweet = Tweet(share_text=share_text,
                          user_id=myuser.key.id(),
                          user_name=myuser.user_name,
                          time=datetime.datetime.now())

            if blobinfo != None:
                tweet.avatar = upload_file.key()
            tweet.put()

            myuser.tweet_ids.append(tweet.key.id())
            myuser.put()

        self.redirect("/")
