import os
from struct import unpack

class Char:
    def __init__(self, width, lines=None):
        self.width = width
        self.lines = [] if lines is None else lines


class Font:

    def __init__(self, start_chr=0, end_chr=0, height=0, chars=None, bw=0):
        self.start_chr = start_chr
        self.end_chr = end_chr
        self.height = height
        self.chars = [] if chars is None else chars
        self.bw = bw # for lulz

    def read_data(self, data, offset):
        self.chars = []
        hdrpos = offset - 8
        self.start_char, self.end_char, self.bw = unpack('BBB', data[hdrpos:hdrpos+3]) # first char ASCII code
        #self.end_char = data[hdrpos+1] # last char ASCII code
        #self.bw = data[hdrpos+2] # char img width in bytes
        # 0 unknown
        self.height, = unpack('B', data[hdrpos+4]) # height in bytes
        # 1 unknown
        # 1 unknown
        # 0 unknown
        char_cnt = self.end_char - self.start_char + 1
        width_off = offset - char_cnt - 8
        for i, ch_width in enumerate(unpack('B'*char_cnt, data[width_off:width_off+char_cnt])):
            char = Char(ch_width)
            for j in xrange(0, self.height):
                x = 0
                ln_data = [0]*ch_width
                for k in range(0, self.bw):
                    B_pos = offset + (j * char_cnt + i) * self.bw + k
                    ln_B, = unpack('B', data[B_pos:B_pos+1])
                    for bc in xrange(0, 8):
                        if x >= ch_width: break
                        ln_data[x] = 1 if ln_B & 0x80 else 0
                        x += 1
                        ln_B <<= 1
                char.lines.append(ln_data)
            self.chars.append(char)


def read_fonts(fname):
    data = open(fname).read()
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    cnt = unpack('H', data[pos:pos+2])[0] ; pos += 2

    fonts = []
    for offs in unpack('H' * cnt, data[pos:pos + 2 * cnt]):
        font = Font()
        font.read_data(data, offs)
        fonts.append(font)
    return fonts


def readData(dlPath):
    fonts = {}
    for ext in ('fnt', 'utl'):
        fname = os.path.join(dlPath, 'fonts.') + ext
        fonts[ext] = read_fonts(fname)
    return fonts


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    fonts = readData(dlPath)

    for ext, fnts in fonts.iteritems():
        print '------', ext
        for i, fnt in enumerate(fnts):
            print "-----", i, 'h:', fnt.height, fnt.start_char, '-', fnt.end_char, len(fnt.chars), 'bw', fnt.bw
            chC = fnt.start_char
            for ch in fnt.chars:
                print 'ch: %d, w: %d'%(chC, ch.width)
                chC += 1
                for r in ch.lines:
                    print ''.join([('.','#')[b] for b in r])
                print
            print

