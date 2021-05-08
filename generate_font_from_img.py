import sys

import pygame

from reader_fnt import Char, Font

image_file = sys.argv[1]
font_file = sys.argv[2]

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
    print chars[-1]
    y += font_height + 1
'''
for ch in fonts[0]['chars'][:5]:
    for ln in ch['lines']:
        print ''.join(map(str, ln))
    print
'''
fontdata = []
for i, fnt in enumerate(fonts):
    data = []
    for ch in fnt.chars:
        data.append(ch.width)
    max_w = max(data)
    byte_w = max_w / 8 + (1 if max_w % 8 else 0)
    print i, fnt.start_chr, '-', fnt.end_chr, len(fnt.chars), fnt.height, 'bw', byte_w
    data += [fnt.start_chr, fnt.end_chr, byte_w, 0, fnt.height, 1, 1, 0]
    for y in range(0, fnt.height):
        for ch in fnt.chars:
            val = 0
            for p in ch.lines[y]:
                val <<= 1
                val |= p
            val <<= (byte_w*8) - ch.width
            bts = []
            for b in range(byte_w):
                bts.insert(0, val & 0xff)
                val >>= 8
            #if i == 1: print bts
            data += bts
    fontdata.append(data)

data = [len(fonts), 0]
offs = len(data) + 2 * len(fonts)
for i, fnt in enumerate(fonts):
    offs += 8 + len(fnt.chars)
    data += [offs & 0xff, offs >> 8]
    offs += len(fontdata[i]) - (8 + len(fnt.chars))

for fd in fontdata:
    data += fd

#print fontdata[1][8 + len(fonts[1]['chars']):]

f = open(font_file, 'wb')
f.write(bytearray(data))
f.close()

