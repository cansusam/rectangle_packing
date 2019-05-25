import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.animation as animation

randInt = 40
max_X = randInt
max_Y = randInt

area_matrix = np.zeros([max_X, max_Y])

np.random.seed(123123)
x = []
y = []
w = []
h = []

all_points = []

errorBoxes = []
edgeColor = 'None'
alpha = 1
ims = []
fig, ax = plt.subplots(1)
ax.set_xlim([0, max_X])
ax.set_ylim([0, max_Y])

def animate(p):
    ax.add_collection(ims[p])
    ax.errorbar(x[0:p], y[0:p], fmt='None')

def get_set_of_points_in_new_rectangle(newX, newY, newW, newH):
    list = []
    for i in range(newX,newX+newW):
        for j in range(newY,newY+newH):
            list.append([i,j])
    return list

def check_if_overlap_happens(all_points: list, new_points: list, area_matrix):
    for element in new_points:
        if all_points.__contains__(element):
            return False
    for element in new_points:
        area_matrix[element[0]][element[1]] = 1
    return True

def find_closest_point(x: int, y: int, area_matrix):
    available_x = 0
    available_y = 0
    for i in area_matrix[x:, y]:
        if i == 0:
            available_x += 1
        else:
            break
    for i in area_matrix[x, y:]:
        if i == 0:
            available_y += 1
        else:
            break
    return [available_x, available_y]

possible_points = get_set_of_points_in_new_rectangle(0, 0, max_X, max_Y)

while len(possible_points) != 0:
    new_all_points = []
    while True:
        temp = possible_points[np.random.randint(len(possible_points))]
        newX = temp[0]
        newY = temp[1]
        [maxW, maxH] = find_closest_point(newX, newY, area_matrix)
        if maxW > 0 and maxH > 0:
            newW = np.random.randint(maxW) + 1
            newH = np.random.randint(maxH) + 1
            new_all_points = get_set_of_points_in_new_rectangle(newX, newY, newW, newH)
            if check_if_overlap_happens(all_points, new_all_points, area_matrix):
                break
    all_points = all_points + new_all_points
    possible_points = [t for t in possible_points if t not in new_all_points]
    x = np.append(x, newX)
    y = np.append(y, newY)
    w = np.append(w, newW)
    h = np.append(h, newH)

    rect = Rectangle((newX, newY), newW, newH, color=cm.jet(np.random.randint(256)))
    errorBoxes.append(rect)

    pc = PatchCollection(errorBoxes, alpha=alpha, edgecolor=edgeColor, match_original=True, animated=True)
    ims.append(pc,)

# writerName = 'ffmpeg'
# writerFormat = '.mp4'
writerName = 'imagemagick'
writerFormat = '.gif'
Writer = animation.writers[writerName]
writer = Writer(metadata=dict(artist='me'))
anim = animation.FuncAnimation(fig, func=animate, frames=len(ims), interval=200, blit=False)
anim.save("Animations/"+str(max_X)+'x'+str(max_Y)+str(writerFormat), writer=writer)

if len(possible_points) == 0:
    print("all possible points are used")
else:
    print(len(possible_points) + " possible points are remained")
