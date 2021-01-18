from io import BytesIO
import json

import requests
from PIL import Image, ImageTk

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

print(json.dumps(lstMediaItems, indent=4))

# https://stackoverflow.com/a/23489503/9586164
# response = requests.get(url)
# img = Image.open(response.raw)
for mediaItem in lstMediaItems:
    if ('JPG' in mediaItem['filename']):
        url = mediaItem['baseUrl']

# img = Image.open(BytesIO(response.content))

import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()


response = requests.get(url)
pilImage = Image.open(BytesIO(response.content))
showPIL(pilImage)
