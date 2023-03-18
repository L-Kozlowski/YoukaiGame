import pygame


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.old_color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.click = 0
        self.box_outline = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.display_color = False

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            if self.click > 0:
                self.click -= 1
                pygame.draw.rect(win, self.color, self.box_outline, 0)
            else:
                pygame.draw.rect(win, outline, self.box_outline, 0)

        pygame.draw.rect(win, self.color, self.box, 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def is_clicked(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.box.collidepoint(pos):
            self.click = 5
            self.color = (200, 100, 200)
            self.display_color = True
            return True
        return False

    def clear_cliked(self):
        if self.display_color:
            self.color = self.old_color
