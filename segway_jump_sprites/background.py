import pygame
import random


class Background(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.name = "background"
        self.game = game

        r = random.randint(1, 4)
        if r == 1:
            self.image = self.game.steelpate_1_image
        elif r == 2:
            self.image = self.game.steelpate_2_image
        elif r == 3:
            self.image = self.game.steelpate_3_image
        elif r == 4:
            self.image = self.game.steelpate_4_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
