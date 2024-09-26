import os
import sys
import time

import cv2
import keyboard

WIDTH = 128

CLEAR = "\033[2J"
RESET_CURSOR = "\033[H"


class VideoReader:
    def __init__(self):
        self.vidcap = None
        self.count = 0

        self.playing = False


    def play(self, filename):
        self.vidcap = cv2.VideoCapture(filename)
        self.count = 0
        print("\033[?25l", end="")
        self.playing = True

    def update(self):
        self.playing, image = self.vidcap.read()

        image = cv2.resize(image, (WIDTH, int(WIDTH / image.shape[1] * image.shape[0])))

        rows, cols, _ = image.shape

        print(RESET_CURSOR, end="")

        for y in range(0, rows, 2):
            for x in range(0, cols, 2):
                b1, g1, r1 = image[y, x]
                b2, g2, r2 = image[y + 1, x]
                print(f'\033[38;2;{r2};{g2};{b2};48;2;{r1};{g1};{b1}m▄', end="")
                b1, g1, r1 = image[y, x + 1]
                b2, g2, r2 = image[y + 1, x + 1]
                print(f'\033[38;2;{r2};{g2};{b2};48;2;{r1};{g1};{b1}m▄', end="")

            print('\033[39;49m')

        self.count += 1

    def stop(self):
        self.vidcap.release()
        self.playing = False
        print(CLEAR + "\033[?25l", end="")


class Explorer:
    def __init__(self, app_):
        self.dir = ["C:/", "Users"]
        self.cursor = 0
        self.app = app_

    def scroll(self, index):
        self.cursor += index

    def enter(self):
        files = os.listdir(os.path.join(*self.dir))
        if os.path.isdir(os.path.join(*self.dir, files[self.cursor])):
            self.dir.append(files[self.cursor])
            self.cursor = 0
        elif os.path.isfile(os.path.join(*self.dir, files[self.cursor])):
            self.app.start_video(os.path.join(*self.dir, files[self.cursor]))

    def back(self):
        self.dir.pop()
        self.cursor = 0

    def update(self):
        print(RESET_CURSOR + ("█"*(os.get_terminal_size()[0])))  # First line
        line = os.get_terminal_size()[1]-3

        print(("██" + " " * (os.get_terminal_size()[0] - 4)) + "██")  # Skip one
        line -= 1

        files = os.listdir(os.path.join(*self.dir))

        for i, file in enumerate(files):
            s = "●" if i == self.cursor else "○"
            is_d = os.path.isdir(os.path.join(*self.dir, file))
            f = "📁 " if is_d else "   "

            print(f"██  {s} {f}" + file + " " * (os.get_terminal_size()[0] - 11 - len(file)) + "██")
            line -= 1

        for _ in range(line):
            print(("██" + " " * (os.get_terminal_size()[0]-4)) + "██")
        print(("█" * (os.get_terminal_size()[0])))


class App:
    def __init__(self):
        self.video = VideoReader()
        self.explorer = Explorer(self)
        self.mode = 0  # 0: explorer; 1: video

    def start_video(self, filename):
        self.mode = 1
        app.video.play(filename)

    def loop(self):
        self.explorer.update()
        while True:
            if self.mode == 0:
                if keyboard.is_pressed("down"):
                    self.explorer.scroll(1)
                    self.explorer.update()
                    time.sleep(0.2)
                elif keyboard.is_pressed("up"):
                    self.explorer.scroll(-1)
                    self.explorer.update()
                    time.sleep(0.2)
                elif keyboard.is_pressed("enter"):
                    self.explorer.enter()
                    self.explorer.update()
                    time.sleep(0.2)
                elif keyboard.is_pressed("esc"):
                    self.explorer.back()
                    self.explorer.update()
                    time.sleep(0.2)

            elif self.mode == 1:
                self.video.update()
                if keyboard.get_hotkey_name() == "space":
                    self.video.stop()
                    self.mode = 0




app = App()
app.loop()
