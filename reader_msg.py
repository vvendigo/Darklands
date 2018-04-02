from collections import OrderedDict

choiceTypes = {0x15:'STD', 0x10:'PTN', 0x16:'SNT', 0x06:'BTL'}

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
        elif o == 29:
            pass # (end of bullet?)
        else:
            out += '['+choiceTypes.get(o, str(o))+']'
    return out

def parseCard(txt):
    out = [];
    curData = ''
    curState = 'text'
    for ch in txt:
        o = ord(ch)
        if o >= 30 and o < 127: # char
            curData += ch
        elif ch == '\n' or o == 20: # end of block
            if curData:
                if curState=='text':
                    out.append(curData)
                else:
                    out[-1].append(curData)
                curData = ''
            curState = 'text'
        elif o == 29: # end of bullet
            out[-1].append(curData)
            curData = ''
        elif o in choiceTypes:
            curState = 'choice'
            out.append([choiceTypes[o]])
        else:
            print '!!! %d'%o
    if curData:
        if curState=='text':
            out.append(curData)
        else:
            out[-1].append(curData)
    return out


def readData(fname):
    data = open(fname).read()
    dataLen = len(data)

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
        c['elements'] = parseCard(data[pos:pos2])
        pos = pos2 + 1
        cards.append(c)
    return cards


def printCard(c):
    for e in c:
        if type(e) == str:
            print e
        elif len(e)==3:
            print "%s %s%s"%(e[0], e[1], e[2])


# main ------------
if __name__ == '__main__':
    from utils import itemStr, itemLn
    import sys

    fname = sys.argv[1]
    cards = readData(fname)

    for i, c in enumerate(cards):
        print '#', i
        #print c['unknown1'], c['unknown2']
        #print '%3d'%i, itemLn(c, ('unknown1', 'unknown2'))#('textOffsY', 'textOffsX', 'unknown1', 'textWidth', 'unknown2'))

        #print itemStr(c)

        print c['text']
        print '--------'
        printCard(c['elements'])
        print

