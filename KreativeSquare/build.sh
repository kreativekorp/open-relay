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
PUAABOOK="python ../openrelay-tools/tools/puaabook.py"
PYPUAA="python ../openrelay-tools/tools/pypuaa.py"

# Clean
rm -f KreativeSquare.sfd-* KreativeSquare.ttf KreativeSquare.eot KreativeSquare.zip KreativeSquareTmp.* KreativeSquareSM.*
rm -rf kreativesquare

# Make timestamped version
$SFDPATCH KreativeSquare.sfd patches/timestamp.txt > KreativeSquareTmp.sfd

# Make strict monospace version
$SFDPATCH KreativeSquareTmp.sfd patches/strictmono.txt > KreativeSquareSM.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	KreativeSquareTmp.sfd KreativeSquareSM.sfd
mv KreativeSquareTmp.ttf KreativeSquare.ttf
rm KreativeSquareTmp.sfd

# Inject PUAA table
PUAAFLAGS="zuombxkkehsl"
$BLOCKS $PUAAFLAGS > Blocks.txt
$UNIDATA $PUAAFLAGS > UnicodeData.txt
$PUAABOOK -D Blocks.txt UnicodeData.txt -I KreativeSquare.ttf -O pua.html
$PYPUAA compile -D Blocks.txt UnicodeData.txt -I KreativeSquare.ttf KreativeSquareSM.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < KreativeSquare.ttf > KreativeSquare.eot
$TTF2EOT < KreativeSquareSM.ttf > KreativeSquareSM.eot

# Create zip
zip KreativeSquare.zip OFL.txt KreativeSquare*.ttf KreativeSquare*.eot pua.html

# Create lowercase versions
mkdir kreativesquare
cp KreativeSquare.ttf kreativesquare/kreativesquare.ttf
cp KreativeSquare.eot kreativesquare/kreativesquare.eot
cp KreativeSquareSM.ttf kreativesquare/kreativesquaresm.ttf
cp KreativeSquareSM.eot kreativesquare/kreativesquaresm.eot
cp KreativeSquare.zip kreativesquare/kreativesquare.zip
