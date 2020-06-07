""" SegwayJump Copyright © 2018 Tom Schimansky """

from segway_jump_libraries.settings import *
from segway_jump_objects.platform import Platform, SideMovingPlatform, UpMovingPlatform
from segway_jump_objects.player import Player
from segway_jump_objects.coin import Coin
from segway_jump_objects.menubutton import MenuButton
from segway_jump_objects.item import EndItem, JumpBoost, SpeedDrop
from segway_jump_objects.background import Background
from segway_jump_libraries.Saving import save, read

from pygame.locals import *

import os
import random as rd

import segway_jump_levels.level1
import segway_jump_levels.level2
import segway_jump_levels.level3

import pygame as pg


class Game(object):
    def __init__(self):
        pg.init()
        print(TITLE + " Version " + VERSION + " Copyright © 2018 Tom Schimansky")

        global HEIGHT
        info_object = pg.display.Info()
        HEIGHT = round(WIDTH * (info_object.current_h / info_object.current_w))

        flags = HWSURFACE | DOUBLEBUF | FULLSCREEN
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags, 32)
        self.load_screen()

        pg.font.init()

        self.path = os.path.dirname(__file__)

        self.running = True
        self.playing = False
        self.pause = False
        self.act_level = None
        self.time = 0
        self.command_pressed = False

        self.highscore = []
        self.levels = []

        pg.display.set_icon(load_image_from_txt(self.path + "/assets/icons/icon.png", "icon", (312, 312)))
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.load()

    def load(self):
        try:
            self.highscore = read(self.path + "/assets/highscore_files/highscore.txt", "int", 1)
        except Exception:
            self.highscore = [0, 0, 0]

        self.levels.append(segway_jump_levels.level1.Level())
        self.levels.append(segway_jump_levels.level2.Level())
        self.levels.append(segway_jump_levels.level3.Level())

        self.backgroundmusic = pg.mixer.Sound(self.path + "/assets/sounds/Ambient Background Music - Cicada 3301.wav")
        self.coinsound = pg.mixer.Sound(self.path + "/assets/sounds/Blup.wav")
        self.diesound = pg.mixer.Sound(self.path + "/assets/sounds/sfx_die.wav")
        self.buttonsound = pg.mixer.Sound(self.path + "/assets/sounds/button-27.wav")
        self.jumpsound = pg.mixer.Sound(self.path + "/assets/sounds/JumpSound.wav")
        self.powerupsound = pg.mixer.Sound(self.path + "/assets/sounds/powerup.wav")
        self.winsound = pg.mixer.Sound(self.path + "/assets/sounds/Ding - Sound.wav")

        self.coins_image = load_image_from_txt(
            self.path + "/assets/images/coins.png", "coins", (174, 60)).convert_alpha()
        self.endbutton_image = load_image_from_txt(
            self.path + "/assets/images/endbutton.png", "endbutton", (171, 60)).convert_alpha()
        self.banner_icon = load_image_from_txt(self.path + "/assets/icons/icon.png", "icon", (312, 312)).convert_alpha()
        self.banner = load_image_from_txt(self.path + "/assets/images/banner.png", "banner", (764, 311)).convert_alpha()

        self.lw1 = load_image_from_txt(self.path + "/assets/images/playerleft1.png",
                                       "playerleft1", (50, 138)).convert_alpha()
        self.lw2 = load_image_from_txt(self.path + "/assets/images/playerleft2.png",
                                       "playerleft2", (50, 138)).convert_alpha()
        self.lw3 = load_image_from_txt(self.path + "/assets/images/playerleft3.png",
                                       "playerleft3", (50, 138)).convert_alpha()
        self.j4 = load_image_from_txt(self.path + "/assets/images/playerleft4.png",
                                      "playerleft4", (50, 122)).convert_alpha()
        self.j5 = load_image_from_txt(self.path + "/assets/images/playerleft5.png",
                                      "playerleft5", (50, 154)).convert_alpha()

        self.platform_image = load_image_from_txt(
            self.path + "/assets/images/platform.png", "platform", (120, 120)).convert()
        self.floatingplatorm_image = load_image_from_txt(self.path + "/assets/images/floatingplatform.png",
                                                         "floatingplatform", (120, 31)).convert_alpha()
        self.upmovingplatformsocket_image = load_image_from_txt(
            self.path + "/assets/images/movingsocketplatform.png", "movingsocketplatform", (120, 120)).convert_alpha()
        self.emptyplatform_image = load_image_from_txt(self.path + "/assets/images/middleplatform.png",
                                                       "middleplatform", (120, 120)).convert()
        self.sidemovingplatform_image = load_image_from_txt(
            self.path + "/assets/images/movingfloatingplatform.png", "movingfloatingplatform", (120, 31)).convert_alpha()
        self.upmovingplatform_image = load_image_from_txt(self.path + "/assets/images/movingplatform.png",
                                                          "movingplatform", (120, 320)).convert_alpha()

        self.coin1_image = load_image_from_txt(
            self.path + "/assets/images/coin1.png", "coin1", (50, 50)).convert_alpha()

        self.finish_image = load_image_from_txt(
            self.path + "/assets/images/finish.png", "finish", (100, 100)).convert_alpha()
        self.jumpboost_image = load_image_from_txt(
            self.path + "/assets/images/jumpboost.png", "jumpboost", (100, 100)).convert_alpha()
        self.speeddrop_image = load_image_from_txt(
            self.path + "/assets/images/speeddrop.png", "speeddrop", (100, 100)).convert_alpha()

        self.level_image = load_image_from_txt(
            self.path + "/assets/images/levels.png", "levels", (927, 564)).convert_alpha()
        self.menubutton_image = load_image_from_txt(
            self.path + "/assets/images/menubutton.png", "menubutton", (171, 60)).convert_alpha()
        self.startbutton_image = load_image_from_txt(
            self.path + "/assets/images/startbutton.png", "startbutton", (172, 60)).convert_alpha()

        self.steelpate1_image = load_image_from_txt(
            self.path + "/assets/images/Steelplate1.png", "steelplate1", (405, 191)).convert_alpha()
        self.steelpate2_image = load_image_from_txt(
            self.path + "/assets/images/Steelplate2.png", "steelplate2", (328, 302)).convert_alpha()
        self.steelpate3_image = load_image_from_txt(
            self.path + "/assets/images/Steelplate3.png", "steelplate3", (300, 191)).convert_alpha()
        self.steelpate4_image = load_image_from_txt(
            self.path + "/assets/images/Steelplate4.png", "steelplate4", (190, 300)).convert_alpha()

    def new(self):
        self.backgroundmusic.stop()
        self.backgroundmusic.play(-1)
        self.player = Player(self)

        self.platnumber = 0
        self.shift = 0
        self.score = 0

        self.platforms = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()
        self.lastbackground = 100
        self.coins = pg.sprite.Group()

        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.time = self.clock.tick(FPS)

    def update(self):
        self.all_sprites.update()

        if len(self.platforms) < 30:
            try:
                for i in range(len(self.levels[self.act_level].array[self.platnumber])):
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 1 or self.levels[self.act_level].array[self.platnumber][i][1] == 2 or self.levels[self.act_level].array[self.platnumber][i][1] == 6 or self.levels[self.act_level].array[self.platnumber][i][1] == 7:
                        platform = Platform(self, round(self.platnumber * 120) - self.shift, HEIGHT -
                                            self.levels[self.act_level].array[self.platnumber][i][0], self.levels[self.act_level].array[self.platnumber][i][1])
                        self.platforms.add(platform)
                        self.all_sprites.add(platform)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 3:
                        platform = SideMovingPlatform(self, round(self.platnumber * 120) - self.shift, HEIGHT -
                                                      self.levels[self.act_level].array[self.platnumber][i][0], self.levels[self.act_level].array[self.platnumber][i][1])
                        self.platforms.add(platform)
                        self.all_sprites.add(platform)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 5:
                        coin = Coin(self, (self.platnumber * 120) - self.shift, HEIGHT -
                                    self.levels[self.act_level].array[self.platnumber][i][0])
                        self.coins.add(coin)
                        self.all_sprites.add(coin)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 4:
                        platform = UpMovingPlatform(round(self.platnumber * 120) - self.shift,
                                                    HEIGHT - self.levels[self.act_level].array[self.platnumber][i][0], self)
                        self.platforms.add(platform)
                        self.all_sprites.add(platform)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 8:
                        item = EndItem(round(self.platnumber * 120) - self.shift, HEIGHT -
                                       self.levels[self.act_level].array[self.platnumber][i][0], self)
                        self.coins.add(item)
                        self.all_sprites.add(item)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 9:
                        item = JumpBoost(round(self.platnumber * 120) - self.shift, HEIGHT -
                                         self.levels[self.act_level].array[self.platnumber][i][0], self)
                        self.coins.add(item)
                        self.all_sprites.add(item)
                    if self.levels[self.act_level].array[self.platnumber][i][1] == 10:
                        item = SpeedDrop(round(self.platnumber * 120) - self.shift, HEIGHT -
                                         self.levels[self.act_level].array[self.platnumber][i][0], self)
                        self.coins.add(item)
                        self.all_sprites.add(item)
            except:
                pass
            self.platnumber += 1

        if len(self.backgrounds) < 5:
            pos = self.lastbackground + rd.randint(100, 300)
            b = Background(self, pos, rd.randint(100, 600))
            self.lastbackground = pos + b.rect.width
            self.backgrounds.add(b)

        if self.player.rect.x >= WIDTH / 2:
            self.shift += abs(self.player.speed.x)
            self.player.rect.x -= abs(self.player.speed.x)
            for platform in self.platforms:
                platform.rect.right -= abs(self.player.speed.x)
                if platform.rect.right < 0:
                    platform.kill()
            for coin in self.coins:
                coin.rect.right -= abs(self.player.speed.x)
                if coin.rect.right < 0:
                    coin.kill()
            self.lastbackground -= abs(self.player.speed.x) / 2
            for background in self.backgrounds:
                background.rect.right -= abs(self.player.speed.x) / 2
                if background.rect.right < 0:
                    background.kill()

        if self.player.rect.y > HEIGHT:
            if NO_DIE is True:
                self.player.rect.y = -200
            else:
                self.playing = False
                self.diesound.play()

        if self.player.rect.x < 0:
            self.player.rect.x = 0
            self.player.speed.x = 0

        pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] == 1:
            if pos[0] > WIDTH - 200 and pos[0] < WIDTH - 200 + 180 and pos[1] > 20 and pos[1] < 20 + 60:
                self.playing = False
                self.buttonsound.play()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False

            if event.type == pg.KEYDOWN:
                if event.key == 310:
                    self.command_pressed = True
                if event.key == 113 and self.command_pressed is True:
                    self.running = False
                    self.playing = False
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == 310:
                    self.command_pressed = False

    def draw(self):

        self.screen.fill(BLACK)
        self.backgrounds.draw(self.screen)
        self.all_sprites.draw(self.screen)

        if SHOW_FPS is True:
            self.new_text("fps: " + str(round(self.clock.get_fps())), 15, WHITE, "chalkboard", 230, 10)
            pg.display.set_caption(str(round(self.clock.get_fps())))

        self.screen.blit(self.coins_image, (20, 20))
        self.screen.blit(self.endbutton_image, (WIDTH - 200, 20))
        self.new_text(str(self.score), 40, COIN_COLOR, "chalkboard", 90, 25)

        if self.player.jumpboost > 0:
            self.screen.blit(self.jumpboost_image, (220, 20))
        if self.player.speeddrop > 0:
            self.screen.blit(self.speeddrop_image, (360, 20))

        pg.display.flip()

    def new_text(self, text, size, color, font, x, y):
        font = pg.font.Font("assets/fonts/Chalkboard_Bold.ttf", size)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = (x, y)
        self.screen.blit(surface, rect)

    def wait(self, funcs):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == 310:
                        self.command_pressed = True
                if event.type == pg.KEYUP:
                    if event.key == 310:
                        self.command_pressed = False
                if event.type == pg.KEYDOWN:
                    if event.key == 113 and self.command_pressed is True:
                        waiting = False
                        self.running = False
                    if event.key == 27:
                        waiting = False
                        self.running = False

            for i in range(len(funcs)):
                if funcs[i]() is True:
                    return i

    def start_screen(self):
        self.backgroundmusic.stop()
        self.backgroundmusic.play()
        self.screen.fill(BLACK)
        self.screen.blit(self.banner, (WIDTH / 2 - (self.banner.get_width() / 2), 100))
        button = MenuButton(self, WIDTH / 2, HEIGHT / 2 + 160, self.menubutton_image, enter=True)

        pg.display.flip()

        self.wait([button.check_click])

        self.level_screen()

    def end_screen(self):
        self.screen.fill(BLACK)
        if self.running is False:
            return

        if self.score > self.highscore[self.act_level]:
            self.highscore[self.act_level] = self.score
            self.new_text("NEW HIGHSCORE", 40, COIN_COLOR, "chalkboard", WIDTH / 2 + 150, 300)

        self.screen.blit(self.banner_icon, (WIDTH / 2 - (self.banner_icon.get_width() / 2) - 200, 100))
        self.new_text("SCORE: " + str(self.score), 40, COIN_COLOR, "chalkboard", WIDTH / 2 + 150, 150)
        self.new_text("HIGHSCORE: " + str(self.highscore[self.act_level]),
                      40, COIN_COLOR, "chalkboard", WIDTH / 2 + 150, 220)
        button = MenuButton(self, WIDTH / 2, HEIGHT / 2 + 160, self.menubutton_image, enter=True)

        pg.display.flip()

        self.wait([button.check_click])

        self.level_screen()

    def level_screen(self):
        self.screen.fill(BLACK)

        if self.running is False:
            return

        self.screen.blit(self.level_image, (WIDTH / 2 - (self.level_image.get_width() / 2),
                                            HEIGHT / 2 - (self.level_image.get_height() / 2)))
        button1 = MenuButton(self, WIDTH / 2 + 230, HEIGHT / 2 - 30 - 190, self.startbutton_image)
        button2 = MenuButton(self, WIDTH / 2 + 230, HEIGHT / 2 - 30, self.startbutton_image)
        button3 = MenuButton(self, WIDTH / 2 + 230, HEIGHT / 2 - 30 + 190, self.startbutton_image)

        self.new_text("COLLECTED: " + str(self.highscore[0]) + "/" + str(self.levels[0].maxcoins),
                      30, COIN_COLOR, "chalkboard", WIDTH / 2 - 110, HEIGHT / 2 - 30 - 190 + 65)
        self.new_text("COLLECTED: " + str(self.highscore[1]) + "/" + str(self.levels[1].maxcoins),
                      30, COIN_COLOR, "chalkboard", WIDTH / 2 - 110, HEIGHT / 2 - 30 + 65)
        self.new_text("COLLECTED: " + str(self.highscore[2]) + "/" + str(self.levels[2].maxcoins),
                      30, COIN_COLOR, "chalkboard", WIDTH / 2 - 110, HEIGHT / 2 - 30 + 190 + 65)

        pg.display.flip()

        level = self.wait([button1.check_click, button2.check_click, button3.check_click])

        self.act_level = level

    def load_screen(self):
        self.screen.fill(BLACK)
        self.new_text("loading...", 25, WHITE, "chalkboard", WIDTH / 2, HEIGHT / 2)

        pg.display.flip()

    def save(self):
        save(self.path + "/assets/highscore_files/highscore.txt", self.highscore, 1)


game = Game()
game.start_screen()
while game.running:
    game.new()
    game.run()
    game.end_screen()
game.save()

pg.quit()
