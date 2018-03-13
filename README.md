# Darklands
Darklands (1992 game from Microprose) file reading utils and preserved file format docs

Based heavily upon work of Merle (wallace.net/darklands) and Joel "Quadko" McIntyre.

Probably not suitable for Windows because of lazy filepaths handling.

[Some outputs and file format docs online](http://wendigo.online-siesta.com/darklands/)


## TODO
* File format documentation of my own
* MSG cards connections
* Weapon attributes

## Repository contents

### Dirs
* DL/ - put your Darklands instalation here
* game_patches/ - essential patches to upgrade Darklands to the latest version (.7)

* file_formats/ - gathered docs on DL file formats (corrections included)

* tmp/ - you may direct output there


### Scripts
#### Auxilary
* aux_show_fonts.py - renders system fonts usable by Pygame
* aux_check_pics.py - some PIC files scanning
* aux_generate_simple_map.py - very simple HTML map with cities and locations

#### Extracting
* extract_cat.py - extracts catalogue (.CAT) files

#### Generators
* generate_map_png.py - outputs HUGE image of DL landscape with city and village names
* generate_map_web.py - outputs HUGE webpage of simplified DL map with city info

#### Readers
* reader_cty.py - cities
* reader_loc.py - map locations (cities, villages, castles...)
* reader_lst.py - item types & attrs, saints and formula names
* reader_map.py - tile map
* reader_msg.py - dialogs - WIP
* reader_pic.py - image format

#### Common libs
* utils.py


### Misc
* dosbox.conf - to ease running of the game

## Dependencies
* Pygame lib for imagery

