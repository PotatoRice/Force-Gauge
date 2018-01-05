import tkinter
import serial
from time import gmtime, strftime
import os
from mark10 import serialLoop

runLoop = True
print("xd")

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

t3 = tkinter.Label(frame, text="Dump data interval (minutes):")
t3.pack()
intervalField = tkinter.Entry(frame, width = 5)
intervalField.pack()
intervalField.insert(0, "60")
CheckMaxVar = tkinter.IntVar()
dataOption = tkinter.Checkbutton(frame, text="Output only maximums",
                                 variable = CheckMaxVar)
dataOption.select()
dataOption.pack()




def run():
    #sets our fullPath as our current directory + the current date and
    #time so that our text file is saved in the format "2017-12-15 0924"
    fullPath = pathField.get() + "\\" + \
    strftime(("%Y-%m-%d %H%M")+ ".txt")
    #serialSetup(self.portField.get(), self.fullpath, 1000)
    #runLoop = True
    print("running")
run_button = tkinter.Button(frame,text="Run", command = run)
run_button.pack()

def pause():
    runLoop = False
    print("loop status: " + str(runLoop) + "\n-\n-\n-\n-\n-\n-")
    
pause_button = tkinter.Button(frame, text="Pause", command = pause)
pause_button.pack()

close_button = tkinter.Button(frame, text="Close",
                              command = lambda: root.destroy())
close_button.pack()
            


while True:
    root.update_idletasks()
    root.update()
    if runLoop == True:
        '''serialPass(self.portField.get(), self.fullPath, 1000, 2, 250,
                    CheckMaxVar.get(), self.intervalField.get())'''
        print("loop status: " + str(runLoop))
        
    
                

    

    

    




