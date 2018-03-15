#!/bin/bash

DIR=$1
LEN=$2

for F in `ls $DIR/ -1` ; do
	printf '%12s: ' $F
	hexdump -v -e '/1 "%02X "' $DIR/$F | head -c $LEN
	echo
done

