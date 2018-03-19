# Darklands
Darklands (1992 game from Microprose) file reading utils and preserved file format docs

Based heavily upon work of Merle (wallace.net/darklands) and Joel "Quadko" McIntyre.

Probably not suitable for Windows because of lazy filepaths handling.

[Some outputs and file format docs online](http://wendigo.online-siesta.com/darklands/)


## TODO (Short term goals)
* Fixing up-to-date XSLT
* IMC format
* MSG cards connections
* Weapon attributes

## Repository contents

### Dirs
* DL/ - put your Darklands installed files here
* game_patches/ - essential patches to upgrade Darklands to the latest version (.7)

* file_formats/ - gathered docs on DL file formats (up-to-date/ contains updated Merle's docs)

* tmp/ - you may direct output there


### Scripts
#### Auxilary
* aux_count_bytes.py - file byte histogram counter
* aux_find_bytes.py - find bytes in file, limited by max distance from first found to last
* aux_generate_simple_map.py - very simple HTML map with cities and locations
* aux_check_pics.py - some PIC files scanning
* aux_show_fonts.py - renders system fonts usable by Pygame

* aux_hexdump_dir.sh - first N chars of hexdump of all files in directory
* aux_convert_pics.sh - convert all DL/pics/*.pic to tmp/pics/*.pic.png

#### Extracting
* extract_cat.py - extracts catalogue (.CAT) files

#### Generators
* generate_map_png.py - outputs HUGE image of DL landscape with city and village names
* generate_map_web.py - outputs HUGE webpage of simplified DL map with city info

#### Readers
* reader_cty.py - cities
* reader_drle.py - "DarklandsRLE" decompression (used for .IMC, in imap.cat, bc) (can decompress file if run directly)
* reader_exe.py - strings extraction - WIP
* reader_imc.py - battle sprites - WIP
* reader_loc.py - map locations (cities, villages, castles...)
* reader_lst.py - item types & attrs, saints and formula names
* reader_map.py - tile map
* reader_msg.py - dialogs - WIP
* reader_pic.py - image format (can convert .PIC to .PNG if run directly)
* reader_tacanim.py - mysterious file loaded before battle

#### Common libs
* utils.py


### Misc
* dosbox.conf - to ease running of the game

## Dependencies
* Pygame lib for imagery

