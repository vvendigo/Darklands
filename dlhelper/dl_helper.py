import os, sys, time
from argparse import ArgumentParser

app_name = 'Darklander\'s Little Helper'

if getattr(sys, 'frozen', False):
    app_path = sys.executable
elif __file__:
    app_path = __file__

aparser = ArgumentParser(prog=app_name, description='Darklands map viewer and quest lister.')
aparser.add_argument('path', nargs='?', default=os.path.dirname(app_path))
aparser.add_argument('-r', '--rename-saves', action='store_true', default=False)
args = aparser.parse_args()

dl_path = args.path
print('Using path', dl_path)
#'/home/wendigo/.steam/steam/steamapps/common/Darklands/DARKLAND'


from glob import glob
import math
from random import random, seed as srand

import pygame

import reader_map
import reader_loc
import reader_lst
import format_cty
from format_pic import Pic, default_pal
from format_fnt import read_fonts
import format_sav

pygame.init()
pygame.display.set_caption(app_name)
screen = pygame.display.set_mode((800,550), pygame.HWSURFACE|pygame.DOUBLEBUF)

print('Rading fonts...')
font_data = read_fonts(os.path.join(dl_path, 'FONTS.FNT'))[0]

class Font:
    def __init__(self, fdata, size, color):
        self.size = size
        self.imgs = []
        self.start_char = fdata.start_char
        self.height = fdata.height*size
        for char in fdata.chars:
            s = pygame.Surface((char.width*size, self.height), pygame.SRCALPHA)
            for y, ln in enumerate(char.lines):
                    for x, p in enumerate(ln):
                        if p:
                            pygame.draw.rect(s, color, (x*size, y*size, size, size))
            self.imgs.append(s)
    def str_width(self, s):
        slen = 0
        for ch in s:
            slen += self.size if slen else 0
            slen += self.imgs[ord(ch) - self.start_char].get_width()
        return slen
    def render(self, sf, x, y, s, bg=None):
        if bg:
            w = self.str_width(s)
            pygame.draw.rect(sf, bg, (x-self.size, y-1, w+2*self.size, self.height+2))
        for ch in s:
            img = self.imgs[ord(ch) - self.start_char]
            sf.blit(img, (x, y))
            x += img.get_width() + self.size

font1 = Font(font_data, 3, (0x70,0x7d,0x49))
font2 = Font(font_data, 3, (255,64,64))
font3 = Font(font_data, 3, (255,255,255))
font4 = Font(font_data, 3, (255,64,64))
font5 = Font(font_data, 2, (0x70,0x7d,0x49))
font6 = Font(font_data, 2, (255, 32, 32))

class Log:
    def __init__(self, x, y, font):
        self.sf = screen
        self.x = x
        self.y = y
        self.font = font
    def print(self, s):
        self.font.render(self.sf, self.x, self.y, s)
        self.y += self.font.height + self.font.size
        pygame.display.flip()

log = Log(2, 2, font1)

log.print('Welcome to ' + app_name+'!')

log.print('Reading images...')
def get_pic(fname, palname=None):
    pic = Pic(os.path.join(dl_path, 'PICS', fname+'.PIC'))
    if palname:
        pic.read_file(os.path.join(dl_path, 'PICS', palname+'.PIC'), palOnly=True)
    if not pic.pal:
        pic.pal = default_pal
    pic = pic.render_image()
    return pygame.transform.scale(pic, (pic.get_width()*scale, pic.get_height()*scale))
# 'RPHORIZ','RPVERT','ARMBRSH5','ARMBRSH13'
scale = 1.23
pygame.display.set_icon(get_pic('HANDICON'))
scale = 3
img_panel = get_pic('ARMBRSH5', 'ARMBACK')
img_scroll = get_pic('ARMBRS10', 'ARMBACK')


log.print('Reading map data...')
map_data = reader_map.readData(dl_path)
log.print('Reading cities...')
cities = format_cty.readData(dl_path)
log.print('Reading locs...')
locs = reader_loc.readData(dl_path)
log.print('Reading items, saints & formulae...')
items, saints, formulas  = reader_lst.readData(dl_path)

class Panel:
    def __init__(self, img, top, middle, bottom, left, center, right):
        self.img = img
        self.top = top
        self.middle = middle
        self.bottom = bottom
        self.left = left
        self.center = center
        self.right = right

    def render(self, sf, x, y, w, h):
        sf.blit(self.img, (x,y), (0,0,self.left, self.top))
        sf.blit(self.img, (x+w-self.right,y), (self.left+self.center,0,self.right, self.top))
        sf.blit(self.img, (x,y+h-self.bottom), (0,self.top+self.middle, self.left, self.bottom))
        sf.blit(self.img, (x+w-self.right,y+h-self.bottom), (self.left+self.center,self.top+self.middle,self.right, self.bottom))
        for ix in range(0, w-self.left-self.right, self.center):
            tw = self.center
            if ix + tw > w-self.left-self.right:
                tw -= (ix + tw) - (w-self.left-self.right)
            sf.blit(self.img, (x + self.left + ix, y), (self.left, 0, tw, self.top))
            sf.blit(self.img, (x + self.left + ix, y+h-self.bottom), (self.left, self.top+self.middle, tw, self.bottom))
            for iy in range(0, h-self.top-self.bottom, self.middle):
                th = self.middle
                if iy + th > h-self.top-self.bottom:
                    th -= (iy + th) - (h-self.top-self.bottom)
                sf.blit(self.img, (x + self.left + ix, y + self.top + iy), (self.left, self.top, tw, th))

                sf.blit(self.img, (x, y + self.top + iy), (0, self.top, self.left, th))
                sf.blit(self.img, (x + w - self.right, y + self.top + iy), (self.left+self.center, self.top, self.right, th))





p_panel = Panel(img_panel, 4*scale, (64-9)*scale, 4*scale, 5*scale, (115-10)*scale, 5*scale)
p_scroll = Panel(img_scroll, 10*scale, (55-24)*scale, 12*scale, 10*scale, (137-20)*scale, 10*scale)

class Widget:
    def __init__(self, sf, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sf = sf
        self.bak_clip = None
    def set_clip(self, *r):
        self.bak_clip = self.sf.get_clip()
        self.sf.set_clip(r)
    def del_clip(self):
        self.sf.set_clip(self.bak_clip)
        self.bak_clip = None
    def render(self, sf):
        pass
    def behave(self, event):
        pass

class Map(Widget):
    def __init__(self, sf, x, y, w, h):
        super().__init__(sf, x, y, w, h)
        self.drag = False
        self.active_loc = None
        self.party_pos = None
        self.target_coords = None
        self.target_coords_exact = True
        self.img_map = None
        self.locs = []
        self.zoom = None
        for i, loc in enumerate(locs):
            if loc['icon']:
                continue
            self.locs.append([i, loc['name'], loc['coords'], [(),(),()]])
        self.zooms = ([2, 1, 0.5, None],[4, 2, 1.5, None],[8,4,3, None]) #(tw, th, td) tile dimensions + tile y-dist for blit
        self.map_width, self.map_height = len(map_data[0]), len(map_data) # in tiles
        for z in range(0, len(self.zooms)):
            self.set_zoom(z)
            self.make_map()
        self.set_zoom(1)
        self.map_center_x = self.img_map.get_width() / 2
        self.map_center_y = self.img_map.get_height() / 2
    def img_coords(self, x, y):
        return x*self.tw + (self.tw/2 if y%2 else 0), y * self.dh
    def map_coords(self, x, y):
        my = y // self.dh
        return (x - (self.tw/2 if my%2 else 0)) // self.tw, my
    def set_zoom(self, zoom):
        if zoom == self.zoom or zoom < 0 or zoom >= len(self.zooms):
            return False
        self.zoom = zoom
        self.tw, self.th, self.dh, self.img_map = self.zooms[self.zoom]
        return True
    def make_map(self):
        '''
        1* none
        1* sea
        1* river big
        1* river small
        1* coast
        1* moor
        2* meadow?
        2* famr
        2* trees
        2* lt wood
        2* forest
        '''
        pal1 = [(0,0,0,0),
                (0,0,224),
                (0,0,255),
                (64,64,255),
                (64,0,255),
                (0x3a,0xa3,0x6a),
                (128,255,128),
                (128,255,128),
                (0xb1,0xeb,0x57),
                (0xb1,0xeb,0x57),
                (32,255,32),
                (32,255,32),
                (0,255,0),
                (0,255,0),
                (0,192,0),
                (0,192,0)]
        '''
        2* dense wood
        2* brown hills
        2* gray mountains
        2* snow mountains
        1* path
        2* water
        1* bridge
        2* city/building
        '''
        pal2 = [(0,128,0),
                (0,128,0),
                (0x70,0x7d,0x49),
                (0x70,0x7d,0x49),
                (128,128,128),
                (128,128,128),
                (255,255,255),
                (255,255,255),
                (128,128,0),
                (128,128,255),
                (128,128,255),
                (128,128,64),
                (96,96,96),
                (96,96,96)]
        pals = [pal1,pal2]

        img_map = pygame.Surface(((self.map_width+1)*self.tw, (self.map_height+2)*self.dh))
        img_map.fill((4, 154, 0))

        for y, ln in enumerate(map_data):
            for x, tile in enumerate(ln):
                mx, my = self.img_coords(x, y)
                pal, row, col = tile
                pygame.draw.rect(img_map, pals[pal][row], pygame.Rect(mx, my, self.tw, self.th))

        for i, loc in enumerate(locs):
            lt = loc['icon']
            if lt:
                continue
            c = cities[i]
            cs = 3 + c.city_size//2
            x, y = self.img_coords(*loc['coords'])
            pygame.draw.circle(img_map, (255,0,0), (x, y), cs)
            self.locs[i][3][self.zoom] = (x, y)

        routes = set()
        for i, c in enumerate(cities):
            for d in c.dock_destinations:
                routes.add((min(i, d), max(i, d)))

        for r1, r2 in routes:
            x1, y1 = self.img_coords(*locs[r1]['coords'])
            x2, y2 = self.img_coords(*locs[r2]['coords'])
            pygame.draw.line(img_map, (150,150,255), (x1, y1), (x2, y2), 2)

        self.zooms[self.zoom][3] = img_map
    def show_loc(self, i):
        self.active_loc = locs[i]
        self.map_center_x, self.map_center_y = self.img_coords(*locs[i]['coords'])
        self.render()
    def show_coords(self, coords):
        self.map_center_x, self.map_center_y = self.img_coords(*coords)
        self.render()
    def show_target(self, coords, exact = True):
        self.map_center_x, self.map_center_y = self.img_coords(*coords)
        self.target_coords = coords
        self.target_coords_exact = exact
        self.render()
    def check_active_loc(self, mmx, mmy):
        self.active_loc = None
        for loc in self.locs:
            dx = loc[3][self.zoom][0] - mmx
            dy = loc[3][self.zoom][1] - mmy
            if abs(dx) < 8 and abs(dy) < 8:
                self.active_loc = locs[loc[0]]
                return True
        return False
    def render(self):
        self.set_clip(self.x, self.y, self.w, self.h)
        p_panel.render(self.sf, self.x-scale, self.y, self.w+2*scale, self.h)
        self.del_clip()
        self.set_clip(self.x+3*scale, self.y+3*scale, self.w-6*scale, self.h-6*scale)
        mx = self.x - self.map_center_x + self.w / 2
        my = self.y - self.map_center_y + self.h / 2
        self.sf.blit(self.img_map, (mx, my))
        if self.party_pos:
            x, y = self.img_coords(*self.party_pos)
            pygame.draw.rect(self.sf, (255, 32, 32), (mx + x-scale*4, my + y-scale*4, scale*8, scale*8))
            pygame.draw.rect(self.sf, (255, 255, 255), (mx + x-scale*2, my + y-scale*2, scale*4, scale*4))
        if self.active_loc:
            loc = self.active_loc
            x, y = self.img_coords(*loc['coords'])
            font3.render(self.sf, mx + x, my + y - font3.height, loc['name'], bg=(0,0,0))
        if self.target_coords:
            x, y = self.img_coords(*self.target_coords)
            if self.target_coords_exact:
                pygame.draw.rect(self.sf, (255, 255, 255), (mx + x-scale*2, my + y-scale*2, scale*4, scale*4), scale)
            else:
                font3.render(self.sf, mx + x - scale, my + y - font3.height, '?', bg=(0,0,0))
        self.del_clip()
    def behave(self, event):
        if self.drag and event.type == pygame.MOUSEBUTTONUP:
            self.drag = False
        mx, my = pygame.mouse.get_pos()
        if mx<self.x or mx>=self.x+self.w or my<self.y or my>=self.y+self.h:
            return
        mmx = self.map_center_x+mx-self.x-self.w/2
        mmy = self.map_center_y+my-self.y-self.h/2
        updated = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drag = True
        if self.drag and event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel
            self.map_center_x -= dx
            self.map_center_y -= dy
            updated = True
        elif event.type == pygame.MOUSEMOTION:
            updated = self.check_active_loc(mmx, mmy)
        if event.type == pygame.MOUSEWHEEL:
            new_zoom = self.zoom + event.y
            m_x, m_y = self.map_coords(mmx, mmy)
            if self.set_zoom(new_zoom):
                self.map_center_x, self.map_center_y = self.img_coords(m_x, m_y)
                updated = True
        if updated:
            self.render()

log.print('Map init...')
map_window = Map(screen, 0, 0, 550, 550)


class Box(Widget):
    def __init__(self, sf, x, y, w, h):
        super().__init__(sf, x, y, w, h)
        self.mouse_in = False
    def on_click(self, btn):
        pass
    def on_in(self):
        pass
    def on_out(self):
        pass
    def behave(self, event):
        mx, my = pygame.mouse.get_pos()
        if mx<self.x or mx>=self.x+self.w or my<self.y or my>=self.y+self.h:
            if self.mouse_in:
                self.on_out()
                self.mouse_in = False
            return
        if not self.mouse_in:
            self.on_in()
            self.mouse_in = True
        #print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(event.button)

class Text(Widget):
    def __init__(self, sf, x, y, font, txt):
        w = font.str_width(txt)
        h = font.height
        self.font = font
        self.text = txt
        super().__init__(sf, x, y, w, h)
    def render(self):
        self.font.render(self.sf, self.x, self.y, self.text)

class Button(Box):
    def __init__(self, sf, x, y, font1, txt, font2 = None):
        w = font1.str_width(txt)
        h = font1.height
        self.font1 = font1
        self.font2 = font2
        self.font = self.font1
        self.text = txt
        super().__init__(sf, x, y, w, h)
    def on_in(self):
        if self.font2:
            self.font = self.font2
            self.render()
    def on_out(self):
        if self.font2:
            self.font = self.font1
            self.render()
    def render(self):
        self.font.render(self.sf, self.x, self.y, self.text)

class List(Widget):
    def __init__(self, sf, x, y, w, h, items):
        self.hidden = False
        self.items = []
        self.last_scroll_time = time.time()
        self.accell = 0
        self.list_start = y+10*scale
        self.list_end = y+h-10*scale
        super().__init__(sf, x, y, w, h)
        self.populate(items)
    def populate(self, items):
        self.items = items
        by = self.list_start
        for i in items:
            i.x = self.x+10*scale
            i.y = by
            by += i.h + 2*scale
    def hide(self):
        self.hidden = True
    def show(self):
        self.hidden = False
        self.render()
    def render(self):
        if self.hidden:
            return
        p_scroll.render(screen, self.x, self.y, self.w, self.h)
        self.set_clip(self.x+10*scale, self.y+10*scale, self.w-20*scale, self.h-20*scale)
        for i in self.items:
            i.render()
        self.del_clip()
    def _get_accel(self, d):
        td = time.time() - self.last_scroll_time
        self.last_scroll_time = time.time()
        if td > 0.1:
            self.accell = 5*scale
        else:
            self.accell += 3*scale
            self.accell *= 0.02/td
        return self.accell * d
    def behave(self, event):
        if self.hidden:
            return
        mx, my = pygame.mouse.get_pos()
        if mx<self.x or mx>=self.x+self.w or my<self.y or my>=self.y+self.h:
            return
        if event.type == pygame.MOUSEWHEEL and len(self.items):
            accel = self._get_accel(event.y)
            if self.items[-1].y+self.items[-1].h+accel < self.list_end:
                accel = -(self.items[-1].y + self.items[-1].h - self.list_end)
            if self.items[0].y+accel > self.list_start:
                accel = -(self.items[0].y - self.list_start)
            for i in self.items:
                i.y += accel
            self.render()
        if my<self.list_start or my>=self.list_end:
            return
        self.set_clip(self.x+10*scale, self.y+10*scale, self.w-20*scale, self.h-20*scale)
        for i in self.items:
            i.behave(event)
        self.del_clip()

class CityButton(Button):
    def __init__(self, sf, txt, city_i):
        self.city_i = city_i
        c = cities[city_i].city_contents
        self.has_txt = 'U' if 'has_university' in c else ''
        self.has_txt += 'C' if 'has_cathedral' in c else ''
        self.has_txt += 'K' if 'has_kloster' in c else ''
        super().__init__(sf, 0, 0, font1, txt, font2)
    def on_click(self, btn):
        if btn == 1:
            map_window.show_loc(self.city_i)

class CityList(List):
    def __init__(self, sf, x, y, w, h):
        btns = []
        for loc in sorted(map_window.locs, key=lambda _:_[1]):
            btns.append(CityButton(sf,loc[1], loc[0]))
        super().__init__(sf, x, y, w, h, btns)

list_cities = CityList(screen, 550, 13*scale, 250, 550-13*scale)

log.print('Loading saves...')
saves = []
active_save = None

def rename_saves(s_fnames):
    ''' takes list of *.SAV fnames sorted by mtime '''
    print('Renaming...')
    last_no = 10000
    for fname in s_fnames:
        _, name = os.path.split(fname)
        if name.startswith('DKSV'):
            no = int(name[4:8])
            if no < last_no:
                last_no = no
    for i in range(len(s_fnames)-1, -1, -1):
        if last_no <= 0:
            break
        fname = s_fnames[i]
        dr, name = os.path.split(fname)
        if not name.startswith('DKSAVE'):
            continue
        last_no -= 1
        new_name = 'DKSV%04d'%(last_no)
        print('Rename', name, '>', new_name+'.SAV')
        # DSV, update s_fnames
        bsv_fname = fname[:-3]+'BSV'
        has_bsv = os.path.isfile(bsv_fname)
        if not has_bsv: # check BSV existence
            time.sleep(2)
            has_bsv = os.path.isfile(bsv_fname)
        if not has_bsv:
            print('No BSV file?!')
            break # ??!!
        new_path = os.path.join(dr, new_name)
        if os.path.isfile(new_path + '.SAV'):
            # ignore colliding files
            continue
        s_fnames[i] = new_path + '.SAV'
        os.rename(fname, new_path + '.SAV')
        os.rename(bsv_fname, new_path + '.BSV')

def load_saves():
    global saves
    sfs = glob(os.path.join(dl_path, 'SAVES', 'DK*.SAV'))
    if len(sfs) == len(saves):
        return False
    sfs.sort(key=os.path.getmtime, reverse=True)
    if args.rename_saves:
        rename_saves(sfs)
    saves = []
    print('Loading saves')
    print(os.path.join(dl_path, 'SAVES'))
    for fname in sfs:
        save = format_sav.read_file(fname)
        print(save, fname[fname.rfind('/'):])
        saves.append(save)
    return True
load_saves()

def set_active_save(save):
    global active_save
    active_save = save
    if save.curr_location >= 0:
        map_window.party_pos = locs[save.curr_location]['coords']
    else:
        map_window.party_pos = save.curr_coords
    map_window.show_coords(map_window.party_pos)
    list_saves.render()
    list_quests.update()

def nearest_city_name(x, y):
    nearest_i = None
    nearest_d = None
    for i, l in enumerate(locs[0:91]):
        c = l['coords']
        d = abs(c[0]-x) + abs(c[1]-y)/2
        if nearest_d is None or d < nearest_d:
            nearest_d = d
            nearest_i = i
    return locs[nearest_i]['name']

class SaveButton(Button):
    def __init__(self, sf, save):
        self.save = save
        super().__init__(sf, 0, 0, font1, self.save.save_game_label, font2)
        self.h = font1.height + 2*font5.height
        self.w = 200
        self.clicked = False # for dbl click
    def on_click(self, btn):
        if btn == 1:
            set_active_save(self.save)
            self.clicked = True
    def on_out(self):
        self.clicked = False
        super().on_out()
    def render(self):
        if self.save == active_save:
            pygame.draw.rect(self.sf, (255, 255, 128), (self.x, self.y, self.w, self.h))
        self.font.render(self.sf, self.x, self.y, self.text)
        font5.render(self.sf, self.x, self.y+self.font.height, self.save.curr_location_name)
        font5.render(self.sf, self.x, self.y+self.font.height+font5.height, self.save.curr_date.strftime('%Y/%m/%d %H'))

class SaveList(List):
    def __init__(self, sf, x, y, w, h):
        super().__init__(sf, x, y, w, h, [])
        self.update()
    def update(self):
        btns = []
        for save in saves:
            btns.append(SaveButton(self.sf, save))
        self.populate(btns)
        self.render()

list_saves = SaveList(screen, 550, 13*scale, 250, 550-13*scale)


class QuestButton(Button):
    def __init__(self, sf, quest):
        super().__init__(sf, 0, 0, font5, '', font6)
        self.quest = quest
        self.w = 200
        self.text = []
        self.coords = None
        self.text.append(quest.create_date.strftime('* %Y/%m/%d'))
        if quest.verb == 'return':
            self.text.append('RETURN')
            self.text.append(items[quest.item_i]['name'])
            self.text.append('to ' + quest.who)
            self.text.append('at ' + locs[quest.location_i]['name'])
            self.coords = locs[quest.location_i]['coords']
        elif quest.verb == 'get':
            self.text.append('GET')
            self.text.append(items[quest.item_i]['name'])
            where = 'at ' + locs[quest.location_i]['name']
            if quest.location_ambiguous:
                where = 'near ' + nearest_city_name(*locs[quest.location_i]['coords'])
            self.text.append(where)
            self.text.append('to ' + quest.who)
            self.text.append('at ' + locs[quest.location_back_i]['name'])
            self.coords = locs[quest.location_i]['coords']
        elif quest.verb == 'raubritter':
            self.text.append('SORT OUT')
            self.text.append('raubritter')
            where = 'at ' + locs[quest.location_i]['name']
            if quest.location_ambiguous:
                where = 'near ' + nearest_city_name(*locs[quest.location_i]['coords'])
            self.text.append(where)
            self.text.append('and report')
            self.text.append('to ' + quest.who)
            self.text.append('at ' + locs[quest.location_back_i]['name'])
            self.coords = locs[quest.location_i]['coords']
        elif quest.verb == 'raubritter_return':
            self.text.append('ACCEPT REWARD')
            self.text.append('from ' + quest.who)
            self.text.append('at ' + locs[quest.location_i]['name'])
            self.coords = locs[quest.location_i]['coords']
        else:
            self.text.append('?')
        if quest.expire_date:
            self.text.append(quest.expire_date.strftime('till %Y/%m/%d'))
        self.h = len(self.text) * font5.height + 2*scale
    def render(self):
        y = self.y
        for t in self.text:
            self.font.render(self.sf, self.x, y, t)
            y += font5.height + 1
    def on_click(self, btn):
        if btn == 1 and self.coords:
            if self.quest.location_ambiguous:
                x, y = self.coords
                srand(x + y)
                d = random() * 7
                a = math.pi * 2 * random()
                dx = math.cos(a) * d
                dy = math.sin(a) * d * 2
                x += dx
                y += dy
                map_window.show_target((x, y), False)
            else:
                map_window.show_target(self.coords)

class QuestList(List):
    def __init__(self, sf, x, y, w, h):
        super().__init__(sf, x, y, w, h, [])

    def update(self):
        btns = []
        if active_save:
            s = active_save
            btns.append(Text(self.sf, 0, 0, font1, s.save_game_label))
            btns.append(Text(self.sf, 0, 0, font5, s.curr_date.strftime('%Y/%m/%d %H')))
            btns.append(Text(self.sf, 0, 0, font1, s.curr_location_name))

            for e in s.events:
                if e.hide:
                    continue
                btns.append(QuestButton(self.sf, e))
        self.populate(btns)
        self.render()

list_quests = QuestList(screen, 550, 13*scale, 250, 550-13*scale)


class MenuButton(Button):
    def __init__(self, sf, x, y, text, parent, no):
        self.parent = parent
        self.no = no
        super().__init__(sf, parent.x+x, parent.y+y, font3, text, font4)
    def on_click(self, btn):
        self.parent.on_push(self.no)

class Menu(Widget):
    def __init__(self, sf, x, y, w, h):
        super().__init__(sf, x, y, w, h)
        self.active_button = 1
        self.buttons = [
            MenuButton(screen, 15, 4*scale, 'Map', self, 1),
            MenuButton(screen, 80, 4*scale, 'Save', self, 2),
            MenuButton(screen, 160, 4*scale, 'Quest', self, 3)
        ]
    def render(self):
        self.set_clip(self.x, self.y, self.w, self.h)
        p_panel.render(screen, self.x-scale, self.y, self.w, self.h)
        for b in self.buttons:
            if self.active_button == b.no:
                pygame.draw.rect(self.sf, (255, 255, 0), (b.x, b.y+b.h, b.w, scale))
            b.render()
        self.del_clip()
    def behave(self, event):
        mx, my = pygame.mouse.get_pos()
        if mx<self.x or mx>=self.x+self.w or my<self.y or my>=self.y+self.h:
            return
        for b in self.buttons:
            b.behave(event)
    def on_push(self, button_no):
        if self.active_button == button_no:
            return
        self.active_button = button_no
        if button_no == 1:
            list_saves.hide()
            list_quests.hide()
            list_cities.show()
        elif button_no == 2:
            list_cities.hide()
            list_quests.hide()
            list_saves.show()
        else:
            list_cities.hide()
            list_saves.hide()
            list_quests.show()
        self.render()


menu = Menu(screen, 550-scale, 0, 250+2*scale, 13*scale)
list_cities.hidden = False
list_saves.hidden = True
list_quests.hidden = True

if saves:
    set_active_save(saves[0])

widgets = [
    menu,
    map_window,
    list_cities,
    list_saves,
    list_quests
]

for w in widgets:
    w.render()

pygame.time.set_timer(pygame.USEREVENT, 5000) # timer to check saves
last_mouse_pos = pygame.mouse.get_pos()

while 1:
    pygame.display.flip()
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.USEREVENT:
        # check saves if no mouse motion
        mpos = pygame.mouse.get_pos()
        if mpos[0] == last_mouse_pos[0] and mpos[1] == last_mouse_pos[1]:
            if load_saves() and saves:
                list_saves.update()
                set_active_save(saves[0])
        else:
            last_mouse_pos = mpos

    for w in widgets:
        w.behave(event)
