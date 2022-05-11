#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal

from Qt import QtCore, QtWidgets, QtGui

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)
from NodeGraphQt.constants import (NODE_PROP_QLABEL,
                                       NODE_PROP_QLINEEDIT,
                                       NODE_PROP_QCOMBO,
                                       NODE_PROP_QSPINBOX,
                                       NODE_PROP_COLORPICKER,
                                       NODE_PROP_SLIDER)
# import example nodes from the "example_nodes" package
from examples import group_node
from examples.custom_nodes import (
    basic_nodes,
    custom_ports_node,
    widget_nodes,
)

import tkinter as tk
from PySide2.QtWidgets import (QInputDialog)
import imutils
import requests
import pyautogui
from sneakysnek.recorder import Recorder
from tkinter import filedialog as fd
import json
from PIL import ImageTk, Image
from tkinter import ttk
from threading import Thread

from queue import Queue
record_tasks = Queue()

import numpy as np
import cv2
import mss
import sys


import os.path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


images = []
images_large = []
offsetX = 0
offsetY = 0
shift_down = False
recorder = None
verified = False
size = 500
half = 250 
size_small = 50
half_small = 25 
btn = [] #creates list to store the buttons ins


import sys

class MyWidget(QtWidgets.QWidget): 
    def __init__(self, Login): 
        QtWidgets.QWidget.__init__(self) 
        self.setGeometry(100,100,100,25)
        self.Login = Login

        self.pushbutton = QtWidgets.QPushButton('Enter Key', self)
        self.pushbutton.setGeometry(00,0, 100, 25)

        self.pushbutton.clicked.connect(self.getInput)

    def getInput(self):
        key, entered = QtWidgets.QInputDialog.getText(self, 'Cheat Layer Key', 'Enter Cheat Layer Key:')    
        print(key)
        r = requests.post("https://cheatlayer.com/user/checkDesktopKey", data={'id': key.replace('\r', '').replace('\n', '')})
    #print(r.status_code, r.reason)
    #print(r.json())

        data = r.json()
        print(data)
        if len(data["user"]) > 0: 
          # Replace print with any callback that accepts an 'event' arg
            verified = True

#        tk.messagebox.showinfo("Cheat Layer",  "Logged in!")
            print("Logged in!")
            self.Login()
        with open('config_cheatlayer.txt', 'w') as f:
            f.write(key)


def redrawHistory():
    global verified
    if verified:
        global history
        global imgM
        global imgC
        global imgk
        global frame
        global btn
        global window
        for widget in frame.winfo_children():
            widget.destroy()
        global canvas
        #print(history)
        btn = []
        images = []
        images_large = []
        counter = 0
        for x in history:
            y = x
            
            if isinstance(y, str):
                y = json.loads(x)
    
            #l = tk.Label(frame, text="Event: " + y["type"], font="-size 24")
            #l.pack()
    
            #l.grid(column=0, row=len(history))   # grid dynamically divides the space in a grid
    
            #l.grid(column=0, row=counter)   # grid dynamically divides the space in a grid
            #l22 = tk.Label(frame, text="Postion: " + " (" + str(y["x"]) +"," + str(y["y"])  + ")", font="-size 24")
            #l22.pack()
            #l22.grid(column=0, row=counter + 1)   # grid dynamically divides the space in a grid
    
            if "key" in y:
                #l5 = tk.Label(frame, text="Key: " + y["key"])
                #l5.pack()
                #l5.grid(column=0, row=counter + 2)   # grid dynamically divides the space in a grid
                
                imagek = Image.open(resource_path('keypress.png'))
                imagek = imagek.resize((50,50), Image.ANTIALIAS)
                imgk= ImageTk.PhotoImage(imagek)
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)), image=imgC, width=300,command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
            #btn[len(btn)-1].pack() #this packs the buttons
                btn[len(btn)-1].grid(column=0, row=counter+3)   # grid dynamically divides the space in a grid
    
                separator = ttk.Separator(frame, orient='horizontal')
                separator.grid(column=0, row=counter + 4, sticky="ew")   # grid dynamically divides the space in a grid
    
                counter += 5
            elif "image" in y and "large" in y:
                l6 = tk.Label(frame, text="Target Images: ")
                #l6.pack()
                #l6.grid(column=0, row=1)   # grid dynamically divides the space in a grid
                #l6.grid(column=0, row=counter + 2)   # grid dynamically divides the space in a grid
    
                img = y["image"]
                arry = np.array(img, dtype=np.uint8)
    
                im = Image.fromarray(arry)
                images.append(ImageTk.PhotoImage(image=im))
    
    
                panel = tk.Label(frame, image = images[len(images)-1], borderwidth=2, relief="solid")
                #panel.pack()
                #panel.grid(column=0, row=counter+ 3)   # grid dynamically divides the space in a grid
    
                #print("ADD IMAGE")
                img2 = y["large"]
                arry2 = np.array(img2, dtype=np.uint8)
    
                im2 = Image.fromarray(arry2)
                images_large.append(ImageTk.PhotoImage(image=im2))
    
    
                panel2 = tk.Label(frame, image = images_large[len(images_large)-1], borderwidth=2, relief="solid")
               # panel2.pack()
                #panel2.grid(column=0, row=counter + 4)   # grid dynamically divides the space in a grid
                
                #print("ADD IMAGE")
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)), image=imgC , width=300, command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
            #btn[len(btn)-1].pack() #this packs the buttons
                btn[len(btn)-1].grid(column=0, row=counter+5)   # grid dynamically divides the space in a grid
    
                separator = ttk.Separator(frame, orient='horizontal')
                separator.grid(column=0, row=counter + 6, sticky="ew")   # grid dynamically divides the space in a grid
                counter += 7
                #separator.pack(fill='x')
            else: 
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)),image=imgM, width=300, command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
                btn[len(btn)-1].grid(column=0, row=counter+2)   # grid dynamically divides the space in a grid
    
                separator = ttk.Separator(frame, orient='horizontal')
                separator.grid(column=0, row=counter + 3, sticky="ew")   # grid dynamically divides the space in a grid
               
                counter += 4
                
       
        window.event_generate("<<update>>", when="tail", state=123)
      #  record_tasks.put("update")
#        window.update()

    
def deleteEvent(n):
    
    global history
    global frame
    del history[int(n)]
    
    redrawHistory()

def saveEvent(n, event):
    global positionX
    global positionY
    newX = positionX.get(1.0, "end-1c")
    newY = positionY.get(1.0, "end-1c")
    if isinstance(history[int(n)], str):
        history[int(n)] = json.loads(history[int(n)])
    history[int(n)]["x"] = newX
    history[int(n)]["y"] = newY
    redrawHistory()
        
def openNewWindow(n, typeEvent):
    global window
    
    global positionX
    global positionY
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(window)
    
    # sets the title of the
    # Toplevel widget
    newWindow.title("Edit Event" + n)
    step = json.loads(history[int(n)])   
    # sets the geometry of toplevel
    newWindow.geometry("1000x800")
    ltype = tk.Label(newWindow, text="Event: " + str(step["type"]), font="-size 24")
        #l.pack()

        #l.grid(column=0, row=len(history))   # grid dynamically divides the space in a grid

    ltype.grid(column=0, row=0) 
    lposition = tk.Label(newWindow, text="Postion (" +str(step["x"]) +  "," + str(step["y"]) + "): ", font="-size 24")
        #l.pack()

        #l.grid(column=0, row=len(history))   # grid dynamically divides the space in a grid
    if "click" in step["type"] or "Click" in step["type"]:
        print("image")
        print(step["type"])
        print(step["image"])
        print(int(n))
        img = step["image"]
        arry = np.array(img, dtype=np.uint8)

        im = Image.fromarray(arry)
        imgtk = ImageTk.PhotoImage(image=im) 


        panel = tk.Label(newWindow, image = imgtk, borderwidth=2, relief="solid")
            #panel.pack()
        panel.grid(column=5, row=5)   # grid dynamically divides the space in a grid

            #print("ADD IMAGE")
        img2 = step["large"]
        arry2 = np.array(img2, dtype=np.uint8)

        im2 = Image.fromarray(arry2)
        imgtk2 = ImageTk.PhotoImage(image=im2) 


        panel2 = tk.Label(newWindow, image = imgtk2, borderwidth=2, relief="solid")
           # panel2.pack()
        panel2.grid(column=5, row=6)   # grid dynamically divides the space in a grid
            
    lposition.grid(column=0, row=1) 
    positionX = tk.Text(newWindow,
                       height = 1,
                       width = 30)

    positionX.grid(column=5, row=1)   # grid dynamically divides the space in a grid
    positionY = tk.Text(newWindow,
                       height = 1,
                       width = 30)

    positionY.grid(column=6, row=1)   # grid dynamically divides the space in a grid

    newWindow.iconbitmap('favicon.ico')
    editButton = tk.Button(newWindow, text="Save Changes", command=lambda c=len(btn): saveEvent(n, typeEvent), compound="left")
        #btn[len(btn)-1].pack() #this packs the buttons
    editButton.grid(column=5, row=7)   # grid dynamically divides the space in a grid
    deleteButton = tk.Button(newWindow, text="Delete Event", command=lambda c=len(btn): deleteEvent(n), compound="left")
        #btn[len(btn)-1].pack() #this packs the buttons
    deleteButton.grid(column=5, row=8)   # grid dynamically divides the space in a grid
    newWindow.mainloop()

    # A Label widget to show in toplevel
 
def _on_mousewheel(event):
    global canvas
    canvas.yview_scroll(-1*(event.delta//120), "units")
def donothing():
   x = 0
def cap(x, y, half, size):
    img = pyautogui.screenshot(region=(x-half,y-half, size, size))

    image = np.array(img)
   # cv2.imwrite("in_memory_to_disk.png", image)

     # Write it to the output file
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
history = []
key_mode = "low"
counter = 0
mouse_counter = 0
def eventRecord(event):
    global recorder
    global mouse_counter
    global history
    global half_small
    global window
    global half
    global size
    global counter
    global size_small
    print(event)
   # print(len(history))
    if "MOVE" in str(event.event):
        mouse_counter += 1
        if mouse_counter%6 == 0:
            history.append(json.dumps({"type":"Move Mouse", "x": int(event.x), "y": int(event.y)}, cls=NumpyEncoder))      
    if "CLICK" in str(event.event) and "DOWN" in str(event.direction):
        history.append(json.dumps({"type":"Left Mouse Click", "x": int(event.x), "y": int(event.y), "image": cap(event.x, event.y, half_small, size_small), "large": cap(event.x, event.y, half, size)}, cls=NumpyEncoder))  
    if "CLICK" in str(event.event) and "UP" in str(event.direction):
        history.append(json.dumps({"type":"Left Mouse Lift", "x": int(event.x), "y": int(event.y), "image": cap(event.x, event.y, half_small, size_small), "large": cap(event.x, event.y, half, size)}, cls=NumpyEncoder))  
    if "DOWN" in str(event.event):
        if "KEY_ESCAPE" in str(event.keyboard_key):
            stopRecording()
            #reco
            #window.event_generate("<<stop>>", when="tail", state=123)
            #record_tasks.put("stop")
            #redrawHistory() 
        if "PRINT" in str(event.keyboard_key):
            #stopRecording()
            #reco
            print("PRINT")
            newWindow = tk.Toplevel(window)
    
            newWindow.title("Edit Event" + n)
            step = json.loads(history[int(n)])   
            newWindow.geometry("1000x800")
            img = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            
            #window.event_generate("<<stop>>", when="tail", state=123)
            #record_tasks.put("stop")
            #redrawHistory()
            #  
        else:  
            history.append(json.dumps({"type":"keypress", "key": str(event.keyboard_key)}, cls=NumpyEncoder))  
           
def match(img1, img2):
#sift
    sift = cv2.xfeatures2d.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

#feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)
   # print(len(matches))
    img3 = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:50], img2, flags=2) 
    #v2.imshow("matches", img3)
    #v2.waitKey()
    return len(matches)

def runRecording():
    global verified
    if verified:
        global offsetX
        global offsetY
        
        #print(offsetX)
        #print(offsetY)
        global shift_down
        global canvas
        global window
        global btn
        global history
      #  print history
        for index,y in enumerate(history):
            
            x = y
            if isinstance(x, str):
                x = json.loads(y)
                
            #print(y)
            
            if index > 0:
                btn[index].config(bg="black")
                btn[index -1].config(bg="white") 
                #btn[index].grid(column=0, row=index*6+3)
                frame.update()
                canvas.yview_moveto(index*.0020)
    
                window.update()
    
            for key, value in x.items()  :
                if key == "image":
                    x["image"] = np.asarray(x["image"],dtype = "uint8")
            if x["type"] == "Move Mouse":
                pyautogui.moveTo(x["x"], x["y"]) 
            if x["type"] == "Left Mouse Lift": 
                pyautogui.mouseUp() 
            if x["type"] == "Left Mouse Click": 
                img = pyautogui.screenshot(region=(x["x"]-half_small,x["y"]-half_small, size_small, size_small))
                image =  cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

               # test = match(image, x["image"])
    
                print(half_small)
                print(size_small)
                match_res = cv2.matchTemplate(x["image"], image, cv2.TM_SQDIFF_NORMED)
                print(match_res)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
                print(min_val)
                print(min_loc)
                
                            
                if min_val < 0.01:
                    print("Success")
                    print(str(x["x"]) + "," + str(x["y"]))
                    pyautogui.mouseDown(x["x"], x["y"]) 
                else:
                    img = pyautogui.screenshot()
                    image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                    best_loc = None
                    best_val = 0
                    best_scale = 1.0
                    	# loop over the scales of the image
                    for scale in np.linspace(0.5, 1.0, 50)[::-1]:
                        resized = cv2.resize(x["image"], (int(x["image"].shape[1] * scale), int(x["image"].shape[0] * scale)), interpolation = cv2.INTER_AREA)
                      
                        match_res = cv2.matchTemplate(image, (resized),  cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
                        #print(max_val)
                        #print(max_loc)
                        #print(scale)
                        if max_val > best_val:
                            best_val = max_val
                            best_loc = max_loc
                            best_scale = scale
                    print("BESTS :")
                    print("match:" + str(best_val))
                    print(best_loc)
                    print("scale:" + str(best_scale))

                    #print("SUPER MATCH")
                    if best_val  > .9:
                        pyautogui.mouseDown(best_loc[0] + half_small*best_scale, best_loc[1] + half_small*best_scale)
                         #  offsetX = x["x"] - max_loc[0] + 25
                         #  offsetY = x["y"] - max_loc[1] + 25
                            
            if x["type"] == "keypress":
                if key_mode == "low":
                    if "backspace" in str(x["key"]).split("KEY_")[1].lower():
                         pyautogui.press('backspace')
                    elif "space" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write(" ", interval=0.05) 
                    elif "period" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write(".", interval=0.05) 
                    elif "slash" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write("/", interval=0.05) 
                    elif "return" in str(x["key"]).split("KEY_")[1].lower():
                         pyautogui.press('enter')
                    elif "shift" in str(x["key"]).split("KEY_")[1].lower():
                        if shift_down:
                            pyautogui.keyUp("shift")
                            shift_down = False
                        else:
                            pyautogui.keyDown("shift")
                            shift_down = True
                    else:
                        if shift_down:
                            pyautogui.write(str(x["key"]).split("KEY_")[1].upper(), interval=0.05) 
                        else:
                            pyautogui.write(str(x["key"]).split("KEY_")[1].lower(), interval=0.05)
    #button7location = pyautogui.locateOnScreen('tweet.png')asdfas asdfasdf    asdfasdf   
    #print(button7location)asdfassddss
    #button7point = pyautogui.center(button7location)asdfasdf
    
    #button7x, button7y = button7point
    #pyautogui.click(button7x, button7y)  # clicks the center of where the 7 button was found
    #pyautogui.click('tweet.png') # a shortcut version to click on the center of where the 7 button was found
    
    # Some blocking code in your main thread...


def printInput():
    global recorder
    global verified
    inp = inputtxt.get(1.0, "end-1c")
   # lbl.config(text = "Cheat Layer Key: "+inp)
    r = requests.post("https://cheatlayer.com/user/checkDesktopKey", data={'id': inp.replace('\r', '').replace('\n', '')})
    #print(r.status_code, r.reason)
    #print(r.json())
    data = r.json()
    if len(data["user"]) > 0: 
          # Replace print with any callback that accepts an 'event' arg
        verified = True
        tk.messagebox.showinfo("Cheat Layer",  "Logged in!")
        print("Logged in!")
        with open('config_cheatlayer.txt', 'w') as f:
            f.write(inp)
def startRecording():
    global verified
    if verified:
        global recorder
        counter = 0
        bnt = 0
        recorder = Recorder.record(eventRecord)
def edit(button):
    print(button)
    print(button.split(" ")[1])
    check = json.loads(history[int(button.split(" ")[len(button.split(" ")) - 1])])
    openNewWindow(button.split(" ")[len(button.split(" ")) - 1], check["type"])
def stopRecording():
    global recorder
    recorder.stop()
    redrawHistory()


def loopRecording():
    global recorder
    print("play")
    while True:
        runRecording()   
def playRecording():
    global recorder
    print("play")
    runRecording()   
def newRecording():
    global history
    global frame
    for widget in frame.winfo_children():
        widget.destroy()
    history = []
def saveRecording():
    f = fd.asksaveasfile(mode='w', defaultextension=".cheat")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    for item in history:
        f.write("%s\n" % (item))
    f.close()
def openRecording():
    global verified
    if verified:
        global history
        global canvas
        global frame
        imagek = Image.open(resource_path('keypress.png'))
    #Resize the Image
        imagek = imagek.resize((50,50), Image.ANTIALIAS)
    #Convert the image to PhotoImage
        imgk= ImageTk.PhotoImage(imagek)
        imageC = Image.open(resource_path('click.png'))
    #Resize the Image
        imageC = imageC.resize((50,50), Image.ANTIALIAS)
    #Convert the image to PhotoImage
        imgC= ImageTk.PhotoImage(imageC)
        imageM = Image.open(resource_path('mouse.png'))
    #Resize the Image
        imageM = imageM.resize((50,50), Image.ANTIALIAS)
    #Convert the image to PhotoImage
        imgM = ImageTk.PhotoImage(imageM)
        f = fd.askopenfilename(filetypes=(("Template files", "*.*"),
                                               ("All files", "*.*") ))
        with open(f) as file:
            history = file.readlines()
        #print(history)
        redrawHistory()
    
from PySide2.QtWidgets import (QWidget, QApplication, QGraphicsView,
QGridLayout, QMainWindow, QAction, QMenu, QVBoxLayout, QMenuBar)
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtOpenGL import *
from PySide2.QtCore import *
from PySide2.QtGui import *

image_path_str='image.jpg'

class View(QGraphicsView):
    photo_clicked = QtCore.Signal(QtCore.QPoint)

    def __init__(self, parent):
        super(View, self).__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.photo = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.pixmap = QtGui.QPixmap(image_path_str)
        self.photo.setPixmap(self.pixmap)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = View(self)

        self.layout_contain_P1_P2 = QtWidgets.QGridLayout()
        self.checkbox_P1= QtWidgets.QCheckBox("P1",self)
        self.line_edit_P1_x = QtWidgets.QLineEdit(self)
        self.line_edit_P1_x.setReadOnly(True)
        self.line_edit_P1_y = QtWidgets.QLineEdit(self)
        self.line_edit_P1_y.setReadOnly(True)

        self.layout_contain_P1_P2.addWidget(self.checkbox_P1, 0, 0, Qt.AlignLeft)

        self.grid_layout_P1_x_y = QtWidgets.QGridLayout()
        self.grid_layout_P1_x_y.addWidget(self.line_edit_P1_x, 1, 0, Qt.AlignLeft)
        self.grid_layout_P1_x_y.addWidget(self.line_edit_P1_y, 2, 0, Qt.AlignLeft)

        self.layout_contain_P1_P2.addLayout(self.grid_layout_P1_x_y, 0, 1, 1, 1)
        self.checkbox_P2 = QtWidgets.QCheckBox("P2",self)
        self.line_edit_P2_x = QtWidgets.QLineEdit(self)
        self.line_edit_P2_x.setReadOnly(True)
        self.line_edit_P2_y = QtWidgets.QLineEdit(self)
        self.line_edit_P2_y.setReadOnly(True)

        self.layout_contain_P1_P2.addWidget(self.checkbox_P2, 1, 0, Qt.AlignLeft)
        self.grid_layout_P2_x_y = QtWidgets.QGridLayout()

        self.grid_layout_P2_x_y.addWidget(self.line_edit_P2_x, 0, 0, Qt.AlignLeft)
        self.grid_layout_P2_x_y.addWidget(self.line_edit_P2_y, 1, 0, Qt.AlignLeft)

        self.layout_contain_P1_P2.addLayout(self.grid_layout_P2_x_y, 1, 1, Qt.AlignLeft)

        self.combo_box1 = QtWidgets.QComboBox(self)
        self.combo_box1.addItem("measurements set 1")
        self.combo_box1.addItem("measurements set 1")

        self.combo_box2 = QtWidgets.QComboBox(self)
        self.combo_box2.addItem("P1-P2")
        self.combo_box2.addItem("P3-P4")

        self.vertical1= QtWidgets.QVBoxLayout()

        # self.vertical1.addWidget(self.menubar)
        self.vertical1.addWidget(self.combo_box1)
        self.vertical1.addWidget(self.combo_box2)
        self.vertical1.addLayout(self.layout_contain_P1_P2)

        self.vertical2= QtWidgets.QVBoxLayout()
        self.vertical2.addWidget(self.view)

        self.horizontal= QtWidgets.QHBoxLayout()
        self.horizontal.addLayout(self.vertical1)
        self.horizontal.addLayout(self.vertical2)

        self.setLayout(self.horizontal)
        self.setWindowTitle("Image viewer")
        self.setGeometry(200, 200, 1000, 800)

class Main_window(QMainWindow):

    def __init__(self, parent=None):

        super(Main_window, self).__init__(parent)
        self.window = Window()
        self.setCentralWidget(self.window)
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        newAct = QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)



if __name__ == '__main__':
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    nodes = []
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])

    def drawHistory(history):
        #print(history)
        global nodes
        for x in history:
            x = json.loads(x)
            nodes.append(graph.create_node('nodes.basic.BasicNodeA', name=x["type"], data=x))#, color= "#FFFFFF"
            this_path = os.path.dirname(os.path.abspath(__file__))
            icon = os.path.join(this_path, 'examples', 'mouse.png')
            if "Move" in x["type"]:
                icon = os.path.join(this_path, 'examples', 'mouse.png')
                nodes[len(nodes)-1].create_property('X Coordinate', x["x"], widget_type=NODE_PROP_QLINEEDIT)
                nodes[len(nodes)-1].create_property('Y Coordinate', x["y"], widget_type=NODE_PROP_QLINEEDIT)
                nodes[len(nodes)-1].create_property('Type', "Move", widget_type=NODE_PROP_QLINEEDIT)

            if "Click" in x["type"]:
                icon = os.path.join(this_path, 'examples', 'click.png')
                nodes[len(nodes)-1].create_property('X Coordinate', x["x"], widget_type=NODE_PROP_QLINEEDIT)
                nodes[len(nodes)-1].create_property('Y Coordinate', x["y"], widget_type=NODE_PROP_QLINEEDIT)
                nodes[len(nodes)-1].create_property('Type', "Click", widget_type=NODE_PROP_QLINEEDIT)

            if "keypress" in x["type"]:
                icon = os.path.join(this_path, 'examples', 'keypress.png')
                nodes[len(nodes)-1].create_property('Key', x["key"], widget_type=NODE_PROP_QLINEEDIT)
                nodes[len(nodes)-1].create_property('Type', "Keypress", widget_type=NODE_PROP_QLINEEDIT)

            nodes[len(nodes)-1].create_property('Data', json.dumps(x), widget_type=NODE_PROP_QLINEEDIT)

            nodes[len(nodes)-1].set_icon(icon)
            if len(nodes) > 1:
                nodes[len(nodes)-1].input(0).connect_to(nodes[len(nodes)-2].output(0))
        graph.auto_layout_nodes()
            

    # crate a backdrop node and wrap it around
    # "custom port node" and "group node".
    # fit node selection to the viewer.
        graph.fit_to_selection()
    # Custom builtin widgets 
    # create graph controller.
    verified = False

    
    graph = NodeGraph(drawHistory, verified)
    graph.set_acyclic(False)
    QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
    # registered example nodes.
    graph.register_nodes([
        basic_nodes.BasicNodeA,
        basic_nodes.BasicNodeB,
        custom_ports_node.CustomPortsNode,
        group_node.MyGroupNode,
        widget_nodes.DropdownMenuNode,
        widget_nodes.TextInputNode,
        widget_nodes.CheckboxNode
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()


    # auto layout nodes.
    graph.auto_layout_nodes()

    # crate a backdrop node and wrap it around
    # "custom port node" and "group node".
    # fit node selection to the viewer.
    graph.fit_to_selection()
    # Custom builtin widgets from NodeGraphQt
    # ---------------------------------------

    # create a node properties bin widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)

    # example show the node properties bin widget when a node is double clicked.
    def display_properties_bin(node):
        if not properties_bin.isVisible():
            properties_bin.show()


    # wire function to "node_double_clicked" signal.
    graph.node_double_clicked.connect(display_properties_bin)
    key = 'None'
    if os.path.isfile('config_cheatlayer.txt'):
        with open('config_cheatlayer.txt', 'r') as file:
            key = file.read().replace('\n', '')
    print(key)
    def Login():
        global graph
        graph.startMenu()

    if key == 'None':
        widget = MyWidget(Login)
        widget.show()
    else:
        r = requests.post("https://cheatlayer.com/user/checkDesktopKey", data={'id': key.replace('\r', '').replace('\n', '')})
    #print(r.status_code, r.reason)
    #print(r.json())

        data = r.json()
        print(data)
        if len(data["user"]) > 0: 
          # Replace print with any callback that accepts an 'event' arg
            verified = True

#        tk.messagebox.showinfo("Cheat Layer",  "Logged in!")
            print("Logged in!")
            Login()
        with open('config_cheatlayer.txt', 'w') as f:
            f.write(key)

    # create a nodes tree widget.
    nodes_tree = NodesTreeWidget(node_graph=graph)
    nodes_tree.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    nodes_tree.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    nodes_tree.set_category_label('nodes.widget', 'Widget Nodes')
    nodes_tree.set_category_label('nodes.basic', 'Basic Nodes')
    nodes_tree.set_category_label('nodes.group', 'Group Nodes')
    # nodes_tree.show()

    # create a node palette widget.
    nodes_palette = NodesPaletteWidget(node_graph=graph)
    nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
    nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
    nodes_palette.set_category_label('nodes.group', 'Group Nodes')
    # nodes_palette.show()
    
    app.exec_()