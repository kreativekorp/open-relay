#!/usr/bin/env bash

if command -v fontforge >/dev/null 2>&1; then
	FONTFORGE="fontforge"
elif test -f /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge; then
	FONTFORGE="/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge"
else
	echo "Could not find FontForge."
	exit 1
fi

if command -v ttf2eot >/dev/null 2>&1; then
	TTF2EOT="ttf2eot"
else
	echo "Could not find ttf2eot."
	exit 1
fi

# Clean
rm -f Constructium.sfd-* Constructium.ttf Constructium.eot Constructium.zip
rm -rf constructium

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 128); i = i+1; endloop' Constructium.sfd

# Convert to eot
$TTF2EOT < Constructium.ttf > Constructium.eot

# Create zip
zip Constructium.zip OFL.txt Constructium.sfd Constructium.ttf Constructium.eot

# Create lowercase versions
mkdir constructium
cp Constructium.ttf constructium/constructium.ttf
cp Constructium.eot constructium/constructium.eot
cp Constructium.zip constructium/constructium.zip
