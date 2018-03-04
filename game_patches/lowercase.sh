#!/bin/bash

# Script to lowercase filenames in DL directory
# Run it from here

for D in ../DL ../DL/pics ; do
	echo "Lowercasing $D..."
	cd $D
	for f in *[[:upper:]]*; do mv -- "$f" "${f,,}"; done
	cd -
done
