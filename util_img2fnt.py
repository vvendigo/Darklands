# Util to convert image to .FNT format.
# significant colors are:
#  (255, 0, 255) - right and bottom char boundary
#  (255, 255, 255) - character strokes pixels
#  all other colors are considered blank character pixels
# Use `python util_fnt2img.py DL/FONTS.FNT FONTS.FNT.png` to obtain/see editable font image example.

import sys

import pygame

from format_fnt import Char, Font, write_fonts

image_file = sys.argv[1]
font_file = sys.argv[2]
# and then start_char for every font line in image (default 0)

img = pygame.image.load(image_file)

fonts = []
y = 0
argp = 3

while y < img.get_height():
    yy = y
    print('reading', len(fonts))
    while yy < img.get_height() and img.get_at((0, yy))[:4] != (255, 0, 255, 255):
        yy += 1

    if yy >= img.get_height():
        break

    font_height = yy - y
    #print(' height', font_height)
    start_chr = int(sys.argv[argp]) if argp < len(sys.argv) else 0
    argp += 1

    chars = []
    x = 0
    while 1:
        while x < img.get_width() and img.get_at((x, y))[:4] == (255, 0, 255, 255):
            x += 1
        if x >= img.get_width():
            break
        xx = x
        while xx < img.get_width() and img.get_at((xx, y))[:4] != (255, 0, 255, 255):
            xx += 1
        if xx >= img.get_width() or xx == x:
            break
        char_width = xx - x
        #print(char_width)
        lines = []
        for yy in range(0, font_height):
            ln = []
            for xx in range(0, char_width):
                 ln.append(1 if img.get_at((x+xx, y+yy))[:4] == (255, 255, 255, 255) else 0)
            lines.append(ln)
        chars.append(Char(char_width, lines))
        x += char_width
    fonts.append(Font(start_chr, start_chr + len(chars) - 1, font_height, chars))
    print('h:', font_height, start_chr, '-', start_chr + len(chars) - 1)
    y += font_height + 1

'''
# Add blank space to the top of each char
for i, ha in enumerate((1, 2, 2)):
    fonts[i].height += ha
    for ch in fonts[i].chars:
        for ln in range(0, ha):
            ch.lines.insert(0, [0] * ch.width)
'''

write_fonts(font_file, fonts)

