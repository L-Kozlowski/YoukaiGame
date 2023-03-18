import cv2
import mediapipe as mp
import time
import pygame
import numpy as np


class HandDetector(object):
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5,
                 console_pos=(225, 150), console_size=(380, 200)):
        self.mode = mode
        self.maxHands = max_hands
        self.model_complexity = model_complexity
        self.detectionCon = detection_con
        self.trackCon = track_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
        self.console_pos = console_pos
        self.console_size = console_size
        self.p_time = 0

    def find_hands(self, img, draw=True):
        """ Processes an RGB image and returns the hand landmarks and handedness of each detected hand.
            Draws an landmarks with connection of each detected hand.
        :param img:  An RGB image from camera
        :param draw: decides whether to draw markers
        :return: image with drawn landmarks
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        #  print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Process returns list of positions landmarks from detected hands
        :param img: An RGB image from camera
        :param hand_no: number of hand
        :param draw: decides whether to draw markers on index finger
        :return: returns list of positions landmarks from detected hands
        """

        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id_point, lm in enumerate(my_hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lm_list.append((id_point, cx, cy))
                if draw:
                    if id_point == 8:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lm_list

    def console_panel(self, img):
        """
        Process draws a rectangle in the camera view.
        The rectangle is where the cursor navigates
        :param img: An RGB image from camera
        """
        start_point = self.console_pos
        end_point = self.console_pos[0] + self.console_size[0], self.console_pos[1] + self.console_size[1]
        cv2.rectangle(img, start_point, end_point, (255, 0, 0), 2)

    def calculate_fps(self):
        """
        Calculate fps by current time and saved previous time
        :return: fps
        """
        c_time = time.time()
        fps = 1 / (c_time - self.p_time)
        self.p_time = c_time
        return fps


def video_cap(cam_id, width_cap, height_cap):
    """
    Process captures a video from camera
    :param cam_id: id selected camera
    :param width_cap: width of camera frame
    :param height_cap: height camera frame
    :return: captures a video
    """
    cap = cv2.VideoCapture(cam_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_cap)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_cap)
    return cap


def set_window(window, img, cam_pos=(0, 0)):
    """
    Add camera to the pygame window
    :param cam_pos: camera position on pygame window
    :param window: pygame window
    :param img: An RGB image from camera
    """

    # screen.fill(black)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.rot90(img)
    frame = pygame.surfarray.make_surface(img)
    window.blit(frame, cam_pos)
    # pygame.display.update()


def main():
    cap = video_cap(500, 420)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        fps = detector.calculate_fps()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[8])
        print(img.shape)

        # cv2.imshow("Image", img)

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        detector.console_panel(img)
        img = cv2.flip(img, 1)
        set_window(screen, img)

        cv2.waitKey(1)


if __name__ == "__main__":
    pygame.init()
    size = width, height = 1900, 1000
    black = 0, 0, 0
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    main()
