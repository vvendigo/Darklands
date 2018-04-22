from utils import sread, bread
from collections import OrderedDict

def readData(dlPath):
    fname = dlPath + '/darkland.enm'
    data = map(ord, open(fname).read())
    dataLen = len(data)

    enemyTypes = []
    pos = 0
    for i in xrange(0, 71):
        et = OrderedDict()
        et['image_group'] = sread(data[pos:pos+4]) ; pos += 4
        et['name'] = sread(data[pos:pos+10]) ; pos += 10
        et['num_variants'] = data[pos] ; pos += 1
        et['pal_cnt'] = data[pos] ; pos += 1 # number of palettes in enemypal?
        et['unknown2'] = data[pos] ; pos += 1
        et['pal_start'] = data[pos] ; pos += 1 # palettes starting index in enemypal
        et['unknown4'] = bread(data[pos:pos+2]) ; pos += 2
        attrs = {}
        for attr in ('end','str','agl','per','int','chr','df'):
            attrs[attr] = data[pos] ; pos += 1
        et['attrs'] = attrs
        skills = {}
        for s in ('wEdg','wImp','wFll','wPol','wThr','wBow','wMsl','alch','relg','virt','spkC','spkL','r_w','heal','artf','stlh','strW','ride','wdWs'):
            skills[s] = data[pos] ; pos += 1
        et['skills'] = skills
        et['unknown5'] = data[pos] ; pos += 1
        pos += 1 # const 0
        et['unknown6'] = data[pos] ; pos += 1 # underground related?

        et['unknown7'] = data[pos] ; pos += 1
        et['unknown8'] = data[pos:pos+0x42] ; pos += 0x42
        et['unknown9'] = data[pos:pos+0x1e] ; pos += 0x1e
        et['unknown10'] = data[pos:pos+2] ; pos += 2
        et['vital_arm_type'] = data[pos] ; pos += 1
        et['limb_arm_typetype'] = data[pos] ; pos += 1

        et['armor_q'] = data[pos] ; pos += 1
        et['unknown11'] = data[pos] ; pos += 1
        et['shield_type'] = data[pos] ; pos += 1
        et['shield_q'] = data[pos] ; pos += 1
        et['unknown12'] = data[pos:pos+6] ; pos += 6
        et['unknown13'] = data[pos:pos+6] ; pos += 6
        et['weapon_types'] = data[pos:pos+6] ; pos += 6
        et['weapon_q'] = data[pos] ; pos += 1
        et['unknown14'] = data[pos:pos+11] ; pos += 11
        et['unknown15'] = data[pos:pos+20] ; pos += 20
        enemyTypes.append(et)

    enemies = []
    for i in xrange(0, 82):
        e = OrderedDict()
        e['type'] = bread(data[pos:pos+2]) ; pos += 2
        e['type_str'] = enemyTypes[e['type']]['name']
        e['name'] = sread(data[pos:pos+12]) ; pos += 12
        pos += 8 # all 0
        e['unknown'] = bread(data[pos:pos+2]) ; pos += 2
        e['unknown_bin'] = bin(e['unknown'])
        enemies.append(e)

    return enemyTypes, enemies


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    eTypes, enemies = readData(dlPath)

    for i, et in enumerate(eTypes):
        print '%2d: %s'%(i, itemStr(et))#,('name','unknown10')))

    print
    for i, et in enumerate(enemies):
        print i
        print itemStr(et)

