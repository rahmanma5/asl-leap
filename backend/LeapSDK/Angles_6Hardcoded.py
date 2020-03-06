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
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib/x64'))
sys.path.insert(0, lib_dir)
import Leap, csv


class SampleListener(Leap.Listener):
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

            handAngles = logHandData(handCapture)
            indexAngle = handAngles[0] if handAngles[0] > 0 and handAngles[0] < 180 else 0
            middleAngle = handAngles[1] if handAngles[1] > 0 and handAngles[1] < 180 else 0
            ringAngle = handAngles[2] if handAngles[2] > 0 and handAngles[2] < 180 else 0
            thumbAngle = handAngles[3] if handAngles[3] > 0 and handAngles[3] < 180 else 0

            if hand.grab_strength > 0.9:
                if thumbAngle > 35:
                    print "Could be E"
                else:
                    print "Could be A"

            

            thumbDirectionProximal = hand.fingers[0].bone(1).direction
            thumbDirectionInt = hand.fingers[0].bone(2).direction
            thumbDirectionDistal = hand.fingers[0].bone(3).direction
            diff = thumbDirectionProximal[0] - thumbDirectionDistal[0]

            if thumbDirectionInt[1] > 0.18 and hand.grab_strength < 0.2:
                compareIndex = (middleAngle + ringAngle) / 2.0
                if indexAngle-compareIndex > 10:
                    print "Could be F"
                else:
                    print "Could be B"

            
            #print "It be ", intermediateList[0][1]
            isC = True
            for x in range(1,3):
                if fingerList[x][1][1] < fingerList[x+1][1][1]+10:
                    isC = False
            if isC:
                compareIndex = (middleAngle + ringAngle) / 2.0
                if abs(indexAngle-compareIndex) > 20:
                    print "Could be D"
                else:
                    print "Could be a C"


            # FINGERS:
            # 0 - thumb [x,y,z]
            # 4 - pinky [x,y,z]
            #print "", fingerList[0][0]

            
            

        if not frame.hands.is_empty:
            print ""

def logHandData(hand):
    temp = []
    for x in range(0,4):
        for i in range(0,4):
            currentFinger = hand[x]
            temp.append(str(currentFinger[i][0]))
            for j in range(1,4):
                for k in range(0,3):
                    temp.append(str(currentFinger[i][j][k]))
    #print(temp)
    joint1 = [float(temp[44]),float(temp[45]),float(temp[46])]
    joint2 = [float(temp[54]),float(temp[55]),float(temp[56])]
    joint3 = [float(temp[71]),float(temp[72]),float(temp[73])]

    joint4 = [float(temp[84]),float(temp[85]),float(temp[86])]
    joint5 = [float(temp[94]),float(temp[95]),float(temp[96])]
    joint6 = [float(temp[111]),float(temp[112]),float(temp[113])]

    joint7 = [float(temp[124]),float(temp[125]),float(temp[126])]
    joint8 = [float(temp[134]),float(temp[135]),float(temp[136])]
    joint9 = [float(temp[151]),float(temp[152]),float(temp[153])]

    thumb1 = [float(temp[4]),float(temp[5]),float(temp[6])]
    thumb2 = [float(temp[14]),float(temp[15]),float(temp[16])]
    thumb3 = [float(temp[31]),float(temp[32]),float(temp[33])]

    indexAngle = getAngle(joint1,joint2,joint3)
    middleAngle = getAngle(joint4,joint5,joint6)
    ringAngle = getAngle(joint7,joint8,joint9)
    thumbAngle = getAngle(thumb1,thumb2,thumb3)
    print "Index: ", indexAngle
    print "Middle: ",middleAngle
    print "Ring: ",ringAngle
    print "Thumb: ",thumbAngle

    return [indexAngle,middleAngle,ringAngle,thumbAngle]

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