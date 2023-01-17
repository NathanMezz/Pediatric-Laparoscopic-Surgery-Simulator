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
import time
import datetime

# Class for GUI
class GUI(object):

    def test_button(self):
        print("Test button pressed")
    def __init__(self, cameraID, font, windowName, displayWidth, displayHeight):
        self.image_state = 0

        start = time.time()
        print("Starting program. Please allow a few seconds...")
        '''
         Using cv2.CAP_DSHOW after cameraID specifies direct show, lets program start/open camera much faster.
            - Video recording FPS is incorrect with this though (Using 15fps makes it better, cant hold 30 fps maybe?)
         Some cameras start faster than others
         '''
        self.cap = cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)

        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        # Setting video capture size to be 1280x720p -> This slows startup considerably (Most sets do I think?)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.displayWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.displayHeight)


        # Use this when using direct show setting, otherwise it slows down the startup
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        print(self.cap.get(cv2.CAP_PROP_FPS))
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


        ret, frame = self.cap.read()


        # Main menu image
        self.main_menu = np.zeros([self.displayHeight, self.displayWidth, 3], np.uint8)
        self.font = font
        self.windowName = windowName

        self.out = None # defining variable for future assignment



        cv2.namedWindow(self.windowName)
        end = time.time()
        time_elapsed = end-start
        print("Program ready. It took ", time_elapsed, " seconds to start")

def main():
    '''
    Image states:
    1 = Ring Task
    2 = Suturing Task
    3 = Analysis ? (Maybe split into a couple)
    -1 = quit
    0 = main menu
    '''


    def play_video():

        vid = cv2.VideoCapture("outpy.avi")
        if(vid.isOpened() == False):
            print("Error opening video file")

        while(vid.isOpened()):

            ret,frame = vid.read()
            if ret == True:
                print("test")
                cv2.imshow(GUI.windowName, frame)

                # Press Q on keyboard to exit video at anytime
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        vid.release()
        GUI.image_state = 0



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
                cv2.putText(frame, "Date: " + str(datetime.datetime.now()),(500, 500), GUI.font, 1, (0, 0, 255), 2)
                # TODO: implement the object detection


                GUI.out.write(frame)
                cv2.imshow(GUI.windowName, frame)

        elif GUI.image_state == 2:
            ret, frame = GUI.cap.read()
            cv2.putText(frame, "Suturing Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Main Menu", (1100, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, frame)

        elif GUI.image_state == 3:
            play_video()
        elif GUI.image_state == 0:
            cv2.putText(GUI.main_menu, "Pediatric Laparoscopic Training Simulator", (320, 360), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Ring Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Suturing Task", (1030, 35), GUI.font, 1, (0, 0, 255), 2)
            cv2.putText(GUI.main_menu, "Watch Previous Attempt", (880, 685), GUI.font, 1, (0, 0, 255), 2)
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
                    GUI.out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30,
                                          (GUI.displayWidth, GUI.displayHeight))
                    GUI.image_state = 1     # Ring Task
                # Top right click
                elif y < GUI.displayHeight/2 and x > GUI.displayWidth/2:
                    GUI.image_state = 2     # Suturing Task
                # Bottom left click
                elif y > GUI.displayHeight/2 and x < GUI.displayWidth/2:
                    GUI.image_state = -1    # Quit
                # Bottom right click
                elif y > GUI.displayHeight/2 and x > GUI.displayWidth/2:
                    GUI.image_state = 3
                    print("Bottom right, not set to anything yet")   # TODO: Tutorial Videos?
            # Ring Task options
            elif GUI.image_state == 1:
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:
                    GUI.image_state = 0  # Back to main menu
            # Suturing Task options
            elif GUI.image_state == 2:
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:
                    GUI.image_state = 0  # Back to main menu


    cv2.setMouseCallback(GUI.windowName, mouse_event)

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
    windowName = "Pediatric Laparoscopic Training Simulator"
    displayWidth = 1280
    displayHeight = 720

    # Create an instance of "GUI"
    GUI = GUI(cameraID, font, windowName, displayWidth, displayHeight)

    # Call to execute main method
    main()