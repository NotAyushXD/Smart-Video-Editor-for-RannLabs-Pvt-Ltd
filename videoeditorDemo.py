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
#####Added to solve %1
from moviepy.config import change_settings

now = time.strftime("%Y%m%d-%H%M%S")
print (now)

tqdm(disable=True, total=0)  # initialise internal lock

#####Added to solve %1
change_settings({"FFMPEG_BINARY":"ffmpeg.exe"})

white     = "#ffffff"
lightBlue2  = "#adc5ed"
font    = "Constantia"
fontButtons = (font, 12)
maxWidth    = 800
maxHeight   = 1000
playpause = True
file_name = 'None'
s = ''

i = 0
j = 0

y_val = 650
button_pos_x = {0:30, 1: 270, 2:490}
dicti = {}


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

# def SpeedUp():
#   cap.set(cv2.CAP_PROP_FPS, 60)

#Graphics window
mainWindow = tk.Tk()
mainWindow.configure(bg=lightBlue2)
mainWindow.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))
mainWindow.resizable(0,0)
# mainWindow.overrideredirect(1)

mainFrame = Frame(mainWindow)
mainFrame.place(x=20, y=20)

browse = Button(mainWindow, text = "Browse", font = fontButtons, bg = white, width = 20, height= 1, command=browse_file)
browse.place(x=300,y=400)


def load_videos(video_file):
  def show_frame():
    if playpause == True:
      ret, frame = cap.read()
      cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      img   = Image.fromarray(cv2image).resize((760, 400))
      imgtk = ImageTk.PhotoImage(image = img)
      lmain.imgtk = imgtk
      lmain.configure(image=imgtk)
      lmain.after(10, show_frame)
      
    else:
      print('Pause')

  tqdm(disable=True, total=0)
  class my_app(Frame):

    def __init__(self, master):
      Frame.__init__(self,master)
      self.grid()
    
    def combined_function(self, b_id): #This is one of the areas where I need help. I want this to return the number of the button clicked.

      self.b_id = b_id
      print( self.b_id) #Print Button ID
      
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
      path = str(str(subpath)+"/"+str(dicti[b_id])+"/"+"editted_test_"+str(s)+now+"_.mp4")
      exportedvideo.write_videofile(path,fps=25) # Final Result on the video


    def add_button(self):
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

      self.newButton = Button(self, text=s, font = fontButtons, bg = white, width = 20, height= 1, command = lambda i=i: self.combined_function(i)) 

      self.newButton.pack()
      button_id = i
      dicti[button_id] = s
      print('In fuction',dicti)
      j+=1

      if(i % 3 == 0):
        y_val+= 100

  
  # def TrimVideo():
  #     gd=0
  #     print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))
  #     gd = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
  #     print(gd)
  #     if gd>=3 :
  #       exportedvideo = importedvideo.subclip(gd-3,gd+5)  #Clip the Video
  #     elif gd<3 :
  #       exportedvideo = importedvideo.subclip(0,gd+5)  #Clip the Video
  #     subpath = file_name.split('/')
  #     subpath = subpath[:-1]
  #     subpath = '/'.join(subpath)
  #     path = str(str(subpath)+"/"+s+"/"+"editted_test_"+str(s)+now+"_.mp4")
  #     exportedvideo.write_videofile(path,fps=25) # Final Result on the video

  # tqdm(disable=True, total=0)

  def play():
    global playpause
    playpause = True
    show_frame()

  def pause():
    global playpause
    playpause = False
  #Capture video frames

  # def add_button():
  #   global i
  #   global j
  #   global y_val
  #   i = i + 1
  #   global s
  #   s = textBox.get("1.0","end-1c")

  #   subpath = file_name.split('/')
  #   subpath = subpath[:-1]
  #   subpath = '/'.join(subpath)
  #   subpath = str(subpath +'/'+str(s))
  #   if not os.path.exists(subpath):
  #     os.mkdir(subpath)

  #   newButton = Button(mainWindow, text=s, font = fontButtons, bg = white, width = 20, height= 1, command=TrimVideo)
  #   newButton.place(x=int(button_pos_x[int((j)%3)]),y= y_val)
  #   j+=1

  #   if(i % 3 == 0):
  #       y_val+= 100

  lmain = tk.Label(mainFrame)
  lmain.grid(row=0, column=0)

  importedvideo = VideoFileClip(file_name)  #Video Imported to System

  cap = cv2.VideoCapture(file_name)

  print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))

  ## Play pause button
  play = Button(mainWindow, text = "PLAY", font = fontButtons, bg = white, width = 20, height= 1, command=play)
  play.place(x=490,y=480)
  closeButton = Button(mainWindow, text = "CLOSE", font = fontButtons, bg = white, width = 20, height= 1)
  closeButton.configure(command= lambda: mainWindow.destroy())
  closeButton.place(x=270,y=480)
  pause = Button(mainWindow, text = "PAUSE", font = fontButtons, bg = white, width = 20, height= 1, command=pause)
  pause.place(x=30,y=480)
  show_frame()  #Display
  w = tk.Label(mainWindow, text="Enter the Name of Button !")
  w.place(x=330,y=530)


  textBox=Text(mainWindow, height=1, width=10)
  textBox.place(x=350,y=550)

  app = my_app(mainWindow)
  main_button = Button(mainWindow,text="Submit",command=lambda:app.add_button()).place(x=370,y=580)

mainWindow.mainloop()  #Starts GUI