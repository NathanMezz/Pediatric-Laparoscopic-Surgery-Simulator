import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)


file = open("sensor_data.txt", "r")
lines = file.readlines()

time_arr = []
force_arr = []
test_arr = []

pmwX1_arr= []
pmwY1_arr = []

pmwX2_arr = []
pmwY2_arr = []

for line in lines:
    if(len(line.split("|")) == 10):
        line = line.strip('\n') # Remove new line char from end of line
        vars = line.split("|") # Split each element of the line into a var split up by | character
        time_arr.append(vars[0])
        force_arr.append(vars[1])
        test_arr.append(vars[2])
        pmwX1_arr.append(vars[8])
        pmwY1_arr.append(vars[9])
        pmwX2_arr.append(vars[6])
        pmwY2_arr.append(vars[7])

file.close()
#converts String values in array to numbers
time = [f"{float(num):.2f}" for (num) in time_arr]
force = [f"{float(num):.2f}" for (num) in force_arr]
test = [f"{float(num):.2f}" for (num) in test_arr]
surge_left = [f"{float(num):.2f}" for (num) in pmwX1_arr]
surge_right = [f"{float(num):.2f}" for (num) in pmwX2_arr]
roll_left = [f"{float(num):.2f}" for (num) in pmwY1_arr]
roll_right = [f"{float(num):.2f}" for (num) in pmwY2_arr]
#Ensures float type 32bit
time = np.array(time)
force = np.array(force, dtype=np.float32)
test = np.array(test, dtype=np.float32)
surge_left = np.array(surge_left, dtype=np.float32)
surge_right = np.array(surge_right, dtype=np.float32)
roll_left = np.array(roll_left, dtype=np.float32)
roll_right = np.array(roll_right, dtype=np.float32)

#print(len(time))


#l1, = ax.plot(time, force, label="force")
#l2, = ax.plot(time, test, visible=False, label="test")


visible_range = 15
y_range = 10
#How many x values shown on screen at once
ax.set_xlim(0, visible_range)
ax.set_ylim(-y_range, y_range)


# plt.axes(rect, projection=None, polar=False, **kwargs)
# rect is a 4-tuple of floats  = [left, bottom, width, height]
# A new axes is added with dimensions rect in normalized (0, 1) units using add_axes on the current figure.
# (left, bottom) specify lower left corner coordinates of the new axes in normalized (0, 1) units
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
aypos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

x = time
y1 = force
y2 = test
y3 = surge_left
y4 = surge_right
y5 = roll_left
y6 = roll_right



#fig, ax = plt.subplots()
l1, = ax.plot(x, y1, visible=False, color='blue', label='force')
l2, = ax.plot(x, y2, visible=False, color='red', label='test')
l3, = ax.plot(x, y3, visible=False, color='green', label='L_Surge')
l4, = ax.plot(x, y4, visible=False, color='pink', label='R_Surge')
l5, = ax.plot(x, y5, visible=False, color='purple', label='L_Roll')
l6, = ax.plot(x, y6, visible=False, color='brown', label='R_roll')
lines = [l1, l2, l3, l4, l5, l6]

fig.subplots_adjust(left=0.25)

rax = fig.add_axes([0.025, 0.4, 0.1, 0.2])
for line in lines:
    print(str(line.get_label()))

labels = [str(line.get_label()) for line in lines]
print(labels)
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)

# X-axis Slider(ax, label, valmin, valmax)
xpos = Slider(axpos, 'Time', 0, len(time)-visible_range, valinit=0., valstep=0.1)

# Y-axis Slider
ypos = Slider(aypos, 'Y-Range', 0.1, 2000, valinit=10, valstep=0.1)

def x_update(val):
    pos = xpos.val
    ax.set_xlim(pos, pos+visible_range)
    fig.canvas.draw_idle()

def y_update(val):
    pos = ypos.val
    ax.set_ylim(-pos, pos)
    fig.canvas.draw_idle()
def handleClick(label):
    index = labels.index(label)
    print(index)
    lines[index].set_visible(not lines[index].get_visible()) #Set visibility to be opposite of what it was set at
    print(lines[index].get_visible())
    plt.draw()

check.on_clicked(handleClick)

xpos.on_changed(x_update)
ypos.on_changed(y_update)
plt.show()
