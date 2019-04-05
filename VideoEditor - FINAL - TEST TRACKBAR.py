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

def getFrame(frame_nr):
    global video
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val,1)


def draw_grid(img, line_color=(0, 0, 0), thickness=1, type_=cv2.LINE_AA, pxstep=220):

    x = pxstep

    y = pxstep

    while x < img.shape[1]:

        cv2.line(img, (x, 0), (x, img.shape[0]), color=line_color, lineType=type_, thickness=thickness)

        x = x + pxstep 



    while y < img.shape[0]:

        cv2.line(img, (0, y), (img.shape[1], y), color=line_color, lineType=type_, thickness=thickness)

        y += pxstep



now = str(datetime.now()).replace(":","-")

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

subpathList = []


i = 0

j = 0

y_val = 545

button_pos_x = {0:30, 1: 270, 2:490}

dicti = {}

draw = False

dynamic_buttons = []
dele = ""
trig = False

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
  # try:
  file_name = filedialog.askopenfilename()
  print(file_name)
  load_videos(file_name)
  # except:
    # popupmsg('File was not able to load')

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
delImage = PhotoImage(file = './Images/recycle-bin(1).png')



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
  global nr_of_frames, playSpeed
  def show_frame():
    global draw


    if playpause == True and grids == False:
      ret, frame = cap.read()
      global nr_of_frames, playSpeed
      cv2.setTrackbarPos("frame","Video", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
      cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      img   = Image.fromarray(cv2image).resize((760, 400))
      imgtk = ImageTk.PhotoImage(image = img)
      lmain.imgtk = imgtk
      lmain.configure(image=imgtk)
      lmain.after(10, show_frame)
      cv2.createTrackbar("Frame", "Video", 0,nr_of_frames,getFrame)
      cv2.createTrackbar("Speed", "Video", playSpeed,100,setSpeed)
      # c = cap.get(cv2.CAP_PROP_POS_MSEC)
      # x = c//1000
      # m, s = divmod(x, 60)
      # h, m = divmod(m, 60)
      # print(str("%d Hours %02d Minutes %02d Seconds" % (h, m, s)))

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
        draw_grid(f)
        cv2.setMouseCallback('image',draw_circle)

        while(1):            

            cv2.imshow('image',f)

            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(f,'Press s to save image!',(10,460), font, 1,(0,0,0),1,cv2.LINE_AA)

            k = cv2.waitKey(10)

            if k == 27:                

                draw = False                

                break

            elif k == ord('s'):

                subpath = file_name.split('/')
                x = subpath[-1]
                subpath = subpath[:-1]
                subpath = '/'.join(subpath)
                subpath = subpath+"/"+"Screenshots"
                if not os.path.exists(subpath):
                    os.mkdir(subpath)
                print(subpath)
                cv2.imwrite(subpath+"/"+'Screenshot_'+x + str(ic) + '.png', f)

                cv2.putText(f,'Screenshot Saved.',(10,20), font, 0.5,(0,0,0),1,cv2.LINE_AA)

        cv2.destroyAllWindows()


    else:

        print('Pause')

  tqdm(disable=True, total=0)



  class my_app(Frame):
    def show_entry_fields():
        global dicti
        global trig
        trig = True
        global dele
        x = e1.get()
        dele = int((list(dicti.keys())[list(dicti.values()).index(x)]))
        if dele in dicti: del dicti[dele]
        # del dicti[x]
        my_app.combined_function(0,0)
        # popupmsg("The value entered is not a button")
        print("DICI",dicti)


        # dele = 

    def add_button():
      global dynamic_buttons
      global i
      global j
      global y_val
      global dicti
      i = i + 1
      global subpathList

      global s
      if len(dicti) >11:	
      	popupmsg("ERROR: Limit of buttons")
      	return 0
      s = textBox.get("1.0","end-1c")
      subpath = file_name.split('/')
      subpath = subpath[:-1]
      subpath = '/'.join(subpath)
      subpath = str(subpath +'/'+str(s))
      subpathList.append(subpath)
      if not os.path.exists(subpath):
        os.mkdir(subpath)
      newButton = Button(mainWindow, text=s, font = fontButtons, bg = white, width = 20, height= 1, command = lambda i=i: my_app.combined_function(i,i)) 

      newButton.place(x=int(button_pos_x[int((j)%3)]),y= y_val)
      dynamic_buttons.append(newButton)
      print('dynamic_buttons',dynamic_buttons)
      button_id = i
      dicti[button_id] = s
      print('In fuction',dicti)
      j+=1
      if(i % 3 == 0):
        y_val+= 65

    def __init__(self, master):
      Frame.__init__(self,master)
      self.pack()

    def combined_function(self, b_id):
      global trig
      global cont
      b_id = b_id
      # print(b_id) #Print Button ID

      if(trig == True):
        
        print("DELE",dele)
        dynamic_buttons[dele-1].destroy()

        trig = False
        return 0

        # a.values()# will get values and can iterate and try to get the position

      gd=0
      print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))

      gd = cap.get(cv2.CAP_PROP_POS_MSEC)/1000

      if gd>=3 :

        exportedvideo = importedvideo.subclip(gd-3,gd+5)  #Clip the Video

      elif gd<3 :

        exportedvideo = importedvideo.subclip(0,gd+5)  #Clip the Video

      subpath = file_name.split('/')

      subpath = subpath[:-1]

      subpath = '/'.join(subpath)

      print("DICTIONARY",dicti[b_id])

      filen =  file_name.split('/')[-1]

      filen = filen[:-4]


      c = cap.get(cv2.CAP_PROP_POS_MSEC)
      x = c//1000
      m, s = divmod(x, 60)
      h, m = divmod(m, 60)
      path = str(str(subpath)+"/"+str(dicti[b_id])+"/"+str(filen)+"_"+str(dicti[b_id])+"_"+ str("%02d Hours %02d Minutes %02d Seconds" % (h, m, s))+".mp4")
      # path = str(str(subpath)+"/"+str(dicti[b_id])+"/"+str(filen)+"_"+str(dicti[b_id])+"_"+str(now)+"_"+str(cont)+".mp4")
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
  nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

  playSpeed = 50



  print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))

  ## Play pause button

  # grid = Button(mainWindow, image = gridImage, text = "GRID THEN PLAY", font = fontButtons, bg = white, width = 50, height= 50,command = grid)

  # grid.place(x=590,y=425)

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



  w = tk.Label(mainWindow, text="Button Add")

  w.place(x=230,y=430)


  textBox=Text(mainWindow, height=1, width=15)

  textBox.place(x=200,y=452)

  app = my_app(mainWindow)

  main_button = Button(mainWindow,text="Submit",image = submitImage, command=lambda:my_app.add_button()).place(x=240,y=475)

  l1 = Label(mainWindow, text="Delete Button").place(x=510,y=430)
  e1 = Entry(mainWindow)
  e1.place(x=490,y=452)
  Button(mainWindow, text='Show', image = delImage, command=my_app.show_entry_fields).place(x=520,y=475)
mainWindow.mainloop()  #Starts GUI