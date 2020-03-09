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
lib_dir = os.path.abspath(os.path.join(src_dir, './LEAPSDK/lib/x64'))
sys.path.insert(0, lib_dir)
import Leap, csv
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, FadeTransition
from kivy.uix.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, NumericProperty

import os
import io

files = os.listdir(".")
# print files
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
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, np.ravel(y_train,order='C'))

# predicted value
y_pred = knn.predict(X_test)

# samplePrediction = [-14.9686536789,136.0546875,66.1265411377,-14.9686536789,136.0546875,66.1265411377,0.0,0.0,0.0,-14.9686536789,136.0546875,66.1265411377,-33.8622169495,124.423171997,24.8965930939,0.403531074524,0.24842736125,0.880594432354,-33.8622169495,124.423171997,24.8965930939,-29.7998561859,117.189155579,-9.96576023102,-0.113359838724,0.201864629984,0.972831070423,-29.7998561859,117.189155579,-9.96576023102,-15.952755928,114.50025177,-30.1176795959,-0.562931060791,0.109312951565,0.819243133068,-15.3825874329,157.679107666,60.9750175476,-50.7743492126,161.451721191,1.85731267929,0.512885689735,-0.0546714663506,0.856714248657,-50.7743492126,161.451721191,1.85731267929,-70.1160354614,166.011260986,-38.690410614,0.428336292505,-0.100974462926,0.897960007191,-70.1160354614,166.011260986,-38.690410614,-79.1194229126,162.629898071,-62.2037391663,0.354406058788,0.133102729917,0.925570070744,-79.1194229126,162.629898071,-62.2037391663,-84.766998291,158.412063599,-78.7202301025,0.3144929111,0.234875842929,0.91974323988,-6.70283842087,162.946334839,55.4699363708,-32.581905365,169.327560425,-4.2952041626,0.395465999842,-0.097513474524,0.913289546967,-32.581905365,169.327560425,-4.2952041626,-39.2041053772,129.27053833,-34.5952453613,0.130716592073,0.790691554546,0.598097026348,-39.2041053772,129.27053833,-34.5952453613,-27.9437980652,107.58543396,-17.3833675385,-0.37675127387,0.725547790527,-0.575881004333,-27.9437980652,107.58543396,-17.3833675385,-19.7132358551,105.473457336,0.446611762047,-0.416711568832,0.106928922236,-0.90272796154,3.37654089928,165.577194214,50.5437850952,-11.7187108994,173.768630981,-5.64363479614,0.256924450397,-0.1394200176,0.956322014332,-11.7187108994,173.768630981,-5.64363479614,-14.6286497116,131.718612671,-26.3460712433,0.0619660355151,0.895439088345,0.44085046649,-14.6286497116,131.718612671,-26.3460712433,-7.51458263397,114.45500946,-4.00550079346,-0.244335085154,0.592924356461,-0.767294585705,-7.51458263397,114.45500946,-4.00550079346,-2.57665753365,116.747093201,14.862537384,-0.251451194286,-0.116718493402,-0.960806488991]
# samplePrediction = np.reshape(samplePrediction,(1,-1))
# testy = knn.predict(samplePrediction)
# output report
# print testy
print '\nClassification report:\n', classification_report(y_test, y_pred)

kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 30
        id: buttons
    ScreenManager:
        id: sm
    Label:
        id: text_box
        text: ''
        markup: 'true'
    
'''

class MainScreen(Screen):
    pass

class RevengeScreen(Screen):
    def on_enter(self):
        with open('rots.txt') as f:
            read_in = f.read()
            tester.set_sentence(read_in)
        f.closed

class NewHopeScreen(Screen):
    def on_enter(self):
        with open('new_hope.txt') as f:
            read_in = f.read()
            tester.set_sentence(read_in)
        f.closed

class ScreenManagement(ScreenManager):
    pass


class GUI(App):

    def build(self):
        m = Builder.load_file("screen_layout.kv")
        return m


class SampleListener(Leap.Listener):

    
    
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    cache = []

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        #self.tester = TestingSoftware()
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

            temp = []
            for i in range(0,5):
                for j in range(0,4):
                    for k in range(1,4):
                        for l in range(0,3):
                            temp.append(handCapture[i][j][k][l])

            pitch = direction.pitch * Leap.RAD_TO_DEG
            roll = normal.roll * Leap.RAD_TO_DEG
            yaw = direction.yaw * Leap.RAD_TO_DEG

            velocity = hand.palm_velocity
            # for finger in hand.fingers:
            #     if finger.type == 4: #pinky
                    

            auxiliary = [hand.palm_position[0],hand.palm_position[1],hand.palm_position[2],pitch,roll,yaw]
            for x in auxiliary:
                temp.append(x)

            #samplePrediction = [-14.9686536789,136.0546875,66.1265411377,-14.9686536789,136.0546875,66.1265411377,0.0,0.0,0.0,-14.9686536789,136.0546875,66.1265411377,-33.8622169495,124.423171997,24.8965930939,0.403531074524,0.24842736125,0.880594432354,-33.8622169495,124.423171997,24.8965930939,-29.7998561859,117.189155579,-9.96576023102,-0.113359838724,0.201864629984,0.972831070423,-29.7998561859,117.189155579,-9.96576023102,-15.952755928,114.50025177,-30.1176795959,-0.562931060791,0.109312951565,0.819243133068,-15.3825874329,157.679107666,60.9750175476,-50.7743492126,161.451721191,1.85731267929,0.512885689735,-0.0546714663506,0.856714248657,-50.7743492126,161.451721191,1.85731267929,-70.1160354614,166.011260986,-38.690410614,0.428336292505,-0.100974462926,0.897960007191,-70.1160354614,166.011260986,-38.690410614,-79.1194229126,162.629898071,-62.2037391663,0.354406058788,0.133102729917,0.925570070744,-79.1194229126,162.629898071,-62.2037391663,-84.766998291,158.412063599,-78.7202301025,0.3144929111,0.234875842929,0.91974323988,-6.70283842087,162.946334839,55.4699363708,-32.581905365,169.327560425,-4.2952041626,0.395465999842,-0.097513474524,0.913289546967,-32.581905365,169.327560425,-4.2952041626,-39.2041053772,129.27053833,-34.5952453613,0.130716592073,0.790691554546,0.598097026348,-39.2041053772,129.27053833,-34.5952453613,-27.9437980652,107.58543396,-17.3833675385,-0.37675127387,0.725547790527,-0.575881004333,-27.9437980652,107.58543396,-17.3833675385,-19.7132358551,105.473457336,0.446611762047,-0.416711568832,0.106928922236,-0.90272796154,3.37654089928,165.577194214,50.5437850952,-11.7187108994,173.768630981,-5.64363479614,0.256924450397,-0.1394200176,0.956322014332,-11.7187108994,173.768630981,-5.64363479614,-14.6286497116,131.718612671,-26.3460712433,0.0619660355151,0.895439088345,0.44085046649,-14.6286497116,131.718612671,-26.3460712433,-7.51458263397,114.45500946,-4.00550079346,-0.244335085154,0.592924356461,-0.767294585705,-7.51458263397,114.45500946,-4.00550079346,-2.57665753365,116.747093201,14.862537384,-0.251451194286,-0.116718493402,-0.960806488991]
            temp = np.reshape(temp,(1,-1))
            prediction = knn.predict(temp)

            # if prediction == ["J"] or prediction == ["Z"]:
            #     if len(cache) < 300:
            #         cache.append(prediction)
            #     else:

            velocityX = velocity[0]
            velocityY = velocity[1]
            velocityZ = velocity[2]
            stillHand = False
            if abs(velocityX) < 12 and abs(velocityY) < 12 and abs(velocityY) < 12:
                stillHand = True
            # if not stillHand and (prediction == ["J"] or prediction == ["Z"]):
            #     print("J/Z in progress")
            #     print(velocity)
            # else:
            #     print prediction
            if not stillHand or len(self.cache) < 40:
                self.cache.append(prediction[0])
            else:
                mostOccurred = getMostOccurrences(self.cache)
                # App.get_running_app().root.ids.text_box.text = mostOccurred
                tester.checkAnswer(mostOccurred)
                # print(App.get_running_app().root.current)
                # temppp = App.get_running_app().root.current
                # print(App.get_running_app().root.ids.new_hope.ids)
                # print(App.get_running_app().root.ids[temppp].ids)
                print("Prediction being made: " + mostOccurred)
                self.cache = []
            


            # FINGERS:
            # 0 - thumb [x,y,z]
            # 4 - pinky [x,y,z]
            #print "", fingerList[0][0]

            
            

        #if not frame.hands.is_empty:
            #print ""

def getMostOccurrences(letters):
    d = {}
    for char in letters:
        if char not in d:
            d[char] = 0
        else:
            d[char] += 1

    maxOccurrences = 0
    maxChar = None
    for char in d:
        if d.get(char) > maxOccurrences:
            maxOccurrences = d.get(char)
            maxChar = char

    return maxChar


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
    #print "Index: ", indexAngle
    #print "Middle: ",middleAngle
    #print "Ring: ",ringAngle
    #print "Thumb: ",thumbAngle

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

class TestingSoftware():
    desired_letter = 0
    desired_sentence = ""
    sentence_array = []
    current_screen = ""
    current_index = 0
    def set_sentence(self,desired_input):
        print desired_input
        self.current_screen = App.get_running_app().root.current
        self.sentence_array = desired_input.splitlines()
        self.desired_sentence = self.sentence_array[0].strip()
        self.current_index = 1
        App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]" + self.desired_sentence + "[/color]"
        
    def checkAnswer(self,user_sign):
        print(self.sentence_array)
        print(self.current_index)
        if self.desired_letter >= len(self.desired_sentence):
            self.desired_letter = 0
            self.desired_sentence = self.sentence_array[self.current_index].strip()
            print(self.desired_sentence)
            print(self.current_index)
            self.current_index = self.current_index + 1
            App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]" + self.desired_sentence + "[/color]"
            return
        elif self.desired_letter >= len(self.desired_sentence) and self.current_index == len(self.sentence_array):
            self.desired_letter = 0
            App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]All finished![/color]"
            self.desired_sentence = ""
            return
        if self.desired_sentence[self.desired_letter] == " " or self.desired_sentence[self.desired_letter] == "." or self.desired_sentence[self.desired_letter] == "" or or self.desired_sentence[self.desired_letter] == "!":
            self.desired_letter =  self.desired_letter + 1
            return
        if user_sign == self.desired_sentence[self.desired_letter].upper():
            self.desired_letter =  self.desired_letter + 1
        green_half = "[color=00ff00]" + self.desired_sentence[0:self.desired_letter] + "[/color]"
        red_half = "[color=000000]" + self.desired_sentence[self.desired_letter:len(self.desired_sentence)] + "[/color]"
        App.get_running_app().root.ids[self.current_screen].ids.text_box.text = green_half + red_half
        if self.desired_letter+1 >= len(self.desired_sentence):
            print("GOT HERE")
            print(len(self.sentence_array))
            if self.desired_sentence[self.desired_letter] == "." and self.current_index < len(self.sentence_array):
                print("Am I here??")
                self.desired_letter = 0
                self.desired_sentence = self.sentence_array[self.current_index].strip()
                print(self.desired_sentence)
                print(self.current_index)
                self.current_index = self.current_index + 1
                App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]" + self.desired_sentence + "[/color]"
                return
            elif self.desired_sentence[self.desired_letter] == "." and self.current_index >= len(self.sentence_array):
                print("Am I here?")
                self.desired_letter = 0
                App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]All finished![/color]"
                self.desired_sentence = ""
            
        if red_half == "[color=000000][/color]" and self.current_index < len(self.sentence_array):
            self.desired_letter = 0
            self.desired_sentence = self.sentence_array[self.current_index].strip()
            self.current_index = self.current_index + 1
            App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]" + self.desired_sentence + "[/color]"
        elif red_half == "[color=000000][/color]" and self.current_index == len(self.sentence_array):
            self.desired_letter = 0
            App.get_running_app().root.ids[self.current_screen].ids.text_box.text = "[color=000000]All finished![/color]"
            self.desired_sentence = ""




def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    global tester
    tester = TestingSoftware()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    print getAngle([1,0,0],[0,0,0],[0,1,0])
    GUI().run()
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
