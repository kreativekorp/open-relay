#!/usr/bin/env bash

# Find FontForge
if command -v fontforge >/dev/null 2>&1; then
	FONTFORGE="fontforge"
elif test -f /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge; then
	FONTFORGE="/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge"
else
	echo "Could not find FontForge."
	exit 1
fi

# Find ttf2eot
if command -v ttf2eot >/dev/null 2>&1; then
	TTF2EOT="ttf2eot"
else
	echo "Could not find ttf2eot."
	exit 1
fi

SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
BLOCKS="python ../openrelay-tools/tools/blocks.py"
UNIDATA="python ../openrelay-tools/tools/unicodedata.py"
PYPUAA="python ../openrelay-tools/tools/pypuaa.py"

# Clean
rm -f Constructium.sfd-* Constructium.ttf Constructium.eot Constructium.zip ConstructiumTmp.*
rm -rf constructium

# Make timestamped version
$SFDPATCH Constructium.sfd patches/timestamp.txt > ConstructiumTmp.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	ConstructiumTmp.sfd
mv ConstructiumTmp.ttf Constructium.ttf
rm ConstructiumTmp.sfd

# Inject PUAA table
$BLOCKS cwadkkypjqvgtt > Blocks.txt
$UNIDATA cwadkkypjqvgtt > UnicodeData.txt
$PYPUAA compile -D Blocks.txt UnicodeData.txt -I Constructium.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < Constructium.ttf > Constructium.eot

# Create zip
zip Constructium.zip OFL.txt Constructium.sfd Constructium.ttf Constructium.eot

# Create lowercase versions
mkdir constructium
cp Constructium.ttf constructium/constructium.ttf
cp Constructium.eot constructium/constructium.eot
cp Constructium.zip constructium/constructium.zip
