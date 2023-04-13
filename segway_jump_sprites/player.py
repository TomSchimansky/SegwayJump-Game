from settings import *
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.image = self.game.character_left_walking_1_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 120, -120
        self.speed = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, GRAVITY)

        self.jumpboost = 0
        self.jumpbooston = 0
        self.speeddrop = 0
        self.speeddropon = 0

        lw1 = self.game.character_left_walking_1_image
        lw2 = self.game.character_left_walking_2_image
        lw3 = self.game.character_left_walking_3_image
        j4 = self.game.character_jump_1_image
        j5 = self.game.character_jump_2_image

        self.left_jumping_frames = [j5]
        self.right_jumping_frames = [pygame.transform.flip(j5, True, False)]
        self.left_ducking_frames = [j4]
        self.right_ducking_frames = [pygame.transform.flip(j4, True, False)]
        self.standing_frames = [lw1]
        self.left_walking_frames = [lw1, lw2, lw3]
        self.right_walking_frames = [pygame.transform.flip(lw1, True, False),
                                     pygame.transform.flip(lw2, True, False),
                                     pygame.transform.flip(lw3, True, False)]

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.game.jump_sound.play()
            self.speed.y = JUMP_SPEED - self.jumpboost
            self.jumping = True

    def animate(self):
        now = pygame.time.get_ticks()

        if self.speed.x > 0 and self.speed.y == 0:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_walking_frames)
                self.image = self.left_walking_frames[self.current_frame]

        elif self.speed.x < 0 and self.speed.y == 0:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_walking_frames)
                self.image = self.right_walking_frames[self.current_frame]

        elif self.speed.y < 0 and self.speed.x >= 0:
            if now - self.last_update > 2:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_jumping_frames)
                self.image = self.left_jumping_frames[self.current_frame]

        elif self.speed.y < 0 and self.speed.x < 0:
            if now - self.last_update > 2:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_jumping_frames)
                self.image = self.right_jumping_frames[self.current_frame]

        elif self.speed.y == 0 and self.speed.x == 0 and self.jumping is False:
            if now - self.last_update > 1:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

        bottom = self.rect.bottom
        x = self.rect.x
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animate()

        self.acc.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_X_ACC
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_X_ACC
        self.speed += self.acc

        if self.speed.x > MAX_SPEED-self.speeddrop:
            self.speed.x = MAX_SPEED-self.speeddrop
        if self.speed.x < -MAX_SPEED+self.speeddrop:
            self.speed.x = -MAX_SPEED+self.speeddrop

        self.rect.y += self.speed.y
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if self.speed.y > 0:
                self.rect.bottom = hits[0].rect.top
            elif self.speed.y < 0:
                self.rect.top = hits[0].rect.bottom

            self.speed.y = 0
            self.jumping = False

        self.rect.x += self.speed.x
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if self.speed.x >= 0:
                self.rect.right = hits[0].rect.left
            elif self.speed.x < 0:
                self.rect.left = hits[0].rect.right

            self.speed.x = -self.speed.x * X_WALL_REFLECTION

        hits = pygame.sprite.spritecollide(self, self.game.coins, False)
        for hit in hits:
            if hit.name == "finish":
                hit.kill()
                self.game.playing = False
                self.game.win_sound.play()
            elif hit.name == "jumpboost":
                hit.kill()
                self.jumpbooston = 200
                self.jumpboost = 15
                self.game.powerup_sound.play()
            elif hit.name == "speeddrop":
                hit.kill()
                self.speeddropon = 400
                self.speeddrop = 3
                self.game.powerup_sound.play()
            else:
                hit.kill()
                self.game.score += 1
                self.game.coin_sound.play()

        if self.jumpbooston == 0:
            self.jumpboost = 0
        else:
            self.jumpbooston -= 1

        if self.speeddropon == 0:
            self.speeddrop = 0
        else:
            self.speeddropon -= 1
