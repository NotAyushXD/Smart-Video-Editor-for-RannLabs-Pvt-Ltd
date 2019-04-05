import vlc
import sys
import math
from tkinter import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
import os
import pathlib
from threading import Thread, Event
import time
import platform

def maximum(a,b):
    if(a>=b):
        return a
    else:
        return b
    
def mspf(mp):
    return mp.get_fps()

class ttkTimer(Thread):
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0
    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += self.tick
            self.callback()
    def stop(self):
        self.stopFlag.set()
    def get(self):
        return self.iters

    
global index
index=0
class Player(Tk.Frame):
    def __init__(self, parent, title=None):
        global index
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        if title == None:
            title = "tk_vlc"
        self.parent.title(title)
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
        fileMenu.add_command(label="Exit", underline=1, command=_quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        ctrlpanel = ttk.Frame(self.parent)
        
        ctrlpanel3 = ttk.Frame(self.parent)
        
        pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
        saveVideo  = ttk.Button(ctrlpanel, text="Save Video", command=self.saveVideo)
        plus5  = ttk.Button(ctrlpanel, text="plus5", command=self.plus5)
        minus5  = ttk.Button(ctrlpanel, text="minus5", command=self.minus5)
        play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
        stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
        
        global filename_store,directory_store
        global string1,string2,string3,string4,string5
        global btn1,text_button1
        string1=""
        string2=""
        string3=""
        string4=""
        string5=""
        ctrlpanel2 = ttk.Frame(self.parent)
        textBox=Text(ctrlpanel, height=1, width=10)
        textBox.pack()
        
        text_button1=Button(ctrlpanel2,height=1, width=5, text="ADD 1", command=lambda:[self.set_string(textBox.get("1.0","end-1c"),1),btn1.configure(text=string1,state=NORMAL)])
        text_button1.pack(side="left")
        btn1=ttk.Button(ctrlpanel3,text="btn1",command=lambda:[self.click_event(string1)])
        btn1.configure(state=DISABLED)
        btn1.pack(side="left")
        
        #side="top", fill='both', expand=True, padx=4, pady=4
        
        text_button2=Button(ctrlpanel2, height=1, width=5, text="ADD 2", command=lambda:[self.set_string(textBox.get("1.0","end-1c"),2),btn2.configure(text=string2,state=NORMAL)])
        text_button2.pack(side="left")
        btn2=ttk.Button(ctrlpanel3,text="btn2",command=lambda:[print(btn2['text'])])
        btn2.configure(state=DISABLED)
        btn2.pack(side="left")
        
        text_button3=Button(ctrlpanel2, height=1, width=5, text="ADD 3", command=lambda:[self.set_string(textBox.get("1.0","end-1c"),3),btn3.configure(text=string3,state=NORMAL)])
        text_button3.pack(side="left")
        btn3=ttk.Button(ctrlpanel3,text="btn3",command=lambda:[self.click_event(string3)])
        btn3.configure(state=DISABLED)
        btn3.pack(side="left")
        
        
        ###new = ttk.Button(ctrlpanel,text="changebtns",command = lambda c=len(button_list) : [button_list.append(1),print(button_list),print(c)])
        
        #new = ttk.Button(ctrlpanel,text="changebtns",command=lambda:[i=ttk.Button(ctrlpanel,text=textBox.get("1.0","end-1c"),command=lambda:[print(i['text'])]).pack()])

        #new = ttk.Button(ctrlpanel,text="changebtns",command = : [self.create_button])
        
        
        pause.pack(side=Tk.LEFT)
        saveVideo.pack(side=Tk.LEFT)
        plus5.pack(side=Tk.LEFT)
        minus5.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
       
        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        self.volslider.pack(side=Tk.LEFT)
        ctrlpanel.pack(side=Tk.BOTTOM)
        ctrlpanel3.pack(side=Tk.BOTTOM)
        
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel, variable=self.scale_var, command=self.scale_sel,from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        self.timeslider_last_update = time.time()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)
        # self.Instance = vlc.Instance()
        # self.player = self.Instance.media_player_new()
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()
    
    def click_event(self,text):
        print('file saved to: ',text)
        
    def set_string(self,text,number):
        global string1,string2,string3,string4,string5
        if(number==1):
            string1=text
        elif(number==2):
            string2=text
        elif(number==3):
            string3=text
        elif(number==4):
            string4=text
        elif(number==5):
            string5=text

    def OnExit(self, evt):
        self.Close()

    def OnOpen(self):
        global filename_store,directory_store
        self.OnStop()
        p = pathlib.Path(os.path.expanduser("~"))
        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        if os.path.isfile(fullname):
            dirname  = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            print(dirname)
            print(filename)
            filename_store=str(dirname)+'/'+str(filename)
            directory_store=str(dirname)
            print(filename)
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle())
            self.OnPlay()
            self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        if not self.player.get_media():
            self.OnOpen()
        else:
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def plus5(self):
        global index
        print('index : ' ,index)
        self.player.pause()
        new_time = 25*5 * mspf(self.player)
        self.player.set_time(math.ceil(self.player.get_time()+new_time))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        
    def minus5(self):
        self.player.pause()
        new_time = 25*6 * mspf(self.player)
        self.player.set_time(maximum(0,math.floor(self.player.get_time()-new_time)))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        
    def saveVideo(self):
        global filename_store,directory_store
        tyme = self.player.get_time()
        tyme=tyme*0.001
        ffmpeg_extract_subclip(filename_store,tyme,tyme+5, targetname=directory_store+"/sss.mp4")
        print('video saved')

    def OnPause(self):
        global filename_store
        print(filename_store)
        self.player.pause()

    def OnStop(self):
        self.player.stop()
        self.timeslider.set(0+100)

    def OnTimer(self):
        #global filename_store
        global index
    
        if self.player == None:
            return
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        print('player length : ',dbl)
        #print(filename_store)
        
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def OnToggleVolume(self, evt):
        is_mute = self.player.audio_get_mute()
        self.player.audio_set_mute(not is_mute)
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        Tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):
        Tk_get_root.root= Tk.Tk()
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()    
    root.destroy()
    os._exit(1)

if __name__ == "__main__":
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)
    player = Player(root, title="tkinter vlc")
    root.mainloop()