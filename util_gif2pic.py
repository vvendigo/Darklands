import sys
from PIL import Image

from reader_pic import writeFile

infile = sys.argv[1]
outfile = sys.argv[2] if len(sys.argv)>2 else (infile + '.pic')

del_palette = 16

im = Image.open(infile)

w = im.width
h = im.height

print w, h

# convert palette
im_pal = im.getpalette()
pal = []
for i in range(0, len(im_pal), 3):
    pal.append((im_pal[i+0], im_pal[i + 1], im_pal[i + 2]))
print len(pal)

for i in range(0, del_palette):
    pal[i] = (255, 0, 255)

# crop palette
p = 0
while p < len(pal) and pal[p][0] == 255 and pal[p][1] == 0 and pal[p][2] == 255:
    pal[p] = None
    p += 1

p = len(pal) - 1
while p > 0 and pal[p][0] == 255 and pal[p][1] == 0 and pal[p][2] == 255:
    pal[p] = None
    p -= 1
print pal

# convert img data
im_data = list(im.getdata())
data = []
for y in range(0, h):
    data.append(im_data[y*w:y*w+w])

writeFile(outfile, pal, data)

