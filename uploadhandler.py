from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext.blobstore import BlobKey
from google.appengine.api.images import get_serving_url
from google.appengine.api import images
from datetime import datetime


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        now=datetime.now()
        x=now.strftime("%H:%M:%S")
        user= users.get_current_user()
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename
        collection_key = ndb.Key('Post', user.email())
        collection = collection_key.get()
        collection.imageinfo.append(filename)
        collection.image.append(upload.key())
        collection.caption.append(self.request.get('caption'))
        collection.imageurl.append(get_serving_url(upload.key()))
        collection.timepost.append(x)
        collection.put()
        self.redirect('/')
