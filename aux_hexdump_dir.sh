#!/bin/bash

DIR=$1
LEN=$2

echo -n '             '
HDR=''
for I in `seq 0 100` ; do
	HDR=`printf "%s %2d" "$HDR" $I`
done
echo "$HDR" | head -c $LEN
echo

for F in `ls $DIR/ -1` ; do
	printf '%12s:' $F
	hexdump -v -e '/1 " %02X"' $DIR/$F | head -c $LEN
	echo
done

