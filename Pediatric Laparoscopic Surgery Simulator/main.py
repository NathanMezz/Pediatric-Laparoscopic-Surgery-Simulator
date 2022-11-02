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

        ret, frame = self.cap.read()
        self.displayHeight, self.displayWidth, other = frame.shape

        # basic background TODO: Convert this into main menu image
        self.black_image = np.zeros([self.displayHeight, self.displayWidth, 3], np.uint8)
        self.font = font
        self.windowName = windowName

        cv2.namedWindow(self.windowName)



def main():

    def mouse_event(event, x, y, flags, param):
        # TODO: Check what coordinates button click occurs, change image here instead of in loop (Get rid of image_state var)
        # TODO: If selecting a game, make a call to a method for that game, the while loop for the camera feed can go there
        if event == cv2.EVENT_LBUTTONDOWN:
            # Sectioning window into 4 corners
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
            # Bottom right click
            elif y > GUI.displayHeight/2 and x > GUI.displayWidth/2:
                print("Bottom right")

    cv2.setMouseCallback("Test Window", mouse_event)

    while True:
        ret, frame = GUI.cap.read()

        # Placing text on each image
        cv2.putText(frame, "Test", (25, 35), GUI.font, 1, (0, 0, 255), 2)
        cv2.putText(GUI.black_image, "Test 2", (25, 35), GUI.font, 1, (0, 0, 255), 2)

        # Change window image based on GUI image state
        if GUI.image_state == 0:
            cv2.imshow(GUI.windowName, frame)
        elif GUI.image_state == 1:
            cv2.imshow(GUI.windowName, GUI.black_image)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    GUI.cap.release()
    # TODO: Add a quit button and have program execute the destroy
    cv2.destroyAllWindows

if __name__ == '__main__':
    cameraID = 0 # Set Camera ID to change camera input (0, 1, etc.)
    font = cv2.FONT_HERSHEY_SIMPLEX
    windowName = "Test Window"

    # Create an instance of "GUI"
    GUI = GUI(cameraID, font, windowName)

    # Call to execute main method
    main()




