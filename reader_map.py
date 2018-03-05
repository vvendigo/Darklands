from utils import rbread, bread

def readData(dlPath):
    fname = dlPath + '/darkland.map'

    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    max_x_size = rbread(data[pos:pos+2]) ; pos += 2
    # This word is stored high-byte first
    max_y_size = rbread(data[pos:pos+2]) ; pos += 2
    # This word is stored high-byte first

    #print max_x_size, max_y_size
    row_offsets = [0]*max_y_size
    for i in xrange(0, max_y_size):
        # typo in Wallace's doc - it's double word, not word
        row_offsets[i] = bread(data[pos:pos+4])
        pos += 4
    m = []
    for i in xrange(0, max_y_size):
        line = [None]*max_x_size
        pos = row_offsets[i]
        #print i, pos, row_offsets[i+1] if i+1 < len(row_offsets) else dataLen
        x = 0
        while x < max_x_size:
            b = data[pos]
            pos += 1
            cnt = b >> 5
            pal = (b >> 4) & 0x1
            row = b & 0xf
            #print ' ', pos+x, x, cnt, pal, row
            for c in xrange(0, cnt):
                line[x] = (pal, row)
                x += 1
        m.append(line)

    adjTiles = ((0,),(1,2,3,25),(1,2,3,25,27),(1,2,3,25,27),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,),(12,),(13,),(14,),(15,),
                (16,),(17,),(18,),(19,),(20,),(21,),(22,),(23,),(24,25,27,29),(25,1,2,3),(26,25),(27,2,3),(),(29,),(),(),)

    # get cols
    for y in xrange(0, max_y_size):
        xc = 0 if y%2 else -1
        for x in xrange(0, max_x_size):
            pal, row = m[y][x]
            # differs from Wallace - bits set just by adjanced _same_row_ tiles
            tv = pal*16+row
            col = 0
            
            if y > 0:
                if xc+x>0 and xc+x<max_x_size: col += 1 if m[y-1][xc+x][0]*16+m[y-1][xc+x][1] in adjTiles[tv] else 0
                else: col += 1
                if xc+x+1<max_x_size: col += 2 if m[y-1][xc+x+1][0]*16+m[y-1][xc+x+1][1] in adjTiles[tv] else 0
                else: col += 2
            else:
                col += 1 + 2
            if y+1 < max_y_size:
                if xc+x>0 and xc+x<max_x_size: col += 4 if m[y+1][xc+x][0]*16+m[y+1][xc+x][1] in adjTiles[tv] else 0
                else: col += 4
                if xc+x+1<max_x_size: col += 8 if m[y+1][xc+x+1][0]*16+m[y+1][xc+x+1][1] in adjTiles[tv] else 0
                else: col += 8
            else:
                col += 4 + 8
            m[y][x] = (pal, row, col)

    return m

# main ------------
if __name__ == '__main__':
    import sys

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    m = readData(dlPath)

    print len(m[0]), len(m)

    tiles = [' WWWwsppffttTTTT', 'HHhhMMAA/~~%Cc++']
    tiles = [' ....sppffttTTTT', 'HHhhMMAA/~~%Cc++']
    '''
    for ln in m[37:40]:
        for pal, row, col in ln[75:78]:
            print pal, bin(row), '',
        print
    '''
    for ln in m:
        print ''.join([tiles[pal][row] for pal, row, col in ln])
            
