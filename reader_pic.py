from utils import bread, sread
from struct import pack, unpack
import pygame

import rle, lzw

# Decoding was entirely based on Joel "Quadko" McIntyre PIC reading code
# Now replaced by code based on darkpandaman's JCivED PIC codecs


defaultPal = [ (0,0,0), (0,0,127), (0,127,0), (0,127,127), (127,0,0), (127,0,127), (127,127,0), (192,192,192), (127,127,127), (0,0,255), (0,255,0), (0,255,255), (255,0,0), (255,0,255), (255,255,0), (255,255,255), (0,0,0), (20,20,20), (32,32,32), (44,44,44), (56,56,56), (68,68,68), (80,80,80), (96,96,96), (112,112,112), (128,128,128), (144,144,144), (160,160,160), (180,180,180), (200,200,200), (224,224,224), (252,252,252), (0,0,252), (64,0,252), (124,0,252), (188,0,252), (252,0,252), (252,0,188), (252,0,124), (252,0,64), (252,0,0), (252,64,0), (252,124,0), (252,188,0), (252,252,0), (188,252,0), (124,252,0), (64,252,0), (0,252,0), (0,252,64), (0,252,124), (0,252,188), (0,252,252), (0,188,252), (0,124,252), (0,64,252), (124,124,252), (156,124,252), (188,124,252), (220,124,252), (252,124,252), (252,124,220), (252,124,188), (252,124,156), (252,124,124), (252,156,124), (252,188,124), (252,220,124), (252,252,124), (220,252,124), (188,252,124), (156,252,124), (124,252,124), (124,252,156), (124,252,188), (124,252,220), (124,252,252), (124,220,252), (124,188,252), (124,156,252), (180,180,252), (196,180,252), (216,180,252), (232,180,252), (252,180,252), (252,180,232), (252,180,216), (252,180,196), (252,180,180), (252,196,180), (252,216,180), (252,232,180), (252,252,180), (232,252,180), (216,252,180), (196,252,180), (180,252,180), (180,252,196), (180,252,216), (180,252,232), (180,252,252), (180,232,252), (180,216,252), (180,196,252), (0,0,112), (28,0,112), (56,0,112), (84,0,112), (112,0,112), (112,0,84), (112,0,56), (112,0,28), (112,0,0), (112,28,0), (112,56,0), (112,84,0), (112,112,0), (84,112,0), (56,112,0), (28,112,0), (0,112,0), (0,112,28), (0,112,56), (0,112,84), (0,112,112), (0,84,112), (0,56,112), (0,28,112), (56,56,112), (68,56,112), (84,56,112), (96,56,112), (112,56,112), (112,56,96), (112,56,84), (112,56,68), (112,56,56), (112,68,56), (112,84,56), (112,96,56), (112,112,56), (96,112,56), (84,112,56), (68,112,56), (56,112,56), (56,112,68), (56,112,84), (56,112,96), (56,112,112), (56,96,112), (56,84,112), (56,68,112), (80,80,112), (88,80,112), (96,80,112), (104,80,112), (112,80,112), (112,80,104), (112,80,96), (112,80,88), (112,80,80), (112,88,80), (112,96,80), (112,104,80), (112,112,80), (104,112,80), (96,112,80), (88,112,80), (80,112,80), (80,112,88), (80,112,96), (80,112,104), (80,112,112), (80,104,112), (80,96,112), (80,88,112), (0,0,64), (16,0,64), (32,0,64), (48,0,64), (64,0,64), (64,0,48), (64,0,32), (64,0,16), (64,0,0), (64,16,0), (64,32,0), (64,48,0), (64,64,0), (48,64,0), (32,64,0), (16,64,0), (0,64,0), (0,64,16), (0,64,32), (0,64,48), (0,64,64), (0,48,64), (0,32,64), (0,16,64), (32,32,64), (40,32,64), (48,32,64), (56,32,64), (64,32,64), (64,32,56), (64,32,48), (64,32,40), (64,32,32), (64,40,32), (64,48,32), (64,56,32), (64,64,32), (56,64,32), (48,64,32), (40,64,32), (32,64,32), (32,64,40), (32,64,48), (32,64,56), (32,64,64), (32,56,64), (32,48,64), (32,40,64), (44,44,64), (48,44,64), (52,44,64), (60,44,64), (64,44,64), (64,44,60), (64,44,52), (64,44,48), (64,44,44), (64,48,44), (64,52,44), (64,60,44), (64,64,44), (60,64,44), (52,64,44), (48,64,44), (44,64,44), (44,64,48), (44,64,52), (44,64,60), (44,64,64), (44,60,64), (44,52,64), (44,48,64), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0) ]

# palette for alchemy symbols (COPY*)
#defaultPal[141] = (254, 168, 95)
#defaultPal[142] = (202, 140, 83)
#defaultPal[143] = (153, 91, 32)


def readPal(data, addDefaultPal = False):
    pStart, pEnd = unpack('BB', data[0:2])
    pos = 2
    #print 'Pal', pStart, pEnd, pEnd-pStart+1, len(data)
    out = [None]*256
    if addDefaultPal:
        for i, c in enumerate(defaultPal[:16]):
            out[i] = c
    for i in xrange(pStart, pEnd+1):
        r, g, b = unpack('BBB', data[pos: pos+3])
        out[i] = (r*4, g*4, b*4)
        pos += 3
    print 'Pal', pStart, '-', pEnd
    return out


def readPic(data):
    width, height, mode = unpack('HHB', data[0:5])
    rle_data = lzw.decompress(map(ord, data[5:]), mode)
    data = rle.decode(rle_data)
    picData = []
    for y in xrange(0, height):
        picData.append(data[y*width:y*width + width])
    print 'Pic', width, 'x', height, '(', mode, ')'
    return picData


def readFile(fname, palOnly = False, addDefaultPal = False):
    pal = None
    pic = None

    data = open(fname).read()
    dataLen = len(data)
    #print fname, dataLen
    pos = 0
    while pos < dataLen:
        tag, segLen = unpack('HH', data[pos:pos+4])
        pos += 4
        #print hex(tag), segLen
        if tag == 0x304D:
            print 'Pal read', pos, segLen
            pal = readPal(data[pos:pos+segLen], addDefaultPal)
            if palOnly:
                break
        elif tag == 0x3058 and not palOnly:
            print 'Pic read', pos, segLen
            pic = readPic(data[pos:pos+segLen])
        else: print 'Unknown!'
        pos += segLen
    if pal is None and addDefaultPal:
        pal = defaultPal[:16] + [None] * 240
    return pal, pic





def writePal(fh, pal):
    p_start = 0
    while p_start < len(pal) and pal[p_start] is None:
        p_start += 1
    p_end = 255
    while p_end > 0 and pal[p_end] is None:
        p_end -= 1

    data = [p_start, p_end]
    for i in xrange(p_start, p_end+1):
        c = pal[i]
        data += [c[0]/4, c[1]/4, c[2]/4]
    hdr_data = pack('HH', 0x304D, len(data))
    fh.write(hdr_data)
    fh.write(bytearray(data))

def writePic(fh, pic):
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


def writeFile(fname, pal, pic):
    fh = open(fname, 'wb')
    if pal is not None:
        writePal(fh, pal)
    if pic is not None:
        writePic(fh, pic)
    fh.close()


def renderImage(pal, pic):
    s = pygame.Surface((len(pic[0]), len(pic)), pygame.SRCALPHA, 32)
    #s = s.convert_alpha()
    for y, ln in enumerate(pic):
        for x, ci in enumerate(ln):
            c = pal[ci]
            if ci > 0 and c != None:
                s.fill(c, (x,y, 1, 1))
    return s


def getImage(fname, palExt = None):
    pal, pic = readFile(fname)
    if palExt: pal = palExt
    return renderImage(pal, pic)


def convertImage(infname, outfname, palExt = None):
    img = getImage(infname, palExt = None)
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
    pal, pic = readFile(fname)

    print fname,
    if pic:
        print 'pic', len(pic[0]), len(pic),
    #print pic[0][0]
    if pal:
        print 'pal', len(pal), #pal
    '''
    print
    print

    writeFile('pokus.pic', pal, pic)

    print
    print

    pal, pic = readFile('pokus.pic')
    img = renderImage(pal, pic)
    pygame.image.save(img, 'pokus.pic.png')
    '''

    if pname:
        pal, _ = readFile(pname, palOnly=True)

    if not pal:
        pal = defaultPal
    
    if pic:
        img = renderImage(pal, pic)
        pygame.image.save(img, dname)
    else:
        print '!!!'

