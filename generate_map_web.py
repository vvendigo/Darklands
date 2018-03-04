import sys
import map_reader
import cty_reader
import utils

dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

m = map_reader.readData(dlPath)

width, height = len(m[0]), len(m)

fnames = ('tmp/mapicons.pic.png','tmp/mapicon2.pic.png') # tile "palletes"
tw, th = 16, 12 # tile dimensions
dh = 4 # tile y-dist

print '''<html>
<head>
<meta charset="utf-8">
<title>Map of Darklands</title>
<style type="text/css">
body {margin:0; padding:0; font-size:xx-small;}
.city {color:yellow; text-shadow: 2px 2px #000000; position:absolute; overflow:hidden; cursor: default; width:10em;height:1.4EM}
.city:hover { color:black; text-shadow: none; background-color:white; cursor: auto; border:1px solid black; padding:0.5em; width:auto; height:auto; z-index:1}
'''

for p, fn in enumerate(fnames):
	for r in xrange(0,16):
		for c in xrange(0,16):
			print ".t%d_%d_%d{width:%dpx;height:%dpx; background:url('%s') %dpx %dpx;position:absolute}"\
				%(p, r, c, tw, th, fn, -c*tw, -r*th)

print '''
</style>
</head>
<body>'''
# sprites test
'''
for pal in (0,1):
	print '<div style="position:relative;width:%dpx;height:%dpx;border:1px solid green">'%(16*tw, 16*th)
	for row in xrange(0,16):
		for col in xrange(0,16):
			print '<div class="t%d_%d_%d" style="left:%dpx;top:%dpx"></div>'%(pal, row, col, col*tw, row*th)
	print '</div>'
'''

print '''
<div style="position:relative;width:%dpx;height:%dpx;background-color:#00a000">'''%((width+1)*tw, (height+2)*dh)


for y, ln in enumerate(m):
	#if y < 550: continue
	#if y > 200: continue
	xc = tw/2 if y%2 else 0
	#xc = 0 if y%2 else tw/2
	rs = ''
	for x, tile in enumerate(ln):
		#if x < 200: continue
		#if x > 150: continue
		pal, row, col = tile
		if not ((pal == 0 and row in(1, 3)) or (pal == 1 and row in (8,9,10,11,13))):
			continue
		rs += '<div class="t%d_%d_%d" style="left:%dpx;top:%dpx"></div>'%(pal, row, col, x*tw+xc, y*dh)
	print rs



cities = cty_reader.readData(dlPath)
for c in cities:
	name = utils.tchars(c['full_name'])
	x, y = c['entry_coords']
	x1 = x*tw + (tw/2 if y%2 else 0)
	y1 = y*dh
	x2, y2 = c['exit_coords']
	x2 = x2 * tw + (tw/2 if y%2 else 0)
	y2 = y2*dh
	print '<div class="city" style="left:%dpx;top:%dpx">'\
		%((x1+x2)//2-tw//2, (y1+y2)//2-th//2)
	print "<b>%s</b><br><br>"%(name)
	print cty_reader.cityInfo(c).replace('\n','<br>')
	print '</div>'



print '''</div>
</body>
</html>'''


