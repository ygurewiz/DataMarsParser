import sys
#import datetime
import json

keyWords = ['FIRMWARE_VERSION',
            'FSM300_SET_DIRECTION_DIFF_DATA1',
            'FSM300_DRIVER_CALIBRATION',
            'FSM300_SET_DIRECTION_DIFF_DATA2',
            'ROBOT_STATUS_1',
            'ROBOT_STATUS_2',
            'ROBOT_STATUS_3',
            'LOW_BATTERY',
            'COMMUNICATION_RECEIVED',
            'COMMUNICATION_RESPONSE',
            'ADC_TEMPERATURE_MEASURED_VALUE',
            'ROBOT_MANAGER_HANDLE_EVENT',
            'FSM300_DRIVER_RESTART',
            'FSM300_DRIVER_DATA_CHECKSUM_ERROR',
            'FSM300_DRIVER_DATA_ANGLE_ERROR',
            'PROTOCOL_VERSION_MISMATCH',
            'TELIT_DRIVER',
            'ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS',
            'ROBOT_MANAGER_CHANGE_PARKING_SIDE',
            'ROBOT_MANAGER_PARSE_EVENT',
            'ROBOT_MANAGER_CHANGE_PARKING',
            'STEP_START_CALIBRATION',
            'FSM300_DRIVER_ACCELEROMETER_TOLERANCE',
            'STEP_START',
            'STEP_END',
            'MOVEMENT',
            'LOCATION_INIT_ON_START_MOVEMENT',
            'SENSORS',
            'ENCODERS_ID_EVENT',
            'LOCATION_DATA_ENCODERS_DISTANCE',
            'LOCATION_SURFACE_DATA',
            'ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN',
            'ROBOT_MANAGER_DEBUG_SENSORS_ARRAY',
            'ROBOT_MANAGER_START_CLEAN',
            'MAGNET',
            'STEP_EDGE_END',
            'SYSTEM',
            'ROBOT_MANAGER_CLEANING_DONE',
            'PROCEDURE_START',
            'LOCATION_CHANGE_SURFACE']

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
    directionAfter = int(str.split(theLine[7].strip(),',')[0])
    directionBefore = int(str.split(theLine[12].strip(),',')[0])
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
def getLOG_FSM300_DRIVER_ACCELEROMETER_TOLERANCE(theLine):
    accelerometrTollerance = int(theLine[6].strip())
    return [accelerometrTollerance]
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
def getLOG_STEP_START(theLine):
    res = ['']
    step = str.split(theLine[5],',')[0].strip()
    if(theLine[3]=='LOG_STEP_START'):
        res = [step]
        return ['LOG_STEP_START',res]
    elif(theLine[3]=='LOG_STEP_START_EDGE_MOVE'):
        toEdge = str.split(theLine[7],',')[0].strip()
        direcionTo = int(theLine[9].strip())
        res = [step,toEdge,direcionTo]
        return ['LOG_STEP_START_EDGE_MOVE',res]
    elif(theLine[3]=='LOG_STEP_START_CROSS_BRIDGE'):
        closestEdge = str.split(theLine[8],',')[0].strip()
        directionToEdge = str.split(theLine[10],',')[0].strip()
        res = [step,closestEdge,directionToEdge]
        return ['LOG_STEP_START_CROSS_BRIDGE',res]
    elif(theLine[3]=='LOG_STEP_START_CALIBRATION'):
        calibrationDirection = theLine[8].strip()
        res =  [step,calibrationDirection]
        return ['LOG_STEP_START_CALIBRATION',res]
def getLOG_STEP_END(theLine):
    step = str.split(theLine[5],',')[0].strip()
    returnValue = theLine[8].strip()
    return [step,returnValue]
def getLOG_MOVEMENT(theLine):
    res = ['']
    if(theLine[3]=='LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT'):
        movement = 'direction_deviation'
        directionDeviationAbsValue =  int(str.split(theLine[8],',')[0].strip())
        direcionTo = int(str.split(theLine[11],',')[0].strip())
        direction = int(theLine[15].strip())
        res = [movement,directionDeviationAbsValue,direcionTo,direction]
        return ['LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT',res]
    elif(theLine[3]=='LOG_MOVEMENT_EDGE_MOVEMENT_END'):
        movement = 'end_move'
        moveReturnValue = theLine[6].strip()
        res = [movement,moveReturnValue]
        return ['LOG_MOVEMENT_EDGE_MOVEMENT_END',res]
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
        return ['LOG_MOVEMENT_EDGE_MOVEMENT_START',res]
    elif(theLine[3]=='LOG_MOVEMENT_END_DIRECTION'):
        movement = 'end_direction_move'
        moveReturnValue = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,moveReturnValue,direction]
        return ['LOG_MOVEMENT_END_DIRECTION',res] #4
    elif(theLine[3]=='LOG_MOVEMENT_ERROR'):
        movement = 'movement_error'
        moveErrorStatus = str.split(theLine[5],',')[0].strip()
        moveReturnValue = theLine[7].strip()
        res =  [movement,moveErrorStatus,moveReturnValue]
        return ['LOG_MOVEMENT_ERROR',res]
    elif(theLine[3]=='LOG_MOVEMENT_FINE_TUNING_TURN_START'):
        movement = 'rotation'
        rotationType = 'fine_tuning' 
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res =  [movement,rotationType,rotationDirection,direction,direcionTo]
        return ['LOG_MOVEMENT_FINE_TUNING_TURN_START',res]
    elif(theLine[3]=='LOG_MOVEMENT_FULL_SPEED_TURN_START'):
        movement = 'rotation'
        rotationType = 'full_speed' 
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res =  [movement,rotationType,rotationDirection,direction,direcionTo]
        return ['LOG_MOVEMENT_FULL_SPEED_TURN_START',res]
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT'):
        movement = str.split(theLine[9],',')[0].strip()
        movementType = str.split(theLine[5],',')[0].strip()
        sensor = str.split(theLine[7],',')[0].strip()
        direction = int(str.split(theLine[11],',')[0].strip())
        miliSecondsToFindEdge = int(theLine[19].strip())
        res =  [movement,movementType,sensor,direction,miliSecondsToFindEdge]
        return ['LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT',res]
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT'):
        movement = theLine[7].strip()
        status = str.split(theLine[5],',')[0].strip()
        res =  [status,movement]
        return ['LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT',res]
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT'):
        movement = 'direction_inner_correction'
        direction = int(str.split(theLine[6],',')[0].strip())
        directionDiff = int(str.split(theLine[9],',')[0].strip())
        correctionState = theLine[12].strip()
        res =  [movement,direction,directionDiff,correctionState]
        return ['LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT',res]
    elif(theLine[3]=='LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT'):
        status = theLine[5].strip()
        res =  [status]
        return ['LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT',res]
    elif(theLine[3]=='LOG_MOVEMENT_INNER_MOVEMENT_END'):
        movement = 'end_inner_move'
        moveReturnValue = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        movementType = theLine[12].strip()
        res = [movement,moveReturnValue,direction,movementType]
        return ['LOG_MOVEMENT_INNER_MOVEMENT_END',res] #3
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
        return ['LOG_MOVEMENT_INNER_MOVEMENT_START',res]  #2
    elif(theLine[3]=='LOG_MOVEMENT_SINGLE_WHEEL_TURN_START'):
        movement = 'rotation'
        rotationType = 'A_turn'
        rotationDirection = str.split(theLine[6],',')[0].strip()
        direction = int(str.split(theLine[9],',')[0].strip())
        direcionTo = int(theLine[12].strip())
        res = [movement,rotationType,rotationDirection,direction,direcionTo]
        return ['LOG_MOVEMENT_SINGLE_WHEEL_TURN_START',res]
    elif(theLine[3]=='LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START'):
        movement = 'direction_sensor'
        direction = int(str.split(theLine[6],',')[0].strip())
        motorToTurn = theLine[10].strip() + '_' + str.split(theLine[11],',')[0].strip()
        motorTurningDirection = theLine[15].strip() + '_' +theLine[16].strip() + '_' + str.split(theLine[17],',')[0].strip()
        sensorState = theLine[20].strip() + '_' +theLine[21].strip()
        res = [movement,direction,motorToTurn,motorTurningDirection,sensorState]
        return ['LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START',res]
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
        return ['LOG_MOVEMENT_START',res] #1
    elif(theLine[3]=='LOG_MOVEMENT_TURN_FINE_TUNING_FAIL'):
        movement = 'rotation'
        rotationType = 'fine_tuning' 
        returnStatus = str.split(theLine[6],',')[0].strip()
        direcionTo = int(str.split(theLine[9],',')[0].strip())
        diffDirection = int(theLine[11].strip())
        res =  [movement,rotationType,returnStatus,direcionTo,diffDirection]
        return ['LOG_MOVEMENT_TURN_FINE_TUNING_FAIL',res]
    elif(theLine[3]=='LOG_MOVEMENT_TURN_IS_FINISHED'):
        movement = 'rotation_end'
        rotationType = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,rotationType,direction,direcionTo]
        return ['LOG_MOVEMENT_TURN_IS_FINISHED',res]
    elif(theLine[3]=='LOG_MOVEMENT_TURN_MOVEMENT_END'):
        movement = 'rotation_end'
        returnValue = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,returnValue,direction,direcionTo]
        return ['LOG_MOVEMENT_TURN_MOVEMENT_END',res]
    elif(theLine[3]=='LOG_MOVEMENT_TURN_MOVEMENT_START'):
        movement = 'rotation_end'
        rotationType = str.split(theLine[6],',')[0].strip()
        direcionTo = int(theLine[12].strip())
        direction = int(str.split(theLine[9],',')[0].strip())
        res =  [movement,rotationType,direction,direcionTo]
        return ['LOG_MOVEMENT_TURN_MOVEMENT_START',res]
    elif(theLine[3]=='LOG_LOCATION_INIT_ON_START_MOVEMENT'):
        directionStr = theLine[7].strip()
        if(directionStr=='EAST'):
            return ['toHeading',directionStr]
        elif(directionStr=='NORTH'):
            return ['toHeading',directionStr]
        elif(directionStr=='SOUTH'):
            return ['toHeading',directionStr]
        elif(directionStr=='WEST'):
             return ['toHeading',directionStr]
        elif(directionStr=='ROTATION'):
            return ['rotation']
        else:
            directionTo = int(directionStr)
            res = ['toDirection',directionTo]
            return ['LOG_LOCATION_INIT_ON_START_MOVEMENT',res]
def getLOG_SENSORS(theLine):
    res = ['']
    if(theLine[3]=='LOG_SENSORS_GAP_DIRECTION_CALIBRATION'):
        offset = int(str.split(theLine[5],',')[0].strip())
        mmOverEdge = int(str.split(theLine[12],',')[0].strip())
        direction = int(str.split(theLine[15],',')[0].strip())
        calibrationOffset = int(str.split(theLine[18],',')[0].strip())
        calibrationDeviation = int(theLine[21].strip())
        res = [offset,mmOverEdge,direction,calibrationOffset,calibrationDeviation]
        return ['LOG_SENSORS_GAP_DIRECTION_CALIBRATION',res]
    elif(theLine[3]=='LOG_SENSORS_ID_EVENT'):
        sensorsId = str.split(theLine[6],',')[0].strip()
        rightSensor = int(str.split(theLine[8],',')[0].strip())
        leftSensor = int(theLine[10].strip())
        res = [sensorsId,rightSensor,leftSensor]
        return ['LOG_SENSORS_ID_EVENT',res]
    elif(theLine[3]=='LOG_SENSORS_ID_EVENT_INFO'):
        sensorsId = str.split(theLine[6],',')[0].strip()
        if(sensorsId=='FRONT_LEFT_SENSOR'):
            rightSensor = 0
            leftSensor = int(str.split(theLine[10],',')[0].strip())
        elif(sensorsId=='FRONT_RIGHT_SENSOR'):
            leftSensor = 0
            rightSensor = int(str.split(theLine[10],',')[0].strip())
        res = [sensorsId,rightSensor,leftSensor]
        return ['LOG_SENSORS_ID_EVENT_INFO',res]
    elif(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA'):
        rightSensor = int(str.split(theLine[7],',')[0].strip())
        leftSensor = int(str.split(theLine[11],',')[0].strip())
        res = [rightSensor,leftSensor]
        return ['LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA',res]
    elif(theLine[3]=='LOG_SENSORS_READ_FRONT_RIGHT'):
        leftSensor = 0
        rightSensor = int(str.split(theLine[7],',')[0].strip())
        res = [rightSensor,leftSensor]
        return ['LOG_SENSORS_READ_FRONT_RIGHT',res]
    elif(theLine[3]=='LOG_SENSORS_READ_FRONT_LEFT'):
        leftSensor = int(str.split(theLine[7],',')[0].strip())
        rightSensor = 0
        res = [rightSensor,leftSensor]
        return ['LOG_SENSORS_READ_FRONT_LEFT',res]
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
        return['LOG_ROBOT_MANAGER_DEBUG_SENSORS_ARRAY',res]
def getLOG_ENCODERS_ID_EVENT(theLine):
    rightEncoderPulses = int(str.split(theLine[7],',')[0].strip())
    leftEncoderPulses = int(str.split(theLine[11],',')[0].strip())
    encoderDistanceMm = int(str.split(theLine[15],',')[0].strip())
    encoderDistancePulses = int(theLine[19].strip())
    return [rightEncoderPulses,leftEncoderPulses,encoderDistanceMm,encoderDistancePulses]
def getLOG_LOCATION_DATA_ENCODERS_DISTANCE(theLine):
    rightEncoderMm = int(theLine[13].strip())
    leftEncoderMm = int(str.split(theLine[8],',')[0].strip())
    return [rightEncoderMm,leftEncoderMm]
def getLOG_LOCATION_SURFACE_DATA(theLine):
    surfaceType = str.split(theLine[6],',')[0].strip()
    surfaceId = int(str.split(theLine[9],',')[0].strip())
    position_X = int(str.split(theLine[11],',')[0].strip())
    position_Y = int(theLine[13].strip())
    return [surfaceType,surfaceId,position_X,position_Y]
def getLOG_ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN(theLine):
    pitch = int(str.split(theLine[5],',')[0].strip())
    readCountBelowMaxTiltAllowed = int(theLine[12].strip())
    return [pitch,readCountBelowMaxTiltAllowed]
def getLOG_ROBOT_MANAGER_START_CLEAN(theLine):
    cleanProcedure = theLine[6].strip()
    return [cleanProcedure]
def getLOG_MAGNET(theLine):
    if(theLine[3]=='LOG_MAGNET_RELEASE'):
        magnetStatus = "release"
        return [magnetStatus]
    if(theLine[3]=='LOG_MAGNET_LOCK'):
        magnetStatus = "lock"
        return [magnetStatus]
def getLOG_STEP_EDGE_END(theLine):
    movement = 'edge_move'
    step = str.split(theLine[5],',')[0].strip()
    returnValue = str.split(theLine[8],',')[0].strip()
    yaw = int(str.split(theLine[10],',')[0].strip())
    roll = int(str.split(theLine[12],',')[0].strip())
    pitch = int(theLine[14].strip())
    return [movement,step,returnValue,yaw,roll,pitch]
def getLOG_SYSTEM(theLine):
    if(theLine[3]=='LOG_SYSTEM_RESET_CAUSE'):
        systemStatus = "reset"
        systemResetCause = str.split(theLine[7],',')[0].strip()
        res = [systemStatus,systemResetCause]
        return ['LOG_SYSTEM_RESET_CAUSE',res]
    if(theLine[3]=='LOG_SYSTEM_POWER_SAVE_ENTER'):
        systemStatus = "power_save_enter"
        res = [systemStatus]
        return ['LOG_SYSTEM_POWER_SAVE_ENTER',res]
    if(theLine[3]=='LOG_SYSTEM_POWER_SAVE_RESUME'):
        systemStatus = "power_save_resume"
        res = [systemStatus]
        return ['LOG_SYSTEM_POWER_SAVE_RESUME',res]
    if(theLine[3]=='LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY'):
        errors = int(theLine[6].strip())
        res = [errors]
        return ['LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY',res]
    if(theLine[3]=='LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO'):
        systemEvent = int(str.split(theLine[6],',')[0].strip())
        currentState = theLine[9].strip()
        res = [systemEvent,currentState]
        return ['LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO',res]
def getLOG_ROBOT_MANAGER_CLEANING_DONE(theLine):
    cleanProcedure = str.split(theLine[6],',')[0].strip()
    returnValue = theLine[9].strip()
    return [cleanProcedure,returnValue]
def getLOG_PROCEDURE_START(theLine):
    procedure = str.split(theLine[5],',')[0].strip()
    startEdge = str.split(theLine[8],',')[0].strip()
    startFromSegment = int( str.split(theLine[13],',')[0].strip())
    startToSegment = int( str.split(theLine[17],',')[0].strip())
    startFromIteration = int(theLine[22].strip())
    return [procedure,startEdge,startFromSegment,startToSegment,startFromIteration]
def getLOG_LOCATION_CHANGE_SURFACE(theLine):
    prevSurfaceId = int(str.split(theLine[7],',')[0].strip())
    prevSurfaceType = str.split(theLine[11],',')[0].strip()
    currentSurfaceType = str.split(theLine[15],',')[0].strip()
    position_X = int( str.split(theLine[17],',')[0].strip())
    position_Y = int(theLine[19].strip())
    return [prevSurfaceId,prevSurfaceType,currentSurfaceType,position_X,position_Y]
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
    data = list()
    i=1
    for line in lines:
        theLine = str.split(line,' ')
        timeStamp = getTimeStamp(theLine)
        found = False
        for key in keyWords:
            index = str.find(theLine[3],key)
            if(not index==-1):
                found = True
                if(key=='FIRMWARE_VERSION'):
                    res = getLOG_FIRMWARE_VERSION(theLine)
                    data.append({"RecordType":"LOG_FIRMWARE_VERSION","time":timeStamp,"FW:":res})
                elif(key=='FSM300_SET_DIRECTION_DIFF_DATA1'):
                    res = getLOG_FSM300_SET_DIRECTION_DIFF_DATA1(theLine)
                    data.append({"RecordType":"LOG_FSM300_SET_DIRECTION_DIFF_DATA1","time":timeStamp,"directionBefore:":res[0],"directionAfter:":res[1]})
                elif(key=='FSM300_DRIVER_CALIBRATION'):
                    res = getLOG_FSM300_DRIVER_CALIBRATION(theLine)
                    data.append({"RecordType":"getLOG_FSM300_DRIVER_CALIBRATION","time":timeStamp,"directionBefore:":res[0],"directionAfter:":res[1]})
                elif(key=='FSM300_SET_DIRECTION_DIFF_DATA2'):
                    res = getLOG_FSM300_SET_DIRECTION_DIFF_DATA2(theLine)
                    data.append({"RecordType":"getLOG_FSM300_SET_DIRECTION_DIFF_DATA2","time":timeStamp,"weightedYaw:":res[0],"yaw:":res[1]})
                elif(key=='ROBOT_STATUS_1'):
                    res = getLOG_ROBOT_STATUS_1(theLine)
                    data.append({"RecordType":"LOG_ROBOT_STATUS_1","time":timeStamp,"currentSurfaceType:":res[0],"surfaceTypeAppearanceNumber:":res[1],"totalDesiredCleanedArea:":res[2],"totalAreaOfFullyCleanedSegments:":res[3],"currentSegmentsSurfaceArea:":res[4]})
                elif(key=='ROBOT_STATUS_2'):
                    res = getLOG_ROBOT_STATUS_2(theLine)
                    data.append({"RecordType":"LOG_ROBOT_STATUS_2","time":timeStamp,"robotState:":res[0],"robotStep:":res[1],"numFullyCleanedSegments:":res[2],"iterationInStep:":res[3],"expectedNumIterations:":res[4]})
                elif(key=='ROBOT_STATUS_3'):
                    res = getLOG_ROBOT_STATUS_3(theLine)
                    data.append({"RecordType":"LOG_ROBOT_STATUS_3","time":timeStamp,"direction:":res[0],"roll:":res[1],"pitch:":res[2],"battery:":res[3],"events:":res[4]})
                elif(key=='LOW_BATTERY'):
                    res = getLOG_LOW_BATTERY(theLine)
                    data.append({"RecordType":"LOG_LOW_BATTERY","time":timeStamp,"battery:":res})
                elif(key=='COMMUNICATION_RECEIVED'):
                    res = getLOG_COMMUNICATION_RECEIVED(theLine)
                    data.append({"RecordType":"LOG_COMMUNICATION_RECEIVED","time":timeStamp,"Command:":res[0],"Media:":res[1],"packetID:":res[2],"serverID:":res[3],"payloadSize:":res[4]})
                elif(key=='COMMUNICATION_RESPONSE'):
                    res = getLOG_COMMUNICATION_RESPONSE(theLine)
                    data.append({"RecordType":"LOG_COMMUNICATION_RESPONSE","time":timeStamp,"response:":res[0],"size:":res[1]})
                elif(key=='ADC_TEMPERATURE_MEASURED_VALUE'):
                    res = getLOG_ADC_TEMPERATURE_MEASURED_VALUE(theLine)
                    data.append({"RecordType":"LOG_ADC_TEMPERATURE_MEASURED_VALUE","time":timeStamp,"internalTemperature:":res[0] })
                elif(key=='ROBOT_MANAGER_HANDLE_EVENT'):
                    res = getLOG_ROBOT_MANAGER_HANDLE_EVENT(theLine)
                    if(res[0]=='LOG_ROBOT_MANAGER_HANDLE_EVENT'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT","time":timeStamp,"Event:":res[1][0],"CurrentState:":res[1][1] })
                    elif(res[0]=='LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_HANDLE_EVENT_CHANGE_STATE","time":timeStamp,"Oldstate:":res[1][0],"Newstate:":res[1][1] })
                    else:
                        found = False
                elif(key=='FSM300_DRIVER_RESTART'):
                    res = getLOG_FSM300_DRIVER_RESTART(theLine)
                    data.append({"RecordType":"LOG_FSM300_DRIVER_RESTART","time":timeStamp,"restartNumber:":res[0],"Offset:":res[1] })
                elif(key=='FSM300_DRIVER_DATA_CHECKSUM_ERROR'):
                    res = getLOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR(theLine)
                    data.append({"RecordType":"LOG_FSM300_DRIVER_DATA_CHECKSUM_ERROR","time":timeStamp,"Index:":res[0],"packetChecksum:":res[1],"calculatedChecksum:":res[2] })
                elif(key=='FSM300_DRIVER_DATA_ANGLE_ERROR'):
                    res = getLOG_FSM300_DRIVER_DATA_ANGLE_ERROR(theLine)
                    if(res[0]=='ANGLE_YAW'):
                        data.append({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentYaw:":res[1],"previousYaw:":res[2] })
                    elif(res[0]=='ANGLE_PITCH'):
                        data.append({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentPitch:":res[1],"previousPitch:":res[2] })
                    elif(res[0]=='ANGLE_ROLL'):
                        data.append({"RecordType":"LOG_FSM300_DRIVER_DATA_ANGLE_ERROR","time":timeStamp,"AngleErrorType:":res[0],"currentRoll:":res[1],"previousRoll:":res[2] })
                    else:
                        found = False
                elif(key=='PROTOCOL_VERSION_MISMATCH'):
                    res = getLOG_PROTOCOL_VERSION_MISMATCH(theLine)
                    data.append({"RecordType":"LOG_PROTOCOL_VERSION_MISMATCH","time":timeStamp,"Major:":res[0],"Minor:":res[1],"FWMajor:":res[2],"FWMinor:":res[3] })
                elif(key=='TELIT_DRIVER'):
                    res = getLOG_TELIT_DRIVER(theLine)
                    if(res[0]=='LOG_TELIT_DRIVER'):
                        data.append({"RecordType":"LOG_TELIT_DRIVER","time":timeStamp,"telitStatus:":res[1][0] })
                    elif(res[0]=='LOG_TELIT_DRIVER_CHANNEL'):
                        data.append({"RecordType":"LOG_TELIT_DRIVER_CHANNEL","time":timeStamp,"telitStatus:":res[1][0],"telitChannel:":res[1][1] })
                    else:
                        found = False
                elif(key=='ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS'):
                    res = getLOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS(theLine)
                    data.append({"RecordType":"LOG_ROBOT_MANAGER_CHECK_CHANGE_PARKING_NOT_BETWEEN_THRESHOLDS","time":timeStamp,"pitch:":res[0],"maxTiltAllowed:":res[1],"minTiltAllowed:":res[2] })
                elif(key=='ROBOT_MANAGER_PARSE_EVENT'):
                    res = getLOG_ROBOT_MANAGER_PARSE_EVENT(theLine)
                    data.append({"RecordType":"LOG_ROBOT_MANAGER_PARSE_EVENT","time":timeStamp,"event:":res[0] })
                elif(key=='ROBOT_MANAGER_CHANGE_PARKING'):
                    res = getLOG_ROBOT_MANAGER_CHANGE_PARKING(theLine)
                    if(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING","time":timeStamp,"direction:":res[1][0] })
                    elif(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_TIME","time":timeStamp,"Hour:":res[1][0],"Minute:":res[1][1],"minCPTime:":res[1][2],"maxCPTime:":res[1][3],"changeParkingTime:":res[1][4] })
                    elif(res[0]=='LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_CHANGE_PARKING_SIDE","time":timeStamp,"pitch:":res[1][0],"maxTiltAllowed:":res[1][1],"minTiltAllowed:":res[1][2] })
                    else:
                        found = False
                elif(key=='FSM300_DRIVER_ACCELEROMETER_TOLERANCE'):
                    res = getLOG_FSM300_DRIVER_ACCELEROMETER_TOLERANCE(theLine)
                    data.append({"RecordType":"LOG_FSM300_DRIVER_ACCELEROMETER_TOLERANCE","time":timeStamp,"accelerometrTollerance:":res[0] })
                elif(key=='SYSTEM'):
                    res = getLOG_SYSTEM(theLine)
                    if(res[0]=='LOG_SYSTEM_RESET_CAUSE'):
                        data.append({"RecordType":"LOG_SYSTEM_RESET_CAUSE","time":timeStamp,"systemStatus:":res[1][0],"systemResetCause:":res[1][1] })
                    elif(res[0]=='LOG_SYSTEM_POWER_SAVE_ENTER'):
                        data.append({"RecordType":"LOG_SYSTEM_POWER_SAVE_ENTER","time":timeStamp,"systemStatus:":res[1][0] })
                    elif(res[0]=='LOG_SYSTEM_POWER_SAVE_RESUME'):
                        data.append({"RecordType":"LOG_SYSTEM_POWER_SAVE_RESUME","time":timeStamp,"systemStatus:":res[1][0] })
                    elif(res[0]=='LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SYSTEM_ERRORS_ARRAY","time":timeStamp,"errors:":res[1][0] })
                    elif(res[0]=='LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_SYSTEM_EVENT_INFO","time":timeStamp,"systemEvent:":res[1][0],"currentState:":res[1][1] })
                    else:
                        found = False
                elif(key=='MOVEMENT'):
                    res = getLOG_MOVEMENT(theLine)
                    if(res[0]=='LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT'):
                        data.append({"RecordType":"LOG_MOVEMENT_DIRECTION_DEVIATION_EDGE_MOVEMENT","time":timeStamp,"movement:":res[1][0],"directionDeviationAbsValue:":res[1][1],"direcionTo:":res[1][2],"direction:":res[1][3] })
                    elif(res[0]=='LOG_MOVEMENT_EDGE_MOVEMENT_END'):
                        data.append({"RecordType":"LOG_MOVEMENT_EDGE_MOVEMENT_END","time":timeStamp,"movement:":res[1][0],"moveReturnValue:":res[1][1] })
                    elif(res[0]=='LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT'):
                        data.append({"RecordType":"LOG_MOVEMENT_HANDLE_TURN_MOVEMENT_EVENT","time":timeStamp,"status:":res[1][0] })
                    elif(res[0]=='LOG_MOVEMENT_EDGE_MOVEMENT_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_EDGE_MOVEMENT_START","time":timeStamp,"movement:":res[1][0],"direction:":res[1][1],"direcionTo:":res[1][2],"heading:":res[1][3] ,"pulses:":res[1][4]})
                    elif(res[0]=='LOG_MOVEMENT_END_DIRECTION'):
                        data.append({"RecordType":"LOG_MOVEMENT_END_DIRECTION","time":timeStamp,"movement:":res[1][0],"moveReturnValue:":res[1][1],"direction:":res[1][2] })
                    elif(res[0]=='LOG_MOVEMENT_ERROR'):
                        data.append({"RecordType":"LOG_MOVEMENT_ERROR","time":timeStamp,"movement:":res[1][0],"moveErrorStatus:":res[1][1],"moveReturnValue:":res[1][2] })
                    elif(res[0]=='LOG_MOVEMENT_FINE_TUNING_TURN_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_FINE_TUNING_TURN_START","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"rotationDirection:":res[1][2],"direction:":res[1][3],"direcionTo:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_FULL_SPEED_TURN_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_FULL_SPEED_TURN_START","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"rotationDirection:":res[1][2],"direction:":res[1][3],"direcionTo:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT'):
                        data.append({"RecordType":"LOG_MOVEMENT_HANDLE_EDGE_MOVEMENT_EVENT","time":timeStamp,"movement:":res[1][0],"movementType:":res[1][1],"sensor:":res[1][2],"direction:":res[1][3],"miliSecondsToFindEdge:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT'):
                        data.append({"RecordType":"LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_CORRECTION_EVENT","time":timeStamp,"movement:":res[1][0],"direction:":res[1][1],"directionDiff:":res[1][2],"correctionState:":res[1][3] })
                    elif(res[0]=='LOG_MOVEMENT_INNER_MOVEMENT_END'):
                        data.append({"RecordType":"LOG_MOVEMENT_INNER_MOVEMENT_END","time":timeStamp,"movement:":res[1][0],"moveReturnValue:":res[1][1],"direction:":res[1][2],"movementType:":res[1][3] })
                    elif(res[0]=='LOG_MOVEMENT_INNER_MOVEMENT_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_INNER_MOVEMENT_START","time":timeStamp,"movement:":res[1][0],"movementType:":res[1][1],"direction:":res[1][2],"direcionTo:":res[1][3],"heading:":res[1][4],"pulses:":res[1][5] })
                    elif(res[0]=='LOG_MOVEMENT_SINGLE_WHEEL_TURN_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_SINGLE_WHEEL_TURN_START","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"rotationDirection:":res[1][2],"direction:":res[1][3],"direcionTo:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_SINGLE_WHEEL_UNTIL_SENSOR_CHANGE_TURN_START","time":timeStamp,"movement:":res[1][0],"direction:":res[1][1],"motorToTurn:":res[1][2],"motorTurningDirection:":res[1][3],"sensorState:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_START","time":timeStamp,"movement:":res[1][0],"movementType:":res[1][1],"direction:":res[1][2],"direcionTo:":res[1][3],"heading:":res[1][4],"pulses:":res[1][5] })
                    elif(res[0]=='LOG_MOVEMENT_TURN_FINE_TUNING_FAIL'):
                        data.append({"RecordType":"LOG_MOVEMENT_TURN_FINE_TUNING_FAIL","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"returnStatus:":res[1][2],"direcionTo:":res[1][3],"diffDirection:":res[1][4] })
                    elif(res[0]=='LOG_MOVEMENT_TURN_IS_FINISHED'):
                        data.append({"RecordType":"LOG_MOVEMENT_TURN_IS_FINISHED","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"direction:":res[1][2],"direcionTo:":res[1][3]})
                    elif(res[0]=='LOG_MOVEMENT_TURN_MOVEMENT_END'):
                        data.append({"RecordType":"LOG_MOVEMENT_TURN_MOVEMENT_END","time":timeStamp,"movement:":res[1][0],"returnValue:":res[1][1],"direction:":res[1][2],"direcionTo:":res[1][3] })
                    elif(res[0]=='LOG_MOVEMENT_TURN_MOVEMENT_START'):
                        data.append({"RecordType":"LOG_MOVEMENT_TURN_MOVEMENT_START","time":timeStamp,"movement:":res[1][0],"rotationType:":res[1][1],"direction:":res[1][2],"direcionTo:":res[1][3] })
                    elif(res[0]=='LOG_LOCATION_INIT_ON_START_MOVEMENT'):
                        if(res[1][0]=='toHeading'):
                            data.append({"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"toHeading:":res[1][1] })
                        elif(res[1][0]=='rotation'):
                            data.append({"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"move_start:":res[1][0] })
                        elif(res[1][0]=='toDirection'):
                            data.append({"RecordType":"LOG_LOCATION_INIT_ON_START_MOVEMENT","time":timeStamp,"directionTo:":res[1][1] })
                        else:
                            found = False
                    elif(res[0]=='LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT'):
                        data.append({"RecordType":"LOG_MOVEMENT_HANDLE_INNER_MOVEMENT_EVENT","time":timeStamp,"status:":res[1][0],"movement:":res[1][1]})
                    else:
                        found = False
                elif(key=='SENSORS'):
                    res = getLOG_SENSORS(theLine)
                    if(res[0]=='LOG_SENSORS_GAP_DIRECTION_CALIBRATION'):
                        data.append({"RecordType":"LOG_SENSORS_GAP_DIRECTION_CALIBRATION","time":timeStamp,"offset:":res[1][0],"mmOverEdge:":res[1][1],"direction:":res[1][2],"calibrationOffset:":res[1][3],"calibrationDeviation:":res[1][4] })
                    elif(res[0]=='LOG_SENSORS_ID_EVENT'):
                        data.append({"RecordType":"LOG_SENSORS_ID_EVENT","time":timeStamp,"sensorsId:":res[1][0],"rightSensor:":res[1][1],"leftSensor:":res[1][2] })
                    elif(res[0]=='LOG_SENSORS_ID_EVENT_INFO'):
                        data.append({"RecordType":"LOG_SENSORS_ID_EVENT_INFO","time":timeStamp,"sensorsId:":res[1][0],"rightSensor:":res[1][1],"leftSensor:":res[1][2]  })
                    elif(res[0]=='LOG_SENSORS_READ_FRONT_LEFT'):
                        data.append({"RecordType":"LOG_SENSORS_READ_FRONT_LEFT","time":timeStamp,"rightSensor:":res[1][0],"leftSensor:":res[1][1]  })
                    elif(res[0]=='LOG_SENSORS_READ_FRONT_RIGHT'):
                        data.append({"RecordType":"LOG_SENSORS_READ_FRONT_RIGHT","time":timeStamp,"rightSensor:":res[1][0],"leftSensor:":res[1][1]  })
                    elif(res[0]=='LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SENSORS_DATA","time":timeStamp,"rightSensor:":res[1][0],"leftSensor:":res[1][1]  })
                    elif(res[0]=='ROBOT_MANAGER_DEBUG_SENSORS_ARRAY'):
                        data.append({"RecordType":"LOG_ROBOT_MANAGER_DEBUG_SENSORS_ARRAY","time":timeStamp,"sensorTime:":res[1][0],"sensorsId:":res[1][1],"rightSensor:":res[1][2],"leftSensor:":res[1][3] })
                    else:
                        found = False
                elif(key=='STEP_END'):
                    res = getLOG_STEP_END(theLine)
                    data.append({"RecordType":"LOG_STEP_END","time":timeStamp,"step:":res[0],"returnValue:":res[1] })
                elif(key=='ENCODERS_ID_EVENT'):
                    res = getLOG_ENCODERS_ID_EVENT(theLine)
                    data.append({"RecordType":"LOG_ENCODERS_ID_EVENT","time":timeStamp,"rightEncoderPulses:":res[0],"leftEncoderPulses:":res[1],"encoderDistanceMm:":res[2],"encoderDistancePulses:":res[3] })
                elif(key=='LOCATION_DATA_ENCODERS_DISTANCE'):
                    res = getLOG_LOCATION_DATA_ENCODERS_DISTANCE(theLine)
                    data.append({"RecordType":"LOG_LOCATION_DATA_ENCODERS_DISTANCE","time":timeStamp,"rightEncoderMm:":res[0],"leftEncoderMm:":res[1] })
                elif(key=='LOCATION_SURFACE_DATA'):
                    res = getLOG_LOCATION_SURFACE_DATA(theLine)
                    data.append({"RecordType":"LOG_LOCATION_SURFACE_DATA","time":timeStamp,"surfaceType:":res[0],"surfaceId:":res[1],"position_X:":res[2],"position_Y:":res[3] })
                elif(key=='ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN'):
                    res = getLOG_ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN(theLine)
                    data.append({"RecordType":"LOG_ROBOT_MANAGER_CHECK_TILT_BEFORE_START_CLEAN","time":timeStamp,"pitch:":res[0],"readCountBelowMaxTiltAllowed:":res[1] })
                elif(key=='ROBOT_MANAGER_START_CLEAN'):
                    res = getLOG_ROBOT_MANAGER_START_CLEAN(theLine)
                    data.append({"RecordType":"LOG_ROBOT_MANAGER_START_CLEAN","time":timeStamp,"cleanProcedure:":res[0] })
                elif(key=='MAGNET'):
                    res = getLOG_MAGNET(theLine)
                    data.append({"RecordType":"LOG_MAGNET","time":timeStamp,"magnetStatus:":res[0] })
                elif(key=='STEP_EDGE_END'):
                    res = getLOG_STEP_EDGE_END(theLine)
                    data.append({"RecordType":"LOG_STEP_EDGE_END","time":timeStamp,"movement:":res[0],"step:":res[1],"returnValue:":res[2],"yaw:":res[3],"roll:":res[4],"pitch:":res[5] })
                elif(key=='STEP_START'):
                    res = getLOG_STEP_START(theLine)
                    if(res[0]=='LOG_STEP_START'):
                        data.append({"RecordType":"LOG_STEP_START","time":timeStamp,"step:":res[1][0] })
                    elif(res[0]=='LOG_STEP_START_EDGE_MOVE'):
                        data.append({"RecordType":"LOG_STEP_START_EDGE_MOVE","time":timeStamp,"step:":res[1][0],"toEdge:":res[1][1],"direcionTo:":res[1][2] })
                    elif(res[0]=='LOG_STEP_START_CROSS_BRIDGE'):
                        data.append({"RecordType":"LOG_STEP_START_CROSS_BRIDGE","time":timeStamp,"step:":res[1][0],"closestEdge:":res[1][1],"directionToEdge:":res[1][2] })
                    elif(res[0]=='LOG_STEP_START_CALIBRATION'):
                        data.append({"RecordType":"LOG_STEP_START_CALIBRATION","time":timeStamp,"step:":res[1][0],"calibrationDirection:":res[1][1] })
                    else:
                        found = False
                elif(key=='ROBOT_MANAGER_CLEANING_DONE'):
                    res = getLOG_ROBOT_MANAGER_CLEANING_DONE(theLine)
                    data.append({"RecordType":"LOG_ROBOT_MANAGER_CLEANING_DONE","time":timeStamp,"cleanProcedure:":res[0],"returnValue:":res[1] })
                elif(key=='PROCEDURE_START'):
                    res = getLOG_PROCEDURE_START(theLine)
                    data.append({"RecordType":"LOG_PROCEDURE_START","time":timeStamp,"procedure:":res[0],"startEdge:":res[1],"startFromSegment:":res[2],"startToSegment:":res[3],"startFromIteration:":res[4] })
                elif(key=='LOCATION_CHANGE_SURFACE'):
                    res = getLOG_LOCATION_CHANGE_SURFACE(theLine)
                    data.append({"RecordType":"LOG_LOCATION_CHANGE_SURFACE","time":timeStamp,"prevSurfaceId:":res[0],"prevSurfaceType:":res[1],"currentSurfaceType:":res[2],"position_X:":res[3],"position_Y:":res[4] })
        if(not found):
            if(theLine[3]=='LOG_GENERAL_DATA'):
                i=i+1
                continue
            else:
                print(line)
        #print(i)
        #print(line)
        #if(i>14323):
        #    print(i)
        i+=1
    json.dump(data,outputFile,separators=(',', ':'), indent=2)




def main(argv):
    (lines,outputFile,logFile)  = openFiles(argv[1])
    logLinesAnalizer(lines,outputFile,logFile.name)
    logFile.close()
    outputFile.close()
    

if __name__ == "__main__":
    main(sys.argv)

