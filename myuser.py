from google.appengine.ext import ndb

class MyUser(ndb.Model):
        email_address = ndb.StringProperty(repeated=False)
        followers= ndb.StringProperty(repeated=True)
        following= ndb.StringProperty(repeated=True)
