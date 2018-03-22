#!/bin/bash

DIR=$1
LEN=$2

echo -n '                     '
HDR=''
for I in `seq 0 99` ; do
	HDR=`printf "%s %3d" "$HDR" $I`
done
echo -n "$HDR" | head -c $LEN
echo

for F in `ls $DIR/ -1` ; do
	printf '%20s:' $F
	#hexdump -v -e '/1 " %02X"' $DIR/$F | head -c $LEN
	hexdump -v -e '/1 " %3u"' $DIR/$F | head -c $LEN
	echo
done

