#!/bin/bash

mkdir -p tmp/pics

for F in `ls DL/pics/*.pic` ; do
	python reader_pic.py $F tmp/pics/
done

