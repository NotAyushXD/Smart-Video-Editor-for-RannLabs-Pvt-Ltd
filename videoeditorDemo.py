import cv2
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from moviepy.editor import *
from tqdm import tqdm
import threading
import time
import datetime
from tkinter import filedialog
import os
from datetime import datetime

#####Added to solve %1
from moviepy.config import change_settings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
try:
    from PIL import Image
except ImportError:
    import Image

def draw_grid(img, line_color=(0, 0, 0), thickness=1, type_=cv2.LINE_AA, pxstep=220):
    x = pxstep
    y = pxstep
    while x < img.shape[1]:
        cv2.line(img, (x, 0), (x, img.shape[0]), color=line_color, lineType=type_, thickness=thickness)
        x = x + pxstep 

    while y < img.shape[0]:
        cv2.line(img, (0, y), (img.shape[1], y), color=line_color, lineType=type_, thickness=thickness)
        y += pxstep

current_milli_time = lambda: int(round(time.time() * 1000))
now = str(current_milli_time())
print (now)

tqdm(disable=True, total=0)  # initialise internal lock

####Added to solve %1
change_settings({"FFMPEG_BINARY":"ffmpeg.exe"})

white     = "#ffffff"
lightBlue2  = "#adc5ed"
font    = "Constantia"
fontButtons = (font, 12)
maxWidth    = 800
maxHeight   = 790
playpause = True
file_name = 'None'
grids = False
s = ''
cont = 0

i = 0
j = 0
y_val = 590
button_pos_x = {0:30, 1: 270, 2:490}
dicti = {}
draw = False

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Exit", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def browse_file():
  global file_name
  try:
    file_name = filedialog.askopenfilename()
    print(file_name)
    load_videos(file_name)
  except:
    popupmsg('File was not able to load')


#Graphics window
mainWindow = tk.Tk()
mainWindow.configure(bg=lightBlue2)
mainWindow.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))
mainWindow.resizable(0,0)
# mainWindow.overrideredirect(1)

mainFrame = Frame(mainWindow)
mainFrame.place(x=20, y=20)
ic = 0

browseImage = PhotoImage(file = './Images/browse1.png')
playImage = PhotoImage(file = './Images/play.png')
closeImage = PhotoImage(file = './Images/close-icon.png')
pauseImage = PhotoImage(file = './Images/pause.png')
submitImage = PhotoImage(file = './Images/Submit.png')
gridImage = PhotoImage(file = './Images/grid1.png')
drawImage = PhotoImage(file = './Images/draw.png')


browse = Button(mainWindow, image = browseImage, text = "Browse", font = fontButtons, bg = white, width = 45, height= 40, command=browse_file)
browse.place(x=370,y=425)

drawing = False # true if mouse is pressed
ix,iy = -1,-1
f = np.zeros((512,512,3), np.uint8)
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global f
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(f,(x,y),5,(0,0,255),-1)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(f,(x,y),5,(0,0,255),-1)

def load_videos(video_file):
  def show_frame():
    global draw
    if playpause == True and grids == False:
      ret, frame = cap.read()     
      cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      img   = Image.fromarray(cv2image).resize((760, 400))
      imgtk = ImageTk.PhotoImage(image = img)
      lmain.imgtk = imgtk
      lmain.configure(image=imgtk)
      lmain.after(10, show_frame)

    elif playpause == True and grids == True:
        ret, frame = cap.read()
        draw_grid(frame)
        cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img   = Image.fromarray(cv2image).resize((760, 400))
        imgtk = ImageTk.PhotoImage(image = img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

    elif draw == True:
        global f
        global ic
        ic+=1
        ret, f = cap.read()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_circle)
        while(1):
            cv2.imshow('image',f) 
            k = cv2.waitKey(10)
            if k == 27:
                cv2.imwrite('SS' + str(ic) + '.png', f)
                draw = False                
                break
        cv2.destroyAllWindows()
            
    else:
        print('Pause')


  tqdm(disable=True, total=0)
  def add_button():
    global i
    global j
    global y_val
    global dicti
    i = i + 1

    global s
    s = textBox.get("1.0","end-1c")
    subpath = file_name.split('/')
    subpath = subpath[:-1]
    subpath = '/'.join(subpath)
    subpath = str(subpath +'/'+str(s))
    if not os.path.exists(subpath):
      os.mkdir(subpath)
    newButton = Button(mainWindow, text=s, font = fontButtons, bg = white, width = 20, height= 1, command = lambda i=i: my_app.combined_function(i,i)) 
    newButton.place(x=int(button_pos_x[int((j)%3)]),y= y_val)
    button_id = i
    dicti[button_id] = s
    print('In fuction',dicti)
    j+=1

    if(i % 3 == 0):
      y_val+= 80

  class my_app(Frame):
    def __init__(self, master):
      Frame.__init__(self,master)
      self.pack()

    def combined_function(self, b_id):
      global cont
      b_id = b_id
      print(b_id) #Print Button ID

      gd=0
      print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))
      gd = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
      print(gd)
      if gd>=3 :
        exportedvideo = importedvideo.subclip(gd-3,gd+5)  #Clip the Video
      elif gd<3 :
        exportedvideo = importedvideo.subclip(0,gd+5)  #Clip the Video
      subpath = file_name.split('/')
      subpath = subpath[:-1]
      subpath = '/'.join(subpath)
      print("DICTIONARY",dicti[b_id])

      path = str(str(subpath)+"/"+str(dicti[b_id])+"/"+"editted_test_"+str(dicti[b_id])+now+"_"+str(cont)+"_.mp4")
      exportedvideo.write_videofile(path,fps=25) # Final Result on the video
      cont +=1

  def play():
    global playpause
    playpause = True
    show_frame()

  def grid():
    global grids
    grids = True
    global playpause
    playpause = False
    show_frame()

  def draw():
      global playpause
      global draw
      playpause = False
      draw = True
      show_frame()

  def pause():
    global playpause
    playpause = False
  #Capture video frames

  lmain = tk.Label(mainFrame)
  lmain.grid(row=0, column=0)

  importedvideo = VideoFileClip(file_name)  #Video Imported to System

  cap = cv2.VideoCapture(file_name)

  print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))
  ## Play pause button
  grid = Button(mainWindow, image = gridImage, text = "GRID THEN PLAY", font = fontButtons, bg = white, width = 50, height= 50,command = grid)
  grid.place(x=590,y=425)
  grid = Button(mainWindow,image = drawImage, text = "DRAW", font = fontButtons, bg = white, width = 50, height= 50,command = draw)
  grid.place(x=695,y=425)

  play = Button(mainWindow,image = playImage ,text = "PLAY", font = fontButtons, bg = white, width = 50, height= 50, command=play)
  play.place(x=20,y=425)

  closeButton = Button(mainWindow, image = closeImage, text = "CLOSE", font = fontButtons, bg = white, width = 50, height= 50)
  closeButton.configure(command= lambda: mainWindow.destroy())
  closeButton.place(x=745,y=0)

  pause = Button(mainWindow, image = pauseImage, text = "PAUSE", font = fontButtons, bg = white, width = 50, height= 50, command=pause)
  pause.place(x=120,y=425)

  show_frame()  #Display

  w = tk.Label(mainWindow, text="Enter the Name of Button !")
  w.place(x=330,y=480)

  textBox=Text(mainWindow, height=1, width=15)
  textBox.place(x=340,y=502)
  app = my_app(mainWindow)

  main_button = Button(mainWindow,text="Submit",image = submitImage, command=lambda:add_button()).place(x=370,y=525)

mainWindow.mainloop()  #Starts GUI
