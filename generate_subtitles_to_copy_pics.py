import os

from format_pic import Pic, default_pal
from format_fnt import read_fonts

import pygame

font = read_fonts('DL/fonts.fnt')[0]

names = [
    ['copy0.pic', 'Calcination'],
    ['copy1.pic', 'Solution'],
    ['copy2.pic', 'Sublimati-on'],
    ['copy3.pic', 'Fermenta-tion'],
    ['copy4.pic', 'Congelation'],
    ['copy5.pic', 'Digestion'],
    ['copy6.pic', 'Separation'],
    ['copy7.pic', 'Multiplica-tion'],
    ['copy8.pic', 'Fixation'],
    ['copy9.pic', 'Distillation'],
    ['copy10.pic', 'Ceration'],
    ['copy11.pic', 'Projection'],
    ['copy12.pic', 'Water'],
    ['copy13.pic', 'Silver'],
    ['copy14.pic', 'Sulpher'],
    ['copy15.pic', 'Mercury'],
    ['copy16.pic', 'Gold'],
    ['copy17.pic', 'Iron'],
    ['copy18.pic', 'Lead'],
    ['copy19.pic', 'Arsenic'],
]


def draw_text(imgdata, txts, x, y, clr):
    for txt in txts:
            tw = 0
            xx = x
            for ch in txt:
                chi = ord(ch) - font.start_chr
                tw += font.chars[chi].width
            xx -= tw/2

            for ch in txt:
                chi = ord(ch) - font.start_chr
                char = font.chars[chi]
                for yy, ln in enumerate(char.lines):
                    for xxx, p in enumerate(ln):
                        if p: imgdata[y+yy][xx+xxx] = clr 
                xx += char.width
            y += font.height

for fname, name in names:
    name = name.split('-')
    if len(name) > 1: name[0] += '-'
    print fname, name

    infile = os.path.join('DL/pics/', fname)

    pic = Pic(infile)

    w = pic.width
    h = pic.height

    draw_text(pic.pic, name, w/2, h - font.height * len(name), 9) # blue

    # preview PNG images:
    #'''
    pic.pal = default_pal[:16] + [None] * 240
    # colors similar to real ones
    pic.pal[141] = (254, 168, 95)
    pic.pal[142] = (202, 140, 83)
    pic.pal[143] = (153, 91, 32)
    img = pic.render_image()
    pygame.image.save(img, fname + '.png')
    #'''

    pic.pal = None
    pic.write_file(fname.upper())

