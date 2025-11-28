import pygame


class Space(object):
    def __init__(self, x, y, width, height, background_color, id_space):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = background_color
        self.color = self.background_color
        self.id = id_space
        self.img = self.background_color
        self.img_display = self.img
        self.change = False

    def check_resize(self):
        rect = self.img_display.get_rect()

        if rect.width == self.width and rect.height == self.height and not self.change:
            self.img_display = self.img_display
            # print("jestem")
        else:

            self.img_display = pygame.transform.scale(self.img, (self.width, self.height))
            self.change = False

    def display(self, win):
        self.check_resize()
        rect = self.img_display.get_rect()
        rect.x = self.x
        rect.y = self.y
        win.blit(self.img_display, rect)

    def change_color(self, color):
        self.color = color

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        if type(self) == Space:
            self.color = self.background_color  # return background color
        return False

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.width, self.height

    def change_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]




