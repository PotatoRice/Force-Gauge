
def serialLoop(port, filePath, dataSize, lowCutoff, transferSpeed,
               outputMaxes, dumpInterval):
    start_time = time.clock()
    print("--------")
    print("Pretending to run loop.")
    print("Port: " + port)
    print("Filepath: " + filePath)
    print("Data Size: " + str(dataSize))
    print("Low value: " + str(lowCutoff))
    print("Transfering at " + str(transferSpeed) + " values per second")
    if outputMaxes:
        print("Outputting only maxes")
    else:
        print("Outputting all data")
    print("Dump interval: " + str(dumpInterval))
    file = open(filePath, "a")
    file.write("Pretend this is data\nbeep boop")

    
