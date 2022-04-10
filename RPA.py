# -*- coding: utf-8 -*-


import tkinter as tk

import imutils
import requests
import pyautogui
from sneakysnek.recorder import Recorder
from tkinter import filedialog as fd
import json
from PIL import ImageTk, Image
from tkinter import ttk

import numpy as np
import cv2
import mss
import sys
images = []
images_large = []
offsetX = 0
offsetY = 0
recorder = None
verified = False
size = 500
half = 250 
size_small = 50
half_small = 25 
btn = [] #creates list to store the buttons ins

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def redrawHistory():
    global verified
    if verified:
        global history
        global frame
        global btn
        for widget in frame.winfo_children():
            widget.destroy()
        global canvas
        imagek = Image.open(resource_path('keypress.png'))
        imagek = imagek.resize((50,50), Image.ANTIALIAS)
        imgk= ImageTk.PhotoImage(imagek)
        imageC = Image.open(resource_path('click.png'))
        imageC = imageC.resize((50,50), Image.ANTIALIAS)
        imgC= ImageTk.PhotoImage(imageC)
        imageM = Image.open(resource_path('mouse.png'))
        imageM = imageM.resize((50,50), Image.ANTIALIAS)
        imgM = ImageTk.PhotoImage(imageM)
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
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)), image=imgC, width=200,command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
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
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)), image=imgC , width=200, command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
            #btn[len(btn)-1].pack() #this packs the buttons
                btn[len(btn)-1].grid(column=0, row=counter+5)   # grid dynamically divides the space in a grid
    
                separator = ttk.Separator(frame, orient='horizontal')
                separator.grid(column=0, row=counter + 6, sticky="ew")   # grid dynamically divides the space in a grid
                counter += 7
                #separator.pack(fill='x')
            else: 
                btn.append(tk.Button(frame, text=y["type"] + " " + str(len(btn)),image=imgM, width=200, command=lambda c=len(btn): edit(btn[c].cget("text")), compound="left"))
                btn[len(btn)-1].grid(column=0, row=counter+2)   # grid dynamically divides the space in a grid
    
                separator = ttk.Separator(frame, orient='horizontal')
                separator.grid(column=0, row=counter + 3, sticky="ew")   # grid dynamically divides the space in a grid
               
                counter += 4
                
        size = (200, len(history)*200)
        canvas.configure(scrollregion='0 0 %s %s' % size)
        
        window.mainloop()
    
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
    return image


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
    global half
    global size
    global counter
    global size_small
   # print(event)
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
            recorder.stop()
            runRecording()   
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
                image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
               # test = match(image, x["image"])
    
    
    
                match_res = cv2.matchTemplate(x["image"], image, cv2.TM_SQDIFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
                print(max_val)
                print(max_loc)
                if max_val > .9:
                    print("Success")
                    print(str(x["x"]) + "," + str(x["y"]))
                    pyautogui.mouseDown(x["x"], x["y"]) 
                else:
                    print("FAILED")
                    img = pyautogui.screenshot()
                    image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                    print(max_loc)
                    
                    match_res = cv2.matchTemplate(x["image"], image, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
                    if max_val > .9:
                        pyautogui.mouseDown(int(max_loc[0] + 25), int(max_loc[1] + 25))
                        print("Click")
                        print("match:" +str(max_val))
                        print(max_loc)
                        print(str(x["x"]) + " " + str(x["y"]))
                        print(str(max_loc[0] + 25) + "," + str(max_loc[1] + 25) )
                        print(str(x["x"])+ "," + str(x["y"]) )
                        print("CLICKED AFTER FAIL")
                    else:
                        best_loc = None
                        best_val = 0
                        best_scale = 1.0
                        	# loop over the scales of the image
                        for scale in np.linspace(0.3, 1.0, 20)[::-1]:
                            resized = cv2.resize(x["image"], (int(x["image"].shape[1] * scale), int(x["image"].shape[0] * scale)), interpolation = cv2.INTER_AREA)
                            #cv2.imshow("img",resized)
                            #cv2.waitKey(1)
                            match_res = cv2.matchTemplate(cv2.cvtColor(np.array(resized), cv2.COLOR_BGR2RGB), image, cv2.TM_CCOEFF_NORMED)
                            _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
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
                        if best_val > .8:
                            pyautogui.mouseDown(best_loc[0] + 25*best_scale, best_loc[1] + 25*best_scale)
                             #  offsetX = x["x"] - max_loc[0] + 25
                             #  offsetY = x["y"] - max_loc[1] + 25
                            
            if x["type"] == "keypress":
                if key_mode == "low":
                    if "space" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write(" ", interval=0.05) 
                    elif "period" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write(".", interval=0.05) 
                    elif "slash" in str(x["key"]).split("KEY_")[1].lower():
                        pyautogui.write("/", interval=0.05) 
                    else:
                        pyautogui.write(str(x["key"]).split("KEY_")[1].lower(), interval=0.05) 
    
    #button7location = pyautogui.locateOnScreen('tweet.png')asdfas asdfasdf    asdfasdf   
    #print(button7location)asdfassddss
    #button7point = pyautogui.center(button7location)asdfasdf
    
    #button7x, button7y = button7point
    #pyautogui.click(button7x, button7y)  # clicks the center of where the 7 button was found
    #pyautogui.click('tweet.png') # a shortcut version to click on the center of where the 7 button was found
    
    # Some blocking code in your main thread...
window = tk.Tk()
window.geometry('200x1080')
     
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
    
    
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newRecording)
filemenu.add_command(label="Open", command=openRecording)
filemenu.add_command(label="Save", command=saveRecording)
filemenu.add_command(label="Play", command=playRecording)
filemenu.add_command(label="Start Recording", command=startRecording)
filemenu.add_command(label="Stop Recording (ESC)", command=stopRecording)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

window.config(menu=menubar)
default = ''
import os.path

if os.path.isfile('config_cheatlayer.txt'):
    with open('config_cheatlayer.txt', 'r') as file:
        default = file.read().replace('\n', '')
# TextBox Creation
window.title("Cheat Layer Desktop RPA Beta")
def on_configure(event):
    global canvas
    global frame
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    
    size = (200, frame.winfo_reqheight())
    print(size)
    canvas.configure(scrollregion='0 0 %s %s' % size)
    #canvas.configure(scrollregion=canvas.bbox('all'))

canvas = tk.Canvas(window,height = 1080 , width = 200)
canvas.bind_all("<MouseWheel>", _on_mousewheel)

#canvas.pack(side=tk.LEFT)
canvas.grid(column=0, row=0)   # grid dynamically divides the space in a grid

scrollbar = tk.Scrollbar(window, command=canvas.yview)
#scrollbar.pack(side=tk.LEFT, fill='y')
scrollbar.grid(column=1, row=0, sticky='ns')   # grid dynamically divides the space in a grid

canvas.configure(yscrollcommand = scrollbar.set)

# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
#canvas.bind('<Configure>', on_configure)

# --- put frame in canvas ---

frame = tk.Frame(canvas)


if len(default) > 1:
    r = requests.post("https://cheatlayer.com/user/checkDesktopKey", data={'id': default.replace('\r', '').replace('\n', '')})
    #print(r.status_code, r.reason)
    #print(r.json())
    data = r.json()
    if len(data["user"]) > 0: 
          # Replace print with any callback that accepts an 'event' arg
        verified = True
        tk.messagebox.showinfo("Cheat Layer",  "Logged in!")
        print("Logged in!")
        
else:
    inputtxt = tk.Text(frame,
                       height = 1,
                       width = 30)
    inputtxt.grid(column=0, row=0)   # grid dynamically divides the space in a grid

    #inputtxt.pack()

# Button Creation
    printButton = tk.Button(frame,
                        text = "Submit Key", 
                        command = printInput)
    printButton.grid(column=0, row=1)   # grid dynamically divides the space in a grid

canvas.create_window((0,0), window=frame, anchor='nw')
window.call('wm', 'attributes', '.', '-topmost', '1')
window.iconbitmap(resource_path('favicon.ico'))

window.mainloop()

