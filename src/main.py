from time import sleep
import tkinter

from google_photo_fetcher import *
from tkinter_ops import *

# Set logger
logger = logging.getLogger(__name__)

# Set default logging level
logging.basicConfig(
    handlers=[RotatingFileHandler('GooglePhotoFrame.log', maxBytes=5000, backupCount=0)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S')
    
root = tkinter.Tk()
root.overrideredirect(1)
# root.geometry("%dx%d+0+0" % (w, h))
root.bind("<Escape>", quit)
root.bind("x", quit)
# Initialize Google Photo Service
service = create_google_photo_service()
MainWindow(root, service)
root.mainloop()


