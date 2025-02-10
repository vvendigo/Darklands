import os
from struct import unpack
from datetime import datetime

from utils import cstrim, tchars


class Event:
    whom = ["Merchant", "#1", "#2", "#3",
            "Foreign Trader", "Pharmacist", "Medici",
            "Hanseatic League", "Fugger", "Schulz", "Mayor",
            "#11"]

    def __init__(self):
        self.hide = False
        self.create_date = None
        self.expire_date = None
        self.verb = None
        self.item_i = None
        self.who_i = None
        self.who = None
        self.location_i = None
        self.location_ambiguous = False
        self.location_back_i = None
        self.data = None

    def from_data(self, data):
        self.data = data
        pos = 10
        h, d, m, y = unpack('HHHH', data[pos:pos+8]) ; pos += 8
        try:
            self.create_date = datetime(y, m+1, d, h)
        except:
            pass
        hh, dd, mm, yy = unpack('HHHH', data[pos:pos+8]) ; pos += 8
        # pos == 26
        self.who_i = unpack('h', data[26:26+2])[0]
        self.who = self.whom[self.who_i] if self.who_i >= 0 else None
        self.location_i = unpack('h', data[28:28+2])[0]
        self.location_back_i = unpack('h', data[30:30+2])[0]
        self.location_ambiguous = self.location_i > 91 # non-cities
        unknown_0 = unpack('h', data[32:32+2])[0]
        _event_state = unpack('h', data[34:34+2])[0]
        unknown_1 = unpack('h', data[36:36+2])[0]
        unknown_2 = unpack('h', data[38:38+2])[0]
        _event_type = unpack('h', data[40:40+2])[0]
        unknown_3 = unpack('h', data[42:42+2])[0]
        unknown_4 = unpack('h', data[44:44+2])[0]
        self.item_i = unpack('h', data[46:46+2])[0]

        if self.who_i < 0 or yy == y:
            self.hide = True
            #return
        #if (_event_state == 7 or unknown_3 == 0 or unknown_4 != 2) and self.item_i == 0:
        #    self.hide = True
        #    #return
        if self.item_i: # item quest
            if yy == 1499:
                self.verb = 'get'
            else:
                self.verb = 'return'
        else: # raubritter
            self.verb = 'raubritter'
        if yy <= 1498:
            self.expire_date = datetime(yy, mm+1, dd, hh)
        if self.verb == 'raubritter' and _event_state == 0x24:
            self.verb = 'raubritter_return'

    def dbg(self):
        for v in range(0, len(self.data), 2):
            print('%05d'%unpack('h', self.data[v:v+2])[0], end=' ')
        print()

    def __str__(self):
        out = '%s - %19s '%(self.create_date, self.expire_date)
        if self.hide:
            out += '####: '
        if self.verb == 'get':
            out += 'Get %d at %s%d and take it to %s at %d'%(self.item_i, '??' if self.location_ambiguous else '', self.location_i, self.who, self.location_back_i)
        elif self.verb == 'return':
            out += 'Return %d to %s at %d'%(self.item_i, self.who, self.location_back_i)
        elif self.verb == 'raubritter':
            out += 'Kill raubritter at %s%d and report to %s at %d'%('??' if self.location_ambiguous else '', self.location_i, self.who, self.location_back_i)
        elif self.verb == 'raubritter_return':
            out += 'Get reward from %s at %d'%(self.who, self.location_i)
        return out


class Save:
    def __init__(self):
        self.curr_location_name = ''
        self.save_game_label = ''
        self.curr_date = None
        self.curr_location = None
        self.curr_coords = None

        self.num_characters = 0
        self.num_events = 0
        self.events = []

    def from_data(self, data):
        pos = 0
        self.curr_location_name = cstrim(unpack('12s', data[pos:pos+12])[0]) ; pos += 12
        pos += 9
        self.save_game_label = cstrim(unpack('23s', data[pos:pos+23])[0]) ; pos += 23
        pos += 18
        pos += 37 #!! not 55
        pos += 1
        pos += 2 # city_contents_seed
        pos += 2
        y, m, d, h = unpack('HHHH', data[pos:pos+8]) ; pos += 8 #!! not reversed
        self.curr_date = datetime(y, m+1, d, h)
        pos += 6 # party_money
        pos += 4
        pos += 2 # reputation
        self.curr_location = unpack('h', data[pos:pos+2])[0] ; pos += 2
        self.curr_coords = unpack('HH', data[pos:pos+4]) ; pos += 4
        pos += 2 # curr_menu
        pos += 6
        pos += 2 # prev_menu
        pos += 2 # bank_notes
        pos += 4
        pos += 2 # philosopher_stone
        pos += 7
        pos += 5 # party_order_indices #!! 5*B not str
        pos += 1
        pos += 1 # party_leader_index
        pos += 3
        pos += 74
        pos += 2 # num_curr_characters
        self.num_characters = unpack('H', data[pos:pos+2])[0] ; pos += 2
        pos += 10 # party_char_indices
        pos += 20 # party_images
        pos += 120 # party_colors
        pos += self.num_characters * 554 # characters data
        self.num_events = unpack('H', data[pos:pos+2])[0] ; pos += 2
        # events
        for i in range(0, self.num_events):
            e = Event()
            e.from_data(data[pos:pos+48]) ; pos += 48
            self.events.append(e)
        #num_locations: word
        #locations: array[ num_locations ] of struct location
        #max_cache_slot: byte
        # num_caches: byte
        # cache_offsets: array[ 0x62 ] of word
        # caches: array[ num_caches ] of struct cache

    def __str__(self):
        return '%s %s %d/%s %s %devs'%(self.save_game_label, self.curr_date, self.curr_location, self.curr_location_name, self.curr_coords, self.num_events)


def read_file(fname):
    save = Save()
    save.from_data(open(fname, 'rb').read())
    return save

# main ------------
if __name__ == '__main__':
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else 'DL/SAVES/DKSAVE0.SAV'

    save = read_file(path)
    print(save)
    for i, event in enumerate(save.events):
        #if not event.hide:
        print("%03d   %s"%(i, event))
        event.dbg()

