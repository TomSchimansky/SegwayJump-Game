import pygame as pg

class EndItem(pg.sprite.Sprite):
    def __init__(self, x,y, game):
        pg.sprite.Sprite.__init__(self)
        self.name = "finish"
        self.game = game

        self.image = self.game.finish_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+10, y+10


class JumpBoost(pg.sprite.Sprite):
    def __init__(self, x,y, game):
        pg.sprite.Sprite.__init__(self)
        self.name = "jumpboost"
        self.game = game

        self.image = self.game.jumpboost_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+10, y+10

class SpeedDrop(pg.sprite.Sprite):
    def __init__(self, x,y, game):
        pg.sprite.Sprite.__init__(self)
        self.name = "speeddrop"
        self.game = game

        self.image = self.game.speeddrop_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+10, y+10

