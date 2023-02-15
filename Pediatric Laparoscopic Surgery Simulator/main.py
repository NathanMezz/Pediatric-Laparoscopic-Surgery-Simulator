'''
SYSC4907 Capstone Engineering Project "Pediatric Laparoscopic Surgery Simulator"

Main program file for Pediatric Laparoscopic Surgery Simulator Project
Run this file to run the project

Author: Nathan Mezzomo
Date Created: November 2, 2022
Last Edited: February 8, 2023
'''

import cv2
import numpy as np
import time
import serial

'''
GUI class contains variables for use throughout the program as well as 
image capture settings, interface settings, etc.
'''
class GUI(object):

    def __init__(self, cameraID, font, windowName, displayWidth, displayHeight, red_low, red_high,
                 green_low, green_high, blue_low, blue_high):
        self.image_state = 5

        start = time.time()
        print("Starting program. Please allow a few seconds...")

        # Using cv2.CAP_DSHOW after cameraID specifies direct show, lets program start/open camera much faster.
        self.cap = cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)

        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        # HSV detection values
        self.red_low = red_low
        self.red_high = red_high
        self.green_low = green_low
        self.green_high = green_high
        self.blue_low = blue_low
        self.blue_high = blue_high

        self.task_state = 0 # Ring/suturing task states
        self.timer = 0 # timer variable for moving between task states in ring task

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.displayWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.displayHeight)

        # Use this when using direct show setting, otherwise it slows down the startup
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        print(self.cap.get(cv2.CAP_PROP_FPS))
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        ret, frame = self.cap.read()

        # Main menu image
        self.main_menu = np.zeros([self.displayHeight, self.displayWidth, 3], np.uint8)

        # Startup screen to show sensors starting
        self.startup_screen = np.zeros([self.displayHeight, self.displayWidth, 3], np.uint8)

        self.font = font
        self.windowName = windowName

        # defining variables for future assignment
        self.out = None     # Video output
        self.ser = None     # Serial var for sensor data input

        cv2.namedWindow(self.windowName)
        end = time.time()
        time_elapsed = end-start
        print("Program ready. It took ", time_elapsed, " seconds to start")

def main():

    '''
    Closes the serial port to stop sensors
    '''
    def stop_sensors():
        GUI.ser.close()

    '''
    Open serial port to start sensor data collection
    '''
    def start_sensors():
        try:
            GUI.ser = serial.Serial('COM5', 9600)
            print("test")
        except serial.SerialException:
            serial.Serial('COM5', 9600).close()
            GUI.ser = serial.Serial('COM5', 9600)
            print("test2")

    '''
    Plays video of most recent task attempt
    '''
    def play_video():

        vid = cv2.VideoCapture("outpy.avi")
        if(vid.isOpened() == False):
            print("Error opening video file")

        while(vid.isOpened()):

            ret,frame = vid.read()
            if ret == True:
                cv2.imshow(GUI.windowName, frame)
                # Press Q on keyboard to exit video at anytime
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        vid.release()
        GUI.image_state = 0

    # set detection bounds based off task state


    '''
    Checks which state the interface is currently is, and processes information depending
    on that state.
    Image States:
    -1 - Quit program
    0 - Main Menu
    1 - Ring Task
    2 - Suturing Task
    3 - Video playback
    4 - Post Task feedback
    5 - Sensor startup page (Initial startup screen to wait for sensor startup)
    '''
    def evaluate_state():
        '''
        Ring task.
        States:
        1 - Red ring/peg
        2 - Green ring/peg
        3 - Blue ring/peg
        other - end of task
        '''
        if GUI.image_state == 1:
            # Get latest video frame
            ret, frame = GUI.cap.read()

            # Only write/show a frame if there was a new capture
            if ret == True:
                # cv2.putText(frame, "Date: " + str(datetime.datetime.now()),(500, 500), GUI.font, 1, (0, 0, 255), 2)
                frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_bound = None
                upper_bound = None

                #set detection bounds based off task state
                if (GUI.task_state == 1):  # red
                    lower_bound = GUI.red_low
                    upper_bound = GUI.red_high
                elif (GUI.task_state == 2):  # green
                    lower_bound = GUI.green_low
                    upper_bound = GUI.green_high
                elif (GUI.task_state == 3):  # blue
                    lower_bound = GUI.blue_low
                    upper_bound = GUI.blue_high
                else:
                    lower_bound = np.array([255, 255, 255])
                    upper_bound = np.array([255, 255, 255])     #TODO: Are these needed here?
                    GUI.image_state = 0
                    return

                myMask = cv2.inRange(frameHSV, lower_bound, upper_bound)

                contours,_ = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                cv2.putText(frame, "Ring Task", (25, 35), GUI.font, 1, (0, 0, 255), 2)
                cv2.putText(frame, "Main Menu", (1100, 35), GUI.font, 1, (0, 0, 255), 2)
                contour_count = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    # Only detect countours of this size range, may need changing if camera view of task differs
                    if area > 150 and area < 6250:
                        contour_count += 1
                        (x, y, w, h) = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x - 20, y - 20), (x + 20 + w, y + 20 + h), (255, 0, 0), 2)

                # if contour count < 2 for 3 seconds, move onto next task state
                stuff = GUI.ser.readline()
                stuff_string = stuff.decode()
                print(stuff_string.rstrip()) # Printing sensor data to console for testing

                #TODO: Process sensor data for warnings, save to file with timestamp...
                if(contour_count < 2 and (time.time() - GUI.timer > 3)):
                    GUI.timer = time.time()
                    GUI.task_state += 1 # move into next state
                elif(contour_count > 1):
                    GUI.timer = time.time() # reset timer

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
        elif GUI.image_state == 5:
            cv2.putText(GUI.startup_screen, "Starting sensors, please wait...", (320, 360), GUI.font, 1, (0, 0, 255), 2)
            cv2.imshow(GUI.windowName, GUI.startup_screen)
            start_sensors()
            key = cv2.waitKey(15000)
            #time.sleep(15)
            GUI.image_state = 0

    '''
    Exits program, shuts everything down as needed
    '''
    def quit_program():
        GUI.cap.release()
        cv2.destroyAllWindows
        stop_sensors()

    '''
    Looks for left mouse click anywhere on screen.
    There are different options depending on the which section of the
    screen is clicked, and which screen is currently active'''
    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Section state changes based on current GUI state
            # Main menu options
            if GUI.image_state == 0:
                # Sectioning window into 4 corners
                # Top left click
                if y < GUI.displayHeight/2 and x < GUI.displayWidth/2:
                    GUI.out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (GUI.displayWidth, GUI.displayHeight))
                    GUI.image_state = 1     # Ring Task
                    GUI.task_state = 1
                    GUI.ser.flushInput()
                    GUI.timer = time.time()
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
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:  # Top Right click
                    GUI.image_state = 0  # Back to main menu
            # Suturing Task options
            elif GUI.image_state == 2:
                if y < GUI.displayHeight / 2 and x > GUI.displayWidth / 2:  # Top Right click
                    GUI.image_state = 0  # Back to main menu

    # Calls mouse_event function if mouse is clicked on the open window
    cv2.setMouseCallback(GUI.windowName, mouse_event)

    print("Starting Sensors, please wait at least 16 seconds")
    '''
    While running, make required calls to evaluate the current program state
    '''
    while True:
        evaluate_state()
        #TODO: add live-feedback checker

        # Can press "q" key anytime to quit, no matter GUI state
        key = cv2.waitKey(1)
        if key == ord("q") or GUI.image_state == -1:    # state -1 will tell program to quit
            quit_program()
            break

'''
This is the first code that runs at program startup.
Set any values that may change here before creation of GUI class object
and call to main()
'''
if __name__ == '__main__':
    cameraID = 1    # Set Camera ID to change camera input (0, 1, etc.)
    font = cv2.FONT_HERSHEY_SIMPLEX
    windowName = "Pediatric Laparoscopic Training Simulator"
    displayWidth = 1280
    displayHeight = 720

    '''
    HSV Ranges
    Use HSV.py to find appropriate values if recalibration required
    '''
    red_low = np.array([0, 200, 150])  # [H, S, V]
    red_high = np.array([15, 255, 255])
    green_low = np.array([25, 100, 50])
    green_high = np.array([95, 255, 255])
    blue_low = np.array([75, 65, 70])
    blue_high = np.array([160, 255, 255])

    # Create an instance of "GUI"
    GUI = GUI(cameraID, font, windowName, displayWidth, displayHeight,
              red_low, red_high, green_low, green_high, blue_low, blue_high)
    # Call to execute main method
    main()