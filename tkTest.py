from tkinter import Tk, Label, Button, Entry, Text
import serial
from time import gmtime, strftime
import os.path

#todo: option to dump all data
#todo: default filepath as current filepath
#todo: button to stop/pause program
#todo: automatically close + reopen text file after certain amount of time
#todo: 


class ForceGaugeGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="FORCE GAUGE READER 3005")
        self.label.pack()
            
        self.pathField = Entry(master)
        self.pathField.pack()
        self.pathField.insert(0, "Enter path here")

        self.portField = Entry(master)
        self.portField.pack()
        self.portField.insert(0, "COM3")

        self.fullPath = strftime("%Y%m%d-%H%M%S") + ".txt"
        self.run_button = Button(master, text="Run Program", command=lambda: self.serialLoop(self.portField.get(), self.fullPath, 100, 10))
        self.run_button.pack()

        self.close_button = Button(master, text="Stop", command=master.quit)
        self.close_button.pack()

    

    

    def serialLoop(self, port, filePath, dataSize, lowCutoff):
        #serial setup. Timeout is none so that we can use read(1) down below to wait
        #for transmission to start
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = 9600
        ser.timeout = None

        print(ser.name)
        ser.open()
        file = open(filePath, "a")

        #Send commands to the M5i. 'N' tells it to send in Newtons,
        #'AOUTn' tells it to automatically send data n times per second
        ser.write(b"N\r\n")
        ser.write(b"AOUT25\r\n")
        print("receiving data")

        #wait until we receive data, program hangs here until data is received.
        ser.read(1)

        try:
            while True:
                dataPoints = [0]
                localMaxima = []
                print("-------")
                input = ser.read(dataSize)
                stringList = input.decode().split("N\r\n")
                for i in range(0, len(stringList)):
                    try:
                        dataPoints.append(float(stringList[i]))
                    except ValueError:
                        pass
                    
                dataPoints.append(0)
                for i in range(1, len(dataPoints)-1):
                    if ((dataPoints[i] > dataPoints[i-1]) & (dataPoints[i] > dataPoints[i+1])):
                        if (dataPoints[i] > lowCutoff):
                            localMaxima.append(dataPoints[i])
                            file.write(str(dataPoints[i])+ "\n")
                print("Data: " + str(dataPoints))
                print("Maxima: " + str(localMaxima))

        #if program ends incorrectly, COM port won't get closed (not a problem) and the file won't be
        #written to (BIG problem). That's why we close both in case of a keyboard interrupt (ctrl + c)
        except KeyboardInterrupt:
            ser.close()
            file.close()

        ser.close()
        file.close()

root = Tk()
my_gui = ForceGaugeGUI(root)
root.mainloop()
