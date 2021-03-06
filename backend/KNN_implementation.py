################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import thread, time, math
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, './LeapSDK/lib'))
sys.path.insert(0, lib_dir)
lib_dir = os.path.abspath(os.path.join(src_dir, './LEAPSDK/lib/x86'))
sys.path.insert(0, lib_dir)
import Leap, csv
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


files = os.listdir(".")
print files
# creating one datatable from all csvs....
allTables = []
for file in files:
    if file.endswith('Data'):
        data = pd.read_csv(file, header=None).select_dtypes(include=['float'])
        data['symbol'] = file[0]
        allTables.append(data)

data = pd.concat(allTables)

data.symbol = data.symbol.astype('category')

# separating into input and output variables then testing and training sets...
X = data.select_dtypes(exclude=['category'])
y = data.copy().select_dtypes(include=['category'])
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# generating model and training. tentatively using 5 as n_neighbors
knn = KNeighborsClassifier(n_neighbors=8, metric='euclidean')
knn.fit(X_train, np.ravel(y_train,order='C'))

# predicted value
y_pred = knn.predict(X_test)

# samplePrediction = [-14.9686536789,136.0546875,66.1265411377,-14.9686536789,136.0546875,66.1265411377,0.0,0.0,0.0,-14.9686536789,136.0546875,66.1265411377,-33.8622169495,124.423171997,24.8965930939,0.403531074524,0.24842736125,0.880594432354,-33.8622169495,124.423171997,24.8965930939,-29.7998561859,117.189155579,-9.96576023102,-0.113359838724,0.201864629984,0.972831070423,-29.7998561859,117.189155579,-9.96576023102,-15.952755928,114.50025177,-30.1176795959,-0.562931060791,0.109312951565,0.819243133068,-15.3825874329,157.679107666,60.9750175476,-50.7743492126,161.451721191,1.85731267929,0.512885689735,-0.0546714663506,0.856714248657,-50.7743492126,161.451721191,1.85731267929,-70.1160354614,166.011260986,-38.690410614,0.428336292505,-0.100974462926,0.897960007191,-70.1160354614,166.011260986,-38.690410614,-79.1194229126,162.629898071,-62.2037391663,0.354406058788,0.133102729917,0.925570070744,-79.1194229126,162.629898071,-62.2037391663,-84.766998291,158.412063599,-78.7202301025,0.3144929111,0.234875842929,0.91974323988,-6.70283842087,162.946334839,55.4699363708,-32.581905365,169.327560425,-4.2952041626,0.395465999842,-0.097513474524,0.913289546967,-32.581905365,169.327560425,-4.2952041626,-39.2041053772,129.27053833,-34.5952453613,0.130716592073,0.790691554546,0.598097026348,-39.2041053772,129.27053833,-34.5952453613,-27.9437980652,107.58543396,-17.3833675385,-0.37675127387,0.725547790527,-0.575881004333,-27.9437980652,107.58543396,-17.3833675385,-19.7132358551,105.473457336,0.446611762047,-0.416711568832,0.106928922236,-0.90272796154,3.37654089928,165.577194214,50.5437850952,-11.7187108994,173.768630981,-5.64363479614,0.256924450397,-0.1394200176,0.956322014332,-11.7187108994,173.768630981,-5.64363479614,-14.6286497116,131.718612671,-26.3460712433,0.0619660355151,0.895439088345,0.44085046649,-14.6286497116,131.718612671,-26.3460712433,-7.51458263397,114.45500946,-4.00550079346,-0.244335085154,0.592924356461,-0.767294585705,-7.51458263397,114.45500946,-4.00550079346,-2.57665753365,116.747093201,14.862537384,-0.251451194286,-0.116718493402,-0.960806488991]
# samplePrediction = np.reshape(samplePrediction,(1,-1))
# testy = knn.predict(samplePrediction)
# output report
# print testy
print '\nClassification report:\n', classification_report(y_test, y_pred)

class SampleListener(Leap.Listener):


    cache = []
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        print frame

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
            #     direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            #     arm.direction,
            #     arm.wrist_position,
            #     arm.elbow_position)

            # Get fingers
            fingerList = []
            handCapture = []
            for finger in hand.fingers:
                fingerCapture = []
                boneList = []
                boneList.append(finger.bone(0).prev_joint)
                boneList.append(finger.bone(1).prev_joint)
                boneList.append(finger.bone(2).prev_joint)
                boneList.append(finger.bone(3).prev_joint)
                boneList.append(finger.bone(4).next_joint)
                fingerList.append(boneList)
                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type],
                #     finger.id,
                #     finger.length,
                #     finger.width)

                # Get bones
                for b in range(0, 4):
                    boneCapture = []
                    bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #     self.bone_names[bone.type],
                    #     bone.prev_joint,
                    #     bone.next_joint,
                    #     bone.direction)
                    boneCapture.append(self.bone_names[bone.type])
                    boneCapture.append(bone.prev_joint)
                    boneCapture.append(bone.next_joint)
                    boneCapture.append(bone.direction)
                    fingerCapture.append(boneCapture)
                handCapture.append(fingerCapture)

            handAngles = getHandAngles(handCapture)
            thumbAngle = handAngles[0] if handAngles[0] > 0 and handAngles[0] < 180 else 0
            indexAngle = handAngles[1] if handAngles[1] > 0 and handAngles[1] < 180 else 0
            middleAngle = handAngles[2] if handAngles[2] > 0 and handAngles[2] < 180 else 0
            ringAngle = handAngles[3] if handAngles[3] > 0 and handAngles[3] < 180 else 0
            pinkyAngle = handAngles[4] if handAngles[4] > 0 and handAngles[4] < 180 else 0

            directions = handAngles[5]
    

            
            # temp = []
            # for i in range(0,5):
            #     for j in range(0,4):
            #         for k in range(1,4):
            #             for l in range(0,3):
            #                 temp.append(handCapture[i][j][k][l])

            # pitch = direction.pitch * Leap.RAD_TO_DEG
            # roll = normal.roll * Leap.RAD_TO_DEG
            # yaw = direction.yaw * Leap.RAD_TO_DEG

            # auxiliary = [hand.palm_position[0],hand.palm_position[1],hand.palm_position[2],pitch,roll,yaw]
            # for x in auxiliary:
            #     temp.append(x)

            #samplePrediction = [-14.9686536789,136.0546875,66.1265411377,-14.9686536789,136.0546875,66.1265411377,0.0,0.0,0.0,-14.9686536789,136.0546875,66.1265411377,-33.8622169495,124.423171997,24.8965930939,0.403531074524,0.24842736125,0.880594432354,-33.8622169495,124.423171997,24.8965930939,-29.7998561859,117.189155579,-9.96576023102,-0.113359838724,0.201864629984,0.972831070423,-29.7998561859,117.189155579,-9.96576023102,-15.952755928,114.50025177,-30.1176795959,-0.562931060791,0.109312951565,0.819243133068,-15.3825874329,157.679107666,60.9750175476,-50.7743492126,161.451721191,1.85731267929,0.512885689735,-0.0546714663506,0.856714248657,-50.7743492126,161.451721191,1.85731267929,-70.1160354614,166.011260986,-38.690410614,0.428336292505,-0.100974462926,0.897960007191,-70.1160354614,166.011260986,-38.690410614,-79.1194229126,162.629898071,-62.2037391663,0.354406058788,0.133102729917,0.925570070744,-79.1194229126,162.629898071,-62.2037391663,-84.766998291,158.412063599,-78.7202301025,0.3144929111,0.234875842929,0.91974323988,-6.70283842087,162.946334839,55.4699363708,-32.581905365,169.327560425,-4.2952041626,0.395465999842,-0.097513474524,0.913289546967,-32.581905365,169.327560425,-4.2952041626,-39.2041053772,129.27053833,-34.5952453613,0.130716592073,0.790691554546,0.598097026348,-39.2041053772,129.27053833,-34.5952453613,-27.9437980652,107.58543396,-17.3833675385,-0.37675127387,0.725547790527,-0.575881004333,-27.9437980652,107.58543396,-17.3833675385,-19.7132358551,105.473457336,0.446611762047,-0.416711568832,0.106928922236,-0.90272796154,3.37654089928,165.577194214,50.5437850952,-11.7187108994,173.768630981,-5.64363479614,0.256924450397,-0.1394200176,0.956322014332,-11.7187108994,173.768630981,-5.64363479614,-14.6286497116,131.718612671,-26.3460712433,0.0619660355151,0.895439088345,0.44085046649,-14.6286497116,131.718612671,-26.3460712433,-7.51458263397,114.45500946,-4.00550079346,-0.244335085154,0.592924356461,-0.767294585705,-7.51458263397,114.45500946,-4.00550079346,-2.57665753365,116.747093201,14.862537384,-0.251451194286,-0.116718493402,-0.960806488991]
            #temp = np.reshape(temp,(1,-1))
            val = [thumbAngle,indexAngle,middleAngle,ringAngle,pinkyAngle]
            for i in directions:
                val.append(i)

            val = np.reshape(val, (1,-1))
            prediction = knn.predict(val)
            print hand.pinch_strength
            print prediction

            # Todo:
            # cache.add([val,prediction,velocity])
            # if cache > 300 pop(0)
            # hard code 2 dynamic letters

            


            # FINGERS:
            # 0 - thumb [x,y,z]
            # 4 - pinky [x,y,z]
            #print "", fingerList[0][0]

            
            

        if not frame.hands.is_empty:
            print ""

def getHandAngles(hand):
    temp = []
    for x in range(0,5):
        for i in range(0,4):
            currentFinger = hand[x]
            temp.append(str(currentFinger[i][0]))
            for j in range(1,4):
                for k in range(0,3):
                    temp.append(str(currentFinger[i][j][k]))
    #print(temp)
    #values found in mapping.txt 
    index_metacarpal_end = [float(temp[44]),float(temp[45]),float(temp[46])]
    index_proximal_end = [float(temp[54]),float(temp[55]),float(temp[56])]
    index_intermediate_end = [float(temp[64]),float(temp[65]),float(temp[66])]
    index_direction = [float(temp[67]),float(temp[68]),float(temp[69])]

    middle_metacarpal_end = [float(temp[84]),float(temp[85]),float(temp[86])]    
    middle_proximal_end = [float(temp[94]),float(temp[95]),float(temp[96])]
    middle_intermediate_end = [float(temp[104]),float(temp[105]),float(temp[106])]
    middle_direction = [float(temp[107]),float(temp[108]),float(temp[109])]

    ring_metacarpal_end = [float(temp[124]),float(temp[125]),float(temp[126])]
    ring_proximal_end = [float(temp[134]),float(temp[135]),float(temp[136])]
    ring_intermediate_end = [float(temp[144]),float(temp[145]),float(temp[146])]
    ring_direction = [float(temp[147]),float(temp[148]),float(temp[149])]

    pinky_metacarpal_end = [float(temp[164]),float(temp[165]),float(temp[166])]
    pinky_proximal_end = [float(temp[174]),float(temp[175]),float(temp[176])]
    pinky_intermediate_end = [float(temp[184]),float(temp[185]),float(temp[186])]
    pinky_direction = [float(temp[187]),float(temp[188]),float(temp[189])]

    thumb_metacarpal_end = [float(temp[4]),float(temp[5]),float(temp[6])]
    thumb_proximal_end = [float(temp[14]),float(temp[15]),float(temp[16])]
    thumb_intermediate_end = [float(temp[24]),float(temp[25]),float(temp[26])]
    thumb_direction = [float(temp[27]),float(temp[28]),float(temp[29])]

    thumbAngle = getAngle(thumb_metacarpal_end,thumb_proximal_end,thumb_intermediate_end)
    indexAngle = getAngle(index_metacarpal_end,index_proximal_end,index_intermediate_end)
    middleAngle = getAngle(middle_metacarpal_end,middle_proximal_end,middle_intermediate_end)
    ringAngle = getAngle(ring_metacarpal_end,ring_proximal_end,ring_intermediate_end)
    pinkyAngle = getAngle(pinky_metacarpal_end,pinky_proximal_end,pinky_intermediate_end)
    
    directions = []
    
    print "Thumb: ",thumbAngle
    print "Index: ", indexAngle
    print "Middle: ",middleAngle
    print "Ring: ",ringAngle
    print "Pinky: ", pinkyAngle

    for i in range(0,2):
        directions.append(thumb_direction[i])
        directions.append(index_direction[i])
        directions.append(middle_direction[i])
        directions.append(ring_direction[i])
        directions.append(pinky_direction[i])
    

    return [thumbAngle,indexAngle,middleAngle,ringAngle,pinkyAngle,directions]

def getAngle(a,b,c):
    ab = [b[0]-a[0],b[1]-a[1],b[2]-a[2]]
    bc = [c[0]-b[0],c[1]-b[1],c[2]-b[2]]

    vectorAB = math.sqrt(ab[0] * ab[0] + ab[1] * ab[1] + ab[2] * ab[2])
    vectorBC = math.sqrt(bc[0] * bc[0] + bc[1] * bc[1] + bc[2] * bc[2])

    abNorm = [ab[0] / vectorAB, ab[1] / vectorAB, ab[2] / vectorAB]
    bcNorm = [bc[0] / vectorBC, bc[1] / vectorBC, bc[2] / vectorBC]

    res = abNorm[0] * bcNorm[0] + abNorm[1] * bcNorm[1] + abNorm[2] * bcNorm[2]

    return math.acos(res)*180.0/ 3.141592653589793

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    print getAngle([1,0,0],[0,0,0],[0,1,0])

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
