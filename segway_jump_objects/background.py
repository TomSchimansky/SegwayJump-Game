import pygame as pg

import random as rd


class Background(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.name = "background"
        self.game = game

        r = rd.randint(1,4)
        if r == 1:
            self.image = self.game.steelpate1_image
        if r == 2:
            self.image = self.game.steelpate2_image
        if r == 3:
            self.image = self.game.steelpate3_image
        if r == 4:
            self.image = self.game.steelpate4_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
