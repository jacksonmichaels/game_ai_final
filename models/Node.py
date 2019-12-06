from . import Constants as const
from graphics import *
# node class for tree structure
class Node:
    def __init__(self, topLeft, botRight, left=None, right=None, direction=const.DIR, room=None, id=""):
        self.tl = topLeft
        self.br = botRight

        self.left = left
        self.right = right

        self.dir = direction  # directioon of the splpit this node made to make its children

        self.room = None

        self.parent = None

        self.room = room

        self.childRooms = []  # all of the rooms under this node in the tree
        self.id = id

    def getSize(self, mode='d'):
        wide = self.br.x - self.tl.x
        tall = self.br.y - self.tl.y

        if (mode == 'd'):  # this is to pick if you want the area or a tuple of the width and height
            return (wide, tall)
        else:
            return wide * tall
