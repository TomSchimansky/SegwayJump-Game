from segway_jump_libraries.settings import *

import pygame as pg

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.jumping = False

        self.current_frame = 0
        self.last_update = 0

        self.image = self.game.lw1

        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = 120, -120

        self.speed = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumpboost = 0
        self.jumpbooston = 0

        self.speeddrop = 0
        self.speeddropon = 0

        self.loadimages()

    def loadimages(self):
        lw1 = self.game.lw1
        lw2 = self.game.lw2
        lw3 = self.game.lw3
        j4 = self.game.j4
        j5 = self.game.j5
        self.left_walking_frames = [lw1, lw2, lw3]

        self.left_jumping_frames = [j5]
        self.right_jumping_frames = [pg.transform.flip(j5, True, False)]

        self.left_ducking_frames = [j4]
        self.right_ducking_frames = [pg.transform.flip(j4, True, False)]

        self.standing_frames = [lw1]

        self.right_walking_frames = [pg.transform.flip(lw1, True, False), pg.transform.flip(lw2, True, False), pg.transform.flip(lw3, True, False)]

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.game.jumpsound.play()
            self.speed.y = JUMP_SPEED - self.jumpboost
            self.jumping = True

    def animate(self):
        now = pg.time.get_ticks()

        if self.speed.x > 0 and self.speed.y == 0:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_walking_frames)
                self.image = self.left_walking_frames[self.current_frame]

        if self.speed.x < 0 and self.speed.y == 0:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_walking_frames)
                self.image = self.right_walking_frames[self.current_frame]

        if self.speed.y < 0 and self.speed.x >= 0:
            if now - self.last_update > 2:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_jumping_frames)
                self.image = self.left_jumping_frames[self.current_frame]

        if self.speed.y < 0 and self.speed.x < 0:
            if now - self.last_update > 2:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_jumping_frames)
                self.image = self.right_jumping_frames[self.current_frame]

        if self.speed.y == 0 and self.speed.x == 0 and self.jumping == False:
            if now - self.last_update > 1:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

        bottom = self.rect.bottom
        x = self.rect.x
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x

        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.animate()

        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            if hits[0].name == "UpMovingPlatform":
                self.rect.bottom = hits[0].rect.top

        self.acc = vec(0, GRAVITY)

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_X_ACC
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_X_ACC

        self.speed += self.acc


        if self.speed.x > MAX_SPEED-self.speeddrop:
            self.speed.x = MAX_SPEED-self.speeddrop
        if self.speed.x < -MAX_SPEED+self.speeddrop:
            self.speed.x = -MAX_SPEED+self.speeddrop

        self.rect.x += (self.speed.x)

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:

            if self.speed.x >= 0:
                self.rect.right = hits[0].rect.left
            elif self.speed.x < 0:
                self.rect.left = hits[0].rect.right

            self.speed.x = -self.speed.x * X_WALL_REFLECTION

        self.rect.y += self.speed.y

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if self.speed.y > 0:
                self.rect.bottom = hits[0].rect.top
            elif self.speed.y < 0:
                self.rect.top= hits[0].rect.bottom

            self.speed.y = 0
            self.jumping = False

        hits = pg.sprite.spritecollide(self, self.game.coins, False)
        for hit in hits:
            if hit.name == "finish":
                hit.kill()
                self.game.playing = False
                self.game.winsound.play()
            elif hit.name == "jumpboost":
                hit.kill()
                self.jumpbooston = 200
                self.jumpboost = 15
                self.game.powerupsound.play()
            elif hit.name == "speeddrop":
                hit.kill()
                self.speeddropon = 400
                self.speeddrop = 3
                self.game.powerupsound.play()
            else:
                hit.kill()
                self.game.score += 1
                self.game.coinsound.play()

        if self.jumpbooston == 0:
            self.jumpboost = 0
        else:
            self.jumpbooston -= 1

        if self.speeddropon == 0:
            self.speeddrop = 0
        else:
            self.speeddropon -= 1





