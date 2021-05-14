# Makes image out of .FNT file (suitable for editation).

import sys
import pygame
from format_fnt import read_fonts

infname = sys.argv[1]
outfname = sys.argv[2]

fonts = read_fonts(infname)

cw = 0
ch = 0
for fnt in fonts:
    ch += 1 + fnt.height
    w = 0
    for char in fnt.chars: w += 1 + char.width
    cw = max(cw, w)

pygame.init()
srf = pygame.Surface((cw, ch), pygame.SRCALPHA, 32)
srf.fill((255, 0, 255))

y = 0
for fnt in fonts:
    x = 0
    for ch in fnt.chars:
        for yy, r in enumerate(ch.lines):
            for xx, b in enumerate(r):
                clr = (255,255,255) if b else (0, 0, 0)
                srf.fill(clr, (x+xx,y+yy, 1, 1))
        x += 1 + ch.width
    y += 1 + fnt.height

pygame.image.save(srf, outfname)

