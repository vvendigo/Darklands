from utils import bread
import reader_drle

def readData(fname, frameCnt=None):
    data = reader_drle.readData(fname)
    fileSize = len(data)

    # heuristic
    pos = 60
    frameCnt = bread(data[pos:pos+2]) ; pos += 2
    dataSize = bread(data[pos:pos+2]) ; pos += 2
    #print fileSize, dataSize, frameCnt, fileSize - 80 - 4 - 8 * 2 * frameCnt
    if dataSize != fileSize - pos - 8 * 2 * frameCnt:
        pos = 80
        frameCnt = bread(data[pos:pos+2]) ; pos += 2
        dataSize = bread(data[pos:pos+2]) ; pos += 2
            
    imgOffs = []
    for i in xrange(0, frameCnt*8):
        imgOffs.append(bread(data[pos:pos+2])) ; pos += 2
    imgs = []
    dataStart = pos
    for offs in imgOffs:
        pos = dataStart + offs*16
        w = data[pos] ; pos += 1
        h = data[pos] ; pos += 1
        img = []
        for y in xrange(0, h):
            pc = data[pos] ; pos += 1 # pixel count
            ws = data[pos] ; pos += 1 # empty space cnt
            ln = [0]*w
            for x in xrange(ws, ws+pc):
                if i==52: print data[pos],
                if pos < fileSize and x < w:
                    ln[x] = data[pos] ; pos += 1
                else:
                    #print w,'x',h,' ', x,y
                    #break
                    pass
            if i==52: print
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
    palIdx = int(sys.argv[2]) if len(sys.argv)>2 else 0
    outDir = sys.argv[3] if len(sys.argv)>3 else None
    data = readData(filePath)
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
    dbgI = -1
    for i, img in enumerate(data):
        imgW += len(img[0]) + 1 if len(img) else 0
        imgH = max(imgH, len(img))
        for ln in img:
            for b in ln:
                s.add(b)
                if i==dbgI: print "%3d"%b,
            if i==dbgI: print
    if dbgI >= 0:
        #print s
        print [x for x in s if x<64 or x>80]
    pal = {
        0: None,
        5: (0,0,0),
        6: (0xaa,0x55,0x00), # wood
        7: (0xaa, 0xaa, 0xaa), # steel
        8: (0x55,0x55,0x55), # gray (belt)
        15: (0xff, 0xff, 0xff), # blade
        120: (0xff, 0xa2, 0x65), # skin?
        122: (0xf3,0x96,0x5d), # skin
        123: (0xc3,0xc3,0xc3), # steel
        124: (0xb2,0xb2,0xb2), # gray (jevelry?)
        #125: (0,255,0), 
        138: (0, 0xff, 0),
        141: (0xff, 0xa2, 0x65), # arm low
        142: (0xd3, 0x82, 0x51),
    }
    #e00cba2 [0, 5, 6, 7, 8, 15, 123, 142
    '''
    pal[122] = (0x76, 0x00, 0x00)
    pal[138] = (0x00, 0x55, 0x96) # saty ?
    pal[141] = (0xff, 0xa2, 0x65) # ruce dole
    pal[236] = (0x00, 0x3e, 0x6e) # saty tmava
    pal[237] = (0x00, 0x55, 0x96) # saty ?
    pal[238] = (0x00, 0x55, 0x96) # saty ?
    pal[239] = (0x00, 0x55, 0x96) # saty
    pal[240] = (0x86, 0x00, 0x00) # vlasy
    pal[241] = (0xa2, 0x00, 0x00) # vlasy
    pal[242] = (0xb6, 0x00, 0x00) # vlasy
    pal[235] = (0xe7, 0x82, 0x3f) # ruce
    pal[142] = (0xd3, 0x82, 0x51)
    pal[120] = (0xff, 0xa2, 0x65)
    pal = [None]
    pal += [(r/5*5,r/5*5,r/5*5) for r in xrange(0,256)]
    '''
    p = filePath.rfind('/')
    imgGrp = filePath[:3] if p < 0 else filePath[p+1:p+4]
    print '!!!', imgGrp
    import reader_enm
    edef = {}
    for e in reader_enm.readData('DL')[0]:
        #print e
        if e['image_group'] == imgGrp:
            edef = e
            break
    if palIdx > edef['pal_cnt']:
        palIdx = 0
    import reader_enemypal
    epals = reader_enemypal.readData('DL')
    pal.update(epals[edef['pal_start']+palIdx])
    import pygame
    if not outDir:
        s = pygame.Surface((imgW, imgH), pygame.SRCALPHA, 32)
        xoff = 0
        for img in data:
            if not img:
                continue
            for y, ln in enumerate(img):
                for x, b in enumerate(ln):
                    c = pal.get(b, (255,0,0))
                    if c != None:
                        s.fill(c, (xoff+x,y, 1, 1))
            xoff += len(img[0]) + 1 
        pygame.image.save(s, filePath+".png")
    else:
        for i in xrange(0, len(data), 8):
            for j in xrange(0,8):
                img = data[i+j]
                s = pygame.Surface((len(img[0]), len(img)), pygame.SRCALPHA, 32)
                for y, ln in enumerate(img):
                    for x, b in enumerate(ln):
                        c = pal.get(b, (255,0,0))
                        if c != None:
                            s.fill(c, (x,y, 1, 1))
                pygame.image.save(s, outDir+"/%d-%02d.png"%(j,i))

