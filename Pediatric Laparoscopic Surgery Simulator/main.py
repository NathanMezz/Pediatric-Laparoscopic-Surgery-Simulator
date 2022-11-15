'''
SYSC4907 Capstone Engineering Project "Pediatric Laparoscopic Surgery Simulator"

Main program file for Pediatric Laparoscopic Surgery Simulator Project
Run this file to run the project

Author: Nathan Mezzomo
Date Created: November 2, 2022
Last Edited: November 2, 2022
'''

import cv2
import numpy as np

# Class for GUI
class GUI(object):
    def __init__(self, cameraID, font, windowName):
        self.image_state = 0

        self.cap = cv2.VideoCapture(cameraID)  # Camera ID can be 0, 1, etc.

        # Setting video capture size to be 1920x1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Setting FPS to 60, may need to lower this for the augmented reality
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        ret, frame = self.cap.read()
        self.displayHeight, self.displayWidth, other = frame.shape

        # Main menu image
        self.main_menu = np.zeros([720, 1280, 3], np.uint8)
        self.font = font
        self.windowName = windowName

        cv2.namedWindow(self.windowName)




def main():

    def evaluate_state():
        if GUI.image_state == 1:
            # Get latest video frame
            ret, frame = GUI.cap.read()
            cv2.putText(frame, "Test", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, frame)
        else:
            cv2.putText(GUI.main_menu, "Pediatric Laparoscopic Training Simulator", (800, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Ring Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, GUI.main_menu)

    def quit_program():
        GUI.cap.release()
        cv2.destroyAllWindows

    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Sectioning window into 4 corners
            # TODO: Section state changes based on current GUI state
            # Top left click
            if y < GUI.displayHeight/2 and x < GUI.displayWidth/2:
                print("Top left")
                GUI.image_state = 1
            # Top right click
            elif y < GUI.displayHeight/2 and x > GUI.displayWidth/2:
                print("Top right")
                GUI.image_state = 0
            # Bottom left click
            elif y > GUI.displayHeight/2 and x < GUI.displayWidth/2:
                print("Bottom left")
                GUI.image_state = -1
            # Bottom right click
            elif y > GUI.displayHeight/2 and x > GUI.displayWidth/2:
                print("Bottom right")

    cv2.setMouseCallback("Test Window", mouse_event)


    #TODO: While running call methods to evaluate state, get newest video frame, etc.
    while True:
        evaluate_state()

        key = cv2.waitKey(1)
        if key == ord("q") or GUI.image_state == -1:    # state -1 will tell program to quit
            quit_program()
            break




if __name__ == '__main__':
    cameraID = 0 # Set Camera ID to change camera input (0, 1, etc.)
    font = cv2.FONT_HERSHEY_SIMPLEX
    windowName = "Test Window"

    # Create an instance of "GUI"
    GUI = GUI(cameraID, font, windowName)

    # Call to execute main method
    main()




