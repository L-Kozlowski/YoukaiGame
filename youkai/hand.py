import sys, pygame
# from Button import Button
import cv2
import HandTrackingModule as htm


class Hand(object):
    def __init__(self, rozdzielczosc = 0):
        self.roz = rozdzielczosc
        self.selected = False
        if self.roz == -1:
            self.cap = htm.video_cap(0, 500, 420)
        else:
            self.cap = htm.video_cap(0, 180, 120)
        self.detector = htm.HandDetector()

    def set_window(self,screen, img):
        if self.roz == -1:
            htm.set_window(screen, img, (0,620))
        else:
            htm.set_window(screen, img, (0,320))

    def get_cursor_position(self, lmList):
        x, y = 0, 0
        if len(lmList) != 0:
            id, x, y = lmList[8]
            w, h = 225, 150
            x = (x - w) * 5
            y = (y - h) * 5
        return x, y

    def get_selected(self):
        return self.selected

    def camera_run(self, screen):
        success, img = self.cap.read()
        img = cv2.flip(img, 1)
        img = self.detector.find_hands(img, draw=False)

        fps = self.detector.calculate_fps()
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        lmList, self.selected = self.detector.find_position(img, draw=True)
        # print(self.selected)
        pos = self.get_cursor_position(lmList)

        self.detector.console_panel(img)
        img = cv2.flip(img, 1)
        self.set_window(screen,img)









