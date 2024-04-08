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
rm -f AlcoSans.sfd-* AlcoSans.ttf AlcoSans.eot AlcoSans.zip AlcoSansTmp.*
rm -rf alcosans

# Make timestamped version
$SFDPATCH AlcoSans.sfd patches/timestamp.txt > AlcoSansTmp.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	AlcoSansTmp.sfd
mv AlcoSansTmp.ttf AlcoSans.ttf
rm AlcoSansTmp.sfd

# Inject PUAA table
$BLOCKS cwadkkypjqvgtt > Blocks.txt
$UNIDATA cwadkkypjqvgtt > UnicodeData.txt
$PYPUAA compile -D Blocks.txt UnicodeData.txt -I AlcoSans.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < AlcoSans.ttf > AlcoSans.eot

# Create zip
zip AlcoSans.zip OFL.txt AlcoSans.sfd AlcoSans.ttf AlcoSans.eot

# Create lowercase versions
mkdir alcosans
cp AlcoSans.ttf alcosans/alcosans.ttf
cp AlcoSans.eot alcosans/alcosans.eot
cp AlcoSans.zip alcosans/alcosans.zip
