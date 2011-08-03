from google.appengine.ext import db

"""Helper db.Model class only"""
class File(db.Model):
    file_blob = db.BlobProperty()

"""db.Model class for storing images from .mht files"""
class Image(db.Model):
    sha1_hash = db.StringProperty()
    filenumber = db.IntegerProperty()
    image_blob = db.BlobProperty()