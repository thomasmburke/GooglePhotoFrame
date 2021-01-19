import tkinter

from PIL import Image, ImageTk


def quit(*args):
    root.destroy()

def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    # root.focus_set()    
    root.bind("<Escape>", quit)
    root.bind("x", quit)
    canvas = tkinter.Canvas(root,width=w,height=h, bd=0)
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
