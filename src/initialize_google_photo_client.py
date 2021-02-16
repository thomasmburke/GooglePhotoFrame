import logging
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set logger
logger = logging.getLogger(__name__)
srcDir = '/home/pi/Desktop/GooglePhotoFrame/src/'

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    logger.info(f"{client_secret_file}-{api_name}-{api_version}-{scopes}")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
 
    cred = None
 
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
 
    if os.path.exists(f'{srcDir}{pickle_file}'):
        with open(f'{srcDir}{pickle_file}', 'rb') as token:
            cred = pickle.load(token)
 
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()
 
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
 
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        logger.info(f"{API_SERVICE_NAME}: service created successfully")
        return service
    except Exception as e:
        logger.error(e)
    return None

def create_google_photo_service():
    API_NAME = 'photoslibrary'
    API_VERSION = 'v1'
    CLIENT_SECRET_FILE = f'{srcDir}google_photo_frame_OAuth.json'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
            'https://www.googleapis.com/auth/photoslibrary.sharing']
    
    return Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES)
