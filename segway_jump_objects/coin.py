import pygame as pg

from math import sin

class Coin(pg.sprite.Sprite):
    def __init__(self,game, x,y):
        pg.sprite.Sprite.__init__(self)
        self.name = "coin"
        self.game = game

        self.counter = 0

        self.image = self.game.coin1_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+35, y+35
        self.pos = self.rect.y

    def update(self):
        self.counter += 0.1
        self.rect.y = self.pos + sin(self.counter)*10


