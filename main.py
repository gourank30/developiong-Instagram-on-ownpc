import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from uploadhandler import UploadHandler
from google.appengine.ext.blobstore import BlobKey
from google.appengine.api.images import get_serving_url
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
import os
from myuser import MyUser
from post import Post
from comnts import Comnts

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'text/html'
            url = ''
            url_string = ''
            myuser=''
            user =''
            welcome = 'Welcome back'
            user= users.get_current_user()
            po=[]
            capt=[]
            im=[]
            cap=[]
            im1=[]
            cap1=[]
            alpo=0
            if user:
                user= users.get_current_user()
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'
                myuser_key = ndb.Key('MyUser', user.email())
                myuser = myuser_key.get()
                if myuser == None:
                    welcome = 'Welcome to the application'
                    myuser = MyUser(id=user.email())
                    myuser.email_address=user.email()
                    myuser.put()
                myuser_key2 = ndb.Key('MyUser', user.email()).get()
                im=myuser_key2.following
                if myuser_key2.following==None:
                    for i in myuser_key2.following:
                        im.append(i)
                im.append(user.email())
                df=[]
                for j in im:
                    ca=ndb.Key('Post', j).get()
                    if ca!=None:
                         for i in range(0,len(ca.timepost)):
                             df.append(ca.timepost[i])
                df.sort(reverse=True)
                for i in range(0,len(df)):
                    f=0
                    for k in range(0,len(im)):
                        if f==0:
                            fg=ndb.Key('Post',im[k]).get()
                            if fg!=None:
                                for j in range(0,len(fg.timepost)):
                                    if fg.timepost[j]==df[i]:
                                        im1.append(fg.imageurl[j])
                                        cap1.append(fg.caption[j])
                                        f=1
                                        break
                        else:
                            break
                po=im1
                capt=cap1
                po.sort(reverse=True)
                capt.sort(reverse=True)
                if len(po)<50:
                    alpo=len(po)
                else:
                    alpo=50
            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            template_values = {
            'alpo':alpo,
            'po':po,
            'capt':capt,
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
        }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

class postimg(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user()
        collection_key = ndb.Key('Post', user.email())
        collection = collection_key.get()
        if collection == None:
            collection = Post(id=user.email())
            collection.put()
        template_values = {
        'collection' : collection,
        'upload_url' : blobstore.create_upload_url('/upload'),
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

class disppostown(webapp2.RequestHandler):
    def get(self):
        count1=0
        count2=0
        im=[]
        cap=[]
        noofp=0
        user= users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser=myuser_key.get()
        fol=myuser.followers
        fow=myuser.following
        for i in fol:
            count1=count1+1
        for i in fow:
            count2=count2+1
        collection_key = ndb.Key('Post', user.email()).get()
        if collection_key==None:
            self.response.write("no post made till now")
        else:
            im=collection_key.imageurl
            cap=collection_key.caption
            im.sort(reverse=True)
            cap.sort(reverse=True)
            for i in cap:
                noofp=noofp+1
        template_values = {
        'user':user,
        'count1':count1,
        'count2':count2,
        'im':im,
        'cap':cap,
        'noofp':noofp
        }
        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(template_values))

class seruse(webapp2.RequestHandler):
    def get(self):
        x=''
        if self.request.get('submit'):
            use=self.request.get('use')
            if use=='':
                x=MyUser.query()
            else:
                n=list(MyUser.query().filter(MyUser.email_address==self.request.get('use')).fetch(keys_only=True))
                if n==None:
                    self.response.write('No user found')
                else:
                    x=ndb.get_multi(n)
        template_values = {
        'use':self.request.get('use'),
        'x':x
        }
        template = JINJA_ENVIRONMENT.get_template('searchpage.html')
        self.response.write(template.render(template_values))

class prof(webapp2.RequestHandler):
    def get(self):
        use=self.request.get('use')
        user= users.get_current_user()
        if use==user.email():
            self.redirect('/disppostown')

        count1=0
        count2=0
        im=[]
        cap=[]
        noofp=0
        followings=''
        mykey=ndb.Key('MyUser',user.email()).get()
        x=mykey.following
        if use in x:
            followings='following'

        myuser_key = ndb.Key('MyUser', use)
        myuser=myuser_key.get()
        fol=myuser.followers
        fow=myuser.following
        for i in fol:
            count1=count1+1
        for i in fow:
            count2=count2+1
        collection_key = ndb.Key('Post', use).get()
        if collection_key==None:
            self.response.write('no upload made till now')
        else:
            im=collection_key.imageurl
            cap=collection_key.caption

            im.sort(reverse=True)
            cap.sort(reverse=True)
            for i in im:
                noofp=noofp+1
        template_values = {
            'followings':followings,
            'use':self.request.get('use'),
            'count1':count1,
            'count2':count2,
            'im':im,
            'cap':cap,
            'noofp':noofp
        }
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))
class flowuser(webapp2.RequestHandler):
    def get(self):

        user= users.get_current_user()
        use=self.request.get('use')
        mykey=ndb.Key('MyUser',user.email()).get()
        mykey.following.append(use)
        mykey.put()
        mykey1=ndb.Key('MyUser',use).get()
        mykey1.followers.append(user.email())
        mykey1.put()
        self.response.out.write(""" </html>
        <!DOCTYPE html>
        <html lang="en" dir="ltr">
          <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
            <meta charset="utf-8">
            <title></title>
          </head>
          <body style="text-align:center;">
          <div class="container p-3 my-3 bg-dark text-white">
            <h1><b>You are now following the user</b> </h1>
            <h6 style="color:red;">Note: Plese refresh the window after going back</h6>
            <input type="button" class="button buttonS" value="Back" onclick="history.back()"><br><br>
         </div </body>
        </html>""")


class unflowuser(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user()
        use=self.request.get('use')
        mykey=ndb.Key('MyUser',user.email()).get()
        mykey.following.remove(self.request.get('use'))
        mykey.put()
        mykey1=ndb.Key('MyUser',self.request.get('use')).get()
        mykey1.followers.remove(user.email())
        mykey1.put()
        self.response.out.write(""" </html>
        <!DOCTYPE html>
        <html lang="en" dir="ltr">
          <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>

            <meta charset="utf-8">
            <title></title>
          </head>
          <body style="text-align:center;">
          <div class="container p-3 my-3 bg-dark text-white">
            <h1><b>You are now not following the user</b> </h1>
            <h6 style="color:red;">Note: Plese refresh the window after going back</h6>
            <input type="button" class="button buttonS" value="Back" onclick="history.back()"><br><br>
            </div>
          </body>
        </html>""")


class viewflo(webapp2.RequestHandler):
    def get(self):
        li=[]
        le=0
        user= users.get_current_user()
        mykey=ndb.Key('MyUser',user.email()).get()
        flo=mykey.followers

        if flo==None:
            self.response.write('user have no flowuser')
        else:
            for i in flo:
                mykey=ndb.Key('MyUser',i).get()
                li.append(mykey.email_address)

            le=len(li)
        template_values={
        'li':li,
        'le':le
        }
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))
class viewing(webapp2.RequestHandler):
    def get(self):
        li=[]
        le=0
        user= users.get_current_user()
        mykey=ndb.Key('MyUser',user.email()).get()
        flo=mykey.following

        if flo==None:
            self.response.write('user have no flowuser')
        else:
            for i in flo:
                mykey=ndb.Key('MyUser',i).get()
                li.append(mykey.email_address)

            le=len(li)
        template_values={
        'li':li,
        'le':le
        }
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))

class viewflo1(webapp2.RequestHandler):
    def get(self):
        li=[]
        le=0
        use=self.request.get('use')

        mykey=ndb.Key('MyUser',use).get()
        flo=mykey.followers

        if flo==None:
            self.response.write('user have no flowuser')
        else:
            for i in flo:
                mykey=ndb.Key('MyUser',i).get()
                li.append(mykey.email_address)

        le=len(li)
        template_values={
        'use':self.request.get('use'),
        'li':li,
        'le':le
        }
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))

class viewing1(webapp2.RequestHandler):
    def get(self):
        li=[]
        le=0;

        use=self.request.get('use')
        mykey=ndb.Key('MyUser',use).get()
        flo=mykey.following
        if flo==None:
            self.response.write('user have no flowuser')
        else:
            for i in flo:
                mykey=ndb.Key('MyUser',i).get()
                li.append(mykey.email_address)
            le=len(li)
        template_values={
        'use':self.request.get('use'),
        'li':li,
        'le':le
        }
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))
class postcomnts(webapp2.RequestHandler):
    def get(self):
        allcom=[]
        lengthofc=0
        lengthofc1=0
        po=self.request.get('po')
        n=list(Comnts.query().filter(Comnts.imageid==self.request.get('po')).fetch(keys_only=True))
        allcom=ndb.get_multi(n)
        allcom.sort(reverse=True)
        if len(allcom)<5:
            lengthofc=len(allcom)
        else:
            lengthofc=5
        if len(allcom)<10:
            lengthofc1=len(allcom)
        else:
            lengthofc1=10
        template_values={
        'lengthofc1':lengthofc1,
        'lengthofc':lengthofc,
        'allcom':allcom,
        'po':self.request.get('po')
        }
        template = JINJA_ENVIRONMENT.get_template('addcomnt.html')
        self.response.write(template.render(template_values))
class viewcoments(webapp2.RequestHandler):
    def get(self):
        allcom=[]
        lengthofc=0
        lengthofc1
        n=list(Comnts.query().filter(Comnts.imageid==self.request.get('im')).fetch(keys_only=True))
        allcom=ndb.get_multi(n)
        allcom.sort(reverse=True)
        if len(allcom)<5:
            lengthofc=len(allcom)
        else:
            lengthofc=5
        if len(allcom)<10:
            lengthofc1=len(allcom)
        else:
            lengthofc1=10
        template_values={
        'lengthofc1':lengthofc1,
        'lengthofc':lengthofc,
        'allcom':allcom,
        'im':self.request.get('im')
        }
        template = JINJA_ENVIRONMENT.get_template('coment2.html')
        self.response.write(template.render(template_values))
class viewcoments(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user()
        img=self.request.get('img')
        if self.request.get('submit'):
            c=Comnts()
            c.imageid=img
            c.comments=self.request.get('comments')
            c.user=user.email()
            c.put()
            self.response.out.write("comenting done")
        template_values={
        'img':self.request.get('img')
        }
        template = JINJA_ENVIRONMENT.get_template('addomentpage.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([ ('/', MainPage),('/viewcoments',viewcoments),('/viewcoments',viewcoments),('/postimg',postimg),('/upload', UploadHandler),('/disppostown',disppostown),('/seruse',seruse),('/prof',prof),('/flowuser',flowuser),('/unflowuser',unflowuser),('/viewflo',viewflo),('/viewflo1',viewflo1),('/viewing1',viewing1),('/viewing',viewing),('/postcomnts',postcomnts)], debug=True)
