import os
import sys
import time

import cv2
import keyboard

WIDTH = 128

CLEAR = "\033[2J"
RESET_CURSOR = "\033[H"
HIDE_CURSOR = "\033[?25l"


class VideoReader:
    def __init__(self):
        self.vidcap = None
        self.count = 0

        self.playing = False


    def play(self, filename):
        os.system("cls")
        self.vidcap = cv2.VideoCapture(filename)
        self.count = 0
        print(HIDE_CURSOR, end="")
        self.playing = True

    def update(self, full_refresh=False):
        if full_refresh:
            os.system("cls")
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
        print(CLEAR, end="")


class Explorer:
    def __init__(self, app_):
        self.dir = ["C:/", "Users"]
        self.cursor = 0
        self.scrolling = 0
        self.app = app_
        self.files = os.listdir(os.path.join(*self.dir))

    def scroll(self, index):
        self.cursor += index
        if self.cursor < 0:
            self.scrolling = len(self.files) - os.get_terminal_size()[1]+5
            self.cursor = len(self.files)-1
        if self.cursor >= len(self.files):
            self.scrolling = 0
            self.cursor = 0

        if self.cursor - self.scrolling > os.get_terminal_size()[1]-8:
            self.scrolling += 1
        if self.cursor - self.scrolling < 2:
            self.scrolling -= 1

        if self.scrolling < 0:
            self.scrolling = 0
        if self.scrolling >= len(self.files):
            self.scrolling = len(self.files)-1

    def enter(self):
        if os.path.isdir(os.path.join(*self.dir, self.files[self.cursor])):
            self.dir.append(self.files[self.cursor])
            self.files = os.listdir(os.path.join(*self.dir))
            self.cursor = 0
            self.scrolling = 0
        elif os.path.isfile(os.path.join(*self.dir, self.files[self.cursor])):
            self.app.start_video(os.path.join(*self.dir, self.files[self.cursor]))

    def back(self):
        self.dir.pop()
        self.cursor = 0

    def update(self, full_refresh=False):
        if full_refresh:
            os.system("cls")
        print(HIDE_CURSOR + RESET_CURSOR + ("█"*(os.get_terminal_size()[0])))  # First line
        line = os.get_terminal_size()[1]-3

        if self.scrolling:
            print(("██  ▲ ▲ ▲" + " " * (os.get_terminal_size()[0] - 11)) + "██")
        else:
            print(("██" + " " * (os.get_terminal_size()[0] - 4)) + "██")
        line -= 1

        for i in range(self.scrolling, len(self.files)):
            file = self.files[i]
            s = "●" if i == self.cursor else "○"
            is_d = os.path.isdir(os.path.join(*self.dir, file))
            f = "📁 " if is_d else "📄 "

            print(f"██  {s} {f}" + file + " " * (os.get_terminal_size()[0] - 11 - len(file)) + "██")
            line -= 1
            if line == 1:
                if i < len(self.files)-1:
                    print(("██  ▼ ▼ ▼" + " " * (os.get_terminal_size()[0] - 11)) + "██")
                    line -= 1
                break

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

        last_size = ()
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

                term_size = os.get_terminal_size()
                if last_size != term_size:
                    last_size = term_size
                    self.explorer.update(True)

            elif self.mode == 1:
                term_size = os.get_terminal_size()
                if last_size != term_size:
                    last_size = term_size
                    self.video.update(True)
                else:
                    self.video.update()
                if not self.video.playing:
                    self.video.stop()
                    self.mode = 0
                    self.explorer.update()
                if keyboard.get_hotkey_name() == "space":
                    self.video.stop()
                    self.mode = 0
                    self.explorer.update()




app = App()
app.loop()
