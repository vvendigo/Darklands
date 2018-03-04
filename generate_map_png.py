import sys
import map_reader
import cty_reader
import loc_reader
import utils
import pygame


dname = sys.argv[1]

dlPath = sys.argv[2] if len(sys.argv) > 2 else 'DL'

m = map_reader.readData(dlPath)

width, height = len(m[0]), len(m)

fnames = ('tmp/mapicons.pic.png','tmp/mapicon2.pic.png') # tile "palletes"
tw, th = 16, 12 # tile dimensions
dh = 4 # tile y-dist

pals = []

for fn in fnames:
	img = pygame.image.load(fn)
	pals.append(img)

pygame.init()
srf = pygame.Surface(((width+1)*tw, (height+2)*dh))
srf.fill((0, 160, 0))

for y, ln in enumerate(m):
	xc = tw/2 if y%2 else 0
	for x, tile in enumerate(ln):
		pal, row, col = tile
		srf.blit(pals[pal], (x*tw+xc, y*dh), (col*tw, row*th, tw, th))

font = pygame.font.SysFont('gentium', 16)
'''
cities = cty_reader.readData(dlPath)
for c in cities:
	name = utils.tchars(c['short_name']).decode('utf-8')
	x1, y1 = c['entry_coords']
	x1 = x1*tw + (tw/2 if y1%2 else 0)
	y1 *= dh
	x2, y2 = c['exit_coords']
	x2 = x2*tw + (tw/2 if y2%2 else 0)
	y2 *= dh
	text = font.render(name, True, (255, 255, 0))
	textS = font.render(name, True, (0, 0, 0, 128))
	cx = (x1+x2)//2 + tw//2
	cy = (y1+y2)//2 + dh//2
	x = cx - text.get_width()//2
	y = cy - text.get_height()//2 - dh
	#print name, x, y, x1, y1, x2, y2
	srf.blit(textS, (x+1, y+1))
	srf.blit(text, (x, y))
'''
fontV = pygame.font.SysFont('gentium', 9)
fonts = (font, 0,0,0,0,0,0,0, fontV)

locs = loc_reader.readData(dlPath)
for loc in locs:
	lt = loc['icon']
	if lt not in (0, 8):
		continue
	name = utils.tchars(loc['name']).decode('utf-8')
	x, y = loc['coords']
	x = x*tw + (tw/2 if y%2 else 0)
	y *= dh
	text = fonts[lt].render(name, True, (255, 255, 0))
	textS = fonts[lt].render(name, True, (0, 0, 0, 128))
	cx = x + tw//2
	cy = y + dh//2
	x = cx - text.get_width()//2
	y = cy - text.get_height()//2 - dh
	#print name, x, y, x1, y1, x2, y2
	srf.blit(textS, (x+1, y+1))
	srf.blit(text, (x, y))

pygame.image.save(srf, dname)

