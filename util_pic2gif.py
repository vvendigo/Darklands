import sys
from PIL import Image

from format_pic import Pic

infile = sys.argv[1]
outfile = sys.argv[2] if len(sys.argv) > 2 else (infile + '.gif')

pic = Pic()
pic.read_file(infile, addDefaultPal=True)

w = pic.width
h = pic.height

im = Image.new('P', (w, h))

im_data = []
for ln in pic.pic:
    im_data += ln
im.putdata(im_data)

im_pal = [255, 0, 255] * 256
for i, c in enumerate(pic.pal):
    if c is not None:
        im_pal[i * 3 + 0] = c[0]
        im_pal[i * 3 + 1] = c[1]
        im_pal[i * 3 + 2] = c[2]

im.putpalette(im_pal)
im.save(outfile, optimize=0, transparency=0)

