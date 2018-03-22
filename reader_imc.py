from utils import bread
import reader_drle

def readData(fname, frameCnt=72): # 16 for DY files
    data = reader_drle.readData(fname)
    fileSize = len(data)

    pos = 82 if frameCnt>16 else 62 # eh...

    dataSize = bread(data[pos:pos+2]) ; pos += 2
    imgOffs = []
    for i in xrange(0, frameCnt):
        imgOffs.append(bread(data[pos:pos+2])) ; pos += 2

    #print fileSize, dataSize, imgOffs

    imgs = []
    dataStart = pos
    for offs in imgOffs:
        pos = dataStart + offs*16
        w = data[pos] ; pos += 1
        h = data[pos] ; pos += 1
        img = []
        for y in xrange(0, h):
            pc = data[pos] ; pos += 1
            ws = data[pos] ; pos += 1
            ln = [0]*w
            for x in xrange(ws, ws+pc):
                ln[x] = data[pos] ; pos += 1
            img.append(ln)
        imgs.append(img)

    return imgs


def extractToFile(inPath, outPath):
    data = readData(inPath)
    fh = open(outPath, "wb")
    for b in data: fh.write(chr(b))
    fh.close()


# main ------------
if __name__ == '__main__':
    import sys

    filePath = sys.argv[1] # file to read
    data = readData(filePath)
    print len(data)
    '''
    import time
    for img in data:
        for ln in img:
            out = ''
            for b in ln:
                out += 'X' if b else '.'
            print out
        time.sleep(0.01)
        print
    '''
    s = set()
    imgW = 0
    imgH = 0
    for i, img in enumerate(data):
        imgW += len(img[0]) + 1
        imgH = max(imgH, len(img))
        for ln in img:
            for b in ln:
                s.add(b)
                if i==4: print b,
            if i==4: print
    print s

    pal = [None]*255
    pal[5] = (0,0,0)
    pal[7] = (0xaa, 0xaa, 0xaa)
    pal[15] = (0xff, 0xff, 0xff)
    pal[138] = (0xff, 0xa2, 0x65)
    pal[141] = (0xff, 0xa2, 0x65) # ruce dole
    pal[236] = (0x38, 0x38, 0x38)
    pal[237] = (0xe7, 0x82, 0x3f)
    pal[238] = (0xff, 0xa2, 0x65)
    pal[239] = (0x05, 0x00, 0x72)
    pal[240] = (0x86, 0x00, 0x00)
    pal[241] = (0xa2, 0x00, 0x00)
    pal[242] = (0xb6, 0x00, 0x00)
    pal[235] = (0xe7, 0x82, 0x3f) # ruce
    pal[142] = (0xff, 0xa2, 0x65)
    pal[120] = (0xff, 0xa2, 0x65)

    import pygame
    s = pygame.Surface((imgW, imgH), pygame.SRCALPHA, 32)
    xoff = 0
    for img in data:
        for y, ln in enumerate(img):
            for x, b in enumerate(ln):
                if pal[b] != None:
                    s.fill(pal[b], (xoff+x,y, 1, 1))
        xoff += len(img[0]) + 1 

    pygame.image.save(s, filePath+".png")


    '''
    human walk animation files there are 72 sprites, which means 9 frames per direction
    wksw:
    82: W - velikost zbytku dat!!
    84: W+x? W W W ... 18x
    82:16256
    84:0 269 537 771 - start dat framu (rozmery) 228+X*16
    15 285 549 784  
    30 298 561 797  
    46 315 574 811  
    60 329 587 823  
    75 346 602 837  
    90 363 616 850  
    105 378 629 863  
    120 393 642 875  
    135 407 654 888  
    150 421 666 900  
    165 436 679 914  
    180 450 692 927  
    195 466 706 943  
    210 480 721 958  
    225 495 734 973  
    240 509 747 989  
    255 524 759 1002

    228:13 28 - rozmery framu? (B)

    dy:
    62: W - velikost zbytku
    64: W+x W W W ... 4x
    62:3136
    64:0 66:46 68:96 70:146
    72:13 74:60 76:109 78:159
    80:26 82:73 84:122 86:173
    88:36 90:85 92:134 94:184

    96:19 26 B - rozmery?
    '''        
    
