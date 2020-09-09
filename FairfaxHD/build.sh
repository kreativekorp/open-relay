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
rm -f FairfaxHD.sfd-* FairfaxHD.ttf FairfaxHD.eot FairfaxHD.zip FairfaxHaxHD.* FairfaxSMHD.*
rm -rf fairfaxhd

# Make programming ligature version
python sfdpatch.py FairfaxHD.sfd ligatures.txt > FairfaxHaxHD.sfd

# Make strict monospace version
python sfdpatch.py FairfaxHD.sfd strictmono.txt > FairfaxSMHD.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	FairfaxHD.sfd FairfaxHaxHD.sfd FairfaxSMHD.sfd

# Convert to eot
$TTF2EOT < FairfaxHD.ttf > FairfaxHD.eot
$TTF2EOT < FairfaxHaxHD.ttf > FairfaxHaxHD.eot
$TTF2EOT < FairfaxSMHD.ttf > FairfaxSMHD.eot

# Create zip
zip FairfaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot
zip FairfaxHaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot
zip FairfaxSMHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot

# Create lowercase versions
mkdir fairfaxhd
cp FairfaxHD.ttf fairfaxhd/fairfaxhd.ttf
cp FairfaxHD.eot fairfaxhd/fairfaxhd.eot
cp FairfaxHD.zip fairfaxhd/fairfaxhd.zip
cp FairfaxHaxHD.ttf fairfaxhd/fairfaxhaxhd.ttf
cp FairfaxHaxHD.eot fairfaxhd/fairfaxhaxhd.eot
cp FairfaxHaxHD.zip fairfaxhd/fairfaxhaxhd.zip
cp FairfaxSMHD.ttf fairfaxhd/fairfaxsmhd.ttf
cp FairfaxSMHD.eot fairfaxhd/fairfaxsmhd.eot
cp FairfaxSMHD.zip fairfaxhd/fairfaxsmhd.zip
