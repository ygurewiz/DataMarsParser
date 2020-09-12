import sys
#import datetime
import json

keyWords = ['LOG_FIRMWARE_VERSION',
            'LOG_FSM300_SET_DIRECTION_DIFF_DATA1',
            'LOG_FSM300_DRIVER_CALIBRATION',
            'LOG_FSM300_SET_DIRECTION_DIFF_DATA2',
            'LOG_ROBOT_STATUS_1',
            'LOG_ROBOT_STATUS_2',
            'LOG_ROBOT_STATUS_3',
            'LOG_LOW_BATTERY',
            'LOG_COMMUNICATION_RECEIVED',
            'LOG_COMMUNICATION_RESPONSE',
            'LOG_ADC_TEMPERATURE_MEASURED_VALUE',
            'LOG_ROBOT_MANAGER_HANDLE_EVENT',
            'LOG_FSM300_DRIVER_RESTART',
            'LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR',
            'LOG_FSM300_DRIVER_DATA_ANGLE_ERROR',
            'LOG_PROTOCOL_VERSION_MISMATCH',
            'LOG_TELIT_DRIVER',
            'LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS',
            'LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE',
            'LOG_ROBOT_MANAGER_PARSE_EVENT',
            'LOG_ROBOT_MANAGER_CHANGE_PARKING']

#opends log file and json result file - returns result file + lines from log
def openFiles(rFileName):
    #open input file
    try:
        rFile = open(rFileName,'r')
    except IOError: 
           print ("Log File: File does not appear to exist.")
           return
    outputfileName = str.replace(rFile.name,'.log','_PARSED.json')
    outputFile = open(outputfileName,'w+')

    lines = rFile.readlines()
    return (lines,outputFile,rFile)

#input line in log, returns string in json format for datetime
def getTimeStamp(theLine):
    dateString = str.split(theLine[0].strip(),'-')
    timeString = str.split(theLine[1].strip(),':')
    timeString.append(theLine[2].strip())
    timeStampString = dateString+timeString
    timeStamp = []
    for t in timeStampString:
        timeStamp.append(int(t.strip()))
    return timeStamp

########################################################################
#get data per key functions
def getLOG_FIRMWARE_VERSION(theLine):
    Major = int(str.split(theLine[5].strip(),',')[0].strip())
    Minor = int(str.split(theLine[7].strip(),',')[0].strip())
    Build = int(str.split(theLine[9].strip(),',')[0].strip())
    return [Major,Minor,Build]

def getLOG_FSM300_SET_DIRECTION_DIFF_DATA1(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="set:"):
            directionAfter = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="Current"):
            directionBefore = int(str.split(theLine[i+2].strip(),',')[0])
    return [directionBefore,directionAfter]

def getLOG_FSM300_DRIVER_CALIBRATION(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="Restart:"):
            directionAfter = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="before"):
            directionBefore = int(str.split(theLine[i+2].strip(),',')[0])
    return [directionBefore,directionAfter]

def getLOG_FSM300_SET_DIRECTION_DIFF_DATA2(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="yaw:"):
            weightedYaw = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="0_360:"):
            yaw = int(str.split(theLine[i+1].strip(),',')[0])
    return [weightedYaw,yaw]

def getLOG_ROBOT_STATUS_1(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="type:"):
            currentSurfaceType = str.split(theLine[i+1].strip(),',')[0].strip()
        if(s=="number:"):
            surfaceTypeAppearanceNumber = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="area:"):
            totalDesiredCleanedArea = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="segments:"):
            totalAreaOfFullyCleanedSegments = int(str.split(theLine[i+1].strip(),',')[0])
        if(i==len(theLine)-1):
            currentSegmentsSurfaceArea = int(str.split(theLine[i].strip(),',')[0])
    return [currentSurfaceType,surfaceTypeAppearanceNumber,totalDesiredCleanedArea,totalAreaOfFullyCleanedSegments,currentSegmentsSurfaceArea]

def getLOG_ROBOT_STATUS_2(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="state:"):
            robotState = str.split(theLine[i+1].strip(),',')[0].strip()
        if(s=="current"):
            robotStep = str.split(theLine[i+2].strip(),',')[0].strip()
        if(s=="segments:"):
            numFullyCleanedSegments = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="Iteration"):
            iterationInStep = int(str.split(theLine[i+3].strip(),',')[0])
        if(s=="iterations"):
            expectedNumIterations = int(str.split(theLine[i+3].strip(),',')[0])
    return [robotState,robotStep,numFullyCleanedSegments,iterationInStep,expectedNumIterations]

def getLOG_ROBOT_STATUS_3(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="direction:"):
            direction = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="roll:"):
            roll = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="pitch:"):
            pitch = int(str.split(theLine[i+1].strip(),',')[0])
        if(s=="volts):"):
            battery = float(str.split(theLine[i+1].strip(),',')[0])/10
        if(s=="events:"):
            events = int(str.split(theLine[i+1].strip(),',')[0])
    return [direction,roll,pitch,battery,events]

def getLOG_LOW_BATTERY(theLine):
    volt = int(str.split(theLine[5].strip(),',')[0])
    miliVolt = int(theLine[7].strip())
    return float(volt+miliVolt/1000)

def getLOG_COMMUNICATION_RECEIVED(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="Command:"):
            if(theLine[i+1]=='SET'):
                if(theLine[i+2]=='DIRECTION,'):
                    Command = 'SET_DIRECTION'
                elif(theLine[i+2]=='ECPOCH'):
                    Command = 'SET_TIME'
            elif(theLine[i+1]=='CHANGE'):
                Command = 'CHANGE_PARKING'
            elif(theLine[i+1]=='GET'):
                Command = 'GET_CONFIG'
            elif(theLine[i+1]=='KEEP'):
                Command = 'KEEP_ALIVE'
            elif(theLine[i+1]=='START'):
                Command = 'START_CLEAN'
            else:
                Command = ""
                print("LOG COMMUNICATION COMMAND NOT LISTED IN PARSE")
        elif(s=="Media:"):
            media = theLine[i+1].strip()
        elif(s=="Packet"):
            packetID = int(str.split(theLine[i+2].strip(),',')[0])
        elif(s=="Server"):
            serverID = int(str.split(theLine[i+2].strip(),',')[0])
        elif(s=="size:"):
            payloadSize = int(str.split(theLine[i+1].strip(),',')[0])
    return [Command,media,packetID,serverID,payloadSize]

def getLOG_COMMUNICATION_RESPONSE(theLine):
    i=-1
    for s in theLine:
        i+=1
        if(s=="ResponseCode:"):
            response = str.split(theLine[i+1],',')[0].strip()
        elif(s=="Size:"):
            size = int(theLine[i+1].strip())
    return [response,size]

def getLOG_ADC_TEMPERATURE_MEASURED_VALUE(theLine):
    internalTemperature = theLine[6].strip()
    return [internalTemperature]

def getLOG_ROBOT_MANAGER_HANDLE_EVENT(theLine):
    index = str.find(theLine[3],'LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE')
    res = ['']
    if(index==-1):
        Event = str.split(theLine[5],',')[0].strip()
        CurrentState = str.split(theLine[8],',')[0].strip()
        res = [Event,CurrentState]
        return ['LOG_ROBOT_MANAGER_HANDLE_EVENT',res]
    else:
        Oldstate = str.split(theLine[5],',')[0].strip()
        NewState = theLine[7].strip()
        res = [Oldstate,NewState]
        return ['LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE',res]

def getLOG_FSM300_DRIVER_RESTART(theLine):
    restartNumber = int(str.split(theLine[6],',')[0].strip())
    Offset = int(theLine[8].strip())
    return [restartNumber,Offset]

def getLOG_PROTOCOL_VERSION_MISMATCH(theLine):
    Major = int(str.split(theLine[7],',')[0].strip())
    Minor = int(str.split(theLine[11],',')[0].strip())
    fwMajor = int(str.split(theLine[15],',')[0].strip())
    fwMinor = int(theLine[19].strip())
    return [Major,Minor,fwMajor,fwMinor]

def getLOG_FSM300_DRIVER_DATA_ANGLE_ERROR(theLine):
    Type = str.split(theLine[5],',')[0].strip()
    value = int(str.split(theLine[7],',')[0].strip())
    previousValue = int(theLine[10].strip())
    return [Type,value,previousValue]

def getLOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR(theLine):
    Index = int(str.split(theLine[5],',')[0].strip())
    packetChecksum = int(str.split(theLine[8],',')[0].strip())
    calculatedChecksum = int(str.split(theLine[11],',')[0].strip())
    return [Index,packetChecksum,calculatedChecksum]

def getLOG_TELIT_DRIVER(theLine):
    index = str.find(theLine[3],'LOG_TELIT_DRIVER_CHANNEL')
    res = ['']
    telitStatus = str.split(theLine[6],',')[0].strip()
    if(index==-1):
        res = [telitStatus]
        return ['LOG_TELIT_DRIVER',res]
    else:
        telitChannel = int(theLine[9].strip())
        res = [telitStatus,telitChannel]
        return ['LOG_TELIT_DRIVER_CHANNEL',res]

def getLOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS(theLine):
    pitch = int(str.split(theLine[6],',')[0])
    maxTiltAllowed = int(str.split(theLine[11],',')[0])
    minTiltAllowed = int(str.split(theLine[16],',')[0])
    return [pitch,maxTiltAllowed,minTiltAllowed]

def getLOG_ROBOT_MANAGER_PARSE_EVENT(theLine):
    event = theLine[5].strip()
    return [event]

def getLOG_ROBOT_MANAGER_CHANGE_PARKING(theLine):
    res = ['']
    if(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING'):
        direction = int(theLine[5].strip())
        res = [direction]
        return ['LOG_ROBOT_MANAGER_CHANGE_PARKING',res]
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME'):
        Hour = int(str.split(theLine[5],',')[0])
        Minute = int(str.split(theLine[7],',')[0])
        minCPTime = int(str.split(theLine[12],',')[0])
        maxCPTime = int(str.split(theLine[17],',')[0])
        changeParkingTime = int(str.split(theLine[22],',')[0])
        res = [Hour,Minute,minCPTime,maxCPTime,changeParkingTime]
        return ['LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME',res]
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE'):
        pitch = int(str.split(theLine[6],',')[0])
        maxTiltAllowed = int(str.split(theLine[11],',')[0])
        minTiltAllowed = int(str.split(theLine[16],',')[0])
        res = [pitch,maxTiltAllowed,minTiltAllowed]
        return ['LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE',res]
###########################################################
#goes over log lines and sets data in json file

def logLinesAnalizer(lines,outputFile,logFileName):
    #data = json.loads()
    #json.dump(logFileName,outputFile, indent=2)
    for line in lines:
        theLine = str.split(line,' ')
        timeStamp = getTimeStamp(theLine)
        found = False
        for key in keyWords:
            index = str.find(line,key)
            if(not index==-1):
                found = True
                if(key=='LOG_FIRMWARE_VERSION'):
                    res = getLOG_FIRMWARE_VERSION(theLine)
                    json.dump({"RecordType":"LOG_FIRMWARE_VERSION","time":timeStamp,"FW:":res}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_FSM300_SET_DIRECTION_DIFF_DATA1'):
                    res = getLOG_FSM300_SET_DIRECTION_DIFF_DATA1(theLine)
                    json.dump({"RecordType":"LOG_FSM300_SET_DIRECTION_DIFF_DATA1","time":timeStamp,"directionBefore:":res[0],"directionAfter:":res[1]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_FSM300_DRIVER_CALIBRATION'):
                    res = getLOG_FSM300_DRIVER_CALIBRATION(theLine)
                    json.dump({"RecordType":"getLOG_FSM300_DRIVER_CALIBRATION","time":timeStamp,"directionBefore:":res[0],"directionAfter:":res[1]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_FSM300_SET_DIRECTION_DIFF_DATA2'):
                    res = getLOG_FSM300_SET_DIRECTION_DIFF_DATA2(theLine)
                    json.dump({"RecordType":"getLOG_FSM300_SET_DIRECTION_DIFF_DATA2","time":timeStamp,"weightedYaw:":res[0],"yaw:":res[1]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_STATUS_1'):
                    res = getLOG_ROBOT_STATUS_1(theLine)
                    json.dump({"RecordType":"LOG_ROBOT_STATUS_1","time":timeStamp,"currentSurfaceType:":res[0],"surfaceTypeAppearanceNumber:":res[1],"totalDesiredCleanedArea:":res[2],"totalAreaOfFullyCleanedSegments:":res[3],"currentSegmentsSurfaceArea:":res[4]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_STATUS_2'):
                    res = getLOG_ROBOT_STATUS_2(theLine)
                    json.dump({"RecordType":"LOG_ROBOT_STATUS_2","time":timeStamp,"robotState:":res[0],"robotStep:":res[1],"numFullyCleanedSegments:":res[2],"iterationInStep:":res[3],"expectedNumIterations:":res[4]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_STATUS_3'):
                    res = getLOG_ROBOT_STATUS_3(theLine)
                    json.dump({"RecordType":"LOG_ROBOT_STATUS_3","time":timeStamp,"direction:":res[0],"roll:":res[1],"pitch:":res[2],"battery:":res[3],"events:":res[4]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_LOW_BATTERY'):
                    res = getLOG_LOW_BATTERY(theLine)
                    json.dump({"RecordType":"LOG_LOW_BATTERY","time":timeStamp,"battery:":res}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_COMMUNICATION_RECEIVED'):
                    res = getLOG_COMMUNICATION_RECEIVED(theLine)
                    json.dump({"RecordType":"LOG_COMMUNICATION_RECEIVED","time":timeStamp,"Command:":res[0],"Media:":res[1],"packetID:":res[2],"serverID:":res[3],"payloadSize:":res[4]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_COMMUNICATION_RESPONSE'):
                    res = getLOG_COMMUNICATION_RESPONSE(theLine)
                    json.dump({"RecordType":"LOG_COMMUNICATION_RESPONSE","time":timeStamp,"response:":res[0],"size:":res[1]}, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ADC_TEMPERATURE_MEASURED_VALUE'):
                    res = getLOG_ADC_TEMPERATURE_MEASURED_VALUE(theLine)
                    json.dump({"RecordType":"LOG_ADC_TEMPERATURE_MEASURED_VALUE","time":timeStamp,"internalTemperature:":res[0] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_MANAGER_HANDLE_EVENT'):
                    res = getLOG_ROBOT_MANAGER_HANDLE_EVENT(theLine)
                    if(res[0]=='LOG_ROBOT_MANAGER_HANDLE_EVENT'):
                        json.dump({"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT","time":timeStamp,"Event:":res[1][0],"CurrentState:":res[1][1] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE'):
                        json.dump({"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE","time":timeStamp,"Oldstate:":res[1][0],"Newstate:":res[1][1] }, outputFile,separators=(',', ':'), indent=2)
                    else:
                        found = False
                elif(key=='LOG_FSM300_DRIVER_RESTART'):
                    res = getLOG_FSM300_DRIVER_RESTART(theLine)
                    json.dump({"RecordType":"LOG_FSM300_DRIVER_RESTART","time":timeStamp,"restartNumber:":res[0],"Offset:":res[1] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR'):
                    res = getLOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR(theLine)
                    json.dump({"RecordType":"LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR","time":timeStamp,"Index:":res[0],"packetChecksum:":res[1],"calculatedChecksum:":res[2] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_FSM300_DRIVER_DATA_ANGLE_ERROR'):
                    res = getLOG_FSM300_DRIVER_DATA_ANGLE_ERROR(theLine)
                    if(res[0]=='ANGLE_YAW'):
                        json.dump({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentYaw:":res[1],"previousYaw:":res[2] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='ANGLE_PITCH'):
                        json.dump({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentPitch:":res[1],"previousPitch:":res[2] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='ANGLE_ROLL'):
                        json.dump({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentRoll:":res[1],"previousRoll:":res[2] }, outputFile,separators=(',', ':'), indent=2)
                    else:
                        found = False
                elif(key=='LOG_PROTOCOL_VERSION_MISMATCH'):
                    res = getLOG_PROTOCOL_VERSION_MISMATCH(theLine)
                    json.dump({"RecordType":"LOG_PROTOCOL_VERSION_MISMATCH","time":timeStamp,"Major:":res[0],"Minor:":res[1],"FWMajor:":res[2],"FWMinor:":res[3] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_TELIT_DRIVER'):
                    res = getLOG_TELIT_DRIVER(theLine)
                    if(res[0]=='LOG_TELIT_DRIVER'):
                        json.dump({"RecordType":"LOG_TELIT_DRIVER","time":timeStamp,"telitStatus:":res[1][0] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='LOG_TELIT_DRIVER_CHANNEL'):
                        json.dump({"RecordType":"LOG_TELIT_DRIVER_CHANNEL","time":timeStamp,"telitStatus:":res[1][0],"telitChannel:":res[1][1] }, outputFile,separators=(',', ':'), indent=2)
                    else:
                        found = False
                elif(key=='LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS'):
                    res = getLOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS(theLine)
                    json.dump({"RecordType":"LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS","time":timeStamp,"pitch:":res[0],"maxTiltAllowed:":res[1],"minTiltAllowed:":res[2] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_MANAGER_PARSE_EVENT'):
                    res = getLOG_ROBOT_MANAGER_PARSE_EVENT(theLine)
                    json.dump({"RecordType":"LOG_ROBOT_MANAGER_PARSE_EVENT","time":timeStamp,"event:":res[0] }, outputFile,separators=(',', ':'), indent=2)
                elif(key=='LOG_ROBOT_MANAGER_CHANGE_PARKING'):
                    res = getLOG_ROBOT_MANAGER_CHANGE_PARKING(theLine)
                    if(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING'):
                        json.dump({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING","time":timeStamp,"direction:":res[1][0] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME'):
                        json.dump({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME","time":timeStamp,"Hour:":res[1][0],"Minute:":res[1][1],"minCPTime:":res[1][2],"maxCPTime:":res[1][3],"changeParkingTime:":res[1][4] }, outputFile,separators=(',', ':'), indent=2)
                    elif(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE'):
                        json.dump({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE","time":timeStamp,"pitch:":res[1][0],"maxTiltAllowed:":res[1][1],"minTiltAllowed:":res[1][2] }, outputFile,separators=(',', ':'), indent=2)
                    else:
                        found = False
        if(not found):
            print(line)
#primitive clean json concat wrong...
def cleanJson(outputFile):
    lines = []
    with open(outputFile.name) as doneJson:
        for l in doneJson:
            if(str.find(l,'}{')>-1):
                l = str.replace(l,'}{\n','},\n{')
            lines.append(l)
        doneJson.close()
    with open(outputFile.name,'w') as doneJson:
        doneJson.writelines(lines)
        doneJson.close()


def main(argv):
    (lines,outputFile,logFile)  = openFiles(argv[1])
    logLinesAnalizer(lines,outputFile,logFile.name)
    logFile.close()
    outputFile.close()
    cleanJson(outputFile)       #clean errors }{
    

if __name__ == "__main__":
    main(sys.argv)

