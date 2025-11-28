import pygame
import button
import os
import Board as b
from time import sleep


pygame.init()

# ------------------------------------------- OKNO STARTOWE GRY --------------------------------------------------------
SCALE = 1.8
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
path = "./yokaiImg/"
image_names = {}
images = {}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Y O K A I   -   p r z e ż y j   p r z y g o d ę   "
                           "w   n i e s a m o w i t y m   ś w i e c i e   d u c h ó w")
# pygame_icon = pygame.image.load('yokaiImg/kartaZakryta2.png')
# pygame.display.set_icon(pygame_icon)

# ------------------------------------ WCZYTANIE WSZYSTKICH OBRAZÓW ----------------------------------------------------
def load_image(image):
    img = pygame.image.load(image)
    w, h = img.get_rect().size
    return pygame.transform.scale(img, (w/SCALE, h/SCALE))


def import_files():
    for file in os.listdir(path):
        if file.endswith(".png"):
            file_name = file[:-4]
            image_names[file_name] = file_name
            file_path = os.path.join(path, file)
            images[file_name] = load_image(file_path)


import_files()

# ----------------------------------------- CZCIONKI I PRZYCISKI -------------------------------------------------------
czcionka = int(round(50/SCALE, 0))
font = pygame.font.SysFont("Bookman Old Style", czcionka)
TEXT_COL = (253, 253, 253)

cursor_surface = pygame.Surface(images["kursor"].get_size(), pygame.SRCALPHA)
cursor_surface.blit(images["kursor"], (0, 0))
pygame.mouse.set_visible(False)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def create_buttons(button_name, x, y):
    return button.Button(x, y, button_name, 1)


def zmien_rozdzielczosc():
    global imgSterowanie, imgTryb, imgMusic, sterowanie_gestem, tryb, muzyka

    if sterowanie_gestem:
        imgSterowanie = images["sterowanieMysza"]
    else:
        imgSterowanie = images["sterowanieGestem"]
    if tryb == 1:
        imgTryb = images["trybCiemny"]
    else:
        imgTryb = images["trybJasny"]

    if muzyka == -1:
        imgMusic = images["dzwiek"]
    else:
        imgMusic = images["brakDzwieku"]



# -------------------------------------------- POMOCNICZE ZMIENNE ------------------------------------------------------
run = True
game_paused = False
menu_state = "main"
rozdzielczosc = 1
tryb = 1
muzyka = -1
sound_2 = 1
imgMusic = images["dzwiek"]
imgTryb = images["trybCiemny"]
imgSterowanie = images["sterowanieGestem"]
sound = pygame.mixer.Sound("./music/Relaxing Japanese Music - Moonlit Sky.mp3")
sound2 = pygame.mixer.Sound("./music/Japanese Battle Music - Ronin.mp3")
sterowanie_gestem = False

# -------------------------------------------- GŁÓWNA PĘTLA GRY --------------------------------------------------------
while run:
    screen.blit(images["tloMax4"], (0, 0))
    if game_paused:
        # -------------------------------------------- MENU GŁÓWNE -----------------------------------------------------
        if menu_state == "main":
            screen.blit(images["Yokai"], ((SCREEN_WIDTH/2)-(225/SCALE), SCREEN_HEIGHT/9))
            # DO ZMIANY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if create_buttons(images["przyciskGraj"], (SCREEN_WIDTH/2)-(385/SCALE), (320/SCALE)).draw(screen):
                menu_state = "play"
            if create_buttons(images["przyciskOpcje"], (SCREEN_WIDTH/2)-(385/SCALE), (500/SCALE)).draw(screen):
                menu_state = "options"
            if create_buttons(images["przyciskInstrukcja"], (SCREEN_WIDTH/2)-(385/SCALE), (680/SCALE)).draw(screen):
                menu_state = "instruction"
            if create_buttons(images["przyciskPomoc2"], SCREEN_WIDTH-(144/SCALE), 0).draw(screen):
                menu_state = "help"
            if create_buttons(images["przyciskWyjscie3"], SCREEN_WIDTH-(68.4/SCALE), 0).draw(screen):
                run = False
        # ------------------------------------------------ GRAJ --------------------------------------------------------
        if menu_state == "play":
            tlo = pygame.transform.scale(images["tlo69"], (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(tlo, (0, 0))
            screen.blit(images["graj"], ((110/SCALE), (100/SCALE)))
            screen.blit(images["tekstGraj"], ((110/SCALE), (SCREEN_HEIGHT/2)-(10/SCALE)))
            if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
                              SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
                menu_state = "chooseCharacter"
        #---------------------------------- help -------------------------------------------------------
        if menu_state == "help":
            tlo = pygame.transform.scale(images["tlo69"], (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(tlo, (0, 0))
            screen.blit(images["pomoc"], ((110 / SCALE), (100 / SCALE)))
            screen.blit(images["pytajnik"], ((110 / SCALE), (SCREEN_HEIGHT / 2) - (150 / SCALE)))
            if create_buttons(images["przyciskWroc"], SCREEN_WIDTH - (297 / SCALE), SCREEN_HEIGHT - (144 / SCALE)).draw(
                    screen):
                menu_state = "main"

        # ----------------------------------------------- OPCJE --------------------------------------------------------
        if menu_state == "options":
            tlo = pygame.transform.scale(images["tlo69"], (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(tlo, (0, 0))
            screen.blit(images["opcje"], ((110/SCALE), (100/SCALE)))
            # --------------------------------------- ROZDZIELCZOŚĆ ----------------------------------------------------
            if create_buttons(images["rozdzielczosc"], (600/SCALE), (360/SCALE)).draw(screen):
                if rozdzielczosc == 1:
                    sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    SCREEN_WIDTH = sc.get_width()
                    SCREEN_HEIGHT = sc.get_height()
                    SCALE = 1
                    czcionka = int(round(50 / SCALE, 0))
                    import_files()
                    zmien_rozdzielczosc()

                else:
                    sc = pygame.display.set_mode((800, 500))
                    SCREEN_WIDTH = sc.get_width()
                    SCREEN_HEIGHT = sc.get_height()
                    SCALE = 1.8
                    czcionka = int(round(50 / SCALE, 0))
                    import_files()
                    zmien_rozdzielczosc()



                rozdzielczosc = rozdzielczosc * (-1)
            # -------------------------------------------- DŹWIĘK ------------------------------------------------------
            if create_buttons(imgMusic, (115 / SCALE), (360 / SCALE)).draw(screen):
                muzyka *= (-1)
                if muzyka == 1:
                    sound.play(-1)
                    sound_2 = 1
                    sleep(0.1)
                    imgMusic = images["brakDzwieku"]
                else:
                    sleep(0.1)
                    imgMusic = images["dzwiek"]
                    sound.stop()
                    sound2.stop()
            # -------------------------------------------- MOTYW -------------------------------------------------------
            if create_buttons(imgTryb, (115 / SCALE), (500 / SCALE)).draw(screen):
                if tryb == 1:
                    path = "./yokaiImgDark/"
                    import_files()
                    imgTryb = images["trybJasny"]
                    tryb = 0
                else:
                    path = "./yokaiImg/"
                    import_files()
                    imgTryb = images["trybCiemny"]
                    tryb = 1

            # -------------------------------------- STEROWANIE GESTEM -------------------------------------------------
            if create_buttons(imgSterowanie, (600 / SCALE), (500 / SCALE)).draw(screen):
                if sterowanie_gestem:
                    sleep(0.1)
                    imgSterowanie = images["sterowanieGestem"]
                    sterowanie_gestem = False
                else:
                    sleep(0.1)
                    imgSterowanie = images["sterowanieMysza"]
                    sterowanie_gestem = True


            if create_buttons(images["przyciskWroc"], SCREEN_WIDTH-(297/SCALE), SCREEN_HEIGHT-(144/SCALE)).draw(screen):
                menu_state = "main"
        # -------------------------------------------- INSTRUKCJA ------------------------------------------------------
        if menu_state == "instruction":
            tlo = pygame.transform.scale(images["tlo69"], (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(tlo, (0, 0))
            screen.blit(images["instrukcja"], ((110/SCALE), (100/SCALE)))
            screen.blit(images["image_instrukacja"], ((110 / SCALE), (SCREEN_HEIGHT / 2) - (180 / SCALE)))


            if create_buttons(images["przyciskWroc"], SCREEN_WIDTH-(297/SCALE), SCREEN_HEIGHT-(144/SCALE)).draw(screen):
                menu_state = "main"
        # ------------------------------------------- WYBÓR POSTACI ----------------------------------------------------
        if menu_state == "chooseCharacter":
            screen.blit(images["tloMax4"], (0, 0))
            draw_text("W y b i e r z    p r z e w o d n i k a ", pygame.font.Font("RUSerius-Regular.ttf",
                      int(round(100/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (610 / SCALE), (SCREEN_HEIGHT / 2) - (400 / SCALE))
            draw_text("S w e j    z a k l ę t e j    d u s z y    . . . ", pygame.font.Font("RUSerius-Regular.ttf",
                      int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (610 / SCALE), (SCREEN_HEIGHT / 2) - (300 / SCALE))

            draw_text("Kappa ", pygame.font.Font("RUSerius-Regular.ttf", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (610 / SCALE), (SCREEN_HEIGHT / 2) + (150 / SCALE))
            draw_text("Rokurokubi ", pygame.font.Font("RUSerius-Regular.ttf", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (340 / SCALE), (SCREEN_HEIGHT / 2) + (150 / SCALE))
            draw_text("Kitsune ", pygame.font.Font("RUSerius-Regular.ttf", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (30 / SCALE), (SCREEN_HEIGHT / 2) + (150 / SCALE))
            draw_text("Oni ", pygame.font.Font("RUSerius-Regular.ttf", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (430 / SCALE), (SCREEN_HEIGHT / 2) + (150 / SCALE))

            if create_buttons(images["postacWoda"], (SCREEN_WIDTH/2)-(670/SCALE),
                              (SCREEN_HEIGHT/2)-(150/SCALE)).draw(screen):
                sound.stop()
                if (muzyka == 1 and sound_2 == 1):
                    sound2.play(-1)
                    sound_2 = 0
                menu_state = "characterDescription"
            if create_buttons(images["postacZiemia"], (SCREEN_WIDTH/2)-(370/SCALE),
                              (SCREEN_HEIGHT/2)-(165/SCALE)).draw(screen):
                sound.stop()
                if (muzyka == 1 and sound_2 == 1):
                    sound2.play(-1)
                    sound_2 = 0
                menu_state = "characterDescription2"
            if create_buttons(images["postacOgien"], (SCREEN_WIDTH/2)-(50/SCALE),
                              (SCREEN_HEIGHT/2)-(130/SCALE)).draw(screen):
                sound.stop()
                if (muzyka == 1 and sound_2 == 1):
                    sound2.play(-1)
                    sound_2 = 0
                menu_state = "characterDescription3"
            if create_buttons(images["postacPowietrze"], (SCREEN_WIDTH/2)+(330/SCALE),
                              (SCREEN_HEIGHT/2)-(130/SCALE)).draw(screen):
                sound.stop()
                if (muzyka == 1 and sound_2 == 1):
                    sound2.play(-1)
                    sound_2 = 0
                menu_state = "characterDescription4"

            # if create_buttons(images["wyjscie3"], SCREEN_WIDTH-(100/SCALE), 16/SCALE).draw(screen):
            #     menu_state = "play" # ZMIENIC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
            #                   SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
            #     pass
                # board = b.Board(SCREEN_WIDTH, SCREEN_HEIGHT, (70, 100, 100), cursor_surface, tryb, rozdzielczosc)
                # board.run()
            if create_buttons(images["wroc2"], (SCREEN_WIDTH / 2) - (630 / SCALE), SCREEN_HEIGHT-(144/SCALE)).draw(screen):
                menu_state = "main"
        # -------------------------------------------- OPIS POSTACI ----------------------------------------------------
        if menu_state == "characterDescription":
            screen.blit(images["tloWodaOpis"], (0, 0))
            screen.blit(images["postacWodaOpis"], ((SCREEN_WIDTH/2)-(580/SCALE), (SCREEN_HEIGHT/2)-(280/SCALE)))
            draw_text("Wybrano postać Kappa, ",
                      pygame.font.SysFont("Bookman Old Style", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (30 / SCALE), (SCREEN_HEIGHT/2)-(170/SCALE))
            draw_text("która kontroluje żywioł",
                      pygame.font.SysFont("Bookman Old Style", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (30 / SCALE), (SCREEN_HEIGHT/2)-(120/SCALE))
            draw_text("wody, użyj swojej intuicji",
                      pygame.font.SysFont("Bookman Old Style", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (30 / SCALE), (SCREEN_HEIGHT/2)-(70/SCALE))
            draw_text("i doprowadź towarzyszy do",
                      pygame.font.SysFont("Bookman Old Style", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (30 / SCALE), (SCREEN_HEIGHT/2)-(20/SCALE))
            draw_text("zwycięstwa!",
                      pygame.font.SysFont("Bookman Old Style", int(round(50/SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (30 / SCALE), (SCREEN_HEIGHT/2)+(30/SCALE))

            if create_buttons(images["wyjscie2"], SCREEN_WIDTH-(100/SCALE), 16/SCALE).draw(screen):
                menu_state = "chooseCharacter"
            if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
                              SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
                #WKEIĆ PANEL GRY
                board = b.Board(SCREEN_WIDTH, SCREEN_HEIGHT, (70, 100, 100), cursor_surface, tryb, rozdzielczosc, sterowanie_gestem)
                board.run()

        if menu_state == "characterDescription2":
            screen.blit(images["tloZiemiaOpis"], (0, 0))
            screen.blit(images["postacZiemiaOpis"],
                        ((SCREEN_WIDTH / 2) - (650 / SCALE), (SCREEN_HEIGHT / 2) - (300 / SCALE)))
            draw_text("Wybrano postać Rokurokubi, ",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (100 / SCALE), (SCREEN_HEIGHT / 2) - (170 / SCALE))
            draw_text("która kontroluje żywioł",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (100 / SCALE), (SCREEN_HEIGHT / 2) - (120 / SCALE))
            draw_text("ziemi, użyj swoich naturalnych",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (100 / SCALE), (SCREEN_HEIGHT / 2) - (70 / SCALE))
            draw_text("zdolności i podejmuj właściwe",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (100 / SCALE), (SCREEN_HEIGHT / 2) - (20 / SCALE))
            draw_text("decyzje!",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) - (100 / SCALE), (SCREEN_HEIGHT / 2) + (30 / SCALE))

            if create_buttons(images["wyjscie2"], SCREEN_WIDTH - (100 / SCALE), 16 / SCALE).draw(screen):
                menu_state = "chooseCharacter"
            if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
                              SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
                # WKEIĆ PANEL GRY
                board = b.Board(SCREEN_WIDTH, SCREEN_HEIGHT, (70, 100, 100), cursor_surface, tryb, rozdzielczosc, sterowanie_gestem)
                board.run()

        if menu_state == "characterDescription3":
            screen.blit(images["tloOgienOpis3"], (0, 0))
            screen.blit(images["postacOgienOpis"],
                        ((SCREEN_WIDTH / 2) - (630 / SCALE), (SCREEN_HEIGHT / 2) - (240 / SCALE)))
            draw_text("Wybrano postać Kitsune, ",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (170 / SCALE))
            draw_text("która kontroluje żywioł",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (120 / SCALE))
            draw_text("ognia, użyj swojej siły",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (70 / SCALE))
            draw_text("i odwagi, by doprowadzić",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (20 / SCALE))
            draw_text("duchy do triumfu!",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) + (30 / SCALE))

            if create_buttons(images["wyjscie2"], SCREEN_WIDTH - (100 / SCALE), 16 / SCALE).draw(screen):
                menu_state = "chooseCharacter"
            if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
                              SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
                # WKEIĆ PANEL GRY
                board = b.Board(SCREEN_WIDTH, SCREEN_HEIGHT, (70, 100, 100), cursor_surface, tryb, rozdzielczosc, sterowanie_gestem)
                board.run()

        if menu_state == "characterDescription4":
            screen.blit(images["tloPowietrzeOpis"], (0, 0))
            screen.blit(images["postacPowietrzeOpis"],
                        ((SCREEN_WIDTH / 2) - (630 / SCALE), (SCREEN_HEIGHT / 2) - (230 / SCALE)))
            draw_text("Wybrano postać Oni, ",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (200 / SCALE))
            draw_text("która kontroluje żywioł",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (150 / SCALE))
            draw_text("powietrza, użyj swojej",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (100 / SCALE))
            draw_text("elastyczności i przewiduj,",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) - (50 / SCALE))
            draw_text("kolejne ruchy, by osiągnąć",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2))
            draw_text("zamierzony rezultat!",
                      pygame.font.SysFont("Bookman Old Style", int(round(50 / SCALE, 0))), TEXT_COL,
                      (SCREEN_WIDTH / 2) + (10 / SCALE), (SCREEN_HEIGHT / 2) + (50 / SCALE))

            if create_buttons(images["wyjscie2"], SCREEN_WIDTH - (100 / SCALE), 16 / SCALE).draw(screen):
                menu_state = "chooseCharacter"
            if create_buttons(images["przyciskRozpocznij"], SCREEN_WIDTH - (530 / SCALE),
                              SCREEN_HEIGHT - (144 / SCALE)).draw(screen):
                # WKEIĆ PANEL GRY
                board = b.Board(SCREEN_WIDTH, SCREEN_HEIGHT, (70, 100, 100), cursor_surface, tryb, rozdzielczosc, sterowanie_gestem)
                board.run()
    else:
        draw_text("Yokai - niesamowite duchy", font, TEXT_COL, SCREEN_WIDTH/3.5, 250) # DO ZMIANY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
                print("Pause")
        if event.type == pygame.QUIT:
            run = False

    x, y = pygame.mouse.get_pos()
    screen.blit(cursor_surface, (x, y))

    pygame.display.update()

pygame.quit()
