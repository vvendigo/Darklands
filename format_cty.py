import os
from struct import unpack
from utils import cstrim, tchars

city_types = ('Free City', 'Ruled City', 'Capital')

class City:
    def __init__(self):
        self.short_name = ''
        self.name = ''
        self.city_size = None
        self.entry_coords = None
        self.exit_coords = None
        self.dock_destinations = []
        self.coast = None
        self.unknown_cd_1 = None
        self.pseudo_ordinal = None
        self.city_type = None
        self.unknown_cd_2 = None
        self.unknown_cd_3 = None
        self.city_contents = {}
        self.unknown_cd_4 = None

        self.qual_blacksmith = None
        self.qual_merchant = None
        self.qual_swordsmith = None
        self.qual_armorer = None
        self.qual_unk1 = None
        self.qual_bowyer = None
        self.qual_tinker = None
        self.qual_unk2 = None
        self.qual_clothing = None
        self.qual_unk3 = None
        self.unknown_cd_5 = None
        self.unknown_cd_6 = None
        self.unknown_cd_5_6 = None

        self.leader_name = None
        self.ruler_name = None
        self.unknown = None
        self.center_name = None
        self.town_hall_name = None
        self.fortress_name = None
        self.cathedral_name = None
        self.church_name = None
        self.market_name = None
        self.unknown2 = None
        self.slum_name = None
        self.unknown3 = None
        self.pawnshop_name = None
        self.kloster_name = None
        self.inn_name = None
        self.university_name = None

        self.str_dock_destinations = []
        self.str_city_type = ''

    def from_data(self, data):
        pos = 0
        self.short_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #city_data = (size 0x2e)
        self.city_size, = unpack('H', data[pos:pos+2]) ; pos += 2
        #Size of the city. Ranges from 3 (small) to 8 (Koln).
        self.entry_coords = unpack('HH', data[pos:pos+4]) ; pos += 4
        # City location on the map. 
        self.exit_coords = unpack('HH', data[pos:pos+4]) ; pos += 4
        # Party coordinates when leaving a city.
        # When you leave a city, you don't exit at the same point as you entered. The exit coordinates were (usually) selected so as not to place you in an untenable position (the ocean, trapped by a river loop, etc).

        dests = []
        for i in xrange(0,4):
            tgt, = unpack('H', data[pos:pos+2])
            pos += 2
            if tgt != 0xffff:
                dests.append(tgt)
        self.dock_destinations = dests
        # Dock destination cities.
        # This contains the indices (in the cities array) of the destinations available via the city docks the docks.
        # 0xffff is used for "no destination". Inland cities have all 0xffffs.

        self.coast, = unpack('H', data[pos:pos+2]) ; pos += 2
        #if coastal, side of the river ???[Hamburg] TODO.
        #    Values are: 0xffff (inland), 0 (north of the river), 1 (south of the river)
        #    0 and 1 cities are on or near tidal zones (swamps), and may be subject to flooding.
        self.unknown_cd_1, = unpack('H', data[pos:pos+2]) ; pos += 2
        # [constant: 4]

        self.pseudo_ordinal, = unpack('H', data[pos:pos+2]) ; pos += 2
        # At first glance, this looks like an ordinal offset running from 0 to 0x5b, but 0x18 is missing, and 0x3c repeats.
        # This value is probably not used.

        self.city_type, = unpack('H', data[pos:pos+2]) ; pos += 2
        # Type of city
        self.unknown_cd_2, = unpack('H', data[pos:pos+2]) ; pos += 2
        #    0, 1, 2, or 3.
        self.unknown_cd_3, = unpack('H', data[pos:pos+2]) ; pos += 2
        # [constant: 0]

        #city_contents = unpack('H', data[pos:pos+2])# bitmask[16 bits]
        city_contents = (ord(data[pos]) << 8) | ord(data[pos+1])# bitmask[16 bits]
        pos += 2
        #Buildings and locations in the city.
        #    Bits are on iff there is one of that type of building.
        opts = ('has_kloster', 'has_slums', 'has_unknown1', 'has_cathedral', 'has_unknown2', 'has_no_fortress',
                'has_town_hall', 'has_polit', 'has_constant1', 'has_constant2', 'has_constant3', 'has_constant4',
                'has_docks', 'has_unknown3', 'has_pawnshop', 'has_university')
        buildings = {}
        for i, o in enumerate(opts):
            buildings[o] = 1 if city_contents & (1 << (15-i)) else 0
        self.city_contents = buildings
        self.bin_city_contents = bin(city_contents)
        self.unknown_cd_4, = unpack('H', data[pos:pos+2]) ; pos += 2
        # [constant: 0]

        self.qual_blacksmith, = unpack('B', data[pos]) ; pos += 1
        #Quality of the blacksmith.
        #    This, and the other nine qualities, all seem to work in the same way.
        #    A zero value indicates that the city does not have that particular shop.
        #    Non-zero values do not exactly equal the quality of the items available, but merely indicate relative qualities! For example, Nurnberg has a 0x31 (49) listed for the armory, but offers q37 (0x25) armor. However, if one city has a higher value than another, then that city's items will be of equal or greater quality.
        #    The quality of the healer is not stored here, but is apparently random. (TODO: verify?)
        #    TODO: comments about Quality of the alchemist, university, pharmacist being the seed thing.
        self.qual_merchant, = unpack('B', data[pos]) ; pos += 1
        #Quality of the merchant. 
        self.qual_swordsmith, = unpack('B', data[pos]) ; pos += 1
        #Quality of the swordsmith. 
        self.qual_armorer, = unpack('B', data[pos]) ; pos += 1
        #Quality of the armorer. 
        self.qual_unk1, = unpack('B', data[pos]) ; pos += 1
        self.qual_bowyer, = unpack('B', data[pos]) ; pos += 1
        #Quality of the bowyer. 
        self.qual_tinker, = unpack('B', data[pos]) ; pos += 1
        #Quality of the tinker. 
        self.qual_unk2, = unpack('B', data[pos]) ; pos += 1
        self.qual_clothing, = unpack('B', data[pos]) ; pos += 1
        # Quality of the clothing merchant. 
        self.qual_unk3, = unpack('B', data[pos]) ; pos += 1
        # [constant: 0]
        self.unknown_cd_5, = unpack('B', data[pos]) ; pos += 1
        # unknown byte
        # Since the following byte is 0 or 1, this and that might actually be a single word value.
        self.unknown_cd_6, = unpack('B', data[pos]) ; pos += 1
        # unknown byte
        # Either zero or one (only a couple of ones).
        self.unknown_cd_5_6, = unpack('H', data[pos-2:pos]) # word

        self.leader_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.ruler_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.unknown = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #TODO: is this non-empty ever? (ditto for other two unknowns)
        self.center_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Name of the political center or town square.
        #TODO: describe what empty values look like
        self.town_hall_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.fortress_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Name of the city fortress or castle.
        self.cathedral_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.church_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.market_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Name of the marketplace.
        self.unknown2 = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Often contains "Munzenplatz". Possibly this is "central square name".
        self.slum_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.unknown3 = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Many places have "Zeughaus", which translates to "armoury"; others end in "-turm" (tower?) or "-tor" (gate?). Quite possible this is for one of the unused "rebellion" codepath.
        self.pawnshop_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Name of the pawnshop.
        #All pawnshops are named the same; this is either 'Leifhaus' or is empty.
        self.kloster_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        #Name of the kloster (church law and administration building).
        self.inn_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32
        self.university_name = cstrim(unpack('32s', data[pos:pos+32])[0]) ; pos += 32

    def __str__(self):
        return '%s%s: %s'%(tchars(self.name), ('/'+tchars(self.short_name)) if self.name != self.short_name else '', str(self.entry_coords))


def read_file(fname):
    data = open(fname).read()

    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0
    cnt = unpack('B', data[pos])[0]
    pos += 1

    cities = []
    for i in xrange(0, cnt):
        #print 'Cty', i
        c = City()
        c.from_data(data[pos:pos+622])
        cities.append(c)
        pos += 622

    # postprocess
    # generate some attrs
    for c in cities:
        c.str_dock_destinations = ', '.join([cities[d].short_name for d in c.dock_destinations])
        c.str_city_type = city_types[c.city_type]

    return cities


def readData(dlPath='DL'):
    return read_file(os.path.join(dlPath, 'darkland.cty'))



# main ------------
if __name__ == '__main__':
    import sys

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    cities = readData(dlPath)

    # print data
    for i, c in enumerate(cities):
        print '#', i, '#'
        print c
        #print vars(c)
        #print 'str_dock_destinations:', c.str_dock_destinations
