import logging
import tkinter
from google_photo_fetcher import *

import requests
from PIL import Image, ImageTk

# Set logger
logger = logging.getLogger(__name__)


def quit(*args):
	root.destroy()

#----------------------------------------------------------------------


class MainWindow():
    #----------------
	def __init__(self, root, service):
		self.service = service
		self.root = root
		self.albumId = get_google_photo_frame_album_id(service=service)
		self.nextPageToken = 'firstRequest'
		self.delay = 1000*5
		
		self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.root.geometry("%dx%d+0+0" % (self.w, self.h))
		self.canvas = tkinter.Canvas(root,width=self.w,height=self.h, bd=0)
		self.canvas.pack()
		self.canvas.configure(background='black')
		# images
		self.displayImage = self.get_display_image()
		
		# set first image on canvas
		self.imageOnCanvas = self.canvas.create_image(self.w/2, self.h/2, image = self.displayImage)
    #----------------
	def PILImage_to_display_image(self, PILImage):
		imgWidth, imgHeight = PILImage.size
		if imgWidth > self.w or imgHeight > self.h:
			ratio = min(self.w/imgWidth, self.h/imgHeight)
			imgWidth = int(imgWidth*ratio)
			imgHeight = int(imgHeight*ratio)
			PILImage = PILImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
		displayImage = ImageTk.PhotoImage(PILImage)
		return displayImage
		
	def get_display_image(self):
		logger.info('in get_display_image...')
		lstMediaItems, self.nextPageToken = get_next_image_url(service=self.service, albumId=self.albumId, nextPageToken=self.nextPageToken)
		imageBytes = get_image_bytes(lstMediaItems[0]['baseUrl'])
		PILImage = create_PILImage(imageBytes)
		displayImage = self.PILImage_to_display_image(PILImage)
		logger.info('setting root after delay...')
		self.root.after(self.delay, self.set_next_display_image)
		return displayImage
		
	def set_next_display_image(self):
		# change image
		self.displayImage = self.get_display_image()
		self.canvas.itemconfig(self.imageOnCanvas, image = self.displayImage)
		#self.root.after(self.delay, self.set_next_display_image)
#----------------------------------------------------------------------
