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

    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            b1, g1, r1 = image[y, x]
            b2, g2, r2 = image[y+1, x]
            print(f'\033[38;2;{r2};{g2};{b2};48;2;{r1};{g1};{b1}m▄', end="", flush=False)
            b1, g1, r1 = image[y, x+1]
            b2, g2, r2 = image[y + 1, x+1]
            print(f'\033[38;2;{r2};{g2};{b2};48;2;{r1};{g1};{b1}m▄', end="", flush=False)

        print(RETURN, flush=False)

    count += 1

    sys.stdout.flush()


vidcap.release()


input()
