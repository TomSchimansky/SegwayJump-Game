import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x ,y ,type):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.game = game

        # Platform
        if type == 1:
            self.name = "Platform"
            self.image = self.game.platform_image

        # FloatingPlatform
        if type == 2:
            self.name = "FloatingPlatform"
            self.image = self.game.floatingplatorm_image

        # UpMovingPlatformSocket
        if type == 6:
            self.name = "UpMovingPlatformSocket"
            self.image = self.game.upmovingplatformsocket_image

        # EmptyPlatform
        if type == 7:
            self.name = "EmptyPlatform"
            self.image = self.game.emptyplatform_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class SideMovingPlatform(pg.sprite.Sprite):
    def __init__(self, game, x ,y ,type):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.game = game

        self.name = "SideMovingPlatform"

        # SideMovingPlatform
        if type == 3:
            self.image = self.game.sidemovingplatform_image

        self.positiony = 0
        self.up = True

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        if self.up:
            self.rect.x -= 1
            self.positiony += 1
        else:
            self.rect.x += 1
            self.positiony -= 1

        hit = pg.sprite.collide_rect(self, self.game.player)
        if hit:
            if self.up == True:
                self.game.player.rect.right = self.rect.left
            else:
                self.game.player.rect.left = self.rect.right

        if self.positiony == 120:
            self.up = False
        if self.positiony == 0:
            self.up = True


class UpMovingPlatform(pg.sprite.Sprite):
    def __init__(self,x ,y, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = type

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





