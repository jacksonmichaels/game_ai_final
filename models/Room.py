from . import Constants as const
from graphics import *
import random
# Room class used as the actual room inside cells
class Room:
    id = 0
    def __init__(self, tl, br, hall):
        self.name = "Normal"
        self.contents = []
        self.difi = 0
        self.hall = hall
        self.id = Room.id
        Room.id += 1
        self.topL = tl
        self.botR = br

        self.shape = Rectangle(self.topL, self.botR)

        self.links = []

        if const.COLORFUL:
            self.color = color_rgb(random.randrange(255), random.randrange(255), random.randrange(255))
        else:
            self.color = color_rgb(255,255,255)

        self.shape.setFill(self.color)
        self.text = Text(Point(self.topL.x + 15, self.topL.y + 15), str(self.id))
        self.text.setFill(color_rgb(100, 100, 100))

        self.text_difi = Text(Point(self.topL.x + 15, self.topL.y + 30), self.difi)
        self.text_difi.setFill(color_rgb(255, 0, 0))

    def setColor(self, color):
        self.shape.setFill(color)

    def setDifi(self, dif):
        self.difi = dif
        self.text_difi.setText(self.difi)

    def addContent(self, thing):
        self.contents.append(Text(Point(self.topL.x + 15, self.topL.y + 15 * (3+len(self.contents))), thing))
        self.contents[-1].setFill(color_rgb(255,255,255))

    def draw(self, window, color=None):
        if (color != None):
            self.shape.setFill(color)
        self.shape.draw(window)
        if (const.DRAW_ID):
            self.text.draw(window)
            self.text_difi.draw(window)
            for cont in self.contents:
                cont.draw(window)

    def unDraw(self):
        self.shape.undraw()
        self.text.undraw()
        self.text_difi.undraw()
        for cont in self.contents:
            cont.undraw()


    def move(self, x, y):
        self.topL.x += x
        self.botR.x += x

        self.topL.y += y
        self.botR.y += y

        self.shape.move(x, y)
        self.text.move(x, y)
        self.text_difi.move(x,y)
        for cont in self.contents:
            cont.move(x,y)

    def getCenter(self):
        return Point((self.topL.x + self.botR.x) / 2, (self.topL.y + self.botR.y) / 2)
