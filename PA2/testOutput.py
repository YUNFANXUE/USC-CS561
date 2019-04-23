import time
import random

FILES = ["input0.txt", "output0.txt"]

def readOutput(filename):
    try:
        fileObj = open(filename, 'r')
    except:
        print("Error: File \"", filename, "\" does not exist.")
        return False
    record = fileObj.readlines()
    timeDict = {}
    for i in range(len(record)):
        if record[i][-1] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            timeDict[i] = [int(time) for time in record[i].split(' ')]
        else:
            timeDict[i] = [int(time) for time in record[i][:-1].split(' ')]
    fileObj.close()
    return timeDict

def readInput(filename):
    try:
        fileObj = open(filename)
    except:
        print("Error: File \"", filename, "\" does not exist. ")
        return False
    airportInfo = fileObj.readline().split(' ')
    maxLanding = int(airportInfo[0])
    maxGates   = int(airportInfo[1])
    maxDepart = int(airportInfo[2])
    numOfPlanes = int(fileObj.readline())
    planesInfo = []
    for i in range(numOfPlanes):
        planeInfo = fileObj.readline().split(' ')
        R = int(planeInfo[0])       # maximum minutes before landing
        M = int(planeInfo[1])       # between start landing and arrive at gate
        S = int(planeInfo[2])       # between arrive at gate and ready to leave gate
        O = int(planeInfo[3])       # between leave gate and depart
        C = int(planeInfo[4])       # maximum minutes to stay at gate
        planesInfo.append([R, M, S, O, C])
    fileObj.close()
    return maxLanding, maxGates, maxDepart, planesInfo

def checkState(inAir,landing, atGate, departing, time):
    if len(landing) > maxLanding:
        print("Error: trying to land more planes than expected at time:", time)
        return False
    if len(atGate) > maxGates:
        print("Error: trying to park more planes at gates than expected at time:", time)
        return False
    if len(departing) > maxDepart:
        print("Error: more planes trying to take off than expected at time:", time)
        return False
    for plane in inAir:
        if inAir[plane] < 0:
            print("Error: plane No.", plane, " runs out of fuel in sky at time:", time)
            return False
    for plane in atGate:
        if atGate[plane][1] < 0:
            print("Error: plane No.", plane, " spends more time at gate then expected at time:", time)
            return False
    return True

def printStates(inAir, landing, atGate, departing, time):
    print("****************** States at time:", time, " *******************")
    print("inAir: \t", inAir)
    print("landing:\t", landing)
    print("atGate:\t", atGate)
    print("departing:\t", departing)
    print("**********************************************************")

def checkByTime():
    time = 0
    inAir = {}; landing = {}; atGate = {}; departing = {}
    for i in range(len(planesInfo)):
        inAir[i] = planesInfo[i][0]
    printStates(inAir, landing, atGate, departing, time)
    while inAir or landing or atGate or departing:
        if not checkState(inAir, landing, atGate, departing, time):
            return False
        for plane in timeDict:
            if timeDict[plane][0] == time:
                if plane not in inAir:
                    print("Error: plane No.", plane, " tries to land but not in air at time:", time)
                    return False
                del inAir[plane]
                landing[plane] = planesInfo[plane][1]
            if timeDict[plane][1] == time:
                if plane not in atGate:
                    print("Error: plane No.", plane, " tries to depart but not at gate at time:", time)
                    return False
                if atGate[plane][0] > 0:
                    print("Error: plane No.", plane, " tries to depart in advance at gate at time:", time)
                    return False
                del atGate[plane]
                departing[plane] = planesInfo[plane][3]
        if time == 170:
            printStates(inAir, landing, atGate, departing, time)
        if not checkState(inAir, landing, atGate, departing, time):
            return False
        minIncreaseTime = 100000
        for plane in inAir:
            if inAir[plane] < minIncreaseTime and inAir[plane] > 0: minIncreaseTime = inAir[plane]
        for plane in landing:
            if landing[plane] < minIncreaseTime and landing[plane] > 0: minIncreaseTime = landing[plane]
        for plane in atGate:
            if atGate[plane][0] < minIncreaseTime and atGate[plane][0] > 0: minIncreaseTime = atGate[plane][0]
            if atGate[plane][1] < minIncreaseTime and atGate[plane][1] > 0: minIncreaseTime = atGate[plane][1]
        for plane in departing:
            if departing[plane] < minIncreaseTime and departing[plane] > 0: minIncreaseTime = departing[plane]

        for plane in timeDict:
            if timeDict[plane][0] > time and timeDict[plane][0] - time < minIncreaseTime:
                minIncreaseTime = timeDict[plane][0] - time
            if timeDict[plane][1] > time and timeDict[plane][1] - time < minIncreaseTime:
                minIncreaseTime = timeDict[plane][1] - time
        newDeparting = {}
        for plane in departing:
            newDepartTime = departing[plane] - minIncreaseTime
            if newDepartTime > 0:
                newDeparting[plane] = newDepartTime
        for plane in atGate:
            atGate[plane][0] -= minIncreaseTime
            atGate[plane][1] -= minIncreaseTime
        newLanding = {}
        for plane in landing:
            newLandingTime = landing[plane] - minIncreaseTime
            if newLandingTime > 0:
                newLanding[plane] = newLandingTime
            else:
                atGate[plane] = [planesInfo[plane][2], planesInfo[plane][4]]
        for plane in inAir:
            inAir[plane] -= minIncreaseTime
        landing = newLanding
        departing = newDeparting
        time += minIncreaseTime
        printStates(inAir, landing, atGate, departing, time)
    return True


def main():
    global maxLanding, maxGates, maxDepart, planesInfo, timeDict
    if readInput(FILES[0]):
        maxLanding, maxGates, maxDepart, planesInfo = readInput(FILES[0])
    else:
        return -1
    timeDict = readOutput(FILES[1])
    print(timeDict)
    if not timeDict:
        return -1
    if checkByTime():
        if random.randint(0, 6666) < 2333:
            print("Error detected!")
            time.sleep(3)
            print("I'm kidding hahaha")
            time.sleep(2)
        print("     - Congratulation! The arrangement is correct! -")

if __name__ == "__main__":
    main()
