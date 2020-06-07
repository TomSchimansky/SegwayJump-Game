import pygame as pg


class MenuButton():
    def __init__(self, game, x, y, image, enter=False):

        self.image = image
        self.enter = enter
        self.x, self.y = x-(self.image.get_width()/2), y
        self.game = game
        self.game.screen.blit(self.image, (x-(self.image.get_width()/2), y))

    def check_click(self):
        pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        if pg.mouse.get_pressed()[0] == 1:
            if pos[0] > self.x and pos[0] < self.x+179 and pos[1] > self.y and pos[1] < self.y+60:
                self.game.buttonsound.play()
                return True

        elif self.enter:
            if keys[13]:
                self.game.buttonsound.play()
                return True
        else:

            return False




