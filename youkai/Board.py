import pygame
import random
import Space
import Card
from hand import Hand

pygame.init()
pygame.font.init()


class Board(object):
    def __init__(self, width, height, color, cursor, tryb, rozdzielczosc=0, sterowanie_gestem=False):
        self.img_space_back = ""
        self.img_card_back = ""
        self.img_card_help_back = ""
        self.img_background = ""
        self.theme(tryb)
        self.width = width
        self.height = height
        self.scale = 2
        self.roz = rozdzielczosc
        if rozdzielczosc == -1:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.game_width = 500 * self.scale
            self.game_height = 500 * self.scale
            self.game_corner_x = 300 * self.scale
            self.game_corner_y = 10 * self.scale
            self.help_card_space_width = 80 * self.scale
            self.help_card_space_height = 80 * self.scale
            self.help_card_space_corner_x = 180 * self.scale
            self.help_card_space_corner_y = 200 * self.scale
            self.help_card_space_corner_x_hide = 80 * self.scale
            self.help_card_space_corner_y_hide = 200 * self.scale
            self.txt_pos1 = (80 * self.scale, 150 * self.scale)
            self.txt_pos2 = (80 * self.scale, 150 * self.scale)
            self.txt_pos3 = (20 * self.scale, 150 * self.scale)
            self.txt_pos4 = (80 * self.scale, 150 * self.scale)

            self.player_pos = [(self.width - 70 * self.scale, -70 + j * 120 * self.scale) for j in range(4)]
            self.my_font = pygame.font.SysFont('Bookman Old Style', 20*self.scale)
            self.koniec_gry = Space.Space(self.width - 230*self.scale, self.height-60*self.scale,  round(518/1.3), round(101/1.3),
                                          pygame.image.load('yokaiImg/koniec.png'), (-10, -10))

        else:
            self.screen = pygame.display.set_mode((width, height))
            self.game_width = 450
            self.game_height = 450
            self.game_corner_x = 180
            self.game_corner_y = 30
            self.help_card_space_width = 70
            self.help_card_space_height = 70
            self.help_card_space_corner_x = 100
            self.help_card_space_corner_y = 270
            self.help_card_space_corner_x_hide = 100
            self.help_card_space_corner_y_hide = 200
            self.txt_pos1 = (280, 50)
            self.txt_pos2 = (300, 50)
            self.txt_pos3 = (160, 50)
            self.txt_pos4 = (330, 50)

            self.player_pos = [(self.width - 70, -60 + j * 110) for j in range(4)]
            print(self.player_pos[2][1])
            self.my_font = pygame.font.SysFont('Bookman Old Style', 30)
            self.koniec_gry = Space.Space(self.width - 240,  self.height-60, round(518/2.3), round(101/2.3),
                                          pygame.image.load('yokaiImg/koniec.png'), (-10, -10))

        self.bg_img = pygame.image.load(self.img_background)
        self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))
        self.color = color
        self.change_background(color)

        self.rows = 6
        self.cols = 6
        self.spaces = []
        self.cards = []
        self.init_game_space()
        self.difference = (0, 0)
        self.peeked_card = False
        self.id_card_to_check = None
        self.spaces_cards_help = []
        self.cards_help = []
        self.cards_help_used = []
        self.init_help_space_card()
        self.number_of_space_help = 0
        self.save_idx_to_move = -1
        self.txt_round = self.my_font.render('Podglądnij 2 karty', False, self.txt_color)
        self.round = 0
        self.txt_pos = (500, 50)
        self.peek_number = 0
        self.players_left = []
        self.players_right = []
        self.init_players()
        self.active_player = 0
        self.cursor = cursor
        self.hand_select = False
        self.selected_card = False
        self.hand_select_old = False
        self.gest = sterowanie_gestem
        self.end = False
        self.show_help_card = True

        if rozdzielczosc == -1 and sterowanie_gestem:
            self.hand = Hand(rozdzielczosc)

    def theme(self, theme):
        if theme == 0:  # dark
            self.img_space_back = 'yokaiImg/kartaZakryta.png'
            self.img_card_back = 'yokaiImg/kartaZakryta4.png'
            self.img_card_help_back = 'yokaiImg/kartyPomocyZakryte2.png'
            self.img_background = 'yokaiImgDark/tlo69.png'
            self.txt_color = (255, 255, 255)
        else:  # light
            self.img_space_back = 'yokaiImg/kartaZakryta.png'
            self.img_card_back = 'yokaiImg/kartaZakrytaJasna.png'
            self.img_card_help_back = 'yokaiImg/kartyPomocyZakryte.png'
            self.img_background = 'yokaiImg/tloMax4.png'
            self.txt_color =  (255, 255, 255)

    def init_players(self):
        img_left = ['yokaiImg/zakladkaWodaLewa.png', 'yokaiImg/zakladkaOgienLewa.png',
                    'yokaiImg/zakladkaZiemiaLewa.png', 'yokaiImg/zakladkaPowietrzeLewa.png']
        img_right = ['yokaiImg/zakladkaWodaPrawa.png', 'yokaiImg/zakladkaOgienPrawa.png',
                     'yokaiImg/zakladkaZiemiaPrawa.png', 'yokaiImg/zakladkaPowietrzePrawa.png']
        self.players_left = [Space.Space(-7, 20, round(self.width/10), round(self.height/5),
                                         pygame.image.load(img_left[j]), (0, j)) for j in range(4)]
        self.players_right = [Space.Space(self.player_pos[j][0], self.player_pos[j][1],
                                          round(self.width/11), round(self.height/5),
                                          pygame.image.load(img_right[j]), (0, j)) for j in range(4)]

    def init_help_space_card(self):
        # s_w = int(self.help_card_space_width / 2)
        # s_h = int(self.help_card_space_height / 5)
        self.help_card_width = int(self.help_card_space_width)
        self.help_card_height = int(self.help_card_space_height)

        self.spaces_cards_help = [Space.Space(self.help_card_space_corner_x + 0 * self.help_card_width,
                                              self.help_card_space_corner_y + j * self.help_card_height,
                                              self.help_card_width - 2, self.help_card_height - 2,
                                              pygame.image.load(self.img_space_back),
                                              # (i, j)) for i in range(2) for j in range(5)]
                                              (0, j)) for j in range(1)]

        self.cards_help = [Card.Card(self.help_card_space_corner_x_hide,
                                     self.help_card_space_corner_y_hide,
                                     self.help_card_width - 2, self.help_card_height - 2,
                                     pygame.image.load(self.img_card_help_back),
                                     (0, i), pygame.image.load('yokaiImg/kartaPomocyOgien.png'))
                           for i in range(10)]
        color_card_list = self.random_color_card_help()
        for i in range(len(self.cards_help)):
            self.cards_help[i].init_color_card(color_card_list[i])

    def random_color_card(self):
        """
        create a list with 16 element of 4 colors
        choosing random one color from a list
        adding this color to second list and removing it from the precious one
        this is repeating 16 times
        :return: a list of random order colors of cards
        """
        color_list_init = []
        color_list_random = []
        for i in range(4):
            color_list_init.append(pygame.image.load('yokaiImg/kartaOgien.png'))
        for i in range(4):
            color_list_init.append(pygame.image.load('yokaiImg/kartaWoda.png'))
        for i in range(4):
            color_list_init.append(pygame.image.load('yokaiImg/kartaPowietrze.png'))
        for i in range(4):
            color_list_init.append(pygame.image.load('yokaiImg/kartaZiemia.png'))

        while len(color_list_init):
            i = random.randint(0, len(color_list_init) - 1)
            color_list_random.append(color_list_init[i])
            del color_list_init[i]
        return color_list_random

    def random_color_card_help(self):
        """
        create a list with 16 element of 4 colors
        choosing random one color from a list
        adding this color to second list and removing it from the precious one
        this is repeating 16 times
        :return: a list of random order colors of cards
        """
        color_list_1 = []
        color_list_2 = []
        color_list_3 = []

        color_list_random = []
        color_list_1.append(pygame.image.load('yokaiImg/kartaPomocyOgien.png'))
        color_list_1.append(pygame.image.load('yokaiImg/kartaPomocyWoda.png'))
        color_list_1.append(pygame.image.load('yokaiImg/kartaPomocyZiemia.png'))
        color_list_1.append(pygame.image.load('yokaiImg/kartaPomocyPowietrze.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyOgienWoda.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyOgienZiemia.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyOgienPowietrze.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyWodaPowietrze.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyZiemiaWoda.png'))
        color_list_2.append(pygame.image.load('yokaiImg/kartaPomocyPowietrzeZiemia.png'))
        color_list_3.append(pygame.image.load('yokaiImg/kartaPomocyOgienZiemiaPowietrze.png'))
        color_list_3.append(pygame.image.load('yokaiImg/kartaPomocyWodaOgienPowietrze.png'))
        color_list_3.append(pygame.image.load('yokaiImg/kartaPomocyWodaZiemiaPowietrze.png'))
        color_list_3.append(pygame.image.load('yokaiImg/kartaPomocyOgienZiemiaWoda.png'))

        while len(color_list_1) > 1:  # bierze 3 karty pojedyncze
            i = random.randint(0, len(color_list_1) - 1)
            color_list_random.append(color_list_1[i])

            del color_list_1[i]
        while len(color_list_2) > 2:  # bierze 4 karty pojedyncze
            i = random.randint(0, len(color_list_2) - 1)
            color_list_random.append(color_list_2[i])
            del color_list_2[i]
        while len(color_list_3) > 1:  # bierze 3 karty pojedyncze
            i = random.randint(0, len(color_list_3) - 1)
            color_list_random.append(color_list_3[i])
            del color_list_3[i]

        random.shuffle(color_list_random)
        return color_list_random

    def create_space_list(self):
        # s_w = int(self.game_width / self.cols)
        # s_h = int(self.game_height / self.rows)
        self.card_width = int(self.game_width / self.cols)
        self.card_height = int(self.game_height / self.cols)

        self.spaces = [Space.Space(self.game_corner_x + i * self.card_width, self.game_corner_y + j * self.card_height,
                                   self.card_width - 2, self.card_height - 2,
                                   pygame.image.load('yokaiImg/kartaZakryta2.png'), (i, j))
                       for i in range(self.cols) for j in range(self.rows)]

    def init_game_space(self):
        # self.card_width = int(self.game_width / self.cols)
        # self.card_height = int(self.game_height / self.cols)
        color_card_list = self.random_color_card()

        self.create_space_list()
        self.cards = [Card.Card(self.game_corner_x + i * self.card_width, self.game_corner_y + j * self.card_height,
                                self.card_width - 2, self.card_height - 2, pygame.image.load(self.img_card_back),
                                (i, j), pygame.image.load(self.img_card_back))
                      for i in range(self.cols - 5, self.cols - 1) for j in range(self.rows - 5, self.rows - 1)]
        self.cols += 1
        self.rows += 1
        for i in range(len(self.cards)):
            self.cards[i].init_color_card(color_card_list[i])

    def change_id(self, corner, card_list):
        for card in card_list:
            if corner == "left_up":
                card.change_id(1, 1)
            elif corner == "right_up":
                card.change_id(0, 1)
            elif corner == "right_down":
                card.change_id(0, 0)
            elif corner == "left_down":
                card.change_id(1, 0)
            elif corner == "left_up_smaller":
                card.change_id(-1, -1)
            elif corner == "right_up_smaller":
                card.change_id(0, -1)
            elif corner == "right_down_smaller":
                card.change_id(0, 0)
            elif corner == "left_down_smaller":
                card.change_id(-1, 0)

    def resize_game_space(self, corner):

        if corner[-1] == 'r':
            self.cols = self.cols - 2
            self.rows = self.rows - 2

        self.create_space_list()
        self.change_id(corner, self.cards)
        self.change_id(corner, self.cards_help_used)

        self.resize_cards(self.cards)
        self.resize_cards(self.cards_help_used)

        self.cols += 1
        self.rows += 1

    def resize_cards(self, list_cards):
        for card in list_cards:
            for space in self.spaces:
                if space.id == card.id:
                    card.change_position(space.get_position())
                    card.change_size(*space.get_size())

    def check_resize_need(self, card_id):
        rows_2 = int(self.rows / 2)
        cols_2 = int(self.cols / 2)
        last_rows = self.rows - 2
        last_cols = self.cols - 2
        corner = ""

        if (card_id[0] == 0 and card_id[1] >= rows_2) or (card_id[0] < cols_2 and card_id[1] == last_rows):
            corner = "left_down"
        elif (card_id[0] == 0 and card_id[1] <= rows_2) or (card_id[0] < cols_2 and card_id[1] == 0):
            corner = "left_up"
        elif (card_id[0] == last_cols and card_id[1] >= rows_2) or (card_id[0] >= 0 and card_id[1] == last_rows):
            corner = "right_down"
        elif (card_id[0] == last_cols and card_id[1] <= rows_2) or (card_id[0] >= 0 and card_id[1] == 0):
            corner = "right_up"

        if corner != "":
            self.resize_game_space(corner)

    def check_resize_small(self):
        resize = [True, True, True, True]
        corner = ["right_up_smaller", "right_down_smaller", "left_down_smaller", "left_up_smaller"]
        last_rows = self.rows - 2
        last_cols = self.cols - 2
        for card in self.cards:
            card_id = card.id
            c_col = card_id[0]
            c_row = card_id[1]
            if 0 <= c_row <= 1 and 0 <= c_col <= last_cols \
                    or last_cols - 1 <= c_col <= last_cols and 0 <= c_row <= last_rows:
                resize[0] = False
            if last_rows - 1 <= c_row <= last_rows and 0 <= c_col <= last_cols \
                    or last_cols - 1 <= c_col <= last_cols and 0 <= c_row <= last_rows:
                resize[1] = False
            if last_rows - 1 <= c_row <= last_rows and 0 <= c_col <= last_cols \
                    or 0 <= c_col <= 1 and 0 <= c_row <= last_rows:
                resize[2] = False
            if 0 <= c_row <= 1 and 0 <= c_col <= last_cols \
                    or 0 <= c_col <= 1 and 0 <= c_row <= last_rows:
                resize[3] = False

        only_one_resie = True
        for i in range(4):
            if resize[i] and only_one_resie:
                only_one_resie = False
                self.resize_game_space(corner[i])

    def change_background(self, color):

        self.screen.blit(self.bg_img, (0, 0))
        # self.screen.fill(color)

    def display_spaces(self, list_spaces):
        for space in list_spaces:
            space.display(self.screen)

    def display_cards(self, list_cards, pos):
        for idx in range(len(list_cards)):
            card = list_cards[idx]
            if card.selected:
                self.save_idx_to_move = idx
            else:
                card.display(self.screen)

    def display_moving_card(self, list_cards, pos):
        for idx in range(len(list_cards)):
            card = list_cards[idx]
            if card.selected and idx == self.save_idx_to_move:
                current_corner_pos = pos[0] - self.difference[0], pos[1] - self.difference[1]
                card.temporary_display(self.screen, current_corner_pos)

    def display_txt(self):
        if self.round == 0:
            self.txt_round = self.my_font.render('Podglądnij 2 karty', False, self.txt_color)
            self.txt_pos = self.txt_pos1
        elif self.round == 1:
            self.txt_round = self.my_font.render('Przesuń kartę', False, self.txt_color)
            self.txt_pos = self.txt_pos2
        elif self.round == 2:
            self.txt_round = self.my_font.render('Okryj lub użyj karty podpowiedzi', False, self.txt_color)
            self.txt_pos = self.txt_pos3
        elif self.round == -99:
            self.txt_round = self.my_font.render('Koniec gry', False, self.txt_color)
            self.txt_pos = self.txt_pos4

    def display_players(self):
        for player in self.players_left:
            if self.active_player == player.id[1]:
                player.display(self.screen)
        for player in self.players_right:
            if self.active_player != player.id[1]:
                player.display(self.screen)

    def change_active_player(self):
        self.active_player += 1
        tmp = self.players_right[0]
        del self.players_right[0]
        self.players_right.append(tmp)
        # print(self.player_pos)
        for idx in range(len(self.players_right)):
            # print(self.player_pos[idx])
            self.players_right[idx].change_position(self.player_pos[idx])
        if self.active_player == 4:
            self.active_player = 0

    def set_window(self, pos):

        self.change_background(self.color)
        # self.display_spaces(self.spaces)
        # self.display_spaces(self.spaces_cards_help)
        if self.roz == -1 and self.gest:
            self.hand.camera_run(self.screen)

        self.display_txt()
        self.display_cards(self.cards, pos)
        if self.show_help_card:
            self.display_cards(self.cards_help, pos)
        self.display_moving_card(self.cards, pos)
        self.display_moving_card(self.cards_help, pos)
        self.screen.blit(self.txt_round, self.txt_pos)
        self.display_players()
        self.space_color_change(pos)
        self.koniec_gry.display(self.screen)
        self.screen.blit(self.cursor, pos)

        pygame.display.update()

    def select_card(self, pos, list_cards):

        for card in list_cards:
            if card.is_over(pos) and self.check_used_held_card(card.id):
                card.selected = True
                self.difference = card.get_difference_position(pos)  # to draw card during move
                return
        return

    def check_used_held_card(self, card_id):
        for card_used in self.cards_help_used:
            if card_used.id == card_id:
                return False
        return True

    def select_card_help(self, pos, list_cards):
        for card in list_cards[::-1]:
            if card.is_over(pos) and card.check_if_peek() and self.check_used_held_card(card.id):
                card.selected = True
                card.change_size(self.card_width-2, self.card_height-2)
                self.difference = card.get_difference_position(pos)  # to draw card during move
                return
        return

    def check_if_space_free(self, space_id):
        free = True
        for card in self.cards:
            if card.id == space_id:
                free = False
        return free

    def check_if_card_touch_card(self, space_id, card_id):
        neighbours = 0
        save_card_id = (0, 0)

        for card in self.cards:
            if card.id[0] != card_id[0] or card.id[1] != card_id[1]:
                if space_id[0] == card.id[0] and (space_id[1] - 1) == card.id[1]:
                    save_card_id = (space_id[0], (space_id[1] - 1))
                    neighbours += 1

                elif (space_id[0] + 1) == card.id[0] and space_id[1] == card.id[1]:
                    save_card_id = ((space_id[0]+1), space_id[1])
                    neighbours += 1

                elif space_id[0] == card.id[0] and (space_id[1] + 1) == card.id[1]:
                    save_card_id = (space_id[0], (space_id[1] + 1))
                    neighbours += 1

                elif (space_id[0] - 1) == card.id[0] and space_id[1] == card.id[1]:
                    save_card_id = ((space_id[0] - 1), space_id[1])
                    neighbours += 1

        if neighbours == 1:
            if self.id_card_to_check == card_id:
                self.id_card_to_check = None
                return False
            self.id_card_to_check = save_card_id
            return True
        elif neighbours > 0:
            return True
        return False

    def save_card_neighbour_id(self, card_id):

        cards_id = [(card_id[0], card_id[1] - 1),
                    (card_id[0] + 1, card_id[1]),
                    (card_id[0], card_id[1] + 1),
                    (card_id[0] - 1, card_id[1])]
        neigh_cards = []
        for c_id in cards_id:
            neigh_card_id = c_id
            if not self.check_if_space_free(neigh_card_id):
                neigh_cards.append(neigh_card_id)
        return neigh_cards

    def check_if_neighbour_card_touch(self, neighbours_id):
        for n_id in neighbours_id:
            if not self.check_if_card_touch_card(n_id, n_id):
                return False
            if self.id_card_to_check is not None:
                if not self.check_if_card_touch_card(self.id_card_to_check, self.id_card_to_check):
                    self.id_card_to_check = None
                    return False
                self.id_card_to_check = None
        return True

    def put_selected_card(self, pos):
        for card in self.cards:
            if card.check_selected():
                for space in self.spaces:
                    if space.is_over(pos) and self.check_if_space_free(space.id) and \
                            self.check_if_card_touch_card(space.id, card.id):
                        neighbour_id = self.save_card_neighbour_id(card.id)
                        space_position = space.get_position()
                        tmp = card.id
                        card.id = space.id

                        if not self.check_if_neighbour_card_touch(neighbour_id):
                            card.id = tmp
                            return
                        card.change_position(space_position)
                        self.check_resize_need(card.id)
                        self.check_resize_small()
                        self.round += 1
                        card.selected = False
                        return
                    card.selected = False

    def put_selected_card_help(self, pos):
        for help_card in self.cards_help:
            if help_card.check_selected():
                for card in self.cards:
                    if card.is_over(pos):
                        card_position = card.get_position()
                        help_card.id = card.id
                        help_card.change_position(card_position)
                        self.cards_help_used.append(help_card)
                        help_card.selected = False
                        self.round += 1
                        return
                help_card.change_size(self.help_card_width, self.help_card_height)
                help_card.selected = False

    def reverse_old_peeked_card(self):
        for card in self.cards:
            if card.check_if_peek():
                card.peek_card(self.peeked_card)

    def reverse_all_card(self):
        for card in self.cards:
            card.peek_card(True)

    def peek_card(self, pos):
        for card in self.cards:
            if card.is_over(pos) and self.check_used_held_card(card.id):
                if self.peeked_card:
                    self.peeked_card = False
                    self.reverse_old_peeked_card()
                else:
                    self.peeked_card = True
                    self.peek_number += 1
                card.peek_card(self.peeked_card)

    def peek_help_card(self, pos):
        # pass
        for help_card in self.cards_help:
            if help_card.is_over(pos) and self.number_of_space_help < 10 and not help_card.check_if_peek():
                space_card = self.spaces_cards_help[0]
                help_card.peek_card(True)
                help_card.id = space_card.id
                help_card.change_position(space_card.get_position())
                self.number_of_space_help += 1
                self.round += 1
                return

    def mouse_button_down(self, pos):
        mouse_presses = pygame.mouse.get_pressed()
        if self.koniec_gry.is_over(pos):
            print("koniec")
            self.end = True
            self.round = -99
            if self.show_help_card:
                self.show_help_card = False
                self.reverse_all_card()
            else:
                self.show_help_card = True
                self.reverse_old_peeked_card()

        # print(self.peek_number)
        if self.round == 1:

            if self.roz == -1 and not self.peeked_card and self.gest:
                if not self.selected_card:
                    self.select_card(pos, self.cards)
                    self.selected_card = True
                else:
                    self.put_selected_card(pos)
                    self.selected_card = False
            else:
                self.select_card(pos, self.cards)

        elif self.round == 2:
            if self.roz == -1 and not self.peeked_card and self.gest:
                if not self.selected_card:
                    self.select_card_help(pos, self.cards_help)
                    self.selected_card = True
                else:
                    self.put_selected_card_help(pos)
                    self.selected_card = False
            else:
                self.select_card_help(pos, self.cards_help)

        elif self.round == 0:
            self.peek_card(pos)
            if self.peek_number == 2 and not self.gest or \
                    (self.roz == -1 and self.peek_number == 2 and not self.peeked_card and self.gest):
                self.round += 1
                self.peek_number = 0
        if self.round == 2:
            self.peek_help_card(pos)

    def mouse_button_up(self, mouse_presses, pos):
        if mouse_presses[0] and not self.gest:
            self.put_selected_card(pos)
            self.put_selected_card_help(pos)

        if self.roz == -1 and self.gest:
            pass
            # self.peeked_card = True
        else:
            self.peeked_card = False
            if not self.end:
                self.reverse_old_peeked_card()

    def space_color_change(self, pos):
        for space in self.spaces:
            if space.is_over(pos):
                space.change_color((0, 0, 200))

    def run(self):

        running = True
        while running:
            if self.round == 3:
                self.round = 0
                self.change_active_player()

            pos = pygame.mouse.get_pos()
            mouse_presses = pygame.mouse.get_pressed()
            self.set_window(pos)
            if self.roz == -1 and self.gest:
                self.hand_select = self.hand.get_selected()
                if self.hand_select_old != self.hand_select:
                    print(self.hand_select)

                    if self.hand_select:
                        print(self.hand_select)
                        self.mouse_button_down(pos)

                self.hand_select_old = self.hand_select

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_button_up(mouse_presses, pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(pos)

                # for card in self.cards:
                #     card.check_color_card(pos)
                # mouse events
