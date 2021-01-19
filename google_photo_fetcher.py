import json
import tkinter
from io import BytesIO

import requests
from PIL import Image

from initialize_google_photo_client import service

# https://learndataanalysis.org/mediaitems-resource-google-photos-api-and-python-part-3/

def response_media_items_by_filter(request_body: dict):
    try:
        response_search = service.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get('mediaItems')
        nextPageToken = response_search.get('nextPageToken')
 
        while nextPageToken:
            request_body['pageToken'] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()
 
            if not response_search.get('mediaItem') is None:
                lstMediaItems.extend(response_search.get('mediaItems'))
                nextPageToken = response_search.get('nextPageToken')
            else:
                nextPageToken = ''
        return lstMediaItems
    except Exception as e:
        print(e)
        return None


"""
search method (by album id)
"""
response_albums_list = service.albums().list().execute()
albums_list = response_albums_list.get('albums')
 
album_id = next(filter(lambda x: "GooglePhotoFrame" in x['title'], albums_list))['id']
 
request_body = {
    'albumId': album_id,
    'pageSize': 25
}

lstMediaItems = response_media_items_by_filter(request_body=request_body)

print(json.dumps(lstMediaItems, indent=4))

# for mediaItem in lstMediaItems:
#     if ('HEIC' in mediaItem['filename']):
#         url = mediaItem['baseUrl']





response = requests.get(url)
pilImage = Image.open(BytesIO(response.content))
showPIL(pilImage)
