import os
import sys
import time

from PIL import Image


RETURN = '\033[39;49m\n'

img = Image.open("test.png").convert("RGB")

to_print = []
for y in range(img.height):
    for x in range(img.width):
        r, g, b= img.getpixel((x, y))
        to_print.append(f'\033[38;2;255;82;197;48;2;{r};{g};{b}m  ')

    to_print += RETURN

print("Please dezoom")

while os.get_terminal_size()[0] < img.width*2:
    time.sleep(0.1)

sys.stdout.write("".join(to_print))

input()
