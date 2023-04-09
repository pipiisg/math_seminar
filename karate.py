import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
karate_club = open("karate_club.txt", "r")
connections = {a:[] for a in range(34)}
for a in karate_club:
    s = list(map(int, a.split(" ")))
    connections[s[0] - 1].append(s[1] - 1)
    connections[s[1] - 1].append(s[0] - 1)
class Person:
    def __init__(self, num, val, peopleList):
        self.num = num
        self.val = val
        self.deltaVal = 0
        self.peopleList = peopleList
        self.neighbors = connections[num]
    
    def findDeltaVal(self):
        self.deltaVal = 0
        for a in self.neighbors:
            self.deltaVal += (self.peopleList[a].val - self.val)  / len(self.peopleList) / 10

    def update(self):
        self.val += self.deltaVal
        if self.val > 1:
            self.val = 1
        if self.val < 0:
            self.val = 0
peopleList = []
for a in range(34):
    peopleList.append(Person(a, a % 2, peopleList))
posX = [math.cos(2 * math.pi / 34 * a) for a in range(34)]
posY = [math.sin(2 * math.pi / 34 * a) for a in range(34)]
def runIteration():
    for a in peopleList:
        a.findDeltaVal()
    for a in peopleList:
        a.update()
    valList = list(map(lambda c: c.val, peopleList))
    colorList = list(map(lambda v: [1 - v, 0, v, 0.5], valList))
    return colorList
fig, ax = plt.subplots()
ln = plt.scatter(posX, posY)

def init():
    return ln,

def update(frame):
    print(frame)
    ln.set_color(runIteration())
    return ln,

ani = FuncAnimation(fig, update, frames=range(10000),
                    init_func=init, blit=True)
plt.show()