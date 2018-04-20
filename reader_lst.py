from collections import OrderedDict
from utils import bread, sread


def readData(dlPath):
    fname = dlPath + '/darkland.lst'

    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    itemCnt, saintCnt, formCnt = data[0], data[1], data[2]
    pos = 3

    items = []

    for i in xrange(0, itemCnt):
        c = OrderedDict()
        c['name'] = sread(data[pos:pos+20]) ; pos += 20
        c['short_name'] = sread(data[pos:pos+10]) ; pos += 10
        c['type'] = bread(data[pos:pos+2]) ; pos += 2
        flags = (('is_edged','is_impact','is_polearm','is_flail','is_thrown','is_bow','is_metal_armor','is_shield'),
                ('is_unknown1','is_unknown2','is_component','is_potion','is_relic','is_horse','is_quest_1','is_const0_1'),
                ('is_lockpicks','is_light','is_arrow','is_const0_2','is_quarrel','is_ball','is_const0_3','is_quest_2'),
                ('is_throw_potion','is_const0_4','is_nonmetal_armor','is_missile_weapon','is_unknown3','is_music','is_const0_6','is_const0_7'),
                ('is_unknown4','is_unknown5','is_const0_8','is_const0_9','is_const0_10','is_const0_11','is_const0_12','is_unknown6'))
        for f in flags:
            bits = data[pos] ; pos += 1
            for b,n in enumerate(f):
                c[n] = True if bits & (1 << b) else False
        c['weight'] = data[pos] ; pos += 1
        c['quality'] = data[pos] ; pos += 1
        c['rarity'] = data[pos] ; pos += 1 # missing in Merle's doc!
        c['unknown1'] = bread(data[pos:pos+2]) ; pos += 2
        #Non-zero only for relics.
        #Ranges from 0x06 (St. Edward's Ring) to 0x50 (St. Gabriel's Horn).
        c['unknown2'] = bread(data[pos:pos+2]) ; pos += 2
        #Non-zero only for relics, and for the "residency permit" (which is unused by the game).
        #Ranges from 0x05 to 0x27 (residency permit).
        c['value'] = bread(data[pos:pos+2]) ; pos += 2
        items.append(c)

    saints = []
    for i in xrange(0, saintCnt):
        s = ''
        while data[pos]:
            s += chr(data[pos])
            pos += 1
        pos += 1
        saints.append({'name':s})

    for i in xrange(0, saintCnt):
        s = ''
        while data[pos]:
            s += chr(data[pos])
            pos += 1
        pos += 1
        saints[i]['short_name'] = s

    formulae = []
    for i in xrange(0, formCnt):
        s = ''
        while data[pos]:
            s += chr(data[pos])
            pos += 1
        pos += 1
        formulae.append({'name':s})

    for i in xrange(0, formCnt):
        s = ''
        while data[pos]:
            s += chr(data[pos])
            pos += 1
        pos += 1
        formulae[i]['short_name'] = s

    # read saints descriptions
    fname = dlPath + '/darkland.snt'
    data = map(ord, open(fname).read())
    pos = 1
    for i in xrange(0, len(saints)):
        saints[i]['description'] = sread(data[pos:pos+0x168])
        pos += 0x168

    return items, saints, formulae



# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr, itemLn

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    items, saints, forms  = readData(dlPath)

    # print data
    '''
    for i, c in enumerate(items):
        print '%3d %s'%(i, itemLn(c, (('name',15),'is_unknown1','is_unknown2','is_unknown3', 'is_const0_6','is_const0_7','is_unknown4','is_unknown5','is_unknown6')))
    print

    '''
    for i, c in enumerate(items):
        print '#', i, '#'
        print itemStr(c)

    print

    for i, c in enumerate(saints):
        print '#', i, '#'
        print itemStr(c)

    print

    for i, c in enumerate(forms):
        print '#', i, '#'
        print itemStr(c)

