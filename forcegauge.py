from tkinter import Tk, Label, Button, Entry, Text, Checkbutton
import serial
from time import gmtime, strftime
import os
from mark10temp import serialLoop

#TODO: option to dump all data
#^done, needs testing

#TODO: button to stop/pause program

#TODO: automatically close + reopen text file after certain amount of time
#^done, needs testing



class ForceGaugeGUI:
    def __init__(self, master):
        self.master = master
        master.title("FORCE GAUGE READER 3005")

        self.t1 = Label(master, text="File Path:")
        self.t1.pack()
            
        self.pathField = Entry(master, width=60)
        self.pathField.pack()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pathField.insert(0, dir_path)

        self.t2 = Label(master, text="Port: ")
        self.t2.pack()
        self.portField = Entry(master, width=20)
        self.portField.pack()
        self.portField.insert(0, "COM3")

        self.dataOption = Checkbutton(master, text= "Output only maximums")
        self.dataMaxes = True
        self.dataOption.variable = self.dataMaxes
        self.dataOption.offvalue = False
        self.dataOption.onvalue = True
        self.dataOption.pack()
        self.dataOption.select()

        self.fullPath = dir_path + "\\" + strftime(("%Y-%m-%d %H%M") + ".txt")
        self.run_button = Button(master, text="Start",
                                 command = lambda: serialLoop(self.portField.get(),
                                 self.fullPath,
                                 100, 10, 50, self.dataMaxes))
        self.run_button.pack()

        self.close_button = Button(master, text="Stop", command=master.quit)
        self.close_button.pack()

    

    

    

root = Tk()
my_gui = ForceGaugeGUI(root)
root.mainloop()
