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

# Find ttf2eot
if command -v ttf2eot >/dev/null 2>&1; then
	TTF2EOT="ttf2eot"
else
	echo "Could not find ttf2eot."
	exit 1
fi

SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
SITELENPANA="python ../openrelay-tools/tools/sitelenpana.py"
BLOCKS="python ../openrelay-tools/tools/blocks.py"
UNIDATA="python ../openrelay-tools/tools/unicodedata.py"
PUAABOOK="python ../openrelay-tools/tools/puaabook.py"
PYPUAA="python ../openrelay-tools/tools/pypuaa.py"
TTFHACK="python ../openrelay-tools/tools/ttfhack.py"

# Clean
rm -f *.sfd-* *Tmp* *_base.* FairfaxHD.ttf FairfaxHD.eot FairfaxHD.zip FairfaxHD-NoCJK.* FairfaxPonaHD.* FairfaxPulaHD.* FairfaxHaxHD.* FairfaxSMHD.*
rm -rf fairfaxhd Android

# Make patched versions
$SFDPATCH FairfaxHD.sfd patches/base.txt > FairfaxHD_base.sfd
$SFDPATCH FairfaxHD_base.sfd patches/nocjk.txt > FairfaxHDNoCJK_base.sfd
$SFDPATCH FairfaxHD_base.sfd patches/asuki.txt > FairfaxPonaHD_base.sfd
$SFDPATCH FairfaxHD_base.sfd patches/atuki.txt > FairfaxPulaHD_base.sfd
$SFDPATCH FairfaxHD_base.sfd patches/ligatures.txt > FairfaxHaxHD_base.sfd
$SFDPATCH FairfaxHD_base.sfd patches/strictmono.txt > FairfaxSMHD_base.sfd

# Generate fea
grep -v cjkMark ../features/marks.fea > ../features/marks-nocjk.fea
grep -v uni300 ../features/sequences.fea > ../features/sequences-nocjk.fea
grep -E -v "uni(30|4E|51)" ../features/sitelenpona.txt > ../features/sitelenpona-nocjk.txt
$SITELENPANA -f FairfaxHDNoCJK_base.sfd -i ../features/sitelenpona-nocjk.txt -a /dev/null -o ../features/spnocjk.fea
$SITELENPANA -f FairfaxPonaHD_base.sfd -i ../features/sitelenpona.txt -a ../features/spascii.fea -o ../features/spbase.fea -g glyphs.html -e FairfaxHD.eot -t FairfaxHD.ttf
$SITELENPANA -f FairfaxPulaHD_base.sfd -i ../features/titipula.txt -a ../features/tpascii.fea -o /dev/null

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	FairfaxHD_base.sfd FairfaxHDNoCJK_base.sfd \
	FairfaxPonaHD_base.sfd FairfaxPulaHD_base.sfd \
	FairfaxHaxHD_base.sfd FairfaxSMHD_base.sfd

# Add OpenType features
$FONTTOOLS feaLib -o FairfaxHD.ttf ../features/base.fea FairfaxHD_base.ttf
$FONTTOOLS feaLib -o FairfaxHD-NoCJK.ttf ../features/nocjk.fea FairfaxHDNoCJK_base.ttf
$FONTTOOLS feaLib -o FairfaxPonaHD.ttf ../features/asuki.fea FairfaxPonaHD_base.ttf
$FONTTOOLS feaLib -o FairfaxPulaHD.ttf ../features/atuki.fea FairfaxPulaHD_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxHD.ttf ../features/code.fea FairfaxHaxHD_base.ttf
cp FairfaxSMHD_base.ttf FairfaxSMHD.ttf

# Remove intermediate artifacts
rm *_base.sfd
rm ../features/marks-nocjk.fea
rm ../features/sequences-nocjk.fea
rm ../features/sitelenpona-nocjk.txt
rm ../features/spascii.fea
rm ../features/spbase.fea
rm ../features/spnocjk.fea
rm ../features/tpascii.fea
rm *_base.ttf

# Inject PUAA table
PUAAFLAGS="czuowbanxkkfeypjqvgsittl --no-sylabica-2013 --sylabica-2017 --pua-a-sylabica-2013 --ihatemysalf --halfwidth-and-fullwidth-forms-appendix-a"
$BLOCKS $PUAAFLAGS > Blocks.txt
$UNIDATA $PUAAFLAGS > UnicodeData.txt
$PUAABOOK -D Blocks.txt UnicodeData.txt charts.txt -I FairfaxHD.ttf -O pua.html
$PYPUAA compile -D Blocks.txt UnicodeData.txt \
	-I FairfaxHD.ttf FairfaxHD-NoCJK.ttf \
	-I FairfaxPonaHD.ttf FairfaxPulaHD.ttf \
	-I FairfaxHaxHD.ttf FairfaxSMHD.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < FairfaxHD.ttf > FairfaxHD.eot
$TTF2EOT < FairfaxHD-NoCJK.ttf > FairfaxHD-NoCJK.eot
$TTF2EOT < FairfaxPonaHD.ttf > FairfaxPonaHD.eot
$TTF2EOT < FairfaxPulaHD.ttf > FairfaxPulaHD.eot
$TTF2EOT < FairfaxHaxHD.ttf > FairfaxHaxHD.eot
$TTF2EOT < FairfaxSMHD.ttf > FairfaxSMHD.eot

# Create hacked Android version
mkdir Android
$TTFHACK if=FairfaxHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxHD.ttf
$TTFHACK if=FairfaxHD-NoCJK.ttf yMin=-544 yMax=1308 of=Android/FairfaxHD-NoCJK.ttf
$TTFHACK if=FairfaxPonaHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxPonaHD.ttf
$TTFHACK if=FairfaxPulaHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxPulaHD.ttf
$TTFHACK if=FairfaxHaxHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxHaxHD.ttf
$TTFHACK if=FairfaxSMHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxSMHD.ttf

# Create zip
zip FairfaxHD.zip OFL.txt \
	FairfaxHD.ttf FairfaxHD.eot \
	FairfaxHD-NoCJK.ttf FairfaxHD-NoCJK.eot \
	FairfaxPonaHD.ttf FairfaxPonaHD.eot \
	FairfaxPulaHD.ttf FairfaxPulaHD.eot \
	FairfaxHaxHD.ttf FairfaxHaxHD.eot \
	FairfaxSMHD.ttf FairfaxSMHD.eot \
	Android/* pua.html
cp FairfaxHD.zip FairfaxHD-NoCJK.zip
cp FairfaxHD.zip FairfaxPonaHD.zip
cp FairfaxHD.zip FairfaxPulaHD.zip
cp FairfaxHD.zip FairfaxHaxHD.zip
cp FairfaxHD.zip FairfaxSMHD.zip

# Create lowercase versions
mkdir fairfaxhd
cp FairfaxHD.ttf fairfaxhd/fairfaxhd.ttf
cp FairfaxHD.eot fairfaxhd/fairfaxhd.eot
cp FairfaxHD.zip fairfaxhd/fairfaxhd.zip
cp FairfaxHD-NoCJK.ttf fairfaxhd/fairfaxhd-nocjk.ttf
cp FairfaxHD-NoCJK.eot fairfaxhd/fairfaxhd-nocjk.eot
cp FairfaxHD-NoCJK.zip fairfaxhd/fairfaxhd-nocjk.zip
cp FairfaxPonaHD.ttf fairfaxhd/fairfaxponahd.ttf
cp FairfaxPonaHD.eot fairfaxhd/fairfaxponahd.eot
cp FairfaxPonaHD.zip fairfaxhd/fairfaxponahd.zip
cp FairfaxPulaHD.ttf fairfaxhd/fairfaxpulahd.ttf
cp FairfaxPulaHD.eot fairfaxhd/fairfaxpulahd.eot
cp FairfaxPulaHD.zip fairfaxhd/fairfaxpulahd.zip
cp FairfaxHaxHD.ttf fairfaxhd/fairfaxhaxhd.ttf
cp FairfaxHaxHD.eot fairfaxhd/fairfaxhaxhd.eot
cp FairfaxHaxHD.zip fairfaxhd/fairfaxhaxhd.zip
cp FairfaxSMHD.ttf fairfaxhd/fairfaxsmhd.ttf
cp FairfaxSMHD.eot fairfaxhd/fairfaxsmhd.eot
cp FairfaxSMHD.zip fairfaxhd/fairfaxsmhd.zip
