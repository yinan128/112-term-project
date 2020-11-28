import os
from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
from cmu_112_graphics import *
import time


class Entity(object):
    def __init__(self,x,y,tilePath):
        # x,y better be col,row
        self.x = x
        self.y = y
        self.health = 5
        self.sector = None

        # initiate the spritestrip
        self.tiles = []
        spritestrip = self.loadImage(tilePath)
        for i in range(4):
            # hardcode here
            sprite = spritestrip.crop((24 * i, 0, 24 * (i + 1), 24))
            sprite = self.scaleImage(sprite, 2)
            self.tiles.append(sprite)

        # set a timer
        self.spriteCounter = 0
        self.timer = time.time()

    def move(self,dx,dy):
        self.x += dx
        self.y += dy

    # get realtime updated tile
    def getTile(self,i):
        period = time.time() - self.timer
        self.spriteCounter += int(period/0.1)
        self.spriteCounter %= len(self.tiles)
        # avoid period getting too large, reset it occasionally
        if self.spriteCounter == 0:
            self.timer = time.time()
        # return self.tiles[self.spriteCounter]
        return self.tiles[i]

    # image can only be locally loaded.
    # citation: !!
    def loadImage(self,path=None):
        if (path is None):
            path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select file: ', filetypes=(
            ('Image files', '*.png *.gif *.jpg'), ('all files', '*.*')))
            if (not path): return None
        image = Image.open(path)
        return image

    def scaleImage(self, image, scale):
        return image.resize((round(image.width*scale), round(image.height*scale)))

class Player(Entity):
    def __init__(self,x,y):
        # default tileImage
        super().__init__(x,y,"clone.png")

class Monster(Entity):
    pass