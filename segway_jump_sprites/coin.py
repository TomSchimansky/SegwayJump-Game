import pygame
import math


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.name = "coin"
        self.game = game
        self.counter = 0
        self.image = self.game.coin_1_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x+35, y+35
        self.pos = self.rect.y

    def update(self):
        self.counter += 0.1
        self.rect.y = self.pos + math.sin(self.counter) * 10


