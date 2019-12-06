from . import Constants as const
from . import Node
from . import Room
from graphics import *
import numpy as np
import random

class BSPTree:
    def __init__(self, minSize, window):
        self.adjMatrix = None
        self.distance_matrix = None
        self.min = minSize
        self.win = window
        self.head = Node.Node(Point(0, 0), Point(const.WINDOW_WIDTH, const.WINDOW_HEIGHT), id="")
        self.rooms = []
        self.bossRooms = []
        self.goldRooms = []

    # wrapper function to do all of the generation
    def makeMap(self):
        self.generate(self.head)

        self.makeRoomList(self.head)

        self.rooms = self.head.childRooms

        numNodes = len(self.rooms)
        self.adjMatrix = np.zeros((numNodes,numNodes))

        self.connectRooms(self.head.left.left, self.head.left.right, 1)
        self.connectRooms(self.head.left.right, self.head.right.left, 2)
        self.connectRooms(self.head.right.left, self.head.right.right, -1)



        spawn = self.colorRandomRoom(self.head.left.left.childRooms, const.SPAWN, "spawn")

        self.makeRandomLinks(self.head.left.left.childRooms)
        self.makeRandomLinks(self.head.left.right.childRooms)
        self.makeRandomLinks(self.head.right.left.childRooms)

        goldRooms = self.colorDeadEnds(const.GOLD)

        self.makeBossRooms(goldRooms)

        self.getRandomGoldRoom(self.head.left.left.childRooms, const.KEY_2_COLOR, "pink key")
        self.getRandomGoldRoom(self.head.left.right.childRooms, const.KEY_1_COLOR, "teal key")
        self.getRandomGoldRoom(self.head.right.left.childRooms, const.KEY_3_COLOR, "green key")

        self.getRandomGoldRoom(self.head.right.right.childRooms, const.ESCAPE, "Escape")


        self.makeDistMatrix(self.adjMatrix)


        room_difis = [(room, self.distance_matrix[spawn.id][room.id]) for room in self.rooms]

        for pair in room_difis:
            pair[0].setDifi(pair[1])
            pair[0].draw(self.win)

        for i in room_difis:
            print(i[0].id, i[1])

    def findBossLink(self, id):
        for j in range(len(self.rooms)):
            if (self.adjMatrix[id][j] and self.rooms[j].name != "spawn"):
                self.rooms[j].setColor(const.BOSS)
                self.rooms[j].name = "BossRooms"
                self.rooms[j].addContent("BossRooms")
                return self.rooms[j]

    def makeBossRooms(self, goldRooms):
        for i in range(len(goldRooms)):
            if (goldRooms[i] == 1):
                self.bossRooms.append(self.findBossLink(i))
        return 0

    def colorDeadEnds(self, color):
        vals = self.adjMatrix.sum(axis=1)
        for i in range(len(vals)):
            if (vals[i] == 1 and self.rooms[i].name!="spawn"):
                self.rooms[i].setColor(color)
                self.rooms[i].name = "goldRoom"
                self.rooms[i].addContent("goldRoom")
                self.goldRooms.append(self.rooms[i])
        return vals
    def makeDistMatrix(self, matrix):
        base_mat = matrix.copy()
        morph_mat = matrix.copy()
        k = 2
        while np.count_nonzero(morph_mat == 0):
            new_mat = np.linalg.matrix_power(base_mat, k)
            mask = (morph_mat == 0)
            new_mat = np.multiply(new_mat, mask)
            new_mat[(new_mat!=0)] = k
            morph_mat += new_mat
            k+=1

        self.distance_matrix = morph_mat





    # function to make the tree structure and generate the rooms inside each leaf
    def generate(self, node):
        (wide, tall) = node.getSize()
        if (node.dir):  # if the node im looking at is to be split horizontally
            line = int(random.randrange(0, wide) * 0.4 + wide * 0.3)  # the line that will be used to split the cell

            left = Node.Node(node.tl, Point(node.tl.x + line, node.br.y), direction=not node.dir, id=node.id + 'L ')

            right = Node.Node(Point(node.tl.x + line, node.tl.y), node.br, direction=not node.dir, id=node.id + 'R ')

        else:

            line = int(random.randrange(0, tall) * 0.4 + tall * 0.3)

            left = Node.Node(node.tl, Point(node.br.x, node.tl.y + line), direction=not node.dir, id=node.id + 'L ')

            right = Node.Node(Point(node.tl.x, node.tl.y + line), node.br, direction=not node.dir, id=node.id + 'R ')

        node.left = left
        node.right = right

        node.left.parent = node
        node.right.parent = node

        if (min(left.getSize()[0], left.getSize()[1]) < const.MIN_SIZE):

            room = self.randRoom(left.getSize()[0], left.getSize()[1])

            room.move(left.tl.x, left.tl.y)

            if (const.DRAW_GRID):
                Rectangle(node.left.tl, node.left.br).draw(self.win)

            node.left.room = room

        else:
            self.generate(node.left)

        if (min(right.getSize()[0], right.getSize()[1]) < const.MIN_SIZE):

            room = self.randRoom(right.getSize()[0], right.getSize()[1])

            room.move(right.tl.x, right.tl.y)


            if (const.DRAW_GRID):
                Rectangle(node.right.tl, node.right.br).draw(self.win)

            node.right.room = room

        else:
            self.generate(node.right)

    def linkRooms(self, pair, wall=0):
        link = Line(pair[0].getCenter(), pair[1].getCenter())
        if (const.RIGHT_ANGLE_HALL == False):
            midPoint = link.getCenter()
        else:
            midPoint = Point(pair[0].getCenter().x, pair[1].getCenter().y)

        line1 = Line(pair[0].getCenter(), midPoint)
        line2 = Line(midPoint, pair[1].getCenter())

        color = const.BASE

        if (wall == 2):
            color = const.KEY_1_COLOR
        elif (wall == 1):
            color = const.KEY_2_COLOR
        elif (wall == -1):
            color = const.KEY_3_COLOR
        line1.setFill(color)
        line2.setFill(color)

        line1.setWidth(const.PATH_WIDTH)
        line2.setWidth(const.PATH_WIDTH)

        line1.draw(self.win)
        line2.draw(self.win)

        pair[0].links.append(pair[1])
        pair[1].links.append(pair[0])
        if (pair[0].hall == False and pair[1].hall == False):
            self.adjMatrix[pair[0].id][pair[1].id] = 1
            self.adjMatrix[pair[1].id][pair[0].id] = 1

    def colorRandomRoom(self, list, color, new_name):
        valid = False
        while not valid:
            randomRoom = list[random.randrange(len(list))]
            if (randomRoom.name == "Normal"):
                randomRoom.setColor(color)
                randomRoom.name = new_name
                return randomRoom
                valid = True

    def getRandomGoldRoom(self, list, color, name):
        for room in list:
            if (room.name == "goldRoom"):
                room.setColor(color)
                room.name = name
                room.addContent(name)
                self.findBossLink(room.id).setColor(const.BIG_BOSS)
                return room
        room = list[random.randrange(len(list))]
        room.setColor(color)
        room.name = name
        room.addContent(name)
        return room



    def makeRandomLinks(self, rooms):
        for room in rooms:
            pick = random.randrange(3)
            if (pick == 1):
                distances = [(self.getDist(room.getCenter(), b.getCenter()),b) for b in rooms if b != room]
                distances.sort(key = lambda x: x[0])
                closest = distances[0][1]
                if (self.adjMatrix[room.id][distances[0][1].id] == 1):
                    closest = distances[1][1]
                self.linkRooms((room,closest))


    def makeRoomList(self, node):
        if (node.room):
            node.childRooms.append(node.room)
        if (node.left):
            node.childRooms += self.makeRoomList(node.left)
        if (node.right):
            node.childRooms += self.makeRoomList(node.right)

        return node.childRooms

    def connectRooms(self, nodeA, nodeB, state=0):
        if (nodeA):
            self.connectRooms(nodeA.left, nodeA.right, 0)

        if (nodeB):
            self.connectRooms(nodeB.left, nodeB.right, 0)

        if (nodeA and nodeB):
            pair = self.closestRooms(nodeA.childRooms, nodeB.childRooms)
            self.linkRooms(pair, state)
            if (state != 0):
                return pair
            else:
                return None


    def closestRooms(self, aRooms, bRooms):
        minDist = max(const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
        minPair = None

        for aRoom in aRooms:
            for bRoom in bRooms:
                dist = self.getDist(aRoom.getCenter(), bRoom.getCenter())
                if (dist < minDist):
                    minDist = dist
                    minPair = (aRoom, bRoom)

        return minPair

    def getDist(self, pointA, pointB):
        xdif = (pointA.x - pointB.x) ** 2
        ydif = (pointA.y - pointB.y) ** 2

        hyp = (xdif + ydif) ** 0.5

        return hyp

    def addPoints(self, a, b):
        ret = Point(a.x + b.x, a.y + b.y)

        return ret

    def randRoom(self, width, height):
        minDem = int(min(width, height) / 2)
        tl = Point(random.randrange(width - minDem), random.randrange(height - minDem))

        br = Point(random.randrange(tl.x + minDem, width), random.randrange(tl.y + minDem, height))

        room = Room.Room(tl, br, False)

        return room

    def getNumNodes(self, node):
        count = 1
        if (node.left):
            count+=self.getNumNodes(node.left)

        if (node.right):
            count += self.getNumNodes(node.right)
        return count


