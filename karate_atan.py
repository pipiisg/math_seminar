import matplotlib.pyplot as plt
import networkx as nx
import math
karate_club = open("karate_club.txt", "r")
connections = {a:[] for a in range(34)}
edges = []
for a in karate_club:
    s = list(map(int, a.split(" ")))
    connections[s[0] - 1].append(s[1] - 1)
    connections[s[1] - 1].append(s[0] - 1)
    edges.append((s[0] - 1, s[1] - 1))
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
            self.deltaVal += (self.peopleList[a].val - self.val)
        self.deltaVal = math.atan(self.deltaVal) / 100

    def update(self):
        self.val += self.deltaVal
peopleList = []
G = nx.from_edgelist(edges)
for a in range(34):
    if a == 0:
        valInit = -1
    elif a == 33:
        valInit = 1
    else:
        valInit = 2 * math.exp(10 * nx.resistance_distance(G, 0, a)) / (math.exp(10 * nx.resistance_distance(G, 0, a)) + math.exp(10 * nx.resistance_distance(G, 33, a))) - 1
    peopleList.append(Person(a, valInit, peopleList))
def runIteration():
    for a in peopleList:
        a.findDeltaVal()
    for a in peopleList:
        a.update()
def splitUp():
    l = [1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22]
    for a in peopleList:
        if a.num + 1 in l:
            newL = []
            for b in a.neighbors:
                if b + 1 in l:
                    newL.append(b)
        else:
            newL = []
            for b in a.neighbors:
                if b + 1 not in l:
                    newL.append(b)
        a.neighbors = newL
    newEdges = []
    global edges
    for e in edges:
        if not ((e[0] + 1 in l) ^ (e[1] + 1 in l)):
            newEdges.append(e)
    edges = newEdges
    global G
    G = nx.from_edgelist(edges)
nodePos = {0: [-0.14632845, -0.32413367],
    1: [ 0.01149253, -0.22720004],
    2: [-0.07002121,  0.04324382],
    3: [-0.21928045, -0.20885048],
    4: [-0.21628772, -0.62280177],
    5: [-0.27822264, -0.74079444],
    6: [-0.16628713, -0.75357366],
    7: [-0.20772875, -0.13593929],
    8: [0.09921963, 0.02756592],
    9: [-0.15030646,  0.28993234],
    10: [-0.35010998, -0.60939186],
    11: [-0.49602103, -0.47595671],
    12: [-0.42857598, -0.31116739],
    13: [-0.03457212, -0.06844424],
    16: [-0.26298688, -1.        ],
    17: [ 0.00363821, -0.50099439],
    19: [ 0.13066131, -0.11470648],
    21: [ 0.11204003, -0.45625521],
    23: [0.06025177, 0.52058264],
    25: [-0.19976725,  0.54648043],
    24: [-0.31702844,  0.45806815],
    27: [-0.08805069,  0.39815322],
    28: [0.00564215, 0.25645939],
    29: [0.27280024, 0.53777132],
    26: [0.36257504, 0.6571425 ],
    30: [0.24211696, 0.04088221],
    31: [-0.10371951,  0.20283821],
    32: [0.23248489, 0.29874472],
    14: [0.46090219, 0.20481803],
    15: [0.47338058, 0.40663192],
    18: [0.48994639, 0.30835726],
    20: [0.19682396, 0.57889537],
    22: [0.40488657, 0.48421327],
    33: [0.17643222, 0.28942894]}
for a in range(0):
    runIteration()
colors = list(map(lambda c: 1/(1+math.exp(-c.val)), peopleList))
nx.draw(G, node_color=colors, cmap=plt.cm.Blues, with_labels = True, nodelist = list(range(34)), pos = nodePos)
plt.show()