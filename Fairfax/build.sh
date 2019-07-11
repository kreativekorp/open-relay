#!/usr/bin/env bash

if test -f BitsNPicas.jar; then
	BITSNPICAS="java -jar BitsNPicas.jar"
elif test -f ../BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../BitsNPicas/BitsNPicas.jar"
elif test -f ../Workspace/BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../Workspace/BitsNPicas/BitsNPicas.jar"
elif test -f ../../BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../BitsNPicas/BitsNPicas.jar"
elif test -f ../../Workspace/BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../Workspace/BitsNPicas/BitsNPicas.jar"
elif test -f ../../../BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../../BitsNPicas/BitsNPicas.jar"
elif test -f ../../../Workspace/BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../../Workspace/BitsNPicas/BitsNPicas.jar"
elif test -f ../../../../BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../../../BitsNPicas/BitsNPicas.jar"
elif test -f ../../../../Workspace/BitsNPicas/BitsNPicas.jar; then
	BITSNPICAS="java -jar ../../../../Workspace/BitsNPicas/BitsNPicas.jar"
else
	echo "Could not find BitsNPicas."
	exit 1
fi

if command -v ttf2eot >/dev/null 2>&1; then
	TTF2EOT="ttf2eot"
else
	echo "Could not find ttf2eot."
	exit 1
fi

# Clean
rm -f Fairfax*.ttf Fairfax*.eot Fairfax*.zip
rm -rf fairfax

# Generate ttf
$BITSNPICAS convertbitmap \
	-o Fairfax.ttf -f ttf Fairfax.kbits \
	-o FairfaxBold.ttf -f ttf FairfaxBold.kbits \
	-o FairfaxItalic.ttf -f ttf FairfaxItalic.kbits \
	-o FairfaxSerif.ttf -f ttf FairfaxSerif.kbits

# Convert to eot
$TTF2EOT < Fairfax.ttf > Fairfax.eot
$TTF2EOT < FairfaxBold.ttf > FairfaxBold.eot
$TTF2EOT < FairfaxItalic.ttf > FairfaxItalic.eot
$TTF2EOT < FairfaxSerif.ttf > FairfaxSerif.eot

# Create zip
zip Fairfax.zip OFL.txt Fairfax*.ttf Fairfax*.eot

# Create lowercase versions
mkdir fairfax
cp Fairfax.ttf fairfax/fairfax.ttf
cp Fairfax.eot fairfax/fairfax.eot
cp FairfaxBold.ttf fairfax/fairfaxbold.ttf
cp FairfaxBold.eot fairfax/fairfaxbold.eot
cp FairfaxItalic.ttf fairfax/fairfaxitalic.ttf
cp FairfaxItalic.eot fairfax/fairfaxitalic.eot
cp FairfaxSerif.ttf fairfax/fairfaxserif.ttf
cp FairfaxSerif.eot fairfax/fairfaxserif.eot
cp Fairfax.zip fairfax/fairfax.zip
