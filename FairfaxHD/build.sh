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

# Find fonttools
if command -v fonttools >/dev/null 2>&1; then
	FONTTOOLS="fonttools"
else
	echo "Could not find fonttools."
	exit 1
fi

# Find Bits'n'Picas
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

# Find ttf2eot
if command -v ttf2eot >/dev/null 2>&1; then
	TTF2EOT="ttf2eot"
else
	echo "Could not find ttf2eot."
	exit 1
fi

# Clean
rm -f *.sfd-* *Tmp* *_base.* FairfaxHD.ttf FairfaxHD.eot FairfaxHD.zip FairfaxPonaHD.* FairfaxHaxHD.* FairfaxSMHD.*
rm -rf fairfaxhd

# Make timestamped version
python ../bin/sfdpatch.py FairfaxHD.sfd patches/timestamp.txt > FairfaxHD_base.sfd

# Make sitelen pona version
python ../bin/sfdpatch.py FairfaxHD_base.sfd patches/asuki.txt > FairfaxPonaHD_base.sfd

# Make programming ligature version
python ../bin/sfdpatch.py FairfaxHD_base.sfd patches/ligatures.txt > FairfaxHaxHD_base.sfd

# Make strict monospace version
python ../bin/sfdpatch.py FairfaxHD_base.sfd patches/strictmono.txt > FairfaxSMHD_base.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	FairfaxHD_base.sfd FairfaxPonaHD_base.sfd FairfaxHaxHD_base.sfd FairfaxSMHD_base.sfd

rm *_base.sfd

# Add OpenType features (FontForge completely fouls this up on its own)
cd features
python build.py
cat languages.fea sequences.fea joiners.fea variants.fea extendable.fea extensions.fea > ../FairfaxHD_base.fea
cat languages.fea sequences.fea joiners.fea asuki.fea variants.fea extendable.fea extensions.fea > ../FairfaxPonaHD_base.fea
cat languages.fea sequences.fea joiners.fea ligatures.fea variants.fea extendable.fea extensions.fea > ../FairfaxHaxHD_base.fea
cd ..

$FONTTOOLS feaLib -o FairfaxHD.ttf FairfaxHD_base.fea FairfaxHD_base.ttf
$FONTTOOLS feaLib -o FairfaxPonaHD.ttf FairfaxPonaHD_base.fea FairfaxPonaHD_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxHD.ttf FairfaxHaxHD_base.fea FairfaxHaxHD_base.ttf
cp FairfaxSMHD_base.ttf FairfaxSMHD.ttf

rm *_base.fea
rm *_base.ttf

# Inject PUAA table
python ../bin/blocks.py czuowbanxkkfeypjqvsttl > Blocks.txt
python ../bin/unicodedata.py czuowbanxkkfeypjqvsttl > UnicodeData.txt
$BITSNPICAS injectpuaa \
	-D Blocks.txt UnicodeData.txt \
	-I FairfaxHD.ttf FairfaxPonaHD.ttf FairfaxHaxHD.ttf FairfaxSMHD.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < FairfaxHD.ttf > FairfaxHD.eot
$TTF2EOT < FairfaxPonaHD.ttf > FairfaxPonaHD.eot
$TTF2EOT < FairfaxHaxHD.ttf > FairfaxHaxHD.eot
$TTF2EOT < FairfaxSMHD.ttf > FairfaxSMHD.eot

# Create zip
zip FairfaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot
zip FairfaxPonaHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot
zip FairfaxHaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot
zip FairfaxSMHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot

# Create lowercase versions
mkdir fairfaxhd
cp FairfaxHD.ttf fairfaxhd/fairfaxhd.ttf
cp FairfaxHD.eot fairfaxhd/fairfaxhd.eot
cp FairfaxHD.zip fairfaxhd/fairfaxhd.zip
cp FairfaxPonaHD.ttf fairfaxhd/fairfaxponahd.ttf
cp FairfaxPonaHD.eot fairfaxhd/fairfaxponahd.eot
cp FairfaxPonaHD.zip fairfaxhd/fairfaxponahd.zip
cp FairfaxHaxHD.ttf fairfaxhd/fairfaxhaxhd.ttf
cp FairfaxHaxHD.eot fairfaxhd/fairfaxhaxhd.eot
cp FairfaxHaxHD.zip fairfaxhd/fairfaxhaxhd.zip
cp FairfaxSMHD.ttf fairfaxhd/fairfaxsmhd.ttf
cp FairfaxSMHD.eot fairfaxhd/fairfaxsmhd.eot
cp FairfaxSMHD.zip fairfaxhd/fairfaxsmhd.zip
