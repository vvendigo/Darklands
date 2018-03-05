import sys
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
                ('unknown_f1','unknown_f2','is_component','is_potion','is_relic','is_horse','is_quest_1','const0'),
                ('is_lockpicks','is_light','is_arrow','const0_2','is_quarrel','is_ball','const0_3','is_quest_2'),
                ('is_throw_potion','const0_4','is_nonmetal_armor','is_missile_weapon','const0_5','unknown_f3','is_music','const0_6'),
                ('is_unknown_2','unknown_f4','const0_7','const0_8','const0_9','const0_10','const0_11','is_unknown_3'))
        for f in flags:
            bits = data[pos] ; pos += 1
            for b,n in enumerate(f):
                c[n] = True if bits & (1 << b) else False
        c['weight'] = data[pos] ; pos += 1
        c['quality'] = data[pos] ; pos += 1
        c['rarity?'] = data[pos] ; pos += 1 # missing in Merle's doc!
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

    return items, saints, formulae


def infoStr(c, attrs=None):
    out = ''
    for k, v in c.iteritems():
        if attrs and k not in attrs:
            continue
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

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    items, saints, forms  = readData(dlPath)

    # print data
#    for i, c in enumerate(items):
#        print "%3d %20s %d %d %d"%(i, c['name'], c['rarity?'], c['unknown1'], c['unknown2'])



    # print data
    for i, c in enumerate(items):
        print '#', i, '#'
        print infoStr(c, ('name','is_impact','unknown_f4','const0_5'))
'''
    print

    for i, c in enumerate(saints):
        print '#', i, '#'
        print infoStr(c)

    print

    for i, c in enumerate(forms):
        print '#', i, '#'
        print infoStr(c)
'''
