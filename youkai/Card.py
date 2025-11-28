from Space import Space
import pygame

class Card(Space):
    def __init__(self, x, y, width, height, background_color, id_card, card_color):
        self.card_color = card_color
        self.selected = False
        self.peek = False
        # self.select_back = background_color[0] + 100,background_color[1] + 100,background_color[2] + 100
        # self.select_card = card_color[0] + 50, card_color[1] + 50, card_color[2] + 50
        # self.select_card = (255,255,255)

        super().__init__(x, y, width, height, background_color, id_card)

    def init_color_card(self, color):
        self.card_color = color

    def check_color_card(self, pos):
        pass
        # if self.is_over(pos):
        #     if self.peek:
        #         pass
        #         # self.color = self.select_card
        #     else:
        #         self.color = self.select_back
        # else:
        #     if self.peek:
        #         self.color = self.card_color
        #     else:
        #         self.color = self.background_color


    def change_size(self, width, height):
        self.width = width
        self.height = height

    def check_selected(self):
        return self.selected

    def temporary_display(self, win, pos):

        self.check_resize()
        win.blit(self.img_display, pos)

    def get_difference_position(self, pos):
        return pos[0] - self.x,  pos[1] - self.y

    def change_id(self, i, j):
        self.id = (self.id[0]+i, self.id[1]+j)

    def peek_card(self, peek=False, help_card=False):
        self.peek = peek
        self.change = True
        if self.peek:
            self.img = self.card_color
        else:
            self.img = self.background_color

    def check_if_peek(self):
        if self.peek:
            return True
        return False

