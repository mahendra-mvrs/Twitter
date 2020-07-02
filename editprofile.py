import webapp2
import os
import jinja2

from google.appengine.ext import ndb

from datetime import datetime
from services import Services
from tweet import Tweet


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class EditProfile(webapp2.RedirectHandler):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        user_id = self.request.GET.get("user_id")
        otheruserprofile = True
        follow_text = "Follow"

        if user_id != None:
            myuser_key = ndb.Key("MyUser", user_id)
            myuser = myuser_key.get()

            tweets = Tweet.query(Tweet.user_id == myuser.key.id()).fetch(50)
            if user_id == str(Services().get_login_user().key.id()):
                otheruserprofile = False
            if user_id in Services().get_login_user().user_following:
                follow_text = "Unfollow"


        template_values = {
            "myuser": myuser,
            "tweets":tweets,
            "follow":follow_text,
            "otheruserprofile":otheruserprofile
        }

        template = JINJA_ENVIRONMENT.get_template("editprofile.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        user_id = self.request.get("user_id")

        if self.request.get("update_user") == "Update":

            if self.request.get("date") == "" or user_id == "":
                self.redirect("/editprofile")
                return

            myuser = Services().get_login_user()

            user_first_name = self.request.get("user_first_name")
            user_last_name = self.request.get("user_last_name")
            dob = datetime.strptime(self.request.get("date"), '%Y-%m-%d')

            myuser.first_name = user_first_name
            myuser.last_name = user_last_name
            myuser.dob = dob
            myuser.put()

            self.redirect("/")

        elif self.request.get("follow_user") == "Follow" or self.request.get("follow_user") == "Unfollow":

            myuser = Services().get_login_user()

            if self.request.get("follow_user") == "Follow":
                myuser.user_following.append(user_id)

            else:
                user_following = myuser.user_following
                user_following.remove(user_id)
                myuser.user_following = user_following

            myuser.put()
            self.redirect("/editprofile?user_id={}".format(user_id))

        if self.request.get("cancel"):
            self.redirect("/")