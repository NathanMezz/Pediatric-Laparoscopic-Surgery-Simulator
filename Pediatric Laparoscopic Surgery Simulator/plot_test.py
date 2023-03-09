import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)


file = open("sensor_data.txt", "r")
lines = file.readlines()

time_arr = []
force_arr = []

for line in lines:
    if(len(line.split("|")) == 10):
        line = line.strip('\n') # Remove new line char from end of line
        vars = line.split("|") # Split each element of the line into a var split up by | character
        time_arr.append(vars[0])
        force_arr.append(vars[1])


time = [f"{float(num):.2f}" for (num) in time_arr]
force = [f"{float(num):.2f}" for (num) in force_arr]
time = np.array(time)
force = np.array(force)
print(len(time))
plt.scatter(time, force)


visible_range = 15
#How many x values shown on screen at once
ax.set_xlim(0, visible_range)

# plt.axes(rect, projection=None, polar=False, **kwargs)
# rect is a 4-tuple of floats  = [left, bottom, width, height]
# A new axes is added with dimensions rect in normalized (0, 1) units using add_axes on the current figure.
# (left, bottom) specify lower left corner coordinates of the new axes in normalized (0, 1) units
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)


# Slider(ax, label, valmin, valmax)
spos = Slider(axpos, 'Pos', 0, len(time)-visible_range, valinit=0., valstep=0.1)

def update(val):
    pos = spos.val
    ax.set_xlim(pos, pos+visible_range)
    fig.canvas.draw_idle()


spos.on_changed(update)
plt.show()
