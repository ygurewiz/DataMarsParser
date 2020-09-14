import sys
import datetime
import json

keyWords = ['FIRMWARE_VERSION',
            'FSM300',
            'ROBOT_STATUS',
            'LOW_BATTERY',
            'COMMUNICATION',
            'ADC_TEMPERATURE_MEASURED_VALUE',
            'ROBOT_MANAGER',
            'PROTOCOL_VERSION_MISMATCH',
            'TELIT_DRIVER',
            'STEP',
            'MOVEMENT',
            'LOCATION',
            'SENSORS',
            'ENCODERS_ID_EVENT',
            'MAGNET',
            'SYSTEM',
            'PROCEDURE_START',
            'START_TASK',
            'POWER_RESET']

#opends log file and json result file - returns result file + lines from log
def openFiles(rFileName):
    #open input file
    try:
        rFile = open(rFileName,'r')
    except IOError: 
           print ("Log File: File does not appear to exist.")
           return
    #open run log file
    try:
        runLogFile = open(rFileName+'_'+'RUN_LOG.log','w+')
    except IOError: 
           print ("Log File: File does not appear to exist.")
           return
    outputfileName = str.replace(rFile.name,'.log','_PARSED.json')
    outputFile = open(outputfileName,'w+')

    lines = rFile.readlines()
    return (lines,outputFile,rFile,runLogFile)

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
def getLOG_START_TASK(timeStamp,theLine):
    if(theLine[3]=='LOG_START_TASK'):
        taskId = int(str.split(theLine[6],',')[0])
        fileNameStr = theLine[9].strip()
        if(fileNameStr=='COMMUNICATION' or fileNameStr=='SENSORS' or fileNameStr=='ROBOT'):
            fileName =fileNameStr +'_'+ str.split(theLine[10],',')[0]
            lineNumber = int(theLine[13].strip())
            res = [taskId,fileName,lineNumber]
            return {"RecordType":"LOG_START_TASK","time":timeStamp,"taskId":res[0],"fileName":res[1],"lineNumber":res[2]}
        elif(fileNameStr=='TECHNICIAN,' or fileNameStr=='LOGGER,' or fileNameStr=='WATCHDOG,'):
            fileName =str.split(fileNameStr,',')[0]
            lineNumber = int(theLine[12].strip())
            res = [taskId,fileName,lineNumber]
            return {"RecordType":"LOG_START_TASK","time":timeStamp,"taskId":res[0],"fileName":res[1],"lineNumber":res[2]}
        else:
            return {}
    else:
        return {}
def getLOG_POWER_RESET(timeStamp,theLine):
    if(theLine[3]=='LOG_POWER_RESET'):
        event = 'power_reset'
        return {"RecordType":"LOG_POWER_RESET","time":timeStamp,"event":event}
    else:
        return {}
def getLOG_FIRMWARE_VERSION(timeStamp,theLine):
    if(theLine[3]=='LOG_FIRMWARE_VERSION'):
        Major = int(str.split(theLine[5].strip(),',')[0].strip())
        Minor = int(str.split(theLine[7].strip(),',')[0].strip())
        Build = int(str.split(theLine[9].strip(),',')[0].strip())
        res= [Major,Minor,Build]
        return {"RecordType":"LOG_FIRMWARE_VERSION","time":timeStamp,"FW:":res}
    else:
        return {}
def getLOG_FSM300(timeStamp,theLine):
    if(theLine[3]=='LOG_FSM300_SET_DIRECTION_DIFF_DATA1'):
        callingFunction = theLine[6].strip()+'_'+str.split(theLine[7].strip(),',')[0]
        directionAfter = int(str.split(theLine[11].strip(),',')[0])
        direction = int(str.split(theLine[14].strip(),',')[0])
        callibrationOffset = int(str.split(theLine[17].strip(),',')[0])
        yaw = int(theLine[20].strip())
        res= [callingFunction,directionAfter,direction,callibrationOffset,yaw]
        return {"RecordType":"LOG_FSM300_SET_DIRECTION_DIFF_DATA1","time":timeStamp,"callingFunction:":res[0],"directionAfter:":res[1],"direction:":res[2],"callibrationOffset:":res[3],"yaw:":res[4]}
    elif(theLine[3]=='LOG_FSM300_DRIVER_CALIBRATION'):
        directionAfter = int(str.split(theLine[7].strip(),',')[0])
        directionBefore = int(str.split(theLine[12].strip(),',')[0])
        res= [directionBefore,directionAfter]
        return {"RecordType":"LOG_FSM300_DRIVER_CALIBRATION","time":timeStamp,"directionBefore:":res[0],"directionAfter:":res[1]}
    elif(theLine[3]=='LOG_FSM300_SET_DIRECTION_DIFF_DATA2'):
        weightedYaw = int(str.split(theLine[6].strip(),',')[0])
        yaw = int(theLine[9].strip())
        res= [weightedYaw,yaw]
        return {"RecordType":"LOG_FSM300_SET_DIRECTION_DIFF_DATA2","time":timeStamp,"weightedYaw:":res[0],"yaw:":res[1]}
    elif(theLine[3]=='LOG_FSM300_DRIVER_RESTART'):
        restartNumber = int(str.split(theLine[6],',')[0].strip())
        Offset = int(theLine[8].strip())
        res= [restartNumber,Offset]
        return {"RecordType":"LOG_FSM300_DRIVER_RESTART","time":timeStamp,"restartNumber:":res[0],"Offset:":res[1] }
    elif(theLine[3]=='LOG_FSM300_DRIVER_DATA_ANGLE_ERROR'):
        Type = str.split(theLine[5],',')[0].strip()
        value = int(str.split(theLine[7],',')[0].strip())
        previousValue = int(theLine[10].strip())
        res= [Type,value,previousValue]
        if(res[0]=='ANGLE_YAW'):
            return {"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentYaw:":res[1],"previousYaw:":res[2] }
        elif(res[0]=='ANGLE_PITCH'):
            return {"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentPitch:":res[1],"previousPitch:":res[2] }
        elif(res[0]=='ANGLE_ROLL'):
            return {"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentRoll:":res[1],"previousRoll:":res[2] }
        else:
            return {}
    elif(theLine[3]=='LOG_FSM300_DRIVER_ACCELEROMETER_TOLERANCE'):
        accelerometrTollerance = int(theLine[6].strip())
        res= [accelerometrTollerance]
        return {"RecordType":"LOG_FSM300_DRIVER_ACCELEROMETER_TOLERANCE","time":timeStamp,"accelerometrTollerance:":res[0] }
    elif(theLine[3]=='LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR'):
        Index = int(str.split(theLine[5],',')[0].strip())
        packetChecksum = int(str.split(theLine[8],',')[0].strip())
        calculatedChecksum = int(str.split(theLine[11],',')[0].strip())
        res= [Index,packetChecksum,calculatedChecksum]
        return {"RecordType":"LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR","time":timeStamp,"Index:":res[0],"packetChecksum:":res[1],"calculatedChecksum:":res[2] }
    else:
        return {}
def getLOG_ROBOT_STATUS(timeStamp,theLine):
    if(theLine[3]=='LOG_ROBOT_STATUS_1'):
        currentSurfaceType = str.split(theLine[7].strip(),',')[0]
        surfaceTypeAppearanceNumber = int(str.split(theLine[12].strip(),',')[0])
        totalDesiredCleanedArea = int(str.split(theLine[17].strip(),',')[0])
        totalAreaOfFullyCleanedSegments = int(str.split(theLine[24].strip(),',')[0])
        currentSegmentsSurfaceArea = int(theLine[29].strip())
        res= [currentSurfaceType,surfaceTypeAppearanceNumber,totalDesiredCleanedArea,totalAreaOfFullyCleanedSegments,currentSegmentsSurfaceArea]
        return {"RecordType":"LOG_ROBOT_STATUS_1","time":timeStamp,"currentSurfaceType:":res[0],"surfaceTypeAppearanceNumber:":res[1],"totalDesiredCleanedArea:":res[2],"totalAreaOfFullyCleanedSegments:":res[3],"currentSegmentsSurfaceArea:":res[4]}
    elif(theLine[3]=='LOG_ROBOT_STATUS_2'):
        robotState = str.split(theLine[6].strip(),',')[0]
        robotStep = str.split(theLine[10].strip(),',')[0]
        numFullyCleanedSegments = int(str.split(theLine[16],',')[0])
        iterationInStep = int(str.split(theLine[20],',')[0])
        expectedNumIterations = int(theLine[27].strip())
        res= [robotState,robotStep,numFullyCleanedSegments,iterationInStep,expectedNumIterations]
        return {"RecordType":"LOG_ROBOT_STATUS_2","time":timeStamp,"robotState:":res[0],"robotStep:":res[1],"numFullyCleanedSegments:":res[2],"iterationInStep:":res[3],"expectedNumIterations:":res[4]}
    elif(theLine[3]=='LOG_ROBOT_STATUS_3'):
        direction = int(str.split(theLine[7],',')[0])
        roll = int(str.split(theLine[11],',')[0])
        pitch = int(str.split(theLine[15],',')[0])
        battery = float(str.split(theLine[20],',')[0])/10
        events = int(theLine[23].strip())
        res= [direction,roll,pitch,battery,events]
        return {"RecordType":"LOG_ROBOT_STATUS_3","time":timeStamp,"direction:":res[0],"roll:":res[1],"pitch:":res[2],"battery:":res[3],"events:":res[4]}        
    else:
        return {}
def getLOG_LOW_BATTERY(timeStamp,theLine):
    if(theLine[3]=='LOG_LOW_BATTERY'):
        volt = int(str.split(theLine[5].strip(),',')[0])
        miliVolt = int(theLine[7].strip())
        res= float(volt+miliVolt/1000)
        return {"RecordType":"LOG_LOW_BATTERY","time":timeStamp,"battery:":res}
    else:
        return {}
def getLOG_COMMUNICATION(timeStamp,theLine):
    if(theLine[3]=='LOG_COMMUNICATION_RECEIVED'):
        if(theLine[5]=='ABORT'):
            Command = 'ABORT_AND_GO_HOME'
            media = theLine[10].strip()+'_'+str.split(theLine[11].strip(),',')[0]
            packetID = int(str.split(theLine[14],',')[0])
            serverID = int(str.split(theLine[17],',')[0])
            payloadSize = int(theLine[20].strip())
        elif(theLine[5]=='GET'):
            Command = 'GET_CONFIGURATION'
            media = theLine[8].strip()+'_'+str.split(theLine[9].strip(),',')[0]
            packetID = int(str.split(theLine[12],',')[0])
            serverID = int(str.split(theLine[15],',')[0])
            payloadSize = int(theLine[18].strip())
        elif(theLine[5]=='SET'):
            if(theLine[6]=='ECPOCH'):
                Command = 'SET_ECPOCH_TIME'
                media = theLine[9].strip()+'_'+str.split(theLine[10].strip(),',')[0]
                packetID = int(str.split(theLine[13],',')[0])
                serverID = int(str.split(theLine[16],',')[0])
                payloadSize = int(theLine[19].strip())
            else:
                Command = 'SET_CONFIGURATION'
                media = theLine[8].strip()+'_'+str.split(theLine[9].strip(),',')[0]
                packetID = int(str.split(theLine[12],',')[0])
                serverID = int(str.split(theLine[15],',')[0])
                payloadSize = int(theLine[18].strip())
        elif(theLine[5]=='KEEP'):
            Command = 'KEEP_ALIVE'
            media = theLine[8].strip()+'_'+str.split(theLine[9].strip(),',')[0]
            packetID = int(str.split(theLine[12],',')[0])
            serverID = int(str.split(theLine[15],',')[0])
            payloadSize = int(theLine[18].strip())
        res= [Command,media,packetID,serverID,payloadSize]
        return {"RecordType":"LOG_COMMUNICATION_RECEIVED","time":timeStamp,"Command:":res[0],"Media:":res[1],"packetID:":res[2],"serverID:":res[3],"payloadSize:":res[4]}
    elif(theLine[3]=='LOG_COMMUNICATION_RESPONSE'):
        response = str.split(theLine[5],',')[0]
        size = int(theLine[7].strip())
        res= [response,size]
        return {"RecordType":"LOG_COMMUNICATION_RESPONSE","time":timeStamp,"response:":res[0],"size:":res[1]}
    elif(theLine[3]=='LOG_COMMUNICATION_FAILED_SET_DEVICE_IN_CONFIG_MODE'):
        response = 'failed_set_config'
        res = [response]
        return {"RecordType":"LOG_COMMUNICATION_FAILED_SET_DEVICE_IN_CONFIG_MODE","time":timeStamp,"response:":res[0]}
    elif(theLine[3]=='LOG_COMMUNICATION_INVALID_COMMAND'):
        ErrorCode = str.split(theLine[6],',')[0]
        packetID = int(str.split(theLine[9],',')[0])
        serverID = int(str.split(theLine[12],',')[0])
        media = theLine[14].strip()+'_'+str.split(theLine[15].strip(),',')[0]
        robotState = theLine[19].strip()
        res = [ErrorCode,packetID,serverID,media,robotState]
        return {"RecordType":"LOG_COMMUNICATION_INVALID_COMMAND","time":timeStamp,"ErrorCode:":res[0],"packetID:":res[1],"serverID:":res[2],"media:":res[3],"robotState:":res[4]}
    else:
        return {}
def getLOG_ADC_TEMPERATURE_MEASURED_VALUE(timeStamp,theLine):
    if(theLine[3]=='LOG_ADC_TEMPERATURE_MEASURED_VALUE'):
        internalTemperature = theLine[6].strip()
        res = [internalTemperature]
        return {"RecordType":"LOG_ADC_TEMPERATURE_MEASURED_VALUE","time":timeStamp,"internalTemperature:":res[0] }
    else:
        return {}
def getLOG_ROBOT_MANAGER(timeStamp,theLine):
    if(theLine[3]=='LOG_ROBOT_MANAGER_GO_HOME'):
        retVal = theLine[5].strip()
        res = [retVal]
        return {"RecordType":"LOG_ROBOT_MANAGER_GO_HOME","time":timeStamp,"retVal:":res[0] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE'):
        Oldstate = str.split(theLine[5],',')[0].strip()
        NewState = theLine[7].strip()
        res = [Oldstate,NewState]
        return {"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE","time":timeStamp,"Oldstate:":res[0],"Newstate:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_HANDLE_EVENT'):
        Event = str.split(theLine[5],',')[0].strip()
        CurrentState = str.split(theLine[8],',')[0].strip()
        res = [Event,CurrentState]
        return {"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT","time":timeStamp,"Event:":res[0],"CurrentState:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS'):
        pitch = int(str.split(theLine[6],',')[0])
        maxTiltAllowed = int(str.split(theLine[11],',')[0])
        minTiltAllowed = int(str.split(theLine[16],',')[0])
        res= [pitch,maxTiltAllowed,minTiltAllowed]
        return {"RecordType":"LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS","time":timeStamp,"pitch:":res[0],"maxTiltAllowed:":res[1],"minTiltAllowed:":res[2] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_PARSE_EVENT'):
        event = theLine[5].strip()
        res= [event]
        return {"RecordType":"LOG_ROBOT_MANAGER_PARSE_EVENT","time":timeStamp,"event:":res[0] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN'):
        pitch = int(str.split(theLine[5],',')[0].strip())
        readCountBelowMaxTiltAllowed = int(theLine[12].strip())
        res= [pitch,readCountBelowMaxTiltAllowed]
        return {"RecordType":"LOG_ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN","time":timeStamp,"pitch:":res[0],"readCountBelowMaxTiltAllowed:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_START_CLEAN'):
        cleanProcedure = theLine[6].strip()
        res= [cleanProcedure]
        return {"RecordType":"LOG_ROBOT_MANAGER_START_CLEAN","time":timeStamp,"cleanProcedure:":res[0] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CLEANING_DONE'):
        cleanProcedure = str.split(theLine[6],',')[0].strip()
        returnValue = theLine[9].strip()
        res= [cleanProcedure,returnValue]
        return {"RecordType":"LOG_ROBOT_MANAGER_CLEANING_DONE","time":timeStamp,"cleanProcedure:":res[0],"returnValue:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING'):
        direction = int(theLine[5].strip())
        res = [direction]
        return {"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING","time":timeStamp,"direction:":res[0] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME'):
        Hour = int(str.split(theLine[5],',')[0])
        Minute = int(str.split(theLine[7],',')[0])
        minCPTime = int(str.split(theLine[12],',')[0])
        maxCPTime = int(str.split(theLine[17],',')[0])
        changeParkingTime = int(str.split(theLine[22],',')[0])
        res = [Hour,Minute,minCPTime,maxCPTime,changeParkingTime]
        return {"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME","time":timeStamp,"Hour:":res[0],"Minute:":res[1],"minCPTime:":res[2],"maxCPTime:":res[3],"changeParkingTime:":res[4] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE'):
        pitch = int(str.split(theLine[6],',')[0])
        maxTiltAllowed = int(str.split(theLine[11],',')[0])
        minTiltAllowed = int(str.split(theLine[16],',')[0])
        res = [pitch,maxTiltAllowed,minTiltAllowed]
        return {"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE","time":timeStamp,"pitch:":res[0],"maxTiltAllowed:":res[1],"minTiltAllowed:":res[2] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA'):
        rightSensor = int(str.split(theLine[7],',')[0].strip())
        leftSensor = int(str.split(theLine[11],',')[0].strip())
        res = [rightSensor,leftSensor]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA","time":timeStamp,"rightSensor:":res[0],"leftSensor:":res[1]  }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_ERROR'):
        status = str.split(theLine[5],',')[0].strip()
        retVal = str.split(theLine[7],',')[0].strip()
        res = [status,retVal]
        return {"RecordType":"LOG_ROBOT_MANAGER_ERROR","time":timeStamp,"status:":res[0],"retVal:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_TIME_DURATION'):
        timerDuration = int(str.split(theLine[6],',')[0])
        printTimeDuration = int(theLine[10].strip())
        res = [timerDuration,printTimeDuration]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_TIME_DURATION","time":timeStamp,"timerDuration:":res[0],"printTimeDuration:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_SENSORS_ARRAY'):
        sensorTime = int(str.split(theLine[5],',')[0].strip())
        sensorsId = str.split(theLine[7],',')[0].strip()
        if(sensorsId=='FRONT_LEFT_SENSOR'):
            rightSensor = 0
            leftSensor = int(str.split(theLine[9],',')[0].strip())
        elif(sensorsId=='FRONT_RIGHT_SENSOR'):
            leftSensor = 0
            rightSensor = int(str.split(theLine[9],',')[0].strip())
        res =  [sensorTime,sensorsId,rightSensor,leftSensor]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SENSORS_ARRAY","time":timeStamp,"sensorTime:":res[0],"sensorsId:":res[1],"rightSensor:":res[2],"leftSensor:":res[3] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_ACCEL_DATA'):
        yaw = int(str.split(theLine[5],',')[0])
        roll = int(str.split(theLine[7],',')[0])
        pitch = int(theLine[9].strip())
        res =  [yaw,roll,pitch]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_ACCEL_DATA","time":timeStamp,"yaw:":res[0],"roll:":res[1],"pitch:":res[2] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_OS_EVENTS_DATA'):
        lowLevelOSEvents = int(str.split(theLine[7],',')[0])
        lowLevelOSEvents = int(str.split(theLine[11],',')[0])
        robotManagerOSEvents = int(theLine[16].strip())
        res =  [lowLevelOSEvents,lowLevelOSEvents,robotManagerOSEvents]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_OS_EVENTS_DATA","time":timeStamp,"lowLevelOSEvents:":res[0],"lowLevelOSEvents:":res[1],"robotManagerOSEvents:":res[2] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_STACK_0_1_DATA'):
        stack0Size = int(str.split(theLine[6],',')[0])
        stack0Used = int(str.split(theLine[9],',')[0])
        stack1Size = int(str.split(theLine[12],',')[0])
        stack1Used = int(theLine[15].strip())
        res =  [stack0Size,stack0Used,stack1Size,stack1Used]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_STACK_0_1_DATA","time":timeStamp,"stack0Size:":res[0],"stack0Used:":res[1],"stack1Size:":res[2],"stack0Used:":res[3] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_STACK_2_3_DATA'):
        stack2Size = int(str.split(theLine[6],',')[0])
        stack2Used = int(str.split(theLine[9],',')[0])
        stack3Size = int(str.split(theLine[12],',')[0])
        stack3Used = int(theLine[15].strip())
        res =  [stack2Size,stack2Used,stack3Size,stack3Used]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_STACK_2_3_DATA","time":timeStamp,"stack2Size:":res[0],"stack2Used:":res[1],"stack3Size:":res[2],"stack3Used:":res[3] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_STACK_4_DATA'):
        stack4Size = int(str.split(theLine[6],',')[0])
        stack4Used = int(str.split(theLine[9],',')[0])
        res =  [stack4Size,stack4Used]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_STACK_4_DATA","time":timeStamp,"stack4Size:":res[0],"stack4Used:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY'):
        errors = int(theLine[6].strip())
        res = [errors]
        return {"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY","time":timeStamp,"errors:":res[0] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO'):
        systemEvent = int(str.split(theLine[6],',')[0].strip())
        currentState = theLine[9].strip()
        res = [systemEvent,currentState]
        return {"RecordType":"LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO","time":timeStamp,"systemEvent:":res[0],"currentState:":res[1] }
    elif(theLine[3]=='LOG_ROBOT_MANAGER_PARKED'):
        retVal = 'robot_parked'
        res = [retVal]
        return {"RecordType":"LOG_ROBOT_MANAGER_PARKED","time":timeStamp,"retVal:":res[0] }
    else:
        return {}
def getLOG_PROTOCOL_VERSION_MISMATCH(timeStamp,theLine):
    if(theLine[3]=='LOG_PROTOCOL_VERSION_MISMATCH'):
        Major = int(str.split(theLine[7],',')[0].strip())
        Minor = int(str.split(theLine[11],',')[0].strip())
        fwMajor = int(str.split(theLine[15],',')[0].strip())
        fwMinor = int(theLine[19].strip())
        res= [Major,Minor,fwMajor,fwMinor]
        return {"RecordType":"LOG_PROTOCOL_VERSION_MISMATCH","time":timeStamp,"Major:":res[0],"Minor:":res[1],"FWMajor:":res[2],"FWMinor:":res[3] }
    else:
        return {}
def getLOG_TELIT_DRIVER(timeStamp,theLine):
    if(theLine[3]=='LOG_TELIT_DRIVER'):
        telitStatus = str.split(theLine[6],',')[0].strip()
        res = [telitStatus]
        return {"RecordType":"LOG_TELIT_DRIVER","time":timeStamp,"telitStatus:":res[0] }
    elif(theLine[3]=='LOG_TELIT_DRIVER_CHANNEL'):
        telitStatus = str.split(theLine[6],',')[0].strip()
        telitChannel = int(theLine[9].strip())
        res = [telitStatus,telitChannel]
        return {"RecordType":"LOG_TELIT_DRIVER_CHANNEL","time":timeStamp,"telitStatus:":res[0],"telitChannel:":res[1] }
    else:
        return {}
def getLOG_STEP(timeStamp,theLine):
    if(theLine[3]=='LOG_STEP_START'):
        step = str.split(theLine[5],',')[0].strip()
        res = [step]
        return {"RecordType":"LOG_STEP_START","time":timeStamp,"step:":res[0] }
    elif(theLine[3]=='LOG_STEP_START_EDGE_MOVE'):
        step = str.split(theLine[5],',')[0].strip()
        toEdge = str.split(theLine[7],',')[0].strip()
        direcionTo = int(theLine[9].strip())
        res = [step,toEdge,direcionTo]
        return {"RecordType":"LOG_STEP_START_EDGE_MOVE","time":timeStamp,"step:":res[0],"toEdge:":res[1],"direcionTo:":res[2] }
    elif(theLine[3]=='LOG_STEP_START_CROSS_BRIDGE'):
        step = str.split(theLine[5],',')[0].strip()
        closestEdge = str.split(theLine[8],',')[0].strip()
        directionToEdge = str.split(theLine[10],',')[0].strip()
        res = [step,closestEdge,directionToEdge]
        return {"RecordType":"LOG_STEP_START_CROSS_BRIDGE","time":timeStamp,"step:":res[0],"closestEdge:":res[1],"directionToEdge:":res[2] }
    elif(theLine[3]=='LOG_STEP_START_CALIBRATION'):
        step = str.split(theLine[5],',')[0].strip()
        calibrationDirection = theLine[8].strip()
        res =  [step,calibrationDirection]
        return {"RecordType":"LOG_STEP_START_CALIBRATION","time":timeStamp,"step:":res[0],"calibrationDirection:":res[1] }
    elif(theLine[3]=='LOG_STEP_END'):
        step = str.split(theLine[5],',')[0].strip()
        returnValue = theLine[8].strip()
        res= [step,returnValue]
        return {"RecordType":"LOG_STEP_END","time":timeStamp,"step:":res[0],"returnValue:":res[1] }
    elif(theLine[3]=='LOG_STEP_EDGE_END'):
        movement = 'edge_move'
        step = str.split(theLine[5],',')[0].strip()
        returnValue = str.split(theLine[8],',')[0].strip()
        yaw = int(str.split(theLine[10],',')[0].strip())
        roll = int(str.split(theLine[12],',')[0].strip())
        pitch = int(theLine[14].strip())
        res= [movement,step,returnValue,yaw,roll,pitch]
        return {"RecordType":"LOG_STEP_EDGE_END","time":timeStamp,"movement:":res[0],"step:":res[1],"returnValue:":res[2],"yaw:":res[3],"roll:":res[4],"pitch:":res[5] }
    elif(theLine[3]=='LOG_STEP_ERROR'):
        retVal = theLine[5].strip()
        res= [retVal]
        return {"RecordType":"LOG_STEP_ERROR","time":timeStamp,"retVal:":res[0] }
    else:
        return {}
def getLOG_MOVEMENT(timeStamp,theLine):
    if(theLine[3]=='LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT'):
        movement = 'direction_deviation'
        directionDeviationAbsValue =  int(str.split(theLine[8],',')[0].strip())
        direcionTo = int(str.split(theLine[11],',')[0].strip())
        direction = int(theLine[15].strip())
        res = [movement,directionDeviationAbsValue,direcionTo,direction]
        return {"RecordType":"LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT","time":timeStamp,"movement:":res[0],"directionDeviationAbsValue:":res[1],"direcionTo:":res[2],"direction:":res[3] }
    elif(theLine[3]=='LOG_MOVEMENT_EDGE_MOVEMENT_END'):
        movement = 'end_move'
        moveReturnValue = theLine[6].strip()
        res = [movement,moveReturnValue]
        return {"RecordType":"LOG_MOVEMENT_EDGE_MOVEMENT_END","time":timeStamp,"movement:":res[0],"moveReturnValue:":res[1] }
    elif(theLine[3]=='LOG_MOVEMENT_EDGE_MOVEMENT_START'):
        movement = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(str.split(theLine[12],',')[0].strip())
        headingStr = bool(str.split(theLine[14],',')[0].strip())
        if(headingStr):
            heading = 'forward'
        else:
            heading = 'reverse'
        pulses = int(theLine[17].strip())
        res = [movement,direction,direcionTo,heading,pulses]
        return {"RecordType":"LOG_MOVEMENT_EDGE_MOVEMENT_START","time":timeStamp,"movement:":res[0],"direction:":res[1],"direcionTo:":res[2],"heading:":res[3] ,"pulses:":res[4]}
    elif(theLine[3]=='LOG_MOVEMENT_END_DIRECTION'):
        movement = 'end_direction_move'
        moveReturnValue = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,moveReturnValue,direction]
        return {"RecordType":"LOG_MOVEMENT_END_DIRECTION","time":timeStamp,"movement:":res[0],"moveReturnValue:":res[1],"direction:":res[2] }
    elif(theLine[3]=='LOG_MOVEMENT_ERROR'):
        movement = 'movement_error'
        moveErrorStatus = str.split(theLine[5],',')[0].strip()
        moveReturnValue = theLine[7].strip()
        res =  [movement,moveErrorStatus,moveReturnValue]
        return {"RecordType":"LOG_MOVEMENT_ERROR","time":timeStamp,"movement:":res[0],"moveErrorStatus:":res[1],"moveReturnValue:":res[2] }
    elif(theLine[3]=='LOG_MOVEMENT_FINE_TUNING_TURN_START'):
        movement = 'rotation'
        rotationType = 'fine_tuning' 
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res =  [movement,rotationType,rotationDirection,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_FINE_TUNING_TURN_START","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"rotationDirection:":res[2],"direction:":res[3],"direcionTo:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_FULL_SPEED_TURN_START'):
        movement = 'rotation'
        rotationType = 'full_speed' 
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res =  [movement,rotationType,rotationDirection,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_FULL_SPEED_TURN_START","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"rotationDirection:":res[2],"direction:":res[3],"direcionTo:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT'):
        movement = str.split(theLine[9],',')[0].strip()
        movementType = str.split(theLine[5],',')[0].strip()
        sensor = str.split(theLine[7],',')[0].strip()
        direction = int(str.split(theLine[11],',')[0].strip())
        miliSecondsToFindEdge = int(theLine[19].strip())
        res =  [movement,movementType,sensor,direction,miliSecondsToFindEdge]
        return {"RecordType":"LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT","time":timeStamp,"movement:":res[0],"movementType:":res[1],"sensor:":res[2],"direction:":res[3],"miliSecondsToFindEdge:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT'):
        movement = theLine[7].strip()
        status = str.split(theLine[5],',')[0].strip()
        res =  [status,movement]
        return {"RecordType":"LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT","time":timeStamp,"status:":res[0],"movement:":res[1]}
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT'):
        movement = 'direction_inner_correction'
        direction = int(str.split(theLine[6],',')[0].strip())
        directionDiff = int(str.split(theLine[9],',')[0].strip())
        correctionState = theLine[12].strip()
        res =  [movement,direction,directionDiff,correctionState]
        return {"RecordType":"LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT","time":timeStamp,"movement:":res[0],"direction:":res[1],"directionDiff:":res[2],"correctionState:":res[3] }
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT'):
        status = theLine[5].strip()
        res =  [status]
        return {"RecordType":"LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT","time":timeStamp,"status:":res[0] }
    elif(theLine[3]=='LOG_MOVEMENT_INNER_MOVEMENT_END'):
        movement = 'end_inner_move'
        moveReturnValue = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        movementType = theLine[12].strip()
        res = [movement,moveReturnValue,direction,movementType]
        return {"RecordType":"LOG_MOVEMENT_INNER_MOVEMENT_END","time":timeStamp,"movement:":res[0],"moveReturnValue:":res[1],"direction:":res[2],"movementType:":res[3] }
    elif(theLine[3]=='LOG_MOVEMENT_INNER_MOVEMENT_START'):
        movement = 'start_inner_move'
        movementType = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(str.split(theLine[12],',')[0].strip())
        headingStr = bool(str.split(theLine[14],',')[0].strip())
        if(headingStr):
            heading = 'forward'
        else:
            heading = 'reverse'
        pulses = int(theLine[17].strip())
        res = [movement,movementType,direction,direcionTo,heading,pulses]
        return {"RecordType":"LOG_MOVEMENT_INNER_MOVEMENT_START","time":timeStamp,"movement:":res[0],"movementType:":res[1],"direction:":res[2],"direcionTo:":res[3],"heading:":res[4],"pulses:":res[5] }
    elif(theLine[3]=='LOG_MOVEMENT_SINGLE_WHEEL_TURN_START'):
        movement = 'rotation'
        rotationType = 'A_turn'
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res = [movement,rotationType,rotationDirection,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_SINGLE_WHEEL_TURN_START","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"rotationDirection:":res[2],"direction:":res[3],"direcionTo:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START'):
        movement = 'direction_sensor'
        direction = int(str.split(theLine[6],',')[0].strip())
        motorToTurn = theLine[10].strip() + '_' + str.split(theLine[11],',')[0].strip()
        motorTurningDirection = theLine[15].strip() + '_' +theLine[16].strip() + '_' + str.split(theLine[17],',')[0].strip()
        sensorState = theLine[20].strip() + '_' +theLine[21].strip()
        res = [movement,direction,motorToTurn,motorTurningDirection,sensorState]
        return {"RecordType":"LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START","time":timeStamp,"movement:":res[0],"direction:":res[1],"motorToTurn:":res[2],"motorTurningDirection:":res[3],"sensorState:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_START'):
        movement = 'start_move'
        movementType = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(str.split(theLine[12],',')[0].strip())
        headingStr = bool(str.split(theLine[14],',')[0].strip())
        if(headingStr):
            heading = 'forward'
        else:
            heading = 'reverse'
        pulses = int(theLine[17].strip())
        res = [movement,movementType,direction,direcionTo,heading,pulses]
        return {"RecordType":"LOG_MOVEMENT_START","time":timeStamp,"movement:":res[0],"movementType:":res[1],"direction:":res[2],"direcionTo:":res[3],"heading:":res[4],"pulses:":res[5] }
    elif(theLine[3]=='LOG_MOVEMENT_TURN_FINE_TUNING_FAIL'):
        movement = 'rotation'
        rotationType = 'fine_tuning' 
        returnStatus = str.split(theLine[6],',')[0].strip()
        direcionTo = int(str.split(theLine[9],',')[0].strip())
        diffDirection = int(theLine[11].strip())
        res =  [movement,rotationType,returnStatus,direcionTo,diffDirection]
        return {"RecordType":"LOG_MOVEMENT_TURN_FINE_TUNING_FAIL","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"returnStatus:":res[2],"direcionTo:":res[3],"diffDirection:":res[4] }
    elif(theLine[3]=='LOG_MOVEMENT_TURN_IS_FINISHED'):
        movement = 'rotation_end'
        rotationType = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,rotationType,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_TURN_IS_FINISHED","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"direction:":res[2],"direcionTo:":res[3]}
    elif(theLine[3]=='LOG_MOVEMENT_TURN_MOVEMENT_END'):
        movement = 'rotation_end'
        returnValue = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,returnValue,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_TURN_MOVEMENT_END","time":timeStamp,"movement:":res[0],"returnValue:":res[1],"direction:":res[2],"direcionTo:":res[3] }
    elif(theLine[3]=='LOG_MOVEMENT_TURN_MOVEMENT_START'):
        movement = 'rotation_end'
        rotationType = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,rotationType,direction,direcionTo]
        return {"RecordType":"LOG_MOVEMENT_TURN_MOVEMENT_START","time":timeStamp,"movement:":res[0],"rotationType:":res[1],"direction:":res[2],"direcionTo:":res[3] }
    elif(theLine[3]=='LOG_LOCATION_INIT_ON_START_MOVEMENT'):
        directionStr = theLine[7].strip()
        if(directionStr=='EAST'):
            res= ['toHeading',directionStr]
            return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"toHeading:":res[1] }
        elif(directionStr=='NORTH'):
            res= ['toHeading',directionStr]
            return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"toHeading:":res[1] }
        elif(directionStr=='SOUTH'):
            res= ['toHeading',directionStr]
            return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"toHeading:":res[1] }
        elif(directionStr=='WEST'):
             res= ['toHeading',directionStr]
             return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"toHeading:":res[1] }
        elif(directionStr=='ROTATION'):
            res= ['rotation']
            return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"move_start:":res[0] }
        else:
            directionTo = int(directionStr)
            res = ['toDirection',directionTo]
            return {"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"directionTo:":res[1] }
            

        return ['LOG_LOCATION_INIT_ON_START_MOVEMENT',res]
    else:
        return {}
def getLOG_SENSORS(timeStamp,theLine):
    if(theLine[3]=='LOG_SENSORS_GAP_DIRECTION_CALIBRATION'):
        offset = int(str.split(theLine[5],',')[0].strip())
        mmOverEdge = int(str.split(theLine[12],',')[0].strip())
        direction = int(str.split(theLine[15],',')[0].strip())
        calibrationOffset = int(str.split(theLine[18],',')[0].strip())
        calibrationDeviation = int(theLine[21].strip())
        res = [offset,mmOverEdge,direction,calibrationOffset,calibrationDeviation]
        return {"RecordType":"LOG_SENSORS_GAP_DIRECTION_CALIBRATION","time":timeStamp,"offset:":res[0],"mmOverEdge:":res[1],"direction:":res[2],"calibrationOffset:":res[3],"calibrationDeviation:":res[4] }
    elif(theLine[3]=='LOG_SENSORS_ID_EVENT'):
        sensorsId = str.split(theLine[6],',')[0].strip()
        rightSensor = int(str.split(theLine[8],',')[0].strip())
        leftSensor = int(theLine[10].strip())
        res = [sensorsId,rightSensor,leftSensor]
        return {"RecordType":"LOG_SENSORS_ID_EVENT","time":timeStamp,"sensorsId:":res[0],"rightSensor:":res[1],"leftSensor:":res[2] }
    elif(theLine[3]=='LOG_SENSORS_ID_EVENT_INFO'):
        sensorsId = str.split(theLine[6],',')[0].strip()
        if(sensorsId=='FRONT_LEFT_SENSOR'):
            rightSensor = 0
            leftSensor = int(str.split(theLine[10],',')[0].strip())
        elif(sensorsId=='FRONT_RIGHT_SENSOR'):
            leftSensor = 0
            rightSensor = int(str.split(theLine[10],',')[0].strip())
        res = [sensorsId,rightSensor,leftSensor]
        return {"RecordType":"LOG_SENSORS_ID_EVENT_INFO","time":timeStamp,"sensorsId:":res[0],"rightSensor:":res[1],"leftSensor:":res[2]  }
    elif(theLine[3]=='LOG_SENSORS_READ_FRONT_RIGHT'):
        leftSensor = 0
        rightSensor = int(str.split(theLine[7],',')[0].strip())
        res = [rightSensor,leftSensor]
        return {"RecordType":"LOG_SENSORS_READ_FRONT_RIGHT","time":timeStamp,"rightSensor:":res[0],"leftSensor:":res[1]  }
    elif(theLine[3]=='LOG_SENSORS_READ_FRONT_LEFT'):
        leftSensor = int(str.split(theLine[7],',')[0].strip())
        rightSensor = 0
        res = [rightSensor,leftSensor]
        return {"RecordType":"LOG_SENSORS_READ_FRONT_LEFT","time":timeStamp,"rightSensor:":res[0],"leftSensor:":res[1]  }
    else:
        return {}
def getLOG_ENCODERS_ID_EVENT(timeStamp,theLine):
    if(theLine[3]=='LOG_ENCODERS_ID_EVENT'):
        rightEncoderPulses = int(str.split(theLine[7],',')[0].strip())
        leftEncoderPulses = int(str.split(theLine[11],',')[0].strip())
        encoderDistanceMm = int(str.split(theLine[15],',')[0].strip())
        encoderDistancePulses = int(theLine[19].strip())
        res= [rightEncoderPulses,leftEncoderPulses,encoderDistanceMm,encoderDistancePulses]
        return {"RecordType":"LOG_ENCODERS_ID_EVENT","time":timeStamp,"rightEncoderPulses:":res[0],"leftEncoderPulses:":res[1],"encoderDistanceMm:":res[2],"encoderDistancePulses:":res[3] }
    else:
        return {}
def getLOG_LOCATION(timeStamp,theLine):
    if(theLine[3]=='LOG_LOCATION_DATA_ENCODERS_DISTANCE'):
        rightEncoderMm = int(theLine[13].strip())
        leftEncoderMm = int(str.split(theLine[8],',')[0].strip())
        res= [rightEncoderMm,leftEncoderMm]
        return {"RecordType":"LOG_LOCATION_DATA_ENCODERS_DISTANCE","time":timeStamp,"rightEncoderMm:":res[0],"leftEncoderMm:":res[1] }
    elif(theLine[3]=='LOG_LOCATION_SURFACE_DATA'):
        surfaceType = str.split(theLine[6],',')[0].strip()
        surfaceId = int(str.split(theLine[9],',')[0].strip())
        position_X = int(str.split(theLine[11],',')[0].strip())
        position_Y = int(theLine[13].strip())
        res= [surfaceType,surfaceId,position_X,position_Y]
        return {"RecordType":"LOG_LOCATION_SURFACE_DATA","time":timeStamp,"surfaceType:":res[0],"surfaceId:":res[1],"position_X:":res[2],"position_Y:":res[3] }
    elif(theLine[3]=='LOG_LOCATION_CHANGE_SURFACE'):
        prevSurfaceId = int(str.split(theLine[7],',')[0].strip())
        prevSurfaceType = str.split(theLine[11],',')[0].strip()
        currentSurfaceType = str.split(theLine[15],',')[0].strip()
        position_X = int( str.split(theLine[17],',')[0].strip())
        position_Y = int(theLine[19].strip())
        res= [prevSurfaceId,prevSurfaceType,currentSurfaceType,position_X,position_Y]
        return {"RecordType":"LOG_LOCATION_CHANGE_SURFACE","time":timeStamp,"prevSurfaceId:":res[0],"prevSurfaceType:":res[1],"currentSurfaceType:":res[2],"position_X:":res[3],"position_Y:":res[4] }
    else:
        return ['']
def getLOG_MAGNET(timeStamp,theLine):
    if(theLine[3]=='LOG_MAGNET_RELEASE'):
        magnetStatus = "release"
        res= [magnetStatus]
        return {"RecordType":"LOG_MAGNET","time":timeStamp,"magnetStatus:":res[0] }
    elif(theLine[3]=='LOG_MAGNET_LOCK'):
        magnetStatus = "lock"
        res= [magnetStatus]
        return {"RecordType":"LOG_MAGNET","time":timeStamp,"magnetStatus:":res[0] }
    else:
        return {}
def getLOG_SYSTEM(timeStamp,theLine):
    if(theLine[3]=='LOG_SYSTEM_RESET_CAUSE'):
        systemStatus = "reset"
        systemResetCause = str.split(theLine[7],',')[0].strip()
        res = [systemStatus,systemResetCause]
        return {"RecordType":"LOG_SYSTEM_RESET_CAUSE","time":timeStamp,"systemStatus:":res[0],"systemResetCause:":res[1] }
    elif(theLine[3]=='LOG_SYSTEM_POWER_SAVE_ENTER'):
        systemStatus = "power_save_enter"
        res = [systemStatus]
        return {"RecordType":"LOG_SYSTEM_POWER_SAVE_ENTER","time":timeStamp,"systemStatus:":res[0] }
    elif(theLine[3]=='LOG_SYSTEM_POWER_SAVE_RESUME'):
        systemStatus = "power_save_resume"
        res = [systemStatus]
        return {"RecordType":"LOG_SYSTEM_POWER_SAVE_RESUME","time":timeStamp,"systemStatus:":res[0] }
    else:
        return {}
def getLOG_PROCEDURE_START(timeStamp,theLine):
    if(theLine[3]=='LOG_PROCEDURE_START'):
        procedure = str.split(theLine[5],',')[0].strip()
        startEdge = str.split(theLine[8],',')[0].strip()
        startFromSegment = int( str.split(theLine[13],',')[0].strip())
        startToSegment = int( str.split(theLine[17],',')[0].strip())
        startFromIteration = int(theLine[22].strip())
        res= [procedure,startEdge,startFromSegment,startToSegment,startFromIteration]
        return {"RecordType":"LOG_PROCEDURE_START","time":timeStamp,"procedure:":res[0],"startEdge:":res[1],"startFromSegment:":res[2],"startToSegment:":res[3],"startFromIteration:":res[4] }
    else:
        return {}


 
###########################################################
#goes over log lines and sets data in json file
def logLinesAnalizer(lines,outputFile,logFileName,runLogFile):
    data = list()
    i=1
    for line in lines:
        theLine = str.split(line,' ')
        timeStamp = getTimeStamp(theLine)
        found = False
        lineData = {}
        for key in keyWords:
            index = str.find(theLine[3],key)
            if(not index==-1):
                found = True
                if(key=='FIRMWARE_VERSION'):
                    lineData = getLOG_FIRMWARE_VERSION(timeStamp,theLine)
                    break
                elif(key=='FSM300'):
                    lineData = getLOG_FSM300(timeStamp,theLine)                   
                    break
                elif(key=='STEP'):
                    lineData = getLOG_STEP(timeStamp,theLine)
                    break
                elif(key=='ROBOT_STATUS'):
                    lineData=  getLOG_ROBOT_STATUS(timeStamp,theLine)
                    break
                elif(key=='LOW_BATTERY'):
                    lineData= getLOG_LOW_BATTERY(timeStamp,theLine)
                    break
                elif(key=='COMMUNICATION'):
                    lineData = getLOG_COMMUNICATION(timeStamp,theLine)
                    break
                elif(key=='ADC_TEMPERATURE_MEASURED_VALUE'):
                    lineData = getLOG_ADC_TEMPERATURE_MEASURED_VALUE(timeStamp,theLine)
                    break
                elif(key=='ROBOT_MANAGER'):
                    lineData = getLOG_ROBOT_MANAGER(timeStamp,theLine)
                    break
                elif(key=='PROTOCOL_VERSION_MISMATCH'):
                    lineData = getLOG_PROTOCOL_VERSION_MISMATCH(timeStamp,theLine)
                    break
                elif(key=='TELIT_DRIVER'):
                    lineData = getLOG_TELIT_DRIVER(timeStamp,theLine)
                    break
                elif(key=='SYSTEM'):
                    lineData = getLOG_SYSTEM(timeStamp,theLine)
                    break
                elif(key=='MOVEMENT'):
                    lineData = getLOG_MOVEMENT(timeStamp,theLine)
                    break
                elif(key=='SENSORS'):
                    lineData = getLOG_SENSORS(timeStamp,theLine)
                    break
                elif(key=='ENCODERS_ID_EVENT'):
                    lineData = getLOG_ENCODERS_ID_EVENT(timeStamp,theLine)
                    break
                elif(key=='LOCATION'):
                    lineData = getLOG_LOCATION(timeStamp,theLine)
                    break
                elif(key=='MAGNET'):
                    lineData = getLOG_MAGNET(timeStamp,theLine)
                    break
                elif(key=='PROCEDURE_START'):
                    lineData = getLOG_PROCEDURE_START(timeStamp,theLine)
                    break
                elif(key=='START_TASK'):
                    lineData = getLOG_START_TASK(timeStamp,theLine)
                    break
                elif(key=='POWER_RESET'):
                    lineData = getLOG_POWER_RESET(timeStamp,theLine)
                    break
        if((not found) or (len(lineData)==0)):
            runLogFile.writelines(line)
        else:
            data.append(lineData)
        i+=1
    json.dump(data,outputFile,separators=(',', ':'), indent=2)


def main(argv):
    #open log file, output file, log run file, return lines of log file
    (lines,outputFile,logFile,runLogFile)  = openFiles(argv[1])
    #analize lines one after the other - and create json file as output file
    logLinesAnalizer(lines,outputFile,logFile.name,runLogFile)
    #close and exit
    runLogFile.close()
    logFile.close()
    outputFile.close()
    

if __name__ == "__main__":
    main(sys.argv)

