#!/bin/bash

mkdir -p tmp/pics

for F in `ls DL/pics/*.pic` ; do
	python reader_pic.py $F tmp/pics/
done

# rewrite with forced pallete

ARMPATTS='armbrs*.pic *lim.pic pad-lims.pic *vit.pic weapon*.pic smallsh.pic mediumsh.pic brigstud.pic armsback.pic'
for P in $ARMPATTS ; do
	for F in `ls DL/pics/$P` ; do
			python reader_pic.py $F tmp/pics/ DL/pics/armback.pic
	done
done

python reader_pic.py DL/pics/charicon.pic tmp/pics/ DL/pics/mapicons.pic

