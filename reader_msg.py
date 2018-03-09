import sys
from collections import OrderedDict

fname = sys.argv[1]

data = open(fname).read()
dataLen = len(data)

specChars = {0x10:'POTION', 0x16:'SAINT', 0x06:'FIGHT'}

def vis(txt):
    out = '';
    for ch in txt:
        o = ord(ch)
        if ch >= ' ' and o < 127:
            out += ch
        elif ch == '\n':
            out += ch #'<\\n>'#\n'
        elif o == 20:
            out += '\n'
        else:
            out += '['+specChars.get(o, str(o))+']'
    return out

pos = 0
cardCnt = ord(data[pos]); pos += 1
#print cardCnt

cards = []

for i in xrange(0, cardCnt):
    c = OrderedDict()
    c['textOffsY'] = ord(data[pos]) ; pos += 1
    c['textOffsX'] = ord(data[pos]) ; pos += 1
    c['unknown1'] = ord(data[pos]) ; pos += 1
    c['textMaxX'] = ord(data[pos]) ; pos += 1
    c['unknown2'] = ord(data[pos]) ; pos += 1

    pos2 = data.find('\0', pos)
    if pos2 < 0: pos2 = dataLen
    c['text'] = vis(data[pos:pos2])
    pos = pos2 + 1
    cards.append(c)

from utils import itemStr, itemLn

for i, c in enumerate(cards):
    print '#', i
    #print c['unknown1'], c['unknown2']
    #print '%3d'%i, itemLn(c, ('unknown1', 'unknown2'))#('textOffsY', 'textOffsX', 'unknown1', 'textWidth', 'unknown2'))
    print itemStr(c)
    #print
