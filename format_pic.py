from struct import pack, unpack

import pygame

import rle, lzw

# Decoding was entirely based on Joel "Quadko" McIntyre PIC reading code
# Now replaced by code based on darkpandaman's JCivED PIC codecs


default_pal = [ (0,0,0), (0,0,127), (0,127,0), (0,127,127), (127,0,0), (127,0,127), (127,127,0), (192,192,192), (127,127,127), (0,0,255), (0,255,0), (0,255,255), (255,0,0), (255,0,255), (255,255,0), (255,255,255), (0,0,0), (20,20,20), (32,32,32), (44,44,44), (56,56,56), (68,68,68), (80,80,80), (96,96,96), (112,112,112), (128,128,128), (144,144,144), (160,160,160), (180,180,180), (200,200,200), (224,224,224), (252,252,252), (0,0,252), (64,0,252), (124,0,252), (188,0,252), (252,0,252), (252,0,188), (252,0,124), (252,0,64), (252,0,0), (252,64,0), (252,124,0), (252,188,0), (252,252,0), (188,252,0), (124,252,0), (64,252,0), (0,252,0), (0,252,64), (0,252,124), (0,252,188), (0,252,252), (0,188,252), (0,124,252), (0,64,252), (124,124,252), (156,124,252), (188,124,252), (220,124,252), (252,124,252), (252,124,220), (252,124,188), (252,124,156), (252,124,124), (252,156,124), (252,188,124), (252,220,124), (252,252,124), (220,252,124), (188,252,124), (156,252,124), (124,252,124), (124,252,156), (124,252,188), (124,252,220), (124,252,252), (124,220,252), (124,188,252), (124,156,252), (180,180,252), (196,180,252), (216,180,252), (232,180,252), (252,180,252), (252,180,232), (252,180,216), (252,180,196), (252,180,180), (252,196,180), (252,216,180), (252,232,180), (252,252,180), (232,252,180), (216,252,180), (196,252,180), (180,252,180), (180,252,196), (180,252,216), (180,252,232), (180,252,252), (180,232,252), (180,216,252), (180,196,252), (0,0,112), (28,0,112), (56,0,112), (84,0,112), (112,0,112), (112,0,84), (112,0,56), (112,0,28), (112,0,0), (112,28,0), (112,56,0), (112,84,0), (112,112,0), (84,112,0), (56,112,0), (28,112,0), (0,112,0), (0,112,28), (0,112,56), (0,112,84), (0,112,112), (0,84,112), (0,56,112), (0,28,112), (56,56,112), (68,56,112), (84,56,112), (96,56,112), (112,56,112), (112,56,96), (112,56,84), (112,56,68), (112,56,56), (112,68,56), (112,84,56), (112,96,56), (112,112,56), (96,112,56), (84,112,56), (68,112,56), (56,112,56), (56,112,68), (56,112,84), (56,112,96), (56,112,112), (56,96,112), (56,84,112), (56,68,112), (80,80,112), (88,80,112), (96,80,112), (104,80,112), (112,80,112), (112,80,104), (112,80,96), (112,80,88), (112,80,80), (112,88,80), (112,96,80), (112,104,80), (112,112,80), (104,112,80), (96,112,80), (88,112,80), (80,112,80), (80,112,88), (80,112,96), (80,112,104), (80,112,112), (80,104,112), (80,96,112), (80,88,112), (0,0,64), (16,0,64), (32,0,64), (48,0,64), (64,0,64), (64,0,48), (64,0,32), (64,0,16), (64,0,0), (64,16,0), (64,32,0), (64,48,0), (64,64,0), (48,64,0), (32,64,0), (16,64,0), (0,64,0), (0,64,16), (0,64,32), (0,64,48), (0,64,64), (0,48,64), (0,32,64), (0,16,64), (32,32,64), (40,32,64), (48,32,64), (56,32,64), (64,32,64), (64,32,56), (64,32,48), (64,32,40), (64,32,32), (64,40,32), (64,48,32), (64,56,32), (64,64,32), (56,64,32), (48,64,32), (40,64,32), (32,64,32), (32,64,40), (32,64,48), (32,64,56), (32,64,64), (32,56,64), (32,48,64), (32,40,64), (44,44,64), (48,44,64), (52,44,64), (60,44,64), (64,44,64), (64,44,60), (64,44,52), (64,44,48), (64,44,44), (64,48,44), (64,52,44), (64,60,44), (64,64,44), (60,64,44), (52,64,44), (48,64,44), (44,64,44), (44,64,48), (44,64,52), (44,64,60), (44,64,64), (44,60,64), (44,52,64), (44,48,64), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0) ]

class Pic:


    def __init__(self, fname=None, pal=None):
        self.pal = None
        self.pic = []
        self.width = 0
        self.height = 0
        self.mode = 11
        if fname is not None:
            self.read_file(fname)
        if pal is not None:
            self.pal = pal

    def pal_from_data(self, data, addDefaultPal = False):
        pStart, pEnd = unpack('BB', data[0:2])
        pos = 2
        #print('Pal', pStart, pEnd, pEnd-pStart+1, len(data))
        out = [None]*256
        if addDefaultPal:
            for i, c in enumerate(default_pal[:16]):
                out[i] = c
        for i in range(pStart, pEnd+1):
            r, g, b = unpack('BBB', data[pos: pos+3])
            out[i] = (r*4, g*4, b*4)
            pos += 3
        print('Pal read', pStart, '-', pEnd)
        self.pal = out

    def pic_from_data(self, data):
        self.width, self.height, self.mode = unpack('HHB', data[0:5])
        rle_data = lzw.decompress(data[5:], self.mode)
        data = rle.decode(rle_data)
        self.pic = []
        for y in range(0, self.height):
            self.pic.append(data[y*self.width:y*self.width + self.width])
        print('Pic read', self.width, 'x', self.height, '(', self.mode, ')', len(self.pic))

    def read_file(self, fname, palOnly = False, addDefaultPal = False):
        data = open(fname, 'rb').read()
        dataLen = len(data)
        pos = 0
        while pos < dataLen:
            tag, segLen = unpack('HH', data[pos:pos+4])
            pos += 4
            #print(hex(tag), segLen)
            if tag == 0x304D:
                print('Pal read', pos, segLen)
                self.pal_from_data(data[pos:pos+segLen], addDefaultPal)
                if palOnly:
                    break
            elif tag == 0x3058 and not palOnly:
                print('Pic read', pos, segLen)
                self.pic_from_data(data[pos:pos+segLen])
            else: print('Unknown!')
            pos += segLen
        if self.pal is None and addDefaultPal:
            self.pal = default_pal[:16] + [None] * 240

    def pal_to_file(self, fh):
        pal = self.pal
        p_start = 0
        pal = self.pal
        while p_start < len(pal) and pal[p_start] is None:
            p_start += 1
        p_end = 255
        while p_end > 0 and pal[p_end] is None:
            p_end -= 1

        data = [p_start, p_end]
        for i in range(p_start, p_end+1):
            c = pal[i]
            data += [c[0]/4, c[1]/4, c[2]/4]
        hdr_data = pack('HH', 0x304D, len(data))
        fh.write(hdr_data)
        fh.write(bytearray(data))

    def pic_to_file(self, fh):
        pic = self.pic
        data = pack("HHB", len(pic[0]), len(pic), 11)

        pic_data = []
        for ln in pic:
            pic_data += ln
        pic_data = rle.encode(pic_data)
        pic_data = lzw.compress(pic_data)
        pic_data = bytearray(pic_data)

        hdr_data = pack('HH', 0x3058, len(data) + len(pic_data))
        fh.write(hdr_data)
        fh.write(data)
        fh.write(pic_data)

    def write_file(self, fname):
        fh = open(fname, 'wb')
        if self.pal is not None:
            self.pal_to_file(fh)
        if self.pic != []:
            self.pic_to_file(fh)
        fh.close()

    def render_image(self, ext_pal=None):
        pic = self.pic
        pal = self.pal if ext_pal is None else ext_pal
        s = pygame.Surface((len(pic[0]), len(pic)), pygame.SRCALPHA, 32)
        #s = s.convert_alpha()
        for y, ln in enumerate(pic):
            for x, ci in enumerate(ln):
                c = pal[ci]
                if ci > 0 and c != None:
                    s.fill(c, (x,y, 1, 1))
        return s

    def save_image(self, outfname, palExt = None):
        img = self.render_image(ext_pal = palExt)
        pygame.image.save(img, outfname)


# main ------------
if __name__ == '__main__':
    import sys
    import os

    fname = sys.argv[1]
    ddir = sys.argv[2]
    # opt. file to pallete read from
    pname = None
    if len(sys.argv) == 4:
        pname = sys.argv[3]

    dname = ddir + '/' + os.path.basename(fname) + '.png'
    pic = Pic(fname)

    print(fname, end=' ')
    if pic.pic:
        print('pic', pic.width, 'x', pic.height, end=' ')
    #print pic[0][0]
    if pic.pal:
        print('pal', len(pic.pal), end=' ')
    '''
    print()
    print()

    writeFile('pokus.pic', pal, pic)

    print()
    print()

    pal, pic = readFile('pokus.pic')
    img = renderImage(pal, pic)
    pygame.image.save(img, 'pokus.pic.png')
    '''

    if pname:
        #pic = Pic()
        pic.read_file(pname, palOnly=True)

    if not pic.pal:
        pic.pal = default_pal
    
    if pic:
        img = pic.render_image()
        pygame.image.save(img, dname)
    else:
        print('!!!')

