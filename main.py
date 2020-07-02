#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

import datetime

from editprofile import EditProfile
from uploadhandler import UploadHandler
from viewhandler import ViewPhotoHandler

from services import Services
from myuser import MyUser
from tweet import Tweet


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        user = Services().get_current_user()
        myuser = None
        tweets = None
        edittweet = None

        if user:

            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("MyUser", Services().get_current_user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = Services().create_user(user_id= user.user_id())

            user_name = self.request.GET.get("user_name")
            bio_text = self.request.GET.get("bio_text")

            if user_name != None and user_name != "" and bio_text != None and bio_text != "":

                user_query = MyUser.query(MyUser.user_name == user_name).fetch()

                if len(user_query) > 0:
                    self.redirect("/")
                    return

                myuser.user_name = user_name
                myuser.bio_text = bio_text
                myuser.put()

            tweets = Tweet.query().order(-Tweet.time)
            search_type = self.request.GET.get("query_type")

            if search_type == "user" or search_type == "post":

                search_text = self.request.GET.get("search_text")

                if len(search_text) > 0:

                    if search_type == "user":
                        tweets = Services().search_by_user(text=search_text)
                    else:
                        tweets = Services().search_by_tweet(text=search_text)


            elif search_type == "Delete" or search_type == "Edit":

                query_type = self.request.GET.get("query_type")
                tweet_id = self.request.GET.get("tweet_id")

                if query_type == "Edit":
                    edittweet = Services().get_tweet(tweet_id = tweet_id)
                    tweets = Services().get_all_user_tweets()

                else:
                    Services().delete_tweet(tweet_id = tweet_id)
                    tweets = Services().get_all_user_tweets()

            else:
                tweets = Services().get_all_user_tweets()

        else:
            url = users.create_login_url(self.request.uri)


        template_values = {
            "url": url,
            "myuser": myuser,
            "tweets":tweets,
            "edittweet":edittweet,
            "upload_url" : blobstore.create_upload_url('/upload_photo')
        }

        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers["Content-Type"] = "text/html"

        share_text = self.request.get("share_text")
        share_image = self.request.get("share_image")


        if share_text != None or share_text != "":

            share_type = self.request.get("share_type")

            if share_type == "Update":

                edit_tweet_id = self.request.get("edit_tweet_id")
                edit_tweet = Services().get_tweet(tweet_id=edit_tweet_id)
                edit_tweet.share_text = share_text

                edit_tweet.put()

            else:

                myuser = Services().get_login_user()
                tweet = Tweet(share_text = share_text,
                              user_id = myuser.key.id(),
                              user_name = myuser.user_name,
                              time = datetime.datetime.now())
                tweet.put()

                myuser.tweet_ids.append(tweet.key.id())
                myuser.put()

        self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/editprofile", EditProfile),
    ("/upload_photo", UploadHandler),
    ('/view_photo/([^/]+)?', ViewPhotoHandler)
], debug=True)







