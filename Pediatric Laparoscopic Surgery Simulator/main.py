'''
SYSC4907 Capstone Engineering Project "Pediatric Laparoscopic Surgery Simulator"

Main program file for Pediatric Laparoscopic Surgery Simulator Project
Run this file to run the project

Author: Nathan Mezzomo
Date Created: November 2, 2022
Last Edited: November 17, 2022
'''

import cv2
import numpy as np

# Class for GUI
class GUI(object):
    def __init__(self, cameraID, font, windowName):
        self.image_state = 0

        self.cap = cv2.VideoCapture(cameraID)  # Camera ID can be 0, 1, etc.
        self.object_detector = cv2.createBackgroundSubtractorMOG2()

        # Setting video capture size to be 1280x720p
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Setting FPS to 60, may need to lower this for the augmented reality
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        ret, frame = self.cap.read()
        self.displayHeight, self.displayWidth, other = frame.shape

        # Main menu image
        self.main_menu = np.zeros([720, 1280, 3], np.uint8)
        self.font = font
        self.windowName = windowName

        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        self.out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))

        cv2.namedWindow(self.windowName)




def main():
    '''
    Image states:
    1 = Ring Task
    2 = Suturing Task
    3 = Analysis ? (Maybe split into a couple)
    -1 = quit
    0 = main menu
    '''

    # TODO: If this gets bulky, should generalize text locations to simplify future modifications
    def evaluate_state():
        if GUI.image_state == 1:
            # TODO: Try to add tool tip tracking for the AR
            # TODO: Implement the existing AR for this game that doesn't require sensor input
            # Get latest video frame
            ret, frame = GUI.cap.read()

            # Only write/show a frame if there was a new capture
            if ret == True:
                cv2.putText(frame, "Ring Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
                cv2.putText(frame, "Main Menu", (1100, 35), GUI.font, 1, (0, 0, 255), 2)
                # TODO: implement the object detection

                GUI.out.write(frame)
                cv2.imshow(GUI.windowName, frame)

        elif GUI.image_state == 2:
            ret, frame = GUI.cap.read()
            cv2.putText(frame, "Suturing Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Main Menu", (1100, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, frame)
        elif GUI.image_state == 0:
            cv2.putText(GUI.main_menu, "Pediatric Laparoscopic Training Simulator", (320, 360), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Ring Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Suturing Task", (1025, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Quit", (25, 685), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, GUI.main_menu)

    def quit_program():
        GUI.cap.release()
        cv2.destroyAllWindows

    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Section state changes based on current GUI state
            # Main menu options
            if GUI.image_state == 0:
                # Sectioning window into 4 corners
                # Top left click
                if y < GUI.displayHeight/2 and x < GUI.displayWidth/2:
                    print("Top left")
                    GUI.image_state = 1     # Ring Task
                # Top right click
                elif y < GUI.displayHeight/2 and x > GUI.displayWidth/2:
                    print("Top right")
                    GUI.image_state = 2     # Suturing Task
                # Bottom left click
                elif y > GUI.displayHeight/2 and x < GUI.displayWidth/2:
                    print("Bottom left")
                    GUI.image_state = -1    # Quit
                # Bottom right click
                elif y > GUI.displayHeight/2 and x > GUI.displayWidth/2:
                    print("Bottom right")   # TODO: Tutorial Videos?
            # Ring Task options
            elif GUI.image_state == 1:
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:
                    GUI.image_state = 0  # Back to main menu
            # Suturing Task options
            elif GUI.image_state == 2:
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:
                    GUI.image_state = 0  # Back to main menu


    cv2.setMouseCallback("Test Window", mouse_event)


    # While running, make required calls to evaluate the current program state
    while True:
        evaluate_state()

        # Can press "q" key anytime to quit, no matter GUI state
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