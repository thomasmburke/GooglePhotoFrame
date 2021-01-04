import requests
from PIL import Image

from init_photo_service import service

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

print(lstMediaItems)

# https://stackoverflow.com/a/23489503/9586164
response = requests.get(url)
img = Image.open(response.raw)
