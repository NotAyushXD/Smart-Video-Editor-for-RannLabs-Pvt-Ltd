# SSYX7-517BB-ODDR1-Y7W5V-ODN55
import subprocess
import requests
import random
import tkinter as tk

from tkinter import *

from tkinter import ttk
import os
from tkinter import *
import numpy as np
import sys
import pandas as pd
activate = False
def popupmsg(msg):

    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Exit", command = popup.destroy)
    B1.pack()
    # popup.mainloop()
def close():
	if activate == True:
		pass
	elif activate == False:
		
		sys.exit()

	root.destroy()

    # popup.mainloop()
def GetUUID():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid
# print(GetUUID())

def Generate_Key():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"

    # for i in range(1):
    x = ('-'.join(''.join(random.choice(seq) for _ in range(5)) for _ in range(5)))
    return x

def check_activation():
    global activate
    print(entry_1.get())
    r = requests.post("http://13.233.82.78:8000/activation/",data = {'key':entry_1.get(),'computerID':GetUUID()})
    a = (r.text)
    df = pd.DataFrame(np.array([[a[a.find('Licence'):a.find('Licence')+17], a[a.find('licence_number')+16:a.find('licence_number')+17], a[a.find('expiry_date')+14:a.find('expiry_date')+24]]]),columns=['Detail', 'Licence_number', 'Expiry_date'])
    print(a)
    # df.to_csv('./CHECK.txt', index=None, sep='\t')
    # df.to_dense().to_csv("submission.csv", index = False, sep=',', encoding='utf-8')

    # print(a[11:28])
    # try:
    #     f = open("./CHECK.txt","r+")
    #     a = f.readlines()
    #     print(a)
    # except:
    #     pass

    if a[11:28] == 'Licence Activated':
        
        print('You are allowed to use the software')
        print('Software',str(a) )
        activate = True
        # TRIGGER = True
        # if TRIGGER == True:
        #     import VideoEditor_FINAL
        popupmsg(a)

    elif a[11:28] == 'Invalid Activatio':

        activate = False
        popupmsg('Invalid Activation Key')

        
    # Licence activated &  Invalid Activatio ->  (a[11:28]) 
activation_Key = Generate_Key()

root = Tk()
root.overrideredirect(2)
root.geometry('500x500')
root.title("ACTIVATION CHECK")

label_0 = Label(root, text="ACTIVATION CHECK",width=20,font=("bold", 20))
label_0.place(x=90,y=53)


label_1 = Label(root, text="ACTIVATION KEY",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root)
entry_1.place(x=240,y=130)

label_2 = Label(root, text="Email",width=20,font=("bold", 10))
label_2.place(x=68,y=180)
closeImage1 = PhotoImage(file = './Images/close-icon.png')
closeButton = Button(root,image = closeImage1, text = "CLOSE", width = 50, height= 50)

closeButton.configure(command= close)

root.protocol("WM_DELETE_WINDOW", close)
closeButton.place(x=440,y=0)
entry_2 = Entry(root)
entry_2.place(x=240,y=180)
Button(root, text='Submit',width=20,bg='brown',fg='white', command = check_activation).place(x=180,y=380)
root.mainloop()