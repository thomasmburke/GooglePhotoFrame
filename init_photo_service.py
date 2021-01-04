import os

from google_photo_ops import Create_Service

API_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = '/Users/tomburke/Downloads/google_photo_frame_OAuth.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']
 
service = Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES)          
