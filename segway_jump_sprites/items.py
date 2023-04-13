import pygame


class EndItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.name = "finish"
        self.game = game
        self.image = self.game.finish_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x+10, y+10


class JumpBoost(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.name = "jumpboost"
        self.game = game
        self.image = self.game.jumpboost_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x+10, y+10


class SpeedDrop(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.name = "speeddrop"
        self.game = game
        self.image = self.game.speeddrop_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x+10, y+10
