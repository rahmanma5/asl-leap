import thread, time
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
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s, grab strength: %s" % (
                handType, hand.id, hand.palm_position, hand.grab_strength)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)

            # Get fingers
            fingerList = []
            for finger in hand.fingers:
                boneList = []
                boneList.append(finger.bone(0).prev_joint)
                boneList.append(finger.bone(1).prev_joint)
                boneList.append(finger.bone(2).prev_joint)
                boneList.append(finger.bone(3).prev_joint)
                boneList.append(finger.bone(4).next_joint)
                fingerList.append(boneList)
                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width)

                # Get bones
                for b in range(0, 4):
                    boneCapture = []
                    bone = finger.bone(b)
                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                        self.bone_names[bone.type],
                        bone.prev_joint,
                        bone.next_joint,
                        bone.direction)

            handAnalysis(hand,fingerList)


        if not frame.hands.is_empty:
            print ""

def handAnalysis(hand,fingerList):
    if hand.grab_strength > 0.9:
        print "Could be A"

    thumbDirectionProximal = hand.fingers[0].bone(1).direction
    thumbDirectionInt = hand.fingers[0].bone(2).direction
    thumbDirectionDistal = hand.fingers[0].bone(3).direction
    diff = thumbDirectionProximal[0] - thumbDirectionDistal[0]
    if thumbDirectionInt[1] > 0.18 and hand.grab_strength < 0.2:
        print "Could be B"

    isC = True
    for x in range(1,3):
        if fingerList[x][1][1] < fingerList[x+1][1][1]+10:
            isC = False
    if isC:
        print "Could be a C"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

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
