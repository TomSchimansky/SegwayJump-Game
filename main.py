""" SegwayJump Copyright © 2018 Tom Schimansky """

from settings import *
from segway_jump_sprites.platforms import Platform, SideMovingPlatform, UpMovingPlatform
from segway_jump_sprites.player import Player
from segway_jump_sprites.coin import Coin
from segway_jump_sprites.menubutton import MenuButton
from segway_jump_sprites.items import EndItem, JumpBoost, SpeedDrop
from segway_jump_sprites.background import Background

import os
import json
import random
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.running = True
        self.playing = False
        self.pause = False
        self.current_level = None
        self.time = 0
        self.command_pressed = False
        self.current_path = os.path.dirname(__file__)

        self.icon_image = pygame.image.load(self.current_path + "/assets/icons/icon.png")
        pygame.display.set_icon(self.icon_image)
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SHOWN)
        self.clock = pygame.time.Clock()

        # load levels and highscores
        self.levels = []
        self.load_levels()
        self.highscores = []
        self.load_highscores()
        if len(self.highscores) != len(self.levels):
            raise ValueError("highscores and level files do not match")

        # load sounds
        self.background_music = pygame.mixer.Sound(self.current_path + "/assets/sounds/ambient_background_music_cicada_3301.wav")
        self.coin_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/blup.wav")
        self.die_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/sfx_die.wav")
        self.button_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/button_27.wav")
        self.jump_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/jump_sound.wav")
        self.powerup_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/powerup.wav")
        self.win_sound = pygame.mixer.Sound(self.current_path + "/assets/sounds/ding_sound.wav")

        # load menu images
        self.coins_image = pygame.image.load(self.current_path + "/assets/images/coins.png")
        self.endbutton_image = pygame.image.load(self.current_path + "/assets/images/endbutton.png")
        self.banner_image = pygame.image.load(self.current_path + "/assets/images/banner.png")
        self.level_list_image = pygame.image.load(self.current_path + "/assets/images/level_list.png")
        self.menubutton_image = pygame.image.load(self.current_path + "/assets/images/menubutton.png")
        self.startbutton_image = pygame.image.load(self.current_path + "/assets/images/startbutton.png")

        # load character images
        self.character_left_walking_1_image = pygame.image.load(self.current_path + "/assets/images/player_left_1.png")
        self.character_left_walking_2_image = pygame.image.load(self.current_path + "/assets/images/player_left_2.png")
        self.character_left_walking_3_image = pygame.image.load(self.current_path + "/assets/images/player_left_3.png")
        self.character_jump_1_image = pygame.image.load(self.current_path + "/assets/images/player_jump_1.png")
        self.character_jump_2_image = pygame.image.load(self.current_path + "/assets/images/player_jump_2.png")

        # load game images
        self.platform_image = pygame.image.load(self.current_path + "/assets/images/platform.png").convert()
        self.floatingplatorm_image = pygame.image.load(self.current_path + "/assets/images/floatingplatform.png")
        self.upmovingplatformsocket_image = pygame.image.load(self.current_path + "/assets/images/movingsocketplatform.png")
        self.emptyplatform_image = pygame.image.load(self.current_path + "/assets/images/middleplatform.png").convert()
        self.sidemovingplatform_image = pygame.image.load(self.current_path + "/assets/images/movingfloatingplatform.png")
        self.upmovingplatform_image = pygame.image.load(self.current_path + "/assets/images/movingplatform.png")
        self.coin_1_image = pygame.image.load(self.current_path + "/assets/images/coin_1.png")
        self.finish_image = pygame.image.load(self.current_path + "/assets/images/finish.png")
        self.jumpboost_image = pygame.image.load(self.current_path + "/assets/images/jumpboost.png")
        self.speeddrop_image = pygame.image.load(self.current_path + "/assets/images/speeddrop.png")
        self.steelpate_1_image = pygame.image.load(self.current_path + "/assets/images/steelplate_1.png")
        self.steelpate_2_image = pygame.image.load(self.current_path + "/assets/images/steelplate_2.png")
        self.steelpate_3_image = pygame.image.load(self.current_path + "/assets/images/steelplate_3.png")
        self.steelpate_4_image = pygame.image.load(self.current_path + "/assets/images/steelplate_4.png")

    def load_levels(self):
        with open(self.current_path + "/assets/levels/levels.json", "r") as file:
            self.levels = json.load(file)

    def load_highscores(self):
        if os.path.exists(self.current_path + "/assets/highscores/highscores.json"):
            with open(self.current_path + "/assets/highscores/highscores.json", "r") as file:
                self.highscores = json.load(file)
        else:
            self.highscores = [0] * len(self.levels)

    def save_highscore(self):
        with open(self.current_path + "/assets/highscores/highscores.json", "w") as file:
            json.dump(self.highscores, file)

    def create_text(self, text, size, color, x, y):
        font = pygame.font.Font("assets/fonts/Chalkboard_Bold.ttf", size)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = (x, y)
        self.screen.blit(surface, rect)

    def start_screen(self):
        self.background_music.stop()
        self.background_music.play()
        self.screen.fill(BLACK)
        self.screen.blit(self.banner_image, (WIDTH / 2 - (self.banner_image.get_width() / 2), 100))
        button = MenuButton(self, WIDTH / 2, HEIGHT / 2 + 160, self.menubutton_image, enter=True)

        pygame.display.flip()
        self.wait([button.check_click])
        self.level_screen()

    def level_screen(self):
        if self.running is False:
            return

        self.screen.fill(BLACK)

        self.create_text("Levels:", 40, COIN_COLOR, WIDTH / 2, 30)

        start_buttons = []
        for i, level in enumerate(self.levels):
            self.screen.blit(self.level_list_image, (WIDTH / 2 - (self.level_list_image.get_width() / 2), 100 + i * (self.level_list_image.get_height() + 30)))
            self.create_text(level["name"], 30, COIN_COLOR, WIDTH / 2 - 200, 100 + i * (self.level_list_image.get_height() + 30) + 30)
            self.create_text(f"Highscore: {self.highscores[i]}/{level['maxcoins']}", 20, COIN_COLOR, WIDTH / 2 - 50, 100 + i * (self.level_list_image.get_height() + 30) + 30)
            start_buttons.append(MenuButton(self, WIDTH / 2 + 180, 100 + i * (self.level_list_image.get_height() + 30) + 30, self.startbutton_image))

        pygame.display.flip()
        self.current_level = self.wait([button.check_click for button in start_buttons])

    def new(self):
        self.background_music.stop()
        self.background_music.play(-1)

        self.current_column_number = 0
        self.current_shift = 0
        self.score = 0
        self.last_background_x_pos = 100

        self.player = Player(self)
        self.platforms = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
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

        level_array = self.levels[self.current_level]["array"]
        if len(self.all_sprites) < 50 and self.current_column_number < len(level_array):

            level_array_column = level_array[self.current_column_number]
            for i in range(len(level_array_column)):

                x_position = round(self.current_column_number * 120) - self.current_shift
                y_position = HEIGHT - level_array_column[i][0]

                if level_array_column[i][1] in (1, 2, 6, 7):
                    platform = Platform(self, x_position, y_position, level_array_column[i][1])
                    self.platforms.add(platform)
                    self.all_sprites.add(platform)
                elif level_array_column[i][1] == 3:
                    platform = SideMovingPlatform(self, x_position, y_position)
                    self.platforms.add(platform)
                    self.all_sprites.add(platform)
                elif level_array_column[i][1] == 4:
                    platform = UpMovingPlatform(self, x_position, y_position)
                    self.platforms.add(platform)
                    self.all_sprites.add(platform)
                elif level_array_column[i][1] == 5:
                    coin = Coin(self, x_position, y_position)
                    self.coins.add(coin)
                    self.all_sprites.add(coin)
                elif level_array_column[i][1] == 8:
                    item = EndItem(self, x_position, y_position)
                    self.coins.add(item)
                    self.all_sprites.add(item)
                elif level_array_column[i][1] == 9:
                    item = JumpBoost(self, x_position, y_position)
                    self.coins.add(item)
                    self.all_sprites.add(item)
                elif level_array_column[i][1] == 10:
                    item = SpeedDrop(self, x_position, y_position)
                    self.coins.add(item)
                    self.all_sprites.add(item)
            self.current_column_number += 1

        if len(self.backgrounds) < 6:
            new_x_pos = self.last_background_x_pos + random.randint(100, 300)
            new_background = Background(self, self.last_background_x_pos + random.randint(100, 300), random.randint(100, 600))
            self.last_background_x_pos = new_x_pos + new_background.rect.width
            self.backgrounds.add(new_background)

        if self.player.rect.x >= WIDTH / 2:
            self.current_shift += abs(self.player.speed.x)
            self.player.rect.x -= abs(self.player.speed.x)
            for platform in self.platforms:
                platform.rect.right -= abs(self.player.speed.x)
                if platform.rect.right < 0:
                    platform.kill()
            for coin in self.coins:
                coin.rect.right -= abs(self.player.speed.x)
                if coin.rect.right < 0:
                    coin.kill()
            self.last_background_x_pos -= abs(self.player.speed.x) / 2
            for background in self.backgrounds:
                background.rect.right -= abs(self.player.speed.x) / 2
                if background.rect.right < 0:
                    background.kill()

        if self.player.rect.y > HEIGHT:
            if NO_DIE is True:
                self.player.rect.y = -200
            else:
                self.playing = False
                self.die_sound.play()

        if self.player.rect.x < 0:
            self.player.rect.x = 0
            self.player.speed.x = 0

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if WIDTH - 200 < pos[0] < WIDTH - 200 + 180 and 20 < pos[1] < 20 + 60:
                self.playing = False
                self.button_sound.play()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

            if event.type == pygame.KEYDOWN:
                if event.key == 310:
                    self.command_pressed = True
                if event.key == 113 and self.command_pressed is True:
                    self.running = False
                    self.playing = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == 310:
                    self.command_pressed = False

    def draw(self):
        self.screen.fill(BLACK)
        self.backgrounds.draw(self.screen)
        self.all_sprites.draw(self.screen)

        if SHOW_FPS is True:
            self.create_text(f"FPS: {round(self.clock.get_fps())}", 17, WHITE, 245, 20)

        self.screen.blit(self.coins_image, (20, 20))
        self.screen.blit(self.endbutton_image, (WIDTH - 200, 20))
        self.create_text(str(self.score), 40, COIN_COLOR, 90, 25)

        if self.player.jumpboost > 0:
            self.screen.blit(self.jumpboost_image, (220, 20))
        if self.player.speeddrop > 0:
            self.screen.blit(self.speeddrop_image, (360, 20))

        pygame.display.flip()

    def wait(self, wait_functions):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == 310:
                        self.command_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == 310:
                        self.command_pressed = False
                if event.type == pygame.KEYDOWN:
                    if event.key == 113 and self.command_pressed is True:
                        self.running = False
                    if event.key == 27:
                        self.running = False

            for i, function in enumerate(wait_functions):
                if function() is True:
                    return i

    def end_screen(self):
        if self.running is False:
            return

        self.screen.fill(BLACK)

        if self.score > self.highscores[self.current_level]:
            self.highscores[self.current_level] = self.score
            self.create_text("NEW HIGHSCORE", 40, COIN_COLOR, WIDTH / 2 + 150, 300)

        self.screen.blit(self.icon_image, (WIDTH / 2 - (self.icon_image.get_width() / 2) - 200, 100))
        self.create_text("SCORE: " + str(self.score), 40, COIN_COLOR, WIDTH / 2 + 150, 150)
        self.create_text("HIGHSCORE: " + str(self.highscores[self.current_level]), 40, COIN_COLOR, WIDTH / 2 + 150, 220)
        button = MenuButton(self, WIDTH / 2, HEIGHT / 2 + 160, self.menubutton_image, enter=True)

        pygame.display.flip()
        self.wait([button.check_click])
        self.level_screen()


if __name__ == "__main__":
    game = Game()
    game.start_screen()
    while game.running:
        game.new()
        game.run()
        game.end_screen()
    game.save_highscore()
    pygame.quit()
