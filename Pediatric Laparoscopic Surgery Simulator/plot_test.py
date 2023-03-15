import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

file = open("sensor_data.txt", "r")
lines = file.readlines()

time = []
force = []
L_pitch = []
L_yaw = []
L_surge = []
L_roll = []

R_pitch = []
R_yaw = []
R_surge = []
R_roll = []

for line in lines:
    if(len(line.split("|")) == 10):
        line = line.strip('\n') # Remove new line char from end of line
        vars = line.split("|") # Split each element of the line into a var split up by | character
        time.append(vars[0])
        force.append(vars[1])
        L_pitch.append(vars[2])
        L_yaw.append(vars[3])
        R_pitch.append(vars[4])
        R_yaw.append(vars[5])
        R_surge.append(vars[6])
        R_roll.append(vars[7])
        L_surge.append(vars[8])
        L_roll.append(vars[9])

file.close()
#Converts String values in array to numbers
time = [f"{float(num):.2f}" for (num) in time]
force = [f"{float(num):.2f}" for (num) in force]
L_pitch = [f"{float(num):.2f}" for (num) in L_pitch]
R_pitch = [f"{float(num):.2f}" for (num) in L_pitch]
L_yaw = [f"{float(num):.2f}" for (num) in L_yaw]
R_yaw = [f"{float(num):.2f}" for (num) in R_yaw]
L_surge = [f"{float(num):.2f}" for (num) in L_surge]
R_surge = [f"{float(num):.2f}" for (num) in R_surge]
L_roll = [f"{float(num):.2f}" for (num) in L_roll]
R_roll = [f"{float(num):.2f}" for (num) in R_roll]

#Ensures float type 32bit
#time = np.array(time) --> Don't need?
force = np.array(force, dtype=np.float32)
L_pitch = np.array(L_pitch, dtype=np.float32)
R_pitch = np.array(R_pitch, dtype=np.float32)
L_yaw = np.array(L_yaw, dtype=np.float32)
R_yaw = np.array(R_yaw, dtype=np.float32)
L_surge= np.array(L_surge, dtype=np.float32)
R_surge = np.array(R_surge, dtype=np.float32)
L_roll = np.array(L_roll, dtype=np.float32)
R_roll = np.array(R_roll, dtype=np.float32)


# How many x values shown on screen at once
visible_range = 15  # Range of x values visible at once
y_range = 10    # Default y range
ax.set_xlim(0, visible_range)
ax.set_ylim(-y_range, y_range)


# Slider positioning
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
aypos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)


y1 = force
y2 = L_pitch
y3 = L_surge
y4 = R_surge
y5 = L_roll
y6 = R_roll

# fig, ax = plt.subplots()
l1, = ax.plot(time, y1, visible=False, color='blue', label='Force')
l2, = ax.plot(time, L_pitch, visible=False, color='red', label='Left Pitch')
l3, = ax.plot(time, R_pitch, visible=False, color='green', label='Right Pitch')
l4, = ax.plot(time, L_yaw, visible=False, color='pink', label='Left Yaw')
l5, = ax.plot(time, R_yaw, visible=False, color='purple', label='Right Yaw')
l6, = ax.plot(time, L_surge, visible=False, color='brown', label='Left Surge')
l7, = ax.plot(time, R_surge, visible=False, color='brown', label='Right Surge')
l8, = ax.plot(time, L_roll, visible=False, color='brown', label='Left Roll')
l9, = ax.plot(time, R_surge, visible=False, color='brown', label='Right Roll')
lines = [l1, l2, l3, l4, l5, l6, l7, l8, l9]

fig.subplots_adjust(left=0.25)
rax = fig.add_axes([0.025, 0.4, 0.1, 0.2])

labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)

# X-axis Slider(ax, label, valmin, valmax)
xpos = Slider(axpos, 'Time', 0, len(time)-visible_range, valinit=0., valstep=0.1)
# Y-axis Slider
ypos = Slider(aypos, 'Y-Range', 0.1, 100, valinit=10, valstep=0.1)


def x_update(val):
    pos = xpos.val
    ax.set_xlim(pos, pos+visible_range)
    fig.canvas.draw_idle()


def y_update(val):
    pos = ypos.val
    ax.set_ylim(-pos, pos)
    fig.canvas.draw_idle()


def handle_click(label):
    index = labels.index(label)
    print(index)
    lines[index].set_visible(not lines[index].get_visible()) #Set visibility to be opposite of what it was set at
    print(lines[index].get_visible())
    plt.draw()


check.on_clicked(handle_click)

xpos.on_changed(x_update)
ypos.on_changed(y_update)
plt.show()
