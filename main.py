import os
import email

from hashlib import sha1 #@UnresolvedImport
from tempfile import TemporaryFile
from zipfile import ZipFile
from zipfile import BadZipfile

from models import File
from models import Image

from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Consts():
    WRONG_URL = 'wrong_url'
    UPLOAD_ZIP = 'upload_zip'
    WRONG_ZIP = 'wrong_zip'
    
    ERRORS = { 'wrong_url' : { 'message': "This URL isn't all right" }, 
               'upload_zip' : { 'message': "You need to upload zip file" },
               'wrong_zip' : { 'message': "Zip file is not from Problem Steps Recorder" } 
               }

class WrongFileContentsError(Exception):
    pass

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, None))
        
class ErrorHandler(webapp.RequestHandler):
    def get(self, error):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, Consts.ERRORS[error]))

class UploadHandler(webapp.RequestHandler):
    def post(self):
        res = self.request.get('resolution')
        
        file = File()
        file.file_blob = db.Blob(self.request.get('file'))
        hash = sha1(file.file_blob).hexdigest()
        
        if self.images_exists(hash):
            self.redirect('/problem/%s?res=%s' % (hash, res))
            return
        
        f = TemporaryFile()
        f.write(file.file_blob)
        
        try:
            zipped_file = ZipFile(f)
            success = False
            
            if zipped_file.testzip() is None:
                for name in zipped_file.namelist():
                    if name.endswith('.mht'):
                        contents = zipped_file.read(name)
                        success = self.walk_through_message(contents, hash)
                        
            zipped_file.close()
            if success:
                self.redirect('/problem/%s?res=%s' % (hash, res))
            else:
                raise WrongFileContentsError
            
        except BadZipfile:
            self.redirect('/error/%s' % (Consts.UPLOAD_ZIP))
        except WrongFileContentsError:
            self.redirect('/error/%s' % (Consts.WRONG_ZIP))
        finally:
            f.close()
        
    def walk_through_message(self, message, hash):
        success = False
        msg = email.message_from_string(message)
        counter = 1
        for part in msg.walk():
            contentType = part.get_content_type()
            
            # for now I need only jpeg images
            if contentType == 'image/jpeg':
                image = Image()
                decoded_image = part.get_payload(decode=True)
                image.image_blob = db.Blob(decoded_image)
                image.sha1_hash = hash
                image.filenumber = counter
                image.put()
                
                counter += 1
                # if we have jpeg images in .mht file it's right file
                success = True
        
        return success
                
    def images_exists(self, hash):
        images = Image.gql("WHERE sha1_hash = :h", h = hash)
        
        for image in images:
            if image.sha1_hash == hash:
                return True
        
        return False

class ProblemHandler(webapp.RequestHandler):
    def get(self, hash):
        res = self.request.get('res')
        r = res.split('x')
        
        if len(hash) <> 40:
            self.wrong_url()
            return
        
        # The default is the empty string. 
        # Check for empty resolution string
        if res == '' or '' in r or len(r) < 2:
            self.wrong_url()
            return
        
        # check if dimensions are at least 100x100 
        if len(r[0]) < 3 or len(r[1]) < 3:
            self.wrong_url()
            return
        
        # check if dimensions are numbers at all
        try:
            int(r[0])
            int(r[1])
        except ValueError:
            self.wrong_url()
            return
        
        images = Image.gql("WHERE sha1_hash = :h ORDER BY filenumber", 
                           h = hash) # hash is only first 40 chars
        
        if images.count() == 0:
            self.wrong_url()
            return
        
        template_values = { 'images': images,
                            'hash' : hash,
                            'w' : r[0],
                            'h' : r[1]
                           }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/problem.html')
        self.response.out.write(template.render(path, template_values))
        
    def wrong_url(self):
        self.redirect('/error/%s' % (Consts.WRONG_URL))

class Img(webapp.RequestHandler):
    def get(self):
        image = db.get(self.request.get("img_id"))
        w = int(self.request.get("width"))
        h = int(self.request.get("height"))
        
        if image.image_blob:
            self.response.headers['Content-Type'] = "image/jpeg"
            resized_image = images.resize(image.image_blob, w, h)
            self.response.out.write(resized_image)

def main():
    application = webapp.WSGIApplication(
          [('/', MainHandler),
           ('/error/([^/]+)?', ErrorHandler),
           ('/img', Img),
           ('/upload', UploadHandler),
           ('/problem/([^/]+)?', ProblemHandler),
          ], debug=False)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()