from tkinter import Tk, Label, Button, Entry, Text, Checkbutton, IntVar
import serial
from time import gmtime, strftime
import os
from mark10 import serialLoop



#TODO: button to stop/pause program
#TODO: multithread so the above is possible, that way we aren't running an
#uninterruptable 'while' loop -_-    or don't multithread and just rerun the
#individual process each time (but only do the serial setup once)
'''
def serialSetup(args):
    sets up connection through serial port and tells mark10 to transmit
def serialPass(args):
    reads/process data chunk
runLoop = False
button start (command: runLoop = True)
button stop( command: runLoop = False, sysexit)
button pause
button resume

stop and resume begin disabled, and are enabled when their counterparts are
pressed, and vice versa

while runLoop:
    serialPass(args)
    should work because serial read waits until the the required bytes are
    read, so this loop won't try to run as fast as possible since it hangs
    a bit. Might have buffer issues from going between iterations
need to make sure the GUI loop is still being checked as the while loop runs
that way the runLoop variable can be updated properly

    '''
#TODO: automatically close + reopen text file after certain amount of time
#^done, tested once, needs more testing





class ForceGaugeGUI:
    def __init__(self, master):
        self.master = master
        master.title("FORCE GAUGE READER 3005")

        self.t1 = Label(master, text="File Path:")
        self.t1.pack()
            
        self.pathField = Entry(master, width=60)
        self.pathField.pack()
        #sets our default filepath as our current directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pathField.insert(0, dir_path)

        self.t2 = Label(master, text="Port: ")
        self.t2.pack()
        self.portField = Entry(master, width=10)
        self.portField.pack()
        self.portField.insert(0, "COM3")

        self.t3 = Label(master, text="Dump data interval (minutes):")
        self.t3.pack()
        self.intervalField = Entry(master, width = 5)
        self.intervalField.pack()
        self.intervalField.insert(0, "60")

        CheckVar = IntVar()
        self.dataOption = Checkbutton(master, text= "Output only maximums",
                                      variable = CheckVar)
        self.dataOption.select()
        self.dataOption.pack()
        

        #runs our loop when we press the button, with the parameters from the
        #entry fields
        def run():
            #sets our fullPath as our current directory + the current date and
            #time so that our text file is saved in the format "2017-12-15 0924"
            self.fullPath = self.pathField.get() + "\\" + \
            strftime(("%Y-%m-%d %H%M")+ ".txt")
            serialLoop(self.portField.get(), self.fullPath, 1000, 2, 250,
                       CheckVar.get(), self.intervalField.get())
            
        self.run_button = Button(master, text="Start",
                                 command = lambda: run())
        self.run_button.pack()


        #master quit should raise a SystemExit, which also prompts the program
        #to properly close before it shuts down, which saves our data
        self.close_button = Button(master, text="Close",
                                   command = lambda: root.destroy())
        self.close_button.pack()

    

    

    

root = Tk()
my_gui = ForceGaugeGUI(root)
root.mainloop()
