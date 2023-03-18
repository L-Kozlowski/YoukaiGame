import sys, pygame
from Button import Button
import cv2
import HandTrackingModule as htm

pygame.init()
size = width, height = 1900, 1000
black = 0, 0, 0
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
tab_grid = []


def set_grid():
    for x in range(16):
        for y in range(16):
            tab_grid.append(Button((0, 0, 0), 750 + x * 40, 20 + y * 40, 40, 40, ""))
    for x in range(6,10):
        for y in range(6,10):
            tab_grid.append(Button((100, 0, 0), 750 + x * 40, 20 + y * 40, 40, 40, ""))


def set_window(img, pos):
    screen.fill(black)
    htm.set_window(screen, img)
    for grid in tab_grid:
        grid.draw(screen, (0, 100, 0))

    if pos[0] >0:
        pygame.draw.circle(screen, (0, 200, 200), pos, 10)

    pygame.display.update()


def get_cursor_position(lmList):
    x, y = 0, 0
    if len(lmList) != 0:
        id, x, y = lmList[8]
        w, h = 225, 150
        x = (x - w) * 5
        y = (y - h) * 5
    return x, y


def main():

    set_grid()
    cap = htm.video_cap(0, 500, 420)
    detector = htm.HandDetector()

    while True:
        # camera
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.find_hands(img, draw=False)

        fps = detector.calculate_fps()
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        lmList = detector.find_position(img, draw=True)
        pos = get_cursor_position(lmList)

        detector.console_panel(img)
        img = cv2.flip(img, 1)
        set_window(img, pos)

        # game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for grid in tab_grid:
                    grid.clear_cliked()
                    grid.is_clicked(pos)


if __name__ == "__main__":
    main()








