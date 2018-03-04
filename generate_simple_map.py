import sys
import reader_cty

dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

cities = reader_cty.readData(dlPath)

minX, minY, maxX, maxY = 1000, 1000, 0, 0
for c in cities:
    x, y = c['entry_coords']
    if x < minX: minX = x
    if y < minY: minY = y
    if x > maxX: maxX = x
    if y > maxY: maxY = y

divW = 600
a = float(divW)/(maxX-minX)
divH = int((maxY-minY)*a/2)

print '''
<html>
<head>
</head>
<body>
<div style="position:relative;border:1px solid gray;width:%dpx;height:%dpx">'''%(divW, divH)

for c in cities:
    x, y = c['entry_coords']
    dx, dy = x-minX, y-minY
    print '<div style="position:absolute;width:8px;height:8px;background-color:red;top:%dpx;left:%dpx" title="%s"></div>'%(int(dy*a/2)-4, int(dx*a)-4, c['short_name'])


print '''</div>
</body>
</html>
'''

