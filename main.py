import tkinter
import serial
from time import gmtime, strftime
import os
from setupandloop import serialPass, serialSetup, serialEnd

global runLoop
runLoop = False

global systemClose
systemClose = False

global start_time
start_time = 0

root = tkinter.Tk()

frame = tkinter.Frame(root, borderwidth=2)
frame.pack(expand = 1)
t1 = tkinter.Label(frame, text="File Path:")
t1.pack()
pathField = tkinter.Entry(frame, width = 60)
pathField.pack()
dir_path = os.path.dirname(os.path.realpath(__file__))
pathField.insert(0, dir_path)
t2 = tkinter.Label(frame, text="Port: ")
t2.pack()
portField = tkinter.Entry(frame, width = 10)
portField.pack()
portField.insert(0, "COM3")


CheckMaxVar = tkinter.IntVar()
dataOption = tkinter.Checkbutton(frame, text="Output only maximums",
                                 variable = CheckMaxVar)
dataOption.select()
dataOption.pack()


fullPath = ""

def run():
    #sets our fullPath as our current directory + the current date and
    #time so that our text file is saved in the format "2017-12-15 0924"
    global fullPath
    fullPath = pathField.get() + "\\" + \
    strftime(("%Y-%m-%d %H%M")+ ".txt")
    if serialSetup(portField.get(), fullPath, 250):
        global runLoop
        runLoop = True
    
run_button = tkinter.Button(frame,text="Run", command = run)
run_button.pack()


def end():
    global systemClose
    systemClose = True
    

close_button = tkinter.Button(frame, text="Close", command = end)
close_button.pack()
            

while True:
    root.update()
    if runLoop == True:
        serialPass(1000, 5, 40, CheckMaxVar.get(), portField.get(), fullPath)
    if systemClose == True:
        serialEnd(portField.get())
        root.destroy()
        break

