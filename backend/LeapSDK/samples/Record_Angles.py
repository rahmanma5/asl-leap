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
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib/x86'))
sys.path.insert(0, lib_dir)
import Leap, csv

frameCounter = 1000

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global frameCounter
        frame = controller.frame()

        frame100 = None
        frame300 = None

        if frameCounter == 900 and frame100 != None:
            frame100 = frame
        if frameCounter == 700 and frame300 != None:
            frame300 = frame
        
        if frame100 != None:
            print frame.hands.rightmost.translation(frame100)

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

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

            # Get fingers
            fingerList = []
            handCapture = []
            for finger in hand.fingers:
                print finger.direction
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

            pitch = direction.pitch * Leap.RAD_TO_DEG
            roll = normal.roll * Leap.RAD_TO_DEG
            yaw = direction.yaw * Leap.RAD_TO_DEG
            
            if frameCounter > 0:
                writeToFile(thumbAngle,indexAngle,middleAngle,ringAngle,pinkyAngle,directions)
                frameCounter -= 1
                print frameCounter


            
            

        if not frame.hands.is_empty:
            print ""

def writeToFile(thumb,index,middle,ring,pinky,directions):
    angles = [thumb,index,middle,ring,pinky]
    for i in directions:
        angles.append(i)
    with open('YsaveData', 'a+') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(angles)


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
