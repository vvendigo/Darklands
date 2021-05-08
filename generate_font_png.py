import sys
import pygame
import reader_fnt

infname = sys.argv[1]
outfname = sys.argv[2]

fonts = reader_fnt.read_fonts(infname)

cw = 0
ch = 0
for fnt in fonts:
    ch += 1 + fnt.height
    w = 0
    for char in fnt.chars: w += 1 + char.width
    cw = max(cw, w)

pygame.init()
srf = pygame.Surface((cw, ch), pygame.SRCALPHA, 32)
#srf.fill((0, 0, 0))

y = 0
for fnt in fonts:
    srf.fill((255,0,255), (0, y + fnt.height, cw, 1))
    x = 0
    for ch in fnt.chars:
        srf.fill((255,0,255), (x + ch.width, y, 1, len(ch.lines)))
        for yy, r in enumerate(ch.lines):
            for xx, b in enumerate(r):
                if b: srf.fill((255,255,255), (x+xx,y+yy, 1, 1))
        x += 1 + ch.width
    y += 1 + fnt.height

pygame.image.save(srf, outfname)

