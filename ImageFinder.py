import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import path
from PIL import ImageTk, Image
from tkinter import messagebox as mBox 
from im2txt import run_inference
import pandas as pd
from pandas import DataFrame
import csv

# Functions ------------------------------------------
captions = []    
# End Functions --------------------------------------

win = tk.Tk()
win.title("Image Finder")

tabControl = ttk.Notebook(win)

# Tab Control ----------------------------------------
uploadTab= ttk.Frame(tabControl)
tabControl.add(uploadTab, text='Upload')
tabControl.pack(expand=1, fill="both")
searchTab = ttk.Frame(tabControl)
tabControl.add(searchTab, text='Search')
tabControl.pack(expand=1, fill="both")
# End Tab Control ------------------------------------

# Upload Tab Frame -----------------------------------
def OpenFile():
    dirname = filedialog.askdirectory(initialdir="~/Desktop/", title="Select Directory")
    chosenDir.configure(text='Uploading pictures from: \"'+dirname+"\"")
    dict_list = {}
    for file in os.listdir(dirname):
        if file.endswith(".jpg") or file.endswith("jpeg"):
	    filename = dirname + "/" + file
	    caption_info = run_inference.run_inference(filename)
	    info = caption_info[filename]
	    print(info)
	    # data = { info[0] : filename  }
	    dict_list[info[0]] = filename
	    uploadListBox.insert(tk.END, filename)
	    win.update()

    df = pd.DataFrame(list(dict_list.items()), columns=['Captions', 'Filenames'])
    df.to_csv('data.csv', index = False)

uploadFrame = ttk.LabelFrame(uploadTab, text="Upload an Image")
uploadFrame.grid(column=0, row=0, padx=8, pady=4)

ttk.Label(uploadFrame, text="Select directory to upload pictures:", width=50).grid(column=0, row=0, padx=8, pady=4, sticky='W')
ttk.Button(uploadFrame, text="Open", command=OpenFile).grid(column=0, row=1,padx=8, pady=4, sticky="W")
chosenDir = ttk.Label(uploadFrame, text="Uploading pictures from:", width=50)
chosenDir.grid(column=0, row=2, padx=8, pady=4, sticky="W")

ttk.Label(uploadFrame, text="Files uploaded:", width=50).grid(row=3)
uploadListBox = tk.Listbox(uploadFrame, width=50)

uploadListBox.grid(row=4, padx=8, pady=4, sticky="W")
# End Upload Tab Frame ------------------------------

# Search Tab Frame -----------------------------------
def FindImage():
    df = pd.read_csv('data.csv')
    found_df = (df[(df['Captions'].str.contains(descEntry.get()))])
    found_dict = found_df.set_index('Captions').T.to_dict('string')
    searchListbox.delete(0, tk.END)
    for key in found_dict:
    	searchListbox.insert(tk.END, key)

searchFrame = ttk.LabelFrame(searchTab, text="Search an Image")
searchFrame.grid(column=0, row=0, padx=8, pady=4)

def ShowImage(evt):
    w = evt.widget
    df = pd.read_csv('data.csv')
    #full_dict = df.set_index('Captions').T.to_dict('string')
    #file = file.drop(file.rows[[0]], axis=1) #Removing first column with index numbers
    #full_dict = file.to_dict()
    full_dict = dict(zip(list(df.Captions), list(df.Filenames)))
    print(full_dict)
    print("=========================")
    caption = w.get(w.curselection())
    print('caption: ', caption)
    print("=========================")
    print(w.curselection()[0])
    print('filename: ', full_dict[caption])
    path = full_dict[caption]
    im = Image.open(path)
    tkimage = ImageTk.PhotoImage(im)
    foundImage.image=tkimage
    foundImage.configure(image=tkimage)

ttk.Label(searchFrame, text="Results Found:").grid(column=0, row=3, padx=8, pady=4, sticky="W")
searchListbox = tk.Listbox(searchFrame, selectmode=tk.SINGLE, width=50)
searchListbox.grid(column=0, row=4, padx=8, pady=4, sticky="W")
searchListbox.bind('<<ListboxSelect>>', ShowImage)
foundImage = ttk.Label(searchFrame, width=50)
foundImage.grid(column=0, row=5, padx=8, pady=4, sticky="W")

ttk.Label(searchFrame, text="Enter a keyword that describes the image you want find:").grid(column=0, row=0, padx=8, pady=4, sticky='W')
description = tk.StringVar()
descEntry = ttk.Entry(searchFrame, width=50, textvariable=description)
descEntry.grid(column=0, row=1, padx=8, pady=4, sticky="W")
descEntry.focus()
ttk.Button(searchFrame, text="Search", command=FindImage).grid(column=0, row=2, padx=8, pady=4, sticky="W")
# End Upload Tab Frame ------------------------------

win.mainloop()  # Event loop
