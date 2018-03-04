# Darklands
Darklands (1992 game from Microprose) file reading utils and preserved file format docs

Based heavily upon work of Merle (wallace.net/darklands) and Joel "Quadko" McIntyre.

Probably not suitable for Windows because of lazy filepaths handling.

[Some outputs and file format docs online](http://wendigo.online-siesta.com/darklands/)


## TODO
* loc - cty relation?
* wrong bridge tile rendering
* MSG format

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

#### Extracting
* extract_cat.py - extracts catalogue (.CAT) files

#### Generators
* generate_map_png.py - outputs HUGE image of DL landscape with city and village names
* generate_map_web.py - outputs HUGE webpage of simplified DL map with city info
* generate_simple_map.py - very simple HTML map with cities (AUX maybe?)

#### Readers
* reader_cty.py
* reader_loc.py
* reader_map.py
* reader_msg.py
* reader_pic.py

#### Common libs
* utils.py


### Misc
* dosbox.conf - to ease playing of Darklands

## Dependencies
* Pygame lib for imagery

