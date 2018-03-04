#!/bin/bash

# Script to lowercase filenames in DL directory
# Run it from here

for D in ../DL ../DL/pics ; do
	if cd $D ; then
		echo "Lowercasing $D ..."
		for f in *[[:upper:]]*; do mv -- "$f" "${f,,}"; done
		cd -
	fi
done
