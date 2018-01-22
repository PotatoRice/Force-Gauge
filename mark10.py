import time
import serial
import msvcrt
import sys

'''
def serialSetup(port, filePath, transferSpeed):
    ser = serial.Serial()
    ser.port = port
    ser.timeout = None
    ser.baudrate = 112500

    print(ser.name)
    ser.open()
    file = open(filePath, "a")

    ser.write(b"AOUT" + str(transferSpeed).encode('UTF-8') + b"\r\n")
    ser.write(b"N\r\n")
    print("receiving data")
    try:
        ser.read(1)
    except KeyboardInterrupt:
        pass

def serialPass(dataSize, lowCutoff, outputMaxes):
    try:
    #First, we take in dataSize
    #amount of bytes, then convert those bytes into a string, then take the
    #parts we want from that string (just the numbers) and make a dataPoint list
    #out of it. From there we either output all the data points, or check each
    #number to see if its a max, then output the maxima. 
    dataPoints = [0]
            maximaSub = [0]
            localMaxima = []
            print("-------")
            input = ser.read(dataSize)
            stringList = input.decode().split("N\r\n")
            for i in range(0, len(stringList)):
                try:
                    dataPoints.append(float(stringList[i]))
                except ValueError:
                    pass

            #run this only if we checked the box to print out only maximums
            #we check each data point to see if its at least as large as
            #the points before and after it. If it is, we record that subscript
            #into the maximaSub list. Then we loop through the maximaSub list
            #and add the dataPoint at that index to the localMaxima list, but
            #only if its index is far enough away from the index before it. This
            #is to prevent data like 12, 25, 20, 26, 4 to register as two spikes
            #(25 and 26) when in reality we only want to treat that as 1 spike.
            if outputMaxes == 1:   
                dataPoints.append(0)
                for i in range(1, len(dataPoints)-1):
                    if (dataPoints[i] > lowCutoff):
                        if ((dataPoints[i] >= dataPoints[i-1]) &
                            (dataPoints[i] >= dataPoints[i+1])):
                            maximaSub.append(i)
                for j in range(1, len(maximaSub)):
                    if maximaSub[j]-maximaSub[j-1] > 8:
                        localMaxima.append(dataPoints[maximaSub[j]])
    
                for item in localMaxima:
                    file.write(str(item) + "\n")
                            
                print("Data: " + str(dataPoints))
                print("Maxima: " + str(localMaxima))
            else:
                print("Data: " + str(dataPoints))
                for point in dataPoints:
                    file.write(str(point) + "\n")
                    
            print(outputMaxes)
            print(dumpInterval)
            elapsed = time.clock() - start_time
            if elapsed > float(dumpInterval*60):
                file.close()
                file = open(filePath, "a")
            #if we've run over a certain number of minutes, dump the data we
            #have so far and start recording again        
'''

def serialLoop(port, filePath, dataSize, lowCutoff, transferSpeed,
               outputMaxes, dumpInterval):
    #serial setup. Timeout is none so that we can use read(1) down below to wait
    #for transmission to start
    ser = serial.Serial()
    ser.port = port
    ser.timeout = None
    ser.baudrate = 115200

    print(ser.name)
    ser.open()
    file = open(filePath, "a")
    

    #Send commands to the M5i. 'N' tells it to send in Newtons,
    #'AOUTn' tells it to automatically send data n times per second
    ser.write(b"AOUT" + str(transferSpeed).encode('UTF-8') + b"\r\n")
    ser.write(b"N\r\n")
    
 
    print("receiving data")
    #wait until we receive data, program hangs here until data is received.
    try:
        ser.read(1)
    except KeyboardInterrupt:
        pass

    start_time = time.clock()


    try:
    #following loop runs until interrupted. First, we take in dataSize
    #amount of bytes, then convert those bytes into a string, then take the
    #parts we want from that string (just the numbers) and make a dataPoint list
    #out of it. From there we either output all the data points, or check each
    #number to see if its a max, then output the maxima. 
        while True:
            dataPoints = [0]
            maximaSub = [0]
            localMaxima = []
            print("-------")
            input = ser.read(dataSize)
            stringList = input.decode().split("N\r\n")
            for i in range(0, len(stringList)):
                try:
                    dataPoints.append(float(stringList[i]))
                except ValueError:
                    pass

            #run this only if we checked the box to print out only maximums
            #we check each data point to see if its at least as large as
            #the points before and after it. If it is, we record that subscript
            #into the maximaSub list. Then we loop through the maximaSub list
            #and add the dataPoint at that index to the localMaxima list, but
            #only if its index is far enough away from the index before it. This
            #is to prevent data like 12, 25, 20, 26, 4 to register as two spikes
            #(25 and 26) when in reality we only want to treat that as 1 spike.
            if outputMaxes == 1:   
                dataPoints.append(0)
                for i in range(1, len(dataPoints)-1):
                    if (dataPoints[i] > lowCutoff):
                        if ((dataPoints[i] >= dataPoints[i-1]) &
                            (dataPoints[i] >= dataPoints[i+1])):
                            maximaSub.append(i)
                for j in range(1, len(maximaSub)):
                    if maximaSub[j]-maximaSub[j-1] > 8:
                        localMaxima.append(dataPoints[maximaSub[j]])
    
                for item in localMaxima:
                    file.write(str(item) + "\n")
                            
                print("Data: " + str(dataPoints))
                print("Maxima: " + str(localMaxima))
            else:
                print("Data: " + str(dataPoints))
                for point in dataPoints:
                    file.write(str(point) + "\n")
                    
            print(outputMaxes)
            print(dumpInterval)
            elapsed = time.clock() - start_time
            if elapsed > float(dumpInterval*60):
                file.close()
                file = open(filePath, "a")
            #if we've run over a certain number of minutes, dump the data we
            #have so far and start recording again
            
    #if program ends incorrectly, COM port won't get closed (not a problem)
    #and the file won't be
    #written to (BIG problem). That's why we close both in case of a keyboard
    #interrupt (ctrl + c) or a system exit
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        file.close()

    ser.close()
    file.close()


