import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        super().__init__()
        self.type = type
        self.game = game

        if type == 1:
            self.name = "Platform"
            self.image = self.game.platform_image
        elif type == 2:
            self.name = "FloatingPlatform"
            self.image = self.game.floatingplatorm_image
        elif type == 6:
            self.name = "UpMovingPlatformSocket"
            self.image = self.game.upmovingplatformsocket_image
        elif type == 7:
            self.name = "EmptyPlatform"
            self.image = self.game.emptyplatform_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class SideMovingPlatform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.name = "SideMovingPlatform"
        self.image = self.game.sidemovingplatform_image
        self.position_y = 0
        self.up = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        if self.up:
            self.rect.x -= 1
            self.position_y += 1
        else:
            self.rect.x += 1
            self.position_y -= 1

        hit = pygame.sprite.collide_rect(self, self.game.player)
        if hit:
            if self.up is True:
                self.game.player.rect.right = self.rect.left
            else:
                self.game.player.rect.left = self.rect.right

        if self.position_y == 120:
            self.up = False
        if self.position_y == 0:
            self.up = True


class UpMovingPlatform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.name = "UpMovingPlatform"
        self.image = self.game.upmovingplatform_image
        self.positiony = 0
        self.up = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y-110

    def update(self):
        if self.up:
            self.positiony += 1
            self.rect.y -= 1
        else:
            self.positiony -= 1
            self.rect.y += 1

        if self.positiony == 140:
            self.up = False
        if self.positiony == 0:
            self.up = True





