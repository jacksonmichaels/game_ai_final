import models.Constants as const
from models.BSPTree import BSPTree
from graphics import *


win = GraphWin("Game", const.WINDOW_WIDTH, const.WINDOW_HEIGHT)

win.setBackground(color_rgb(0, 0, 0))

tree = BSPTree(const.MIN_SIZE, win)

tree.makeMap()

win.getMouse()

win.close()
