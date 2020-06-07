"""
Convert .png image to .txt to avoid
using PIL, which causes problems when
compling to .app.

from PIL import Image
def maketxt(path):
   image = Image.open(path)
   data = image.tobytes()
   f = open(path[0:-4]+".txt","wb")
   f.write(data)
   f.close
"""

import pygame as pg


"""colors"""
BLACK = (0  , 0  , 30  )
WHITE = (255, 255, 255)
RED   = (255, 0  , 0  )
GREEN = (0  , 255, 0  )
BLUE  = (0  , 0  , 255)
COIN_COLOR = (199, 102,  41)

"""debug modes"""
SHOW_FPS = False
NO_DIE = False

FPS = 45
WIDTH = 1280
HEIGHT = 0

TITLE = "Segway Jump"
VERSION = "3.2.0"

GRAVITY = 1.6
MAX_SPEED = 8
PLAYER_X_ACC = 1
X_WALL_REFLECTION = 0
JUMP_SPEED = -27


def load_image_from_txt(path, name, size):
    f = open(path[0:-4]+".txt","rb")
    data = f.read()
    return pg.image.fromstring(data, size, "RGBA")
