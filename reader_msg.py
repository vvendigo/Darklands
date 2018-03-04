import sys


fname = sys.argv[1]

data = open(fname).read()
dataLen = len(data)


def vis(txt):
    out = '';
    for ch in txt:
        o = ord(ch)
        if ch >= ' ' and o < 127:
            out += ch
        elif ch == '\n':
            out += '<'+hex(ord(ch))+'>\n'
        else:
            out += '['+hex(ord(ch))+']'
    return out

pos = 0

while pos < dataLen:
    pos2 = data.find('\0', pos)
    if pos2 < 0: pos2 = dataLen
    print vis(data[pos:pos2])
    print '<0x00>'
    pos = pos2 + 1
