from graphics import color_rgb
# for Dir True = vertical False = horizontal
# Constants:
WINDOW_WIDTH = 1200  # width of window
WINDOW_HEIGHT = 600  # height of window
MIN_SIZE = 125  # minimum width or height allowed in a cell
DRAW_GRID = False  # draws the cell outlines
PATH_WIDTH = MIN_SIZE / 25  # width of the hallways, its set automatically but i included it so it can be changed if needed
COLORFUL = False  # sets the graphics to be colorful or black and white
RIGHT_ANGLE_HALL = False  # chooses if the system will make all halls virtical or horizontal. has issues when mixed with colorful
DIR = True
DRAW_ID = True
TREE = False
K_DEGREE = 9
KEY_1_COLOR = color_rgb(0, 255, 255)
KEY_2_COLOR = color_rgb(255, 0, 255)
KEY_3_COLOR = color_rgb(0, 255, 0)
ESCAPE = color_rgb(155, 155, 255)
SPAWN = color_rgb(0, 0, 255)
GOLD = color_rgb(255, 215, 0)
BOSS = color_rgb(255,0,0)
BIG_BOSS = color_rgb(150,0,0)
BASE = color_rgb(255, 255, 255)