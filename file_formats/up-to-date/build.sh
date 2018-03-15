#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "$0 OUT_DIR/"
	exit 1
fi


OUTDIR=`cd "$1"; pwd`

cp -r ./catalogs $OUTDIR/ || exit 1
cp -r ./xml_formats $OUTDIR/ || exit 1
cp index.css $OUTDIR/ || exit 1
DATE=`date -R`
sed "s/25-Jan-4/$DATE/" index.html > $OUTDIR/index.html
mkdir $OUTDIR/formats || exit 1
cp file_format.css $OUTDIR/formats/ || exit 1

cd ./xml_formats || exit 1
for F in `ls *.xml` ; do
	echo $F
	xsltproc file_format.xslt $F > $OUTDIR/formats/`basename $F .xml`.html || exit 1
done
cd -

