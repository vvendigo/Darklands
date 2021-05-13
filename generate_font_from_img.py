import sys

import pygame

from reader_fnt import Char, Font, write_fonts

image_file = sys.argv[1]
font_file = sys.argv[2]
# and then start_char for every font line in image

img = pygame.image.load(image_file)

fonts = []
y = 0
argp = 3

while y < img.get_height():
    yy = y
    print 'reading', len(fonts)
    while yy < img.get_height() and img.get_at((0, yy))[:4] != (255, 0, 255, 255):
        yy += 1

    if yy >= img.get_height():
        break

    font_height = yy - y
    print font_height
    start_chr = int(sys.argv[argp])
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
        #print char_width
        lines = []
        for yy in range(0, font_height):
            ln = []
            for xx in range(0, char_width):
                 ln.append(1 if img.get_at((x+xx, y+yy))[:4] == (255, 255, 255, 255) else 0)
            lines.append(ln)
        chars.append(Char(char_width, lines))
        x += char_width
    fonts.append(Font(start_chr, start_chr + len(chars) - 1, font_height, chars))
    #print chars[-1]
    y += font_height + 1

write_fonts(font_file, fonts)

