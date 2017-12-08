import time
import serial

#serial setup. Timeout is none so that we can use read(1) down below to wait
#for transmission to start
ser = serial.Serial()
ser.port = 'COM3'
ser.baudrate = 9600
ser.timeout = None

print(ser.name)
ser.open()
file = open("data.txt", "w")
file.write("begin data:\n")

#Send commands to the M5i. 'N' tells it to send in Newtons,
#'AOUTn' tells it to automatically send data n times per second
ser.write(b"N\r\n")
ser.write(b"AOUT25\r\n")
print("receiving data")

#wait until we receive data, program hangs here until data is received.
ser.read(1)
dataSize = 100
low = 10

for i in range(0, 10):
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
            if (dataPoints[i] > low):
                localMaxima.append(dataPoints[i])
                file.write(str(dataPoints[i])+ "\n")
    print("Data: " + str(dataPoints))
    print("Maxima: " + str(localMaxima))
ser.close()
file.close()


'''
#commenting out while i try something else

#low is the cutoff point where we determine a spike is not happening
#dataSize is the number of bytes we want to receive per loop
low = 10
dataSize = 50
chunk1 = []
chunk2 = []

for i in range(0, 5):
    print("------")
    input = ser.read(dataSize)
    print(input)

    #converts the input we receive (one long string) into a series of floats
    #that we can use, and adds them to chunk1
    stringList = input.decode().split("N\r\n")
    cutoff = False
    for i in range (0, len(stringList)):
        try:
            check = float(stringList[i])
        except ValueError:
            pass
        if (check < low):
            cutoff = True
        if not cutoff:
            chunk1.append(check)
        else:
            chunk2.append(check)
            
    chunk1Highest = 0
    for i in chunk1:
        if (i>chunk1Highest):
            chunk1Highest = i

    print("Highest value: " + str(chunk1Highest))    
    #TODO: remove this file write, this is for testing    
    for add in chunk1:
        file.write(str(add))
        file.write("\n")
    print(chunk1)

    chunk1 = chunk2
    chunk1 = []
'''

