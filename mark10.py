import time
import serial

def serialLoop(port, filePath, dataSize, lowCutoff, transferSpeed,
               outputMaxes, dumpInterval):
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
    ser.write(b"AOUT" + transferSpeed.encode('UTF-8') + b"\r\n")
    #TODO: test the above line
    
    print("receiving data")
    #wait until we receive data, program hangs here until data is received.
    ser.read(1)

    start_time = time.clock()


    try:
    #following loop runs until interrupted. First, we take in dataSize
    #amount of bytes, then convert those bytes into a string, then take the
    #parts we want from that string (just the numbers) and make a dataPoint list
    #out of it. From there we either output all the data points, or check each
    #number to see if its a max, then output the maxima. 
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
                
            if outputMaxes:   
                dataPoints.append(0)
                for i in range(1, len(dataPoints)-1):
                    if ((dataPoints[i] > dataPoints[i-1]) &
                        (dataPoints[i] > dataPoints[i+1])):
                        if (dataPoints[i] > lowCutoff):
                            localMaxima.append(dataPoints[i])
                            file.write(str(dataPoints[i])+ "\n")
                print("Data: " + str(dataPoints))
                print("Maxima: " + str(localMaxima))
            else:
                print("Data: " + str(dataPoints))
                for point in dataPoints:
                    file.write(str(point) + "\n")
                    #TODO: check above code^

            elapsed = time.clock() - start_time
            if elapsed > dumpInterval*60:
                file.close()
                file = open(filePath, "a")
            #if we've run over a certain number of minutes, dump the data we
            #have so far and start recording again
            #TODO: test above section
            
    #if program ends incorrectly, COM port won't get closed (not a problem)
    #and the file won't be
    #written to (BIG problem). That's why we close both in case of a keyboard
    #interrupt (ctrl + c)
    except KeyboardInterrupt, SystemExit:
        ser.close()
        file.close()

    ser.close()
    file.close()


