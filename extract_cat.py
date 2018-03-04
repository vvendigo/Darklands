import sys
from utils import bread, sread

# catalog filename
fname = sys.argv[1]
# output dir
ddir = sys.argv[2]

data = map(ord, open(fname).read())
dataLen = len(data)
print fname, dataLen, 'B'
pos = 0

cnt = bread(data[pos:pos+2])
print cnt
pos += 2

for i in xrange(0, cnt):
    fn = sread(data[pos:pos+12])
    pos += 12
    # dword TS
    pos += 4
    dataLen = bread(data[pos:pos+4])
    pos += 4
    dataOffs = bread(data[pos:pos+4])
    pos += 4
    print fn, dataOffs, dataLen

    fh = open(ddir+'/'+fn, "wb")
    fh.write(bytearray(data[dataOffs:dataOffs+dataLen]))
    fh.close()
