import time
import serial
import msvcrt
import sys

#This function checks to make sure we have a valid connection with the mark10.
#It also sends the beginning instructions to setup the mark10, which only need
#to be sent once. 
def serialSetup(port, filePath, transferSpeed):
    ser = serial.Serial()
    ser.port = port
    ser.timeout = 2
    ser.baudrate = 115200
    ser.open()

    #Sends the byte encoding of AOUTn, where n is the transfer speed.
    ser.write(b"AOUT" + str(transferSpeed).encode('UTF-8') + b"\r\n")

    #Sends the unit of measurement setting
    ser.write(b"N\r\n")
    if (ser.read(1) == b""):
        print("Port connection error. Check USB connection and try again.")
        return False
    else:
        print("Connection established. Beginning data loop.")
        return True
    ser.close()

#Is called repeatedly in a loop in the main file
def serialPass(dataSize, lowerBound, upperBound, outputMaxes, port, filePath):
    '''Takes in dataSize amount of bytes from the serial stream, then split
    the resulting stream into a list of floats. Those floats are then either
    outputted directly, or processed to find maxima, depending on the checkbox
    option.'''
    try:
        ser = serial.Serial()
        ser.port = port
        ser.timeout = None
        ser.baudrate = 115200
        ser.open()
        
        file = open(filePath, "a")
        dataPoints = [0]
        maximaSub = []
        localMaxima = []
        print("------------")
        input = ser.read(dataSize)
        stringList = input.decode().split("N\r\n")
        for i in range(0, len(stringList)):
            try:
                dataPoints.append(float(stringList[i]))
            except ValueError:
                pass

        #run this only if we checked the box to print out only maximums
        #we check each data point to see if its at least as large as
        #the points 25 indices before and after it. 
        if outputMaxes == 1:   
            for i in range(1, len(dataPoints)-1):
                if (dataPoints[i] > lowerBound) \
                    and (dataPoints[i] < upperBound):
                    big = True
                    #if greater or equal to any data point in the
                    #surrounding area
                    
                    try:
                        for h in range(0, 25):
                            if dataPoints[i] < dataPoints[i-h] and \
                               dataPoints[i-h] > lowerBound and \
                               dataPoints[i-h] < upperBound:
                                big = False
                            if dataPoints[i] < dataPoints[i+h] and \
                               dataPoints[i+h] > lowerBound and \
                               dataPoints[i+h] < upperBound:
                                big = False
                        if (big == True):
                            if len(maximaSub) == 0:
                                maximaSub.append(i)
                            else:
                                if (i - maximaSub[-1] > 25):
                                    maximaSub.append(i)
                                else:
                                    if (dataPoints[i] != \
                                        dataPoints[maximaSub[-1]]):
                                        maximaSub.append(i)
                    except IndexError:
                        pass
            for sub in maximaSub:   
                localMaxima.append(dataPoints[sub])
                
            print("Data: " + str(dataPoints))
            print("Maxima: " + str(localMaxima))
            for point in localMaxima:
                file.write(str(point) + "\n")
        else:
            print("Data: " + str(dataPoints))
            for point in dataPoints:
                file.write(str(point) + "\n")
        
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        file.close()
    ser.close()
    file.close()

#is called when the program closes. Establishes and then closes a connection
#with the serial port in an attempt to properly close the port.
def serialEnd(port):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.open()
    ser.close()
    print("Data loop ended.")
