import sys
import reader_map
import reader_cty
import reader_loc
import reader_pic
import utils
import pygame

# output file name
dname = sys.argv[1] 
# path to Darklands
dlPath = sys.argv[2] if len(sys.argv) > 2 else 'DL'

fontName = 'gentium'

# tile "palletes"
tilePalFnames = (dlPath+'/pics/mapicons.pic',dlPath+'/pics/mapicon2.pic')

print 'Reading map data...'
m = reader_map.readData(dlPath)

width, height = len(m[0]), len(m) # in tiles
tw, th = 16, 12 # tile dimensions
dh = 4 # tile y-dist for bliting

pals = []

for fn in tilePalFnames:
	print 'Reading tile pallete:', fn
	pals.append(reader_pic.getImage(fn))

print "Reading locs..."
locs = reader_loc.readData(dlPath)
locsByCoords = {}
for i,l in enumerate(locs):
	c = l['coords']
	if c in locsByCoords:
		locsByCoords[c].append(i)
	else:
		locsByCoords[c] = [i]

print "Rendering tile map..."
pygame.init()
srf = pygame.Surface(((width+1)*tw, (height+2)*dh))
srf.fill((0, 160, 0))

locIcons = {1:(1, 12, 0), 8:(1, 13, 0), 3:(1, 12, 1), 17:(1, 12, 4), 18:(1, 12, 3), 6:(1, 12, 5)} # castle, village, monastery, lake, shrine, mines

for y, ln in enumerate(m):
	xc = tw/2 if y%2 else 0
	for x, tile in enumerate(ln):
		pal, row, col = tile
		srf.blit(pals[pal], (x*tw+xc, y*dh), (col*tw, row*th, tw, th))
		# render locs
		for li in locsByCoords.get((x,y), []):
			lt = locIcons.get(locs[li]['icon'])
			if lt:
				pal, row, col = lt
				srf.blit(pals[pal], (x*tw+xc, y*dh), (col*tw, row*th, tw, th))

fontBig = pygame.font.SysFont(fontName, 18)
fontSmaller = pygame.font.SysFont(fontName, 12)
fontSmallest = pygame.font.SysFont(fontName, 9)

fonts = {0:fontBig, 8:fontSmaller, 13:0, 15:0, 17:0, 18:0, 19:0, 20:0}

print 'Rendering names...'
for loc in locs:
	lt = loc['icon']
	name = utils.tchars(loc['name']).decode('utf-8')
	x, y = loc['coords']
	x = x*tw + (tw/2 if y%2 else 0)
	y *= dh
	font = fonts.get(lt, fontSmallest)
	if not font: continue
	text = font.render(name, True, (255, 255, 0))
	textS = font.render(name, True, (0, 0, 0, 128))
	cx = x + tw//2
	cy = y + dh//2
	x = cx - text.get_width()//2
	y = cy - text.get_height()//2 - 2*dh
	#print name, x, y, x1, y1, x2, y2
	srf.blit(textS, (x+1, y+1))
	srf.blit(text, (x, y))

pygame.image.save(srf, dname)

