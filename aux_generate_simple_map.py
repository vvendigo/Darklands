import sys
import reader_cty
import reader_loc
import utils

dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

cities = reader_cty.readData(dlPath)

minX, minY, maxX, maxY = 1000, 1000, 0, 0
for c in cities:
    ex, ey = c['entry_coords']
    xx, xy = c['exit_coords']
    minX = min(minX, ex, xx)
    minY = min(minY, ey, xy)
    maxX = max(maxX, ex, xx)
    maxY = max(maxY, ey, xy)

divW = 600
a = float(divW)/(maxX-minX)
divH = int((maxY-minY)*a/2)

print '''
<html>
<head>
<meta charset="utf-8">
<style type="text/css">
.ce, .cx, .l {position:absolute;width:8px;height:8px;}
.ce {background-color:green;}
.cx {background-color:blue;}
.l {border:1px solid red;}
</style>
</head>
<body>
<div style="position:relative;border:1px solid gray;width:%dpx;height:%dpx">'''%(divW, divH)

for c in cities:
    name = utils.tchars(c['short_name'])
    x, y = c['entry_coords']
    dx, dy = x-minX, y-minY
    print '<div class="ce" style="top:%dpx;left:%dpx" title="%s"></div>'%(int(dy*a/2)-4, int(dx*a)-4, name+' E')
    x, y = c['exit_coords']
    dx, dy = x-minX, y-minY
    print '<div class="cx" style="top:%dpx;left:%dpx" title="%s"></div>'%(int(dy*a/2)-4, int(dx*a)-4, name+' X')


locs = reader_loc.readData(dlPath)

for c  in locs:
    name = utils.tchars(c['name'] + '(' + c['str_loc_type'] + ')')
    x, y = c['coords']
    dx, dy = x-minX, y-minY
    print '<div class="l" style="top:%dpx;left:%dpx" title="%s"></div>'%(int(dy*a/2)-4, int(dx*a)-4, name+' L')


print '''</div>
<pre>
'''
for i, l  in enumerate(locs):
    if l['icon'] != 0:
        continue
    lx, ly = l['coords']
    c = cities[i]
    cx, cy = c['entry_coords']
    if l['name'] != c['short_name'] or cx-lx or cy-ly:
        print l['name'], c['short_name'], cx-lx, cy-ly

'''
</pre>
</body>
</html>
'''

