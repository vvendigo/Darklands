from collections import OrderedDict
from utils import bread, sread

cityTypes = ('Free City', 'Ruled City', 'Capital')

def readData(dlPath):
    fname = dlPath + '/darkland.cty'

    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    cnt = data[pos]
    #print cnt, bread(data[pos:pos+1])
    pos += 1

    cities = []

    for i in xrange(0, cnt):
        c = OrderedDict()

        c['short_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['name'] = sread(data[pos:pos+32]) ; pos += 32
        #city_data = (size 0x2e)
        dataPos = pos

        c['city_size'] = bread(data[pos:pos+2]) ; pos += 2
        #Size of the city. Ranges from 3 (small) to 8 (Koln).

        c['entry_coords'] =(bread(data[pos:pos+2]), bread(data[pos+2:pos+4])) ; pos += 4
        # City location on the map. 
        c['exit_coords'] = (bread(data[pos:pos+2]), bread(data[pos+2:pos+4])) ; pos += 4
        # Party coordinates when leaving a city.
        # When you leave a city, you don't exit at the same point as you entered. The exit coordinates were (usually) selected so as not to place you in an untenable position (the ocean, trapped by a river loop, etc).

        dests = []
        for i in xrange(0,4):
            tgt = bread(data[pos:pos+2])
            pos += 2
            if tgt != 0xffff:
                dests.append(tgt)
        c['dock_destinations'] = dests
        # Dock destination cities.
        # This contains the indices (in the cities array) of the destinations available via the city docks the docks.
        # 0xffff is used for "no destination". Inland cities have all 0xffffs.

        c['coast'] = bread(data[pos:pos+2]) ; pos += 2
        #if coastal, side of the river ???[Hamburg] TODO.
        #    Values are: 0xffff (inland), 0 (north of the river), 1 (south of the river)
        #    0 and 1 cities are on or near tidal zones (swamps), and may be subject to flooding.
        c['unknown_cd_1'] = bread(data[pos:pos+2]) ; pos += 2
        # [constant: 4]

        c['pseudo_ordinal'] = bread(data[pos:pos+2]) ; pos += 2
        # At first glance, this looks like an ordinal offset running from 0 to 0x5b, but 0x18 is missing, and 0x3c repeats.
        # This value is probably not used.

        c['city_type'] = bread(data[pos:pos+2]) ; pos += 2
        # Type of city
        c['unknown_cd_2'] = bread(data[pos:pos+2]) ; pos += 2
        #    0, 1, 2, or 3.
        c['unknown_cd_3'] = bread(data[pos:pos+2]) ; pos += 2
        # [constant: 0]

        #city_contents = bread(data[pos:pos+2])# bitmask[16 bits]
        city_contents = (data[pos] << 8) | data[pos+1]# bitmask[16 bits]
        pos += 2
        #Buildings and locations in the city.
        #    Bits are on iff there is one of that type of building.
        opts = ('has_kloster', 'has_slums', 'has_unknown1', 'has_cathedral', 'has_unknown2', 'has_no_fortress',
                'has_town_hall', 'has_polit', 'has_constant1', 'has_constant2', 'has_constant3', 'has_constant4',
                'has_docks', 'has_unknown3', 'has_pawnshop', 'has_university')
        for i, o in enumerate(opts):
            c[o] = 1 if city_contents & (1 << (15-i)) else 0
        c['bin_city_contents'] = bin(city_contents)
        c['unknown_cd_4'] = bread(data[pos:pos+2]) ; pos += 2
        # [constant: 0]

        c['qual_black'] = data[pos] ; pos += 1
        #Quality of the blacksmith.
        #    This, and the other nine qualities, all seem to work in the same way.
        #    A zero value indicates that the city does not have that particular shop.
        #    Non-zero values do not exactly equal the quality of the items available, but merely indicate relative qualities! For example, Nurnberg has a 0x31 (49) listed for the armory, but offers q37 (0x25) armor. However, if one city has a higher value than another, then that city's items will be of equal or greater quality.
        #    The quality of the healer is not stored here, but is apparently random. (TODO: verify?)
        #    TODO: comments about Quality of the alchemist, university, pharmacist being the seed thing.
        c['qual_merch'] = data[pos] ; pos += 1
        #Quality of the merchant. 
        c['qual_sword'] = data[pos] ; pos += 1
        #Quality of the swordsmith. 
        c['qual_armor'] = data[pos] ; pos += 1
        #Quality of the armorer. 
        c['qual_unk1'] = data[pos] ; pos += 1
        c['qual_bow'] = data[pos] ; pos += 1
        #Quality of the bowyer. 
        c['qual_tink'] = data[pos] ; pos += 1
        #Quality of the tinker. 
        c['qual_unk2'] = data[pos] ; pos += 1
        c['qual_cloth'] = data[pos] ; pos += 1
        # Quality of the clothing merchant. 
        c['qual_unk3'] = data[pos] ; pos += 1
        # [constant: 0]
        c['unknown_cd_5'] = data[pos] ; pos += 1
        # unknown byte
        # Since the following byte is 0 or 1, this and that might actually be a single word value.
        c['unknown_cd_6'] = data[pos] ; pos += 1
        # unknown byte
        # Either zero or one (only a couple of ones).
        c['unknown_cd_5-6'] = bread(data[pos-2:pos]) # word

        c['leader_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['ruler_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['unknown'] = sread(data[pos:pos+32]) ; pos += 32
        #TODO: is this non-empty ever? (ditto for other two unknowns)
        c['polit_name'] = sread(data[pos:pos+32]) ; pos += 32
        #Name of the political center or town square.
        #TODO: describe what empty values look like
        c['town_hall_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['fortress_name'] = sread(data[pos:pos+32]) ; pos += 32
        #Name of the city fortress or castle.
        c['cathedral_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['church_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['market_name'] = sread(data[pos:pos+32]) ; pos += 32
        #Name of the marketplace.
        c['unknown2'] = sread(data[pos:pos+32]) ; pos += 32
        #Often contains "Munzenplatz". Possibly this is "central square name".
        c['slum_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['unknown3'] = sread(data[pos:pos+32]) ; pos += 32
        #Many places have "Zeughaus", which translates to "armoury"; others end in "-turm" (tower?) or "-tor" (gate?). Quite possible this is for one of the unused "rebellion" codepath.
        c['pawnshop_name'] = sread(data[pos:pos+32]) ; pos += 32
        #Name of the pawnshop.
        #All pawnshops are named the same; this is either 'Leifhaus' or is empty.
        c['kloster_name'] = sread(data[pos:pos+32]) ; pos += 32
        #Name of the kloster (church law and administration building).
        c['inn_name'] = sread(data[pos:pos+32]) ; pos += 32
        c['university_name'] = sread(data[pos:pos+32]) ; pos += 32
        cities.append(c)

    # read descriptions + generate some attrs
    fname = dlPath + '/darkland.dsc'
    data = map(ord, open(fname).read())
    pos = 1
    for c in cities:
        c['description'] = sread(data[pos:pos+80])
        pos += 80

        c['str_dock_destinations'] = ', '.join([cities[d]['short_name'] for d in c['dock_destinations']])
        c['str_city_type'] = cityTypes[c['city_type']]

    return cities


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    cities = readData(dlPath)

    # print data
    for i, c in enumerate(cities):
        print '#', i, '#'
        print itemStr(c)

