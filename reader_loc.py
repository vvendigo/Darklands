from collections import OrderedDict
from utils import bread, sread

locTypes = (
'city',
'castle', # (lord or evil lord variety)
'castle', # (Raubritter variety)
'monastery',
'Teufelstein', #(looks like tomb or pagan altar) TODO: Teufelstein is one
'cave', # (TODO: what kind?)
'mines',
'7',
'village',
'ruins of a village',
'village2', # (more square than 0x08, and unused?)
'11',
'12',
'tomb',
'14',
'dragon\'s lair', # (invisible; cannot interact?)
'spring',
'lake',
'shrine',
'cave', # (TODO: what kind?)
'pagan altar',
'witch sabbat',
'Templar castle', # (has a black top)
'Hockkonig (the Baphomet castle)', # all gray)
'alpine cave',
'lady of the lake (magician/astrologer)',
'ruins of a Raubritter\'s castle')

def readData(dlPath):
    fname = dlPath + '/darkland.loc'

    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    cnt = bread(data[pos:pos+2])
    #print cnt, bread(data[pos:pos+1])
    pos += 2

    locs = []

    for i in xrange(0, cnt):
        c = OrderedDict()

        c['icon'] = bread(data[pos:pos+2]) ; pos += 2 # (enum location_icon)
        #Map image for the location. Note that this basically corresponds to the 'type' of location.
        #print c['icon']
        c['str_loc_type'] = locTypes[c['icon']] if c['icon'] < len(locTypes) else str(c['icon'])
        c['unknown1'] = bread(data[pos:pos+2]) ; pos += 2
        #c['unknown1_bin'] = bin(c['unknown1'])
        #0 for cities, other locations range from 0x08-0x0e.
        c['coords'] =(bread(data[pos:pos+2]), bread(data[pos+2:pos+4])) ; pos += 4
        #Map coordinates. 
        c['unknown2'] = bread(data[pos:pos+2]) ; pos += 2
        #Ranges from 1-10.
        #Seems to be 4 or 9 for live Raubritters (1 for dead); perhaps it's a strength?
        c['unknown3'] = bread(data[pos:pos+2]) ; pos += 2
        #Most range from 1-5, except pagan altars, which are 0x63 (99).
        c['menu'] = bread(data[pos:pos+2]) ; pos += 2
        #Card displayed on entering the location.
        c['unknown4'] = bread(data[pos:pos+2]) ; pos += 2
        #Always 0x62 except for castles currently occupied by Raubritters (icon=2); those are 0x92.
        c['unknown5'] = data[pos] ; pos += 1
        c['city_size'] = data[pos] ; pos += 1
        #Size of the city.
        #Cities range from 3 (small) to 8 (Koln); non-cities are always 1.
        c['local_rep'] = bread(data[pos:pos+2]) ; pos += 2
        #Local reputation.
        #In this file, this is always zero. The copy of this structure that lives in the saved game files gets non-zero values.
        #Ranges from -150 to 150 (although others claim to have observed numbers outside this range).
        c['unknown6'] = data[pos] ; pos += 1
        #Zero seems to indicate an "active" site.
        #Ruins of a Raubritter castle get 0x04, as do destroyed villages.
        #Some other locations get 0x20 or 0x24.
        c['unknown7_c'] = bread(data[pos:pos+3]) 
        pos += 3
        # [constant: { 0x19, 0x19, 0x19 }]
        c['inn_cache_idx'] = bread(data[pos:pos+2]) ; pos += 2
        #In this file, this is always 0xffff (-1).
        #In a saved game file, if the party stores items at an inn (in a city), this value becomes an index into cache_offsets (found in dksaveXX.sav).
        c['unknown8_c'] = bread(data[pos:pos+2]) ; pos += 2
        #[constant: 0x0000]
        c['unknown9'] = bread(data[pos:pos+2]) ; pos += 2
        #All are zero except for Nurnberg, which is 0xc0.
        c['unknown10_c'] = bread(data[pos:pos+8]) ; pos += 8
        # [constant: all 0x00]
        c['name'] = sread(data[pos:pos+20]) ; pos += 20
        locs.append(c)

    return locs


def infoStr(c):
    out = ''
    for k, v in c.iteritems():
        out += "%s: "%k
        if type(v) == dict:
            out += '{\n'
            for vk, vv in v.iteritems():
                out += "- %s: %s\n"%(vk, vv)
            out += '}'
        else:
            out += str(v)
        out += '\n'
    return out


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    locs = readData(dlPath)

    # print data
    for i, c in enumerate(locs):
        print '#', i, '#'
        print itemStr(c)

