#!/bin/bash

# Script to lowercase filenames in DL directory
# Run it from here

for D in ../DL ../DL/PICS ; do
	if cd $D ; then
		echo "Uppercasing $D ..."
		for f in *[[:lower:]]*; do mv -- "$f" "${f^^}"; done
		cd -
	fi
done
