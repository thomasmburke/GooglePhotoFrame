import json
import logging
import tkinter
from io import BytesIO
from logging.handlers import RotatingFileHandler

import requests
from PIL import Image

from initialize_google_photo_client import create_google_photo_service

# https://learndataanalysis.org/mediaitems-resource-google-photos-api-and-python-part-3/

# Set logger
logger = logging.getLogger(__name__)

def response_media_items_by_filter(request_body: dict, service):
    try:
        response_search = service.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get('mediaItems')
        nextPageToken = response_search.get('nextPageToken')
        logger.info(f"nextPageToken: {nextPageToken}")
 
        while nextPageToken:
            request_body['pageToken'] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()
 
            if not response_search.get('mediaItems') is None:
                lstMediaItems.extend(response_search.get('mediaItems'))
                nextPageToken = response_search.get('nextPageToken')
                logger.info(f"nextPageToken: {nextPageToken}")
            else:
                logger.info(f"no next page: {json.dumps(response_search, indent=4)}")
                nextPageToken = ''
        return lstMediaItems
    except Exception as e:
        logger.error(e)
        return None

def get_next_image_url(service, albumId):
    request_body = {
        'albumId': albumId,
        'pageSize': 1
    }
    lstMediaItems = response_media_items_by_filter(request_body=request_body, service=service)
    logger.info(json.dumps(lstMediaItems, indent=4))
    return lstMediaItems

def get_google_photo_frame_album_id(service):
    response_albums_list = service.albums().list().execute()
    albums_list = response_albums_list.get('albums')
    albumId = next(filter(lambda x: "GooglePhotoFrame" in x['title'], albums_list))['id']
    logger.info(f"GooglePhotoFrame albumId: {albumId}")
    return albumId


if __name__=='__main__':
    # Set default logging level
    logging.basicConfig(
        handlers=[RotatingFileHandler('GooglePhotoFrame.log', maxBytes=5000, backupCount=0)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

    service = create_google_photo_service()
    albumId = get_google_photo_frame_album_id(service=service)
    lstMediaItems = get_next_image_url(service=service, albumId=albumId)
    

    # for mediaItem in lstMediaItems:
    #     if ('HEIC' in mediaItem['filename']):
    #         url = mediaItem['baseUrl']

    # response = requests.get(url)
    # pilImage = Image.open(BytesIO(response.content))
    # showPIL(pilImage)

