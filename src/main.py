from time import sleep

from google_photo_fetcher import *
from tkinter_ops import *

# Set default logging level
logging.basicConfig(
    handlers=[RotatingFileHandler('GooglePhotoFrame.log', maxBytes=5000, backupCount=0)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S')

# Initialize Google Photo Service
service = create_google_photo_service()
# Get the GooglePhotoFrame Album ID
albumId = get_google_photo_frame_album_id(service=service)
nextPageToken='firstRequest'
while True:
    # Get the first batch of images
    lstMediaItems, nextPageToken = get_next_image_url(service=service, albumId=albumId, nextPageToken=nextPageToken)
    logger.info("sleeping for 3 seconds...")
    sleep(3)

# Create slideshow of photos
