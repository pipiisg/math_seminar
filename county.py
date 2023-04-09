import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import matplotlib.animation as animat

vote_data = open("county_stats_2016.csv")
vote_dict = {}
pop_dict = {}
s = csv.reader(vote_data, delimiter=',', quotechar='"')
for row in s:
    try:
        vote_dict[row[0]] = float(row[2]) / (float(row[2]) + float(row[3]))
        pop_dict[row[0]] = float(row[2]) + float(row[3])
    except:
        pass

f = open("county.json")
data = json.load(f) #data.keys() to get keys
county_map = data['county_map']
county_map_inv = {}
for a in county_map.keys():
    county_map_inv[county_map[a] - 1] = str(int(a))
neighbor_map = data['neighbor_map'] # This gets you the neighbor map in dictionary form
coordinates = data['(x,y) coordinates']
latitudes = data['latitude']
longitudes = data['longitude']
class County:
    def __init__(self, num, val, countyList):
        self.num = num
        self.val = val
        self.deltaVal = 0
        self.countyList = countyList
        self.neighbors = neighbor_map[str(self.num)]
        try:
            self.pop = pop_dict[county_map_inv[num - 1]]
        except:
            self.pop = 100000
    
    def findDeltaVal(self):
        self.deltaVal = 0
        for a in self.neighbors:
            self.deltaVal += (self.countyList[a - 1].val - self.val) / 10

    def update(self):
        self.val += self.deltaVal
        if self.val > 1:
            self.val = 1
        if self.val < 0:
            self.val = 0


countyList = []
for a in range(3108):
    try:
        countyList.append(County(a + 1, vote_dict[county_map_inv[a]], countyList))
    except:
        countyList.append(County(a + 1, 0.5, countyList))
def runIteration(ret = True):
    for a in countyList:
        a.findDeltaVal()
    for a in countyList:
        a.update()
    if ret:
        valList = list(map(lambda c: c.val, countyList))
        colorList = list(map(lambda v: [1 - v, 0, v, 0.5], valList))
        return colorList

fig, ax = plt.subplots()
ln = plt.scatter(longitudes, latitudes)

def init():
    return ln,

def update(frame):
    print(frame)
    for a in range(10 * int(2 ** (frame / 10))):
        runIteration(False)
    ln.set_color(runIteration())
    return ln,

ani = FuncAnimation(fig, update, frames=range(30),
                    init_func=init, blit=True)
Writer = animat.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save("county_animation.mp4", writer=writer)
#plt.show()