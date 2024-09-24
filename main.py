import os
import sys

import cv2

RETURN = '\033[39;49m'

vidcap = cv2.VideoCapture('video2.mp4')
success, image = vidcap.read()
count = 0
while success:
    success, image = vidcap.read()

    rows, cols, _ = image.shape

    print("\033[1A"*rows, end="")

    for y in range(rows):
        for x in range(cols):
            b, g, r = image[y, x]
            print(f'\033[38;2;255;82;197;48;2;{r};{g};{b}m  ', end="", flush=False)

            #Utiliser les charactères ▀ et ▄ pour préciser le dessin

        print(RETURN, flush=False)

    count += 1

    sys.stdout.flush()

vidcap.release()


input()
