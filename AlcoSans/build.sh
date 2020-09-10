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
rm -f AlcoSans.sfd-* AlcoSans.ttf AlcoSans.eot AlcoSans.zip
rm -rf alcosans

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	AlcoSans.sfd

# Convert to eot
$TTF2EOT < AlcoSans.ttf > AlcoSans.eot

# Create zip
zip AlcoSans.zip OFL.txt AlcoSans.sfd AlcoSans.ttf AlcoSans.eot

# Create lowercase versions
mkdir alcosans
cp AlcoSans.ttf alcosans/alcosans.ttf
cp AlcoSans.eot alcosans/alcosans.eot
cp AlcoSans.zip alcosans/alcosans.zip
