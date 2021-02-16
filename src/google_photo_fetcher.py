import json
import logging
import tkinter
from io import BytesIO
from logging.handlers import RotatingFileHandler

import requests
from PIL import Image
from time import sleep
import random

from initialize_google_photo_client import create_google_photo_service

# https://learndataanalysis.org/mediaitems-resource-google-photos-api-and-python-part-3/

# Set logger
logger = logging.getLogger(__name__)

def get_next_image_url(service, albumId, nextPageToken='firstRequest'):
    request_body = {
        'albumId': albumId,
        'pageSize': 1
    }
    # Exponential backoff Retry Logic
    n = 0
    while n < 13:
        try:
            if (nextPageToken and nextPageToken != 'firstRequest'):
                request_body['pageToken'] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()
            lstMediaItems = response_search.get('mediaItems')
            nextPageToken = response_search.get('nextPageToken', '')
            logger.info(json.dumps(lstMediaItems, indent=4))
            logger.info(f"nextPageToken: {nextPageToken}")
            return [lstMediaItems, nextPageToken]
        except Exception as e:
            logger.error(e)
            n += 1
            sleepTime = 2**n + random.random()
            if n < 12:
                logger.warning(f'retrying after exponential backoff of {sleepTime} seconds')
                sleep(sleepTime)
            else:
                logger.error('API call to Google Photos Failed several times even with exponential backoff retry logic')

def get_google_photo_frame_album_id(service):
    response_albums_list = service.albums().list().execute()
    albums_list = response_albums_list.get('albums')
    albumId = next(filter(lambda x: "GooglePhotoFrame" in x['title'], albums_list))['id']
    logger.info(f"GooglePhotoFrame albumId: {albumId}")
    return albumId
    
def get_image_bytes(url):
	logger.info('Making request for image...')
	response = requests.get(url)
	logger.info('Returning bytes of image received...')
	return response.content
	
def create_PILImage(imageBytes):
	logger.info('Turning image bytes into PILImage...')
	pilImage = Image.open(BytesIO(imageBytes))
	return pilImage


if __name__=='__main__':
    # Set default logging level
    logging.basicConfig(
        handlers=[RotatingFileHandler('GooglePhotoFrame.log', maxBytes=5000, backupCount=0)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

    service = create_google_photo_service()
    albumId = get_google_photo_frame_album_id(service=service)
    lstMediaItems, nextPageToken = get_next_image_url(service=service, albumId=albumId)
    

    # for mediaItem in lstMediaItems:
    #     if ('HEIC' in mediaItem['filename']):
    #         url = mediaItem['baseUrl']

    # response = requests.get(url)
    # pilImage = Image.open(BytesIO(response.content))
    # showPIL(pilImage)

