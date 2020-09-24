from google.appengine.ext import ndb

class Comnts(ndb.Model):
    imageid=ndb.StringProperty(repeated=False)
    comments=ndb.StringProperty()
    user=ndb.StringProperty()
