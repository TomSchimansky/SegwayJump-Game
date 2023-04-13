import pygame


class MenuButton:
    def __init__(self, game, x, y, image, enter=False):
        self.image = image
        self.enter = enter
        self.x = x-(self.image.get_width()/2)
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.game = game
        self.game.screen.blit(self.image, (x-(self.image.get_width()/2), y))

    def check_click(self):
        pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                self.game.button_sound.play()
                return True
        elif self.enter:
            if keys[13]:
                self.game.button_sound.play()
                return True
        else:
            return False




