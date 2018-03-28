import sys
import reader_map
import reader_cty
import reader_loc
import reader_pic
import utils

# output file name
dname = sys.argv[1] 
# path to Darklands
dlPath = sys.argv[2] if len(sys.argv) > 2 else 'DL'

of = open(dname, 'w')

of.write('var Map = {\n');

print 'Reading map data...'
m = reader_map.readData(dlPath)

width, height = len(m[0]), len(m) # in tiles
tw, th = 16, 12 # tile dimensions
dh = 4 # tile y-dist for bliting
#print width, height

of.write('''
cols: %d,
rows: %d,
tw: %d,
th: %d,
dh: %d,
'''%(width, height, tw, th, dh));


of.write('tiles: [\n');

for ln in m:
    of.write('[')
    for pal, row, col in ln:
        of.write('%d,'%(pal*16*16+row*16+col))
    of.write('],\n')

# JS map tile = ((pal, row, col), [locs])

of.write('''
],
locs: [
''');

print "Reading cities..."
cities = reader_cty.readData(dlPath)
print "Reading locs..."
locs = reader_loc.readData(dlPath)


for i,l in enumerate(locs):
    x,y = l['coords']
    ic = l['icon']
    name = l['name'] if ic else cities[i]['name']
    name = utils.tchars(name)
    of.write('{icon:%d, name:"%s"},\n'%(ic, name))

#srf.fill((4, 154, 0))

of.write('''
],

locIcons: {
    1:[1, 12, 0],   // castle
    2:[1, 12, 0],   // castle
    3:[1, 12, 1],   // monastery
    6:[1, 12, 5],   // mines
    8:[1, 13, 0],   // village
    16:[1, 12, 4],  // spring
    17:[1, 12, 4],  // lake
    18:[1, 12, 3],  //shrine
    22:[1, 12, 13], // templ. castle
    23:[1, 12, 14], // baph. castle
},
locsCoords: {
''')

for i,l in enumerate(locs):
    x,y = l['coords']
    of.write('"%d_%d":%d,\n'%(x, y, i))

of.write('''
},
};
''')

