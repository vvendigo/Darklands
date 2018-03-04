import sys
import os
from common import bread, sread

fname = sys.argv[1]
ddir = sys.argv[2]

dname = ddir + '/' + os.path.basename(fname)

os.mkdir(dname)

data = map(ord, open(fname).read())
dataLen = len(data)
print fname, dataLen, 'B'
pos = 0

cnt = (data[pos+1] << 8) | data[pos]
print cnt, bread(data[pos:pos+2])
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

    fh = open(dname+'/'+fn, "wb")
    fh.write(bytearray(data[dataOffs:dataOffs+dataLen]))
    fh.close()
