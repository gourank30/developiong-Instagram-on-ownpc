from google.appengine.ext import ndb

class Post(ndb.Model):
    caption=ndb.StringProperty(repeated=True)
    imageinfo=ndb.StringProperty(repeated=True)
    image = ndb.BlobKeyProperty(repeated=True)
    imageurl=ndb.StringProperty(repeated=True)
    timepost=ndb.StringProperty(repeated=True)
