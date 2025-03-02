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
SITELENPONA="python ../openrelay-tools/tools/sitelenpona.py"
BLOCKS="python ../openrelay-tools/tools/blocks.py"
UNIDATA="python ../openrelay-tools/tools/unicodedata.py"
PUAABOOK="python ../openrelay-tools/tools/puaabook.py"
PYPUAA="python ../openrelay-tools/tools/pypuaa.py"
TTFHACK="python ../openrelay-tools/tools/ttfhack.py"

# Clean
rm -f *.sfd-* *Tmp* *_base.* FairfaxHD.ttf FairfaxHD.eot FairfaxHD.zip FairfaxPonaHD.* FairfaxPulaHD.* FairfaxLogosHD.* FairfaxHaxHD.* FairfaxSMHD.*
rm -rf fairfaxhd Android

# Make timestamped version
$SFDPATCH FairfaxHD.sfd patches/timestamp.txt > FairfaxHD_base.sfd

# Make sitelen pona version
$SFDPATCH FairfaxHD_base.sfd patches/asuki.txt > FairfaxPonaHD_base.sfd

# Make titi pula version
$SFDPATCH FairfaxHD_base.sfd patches/atuki.txt > FairfaxPulaHD_base.sfd

# Make my logos version
$SFDPATCH FairfaxHD_base.sfd patches/logos.txt > FairfaxLogosHD_base.sfd

# Make programming ligature version
$SFDPATCH FairfaxHD_base.sfd patches/ligatures.txt > FairfaxHaxHD_base.sfd

# Make strict monospace version
$SFDPATCH FairfaxHD_base.sfd patches/strictmono.txt > FairfaxSMHD_base.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	FairfaxHD_base.sfd FairfaxPonaHD_base.sfd FairfaxPulaHD_base.sfd FairfaxHaxHD_base.sfd FairfaxSMHD_base.sfd

rm *_base.sfd

# Add OpenType features (FontForge completely fouls this up on its own)
$SITELENPONA -s -a ../features/asuki.txt -t ../features/atuki.txt -e ../features/extendable.txt -j ../features/joiners.txt -g FairfaxHD.sfd
cat ../features/languages.fea ../features/sequences.fea joiners.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxHD_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea asuki.fea ../features/aargh.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxPonaHD_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea atuki.fea ../features/aargh.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxPulaHD_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea ../features/logos.fea ../features/aargh.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxLogosHD_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea ../features/ligatures.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxHaxHD_base.fea
rm asuki.fea atuki.fea extendable.fea joiners.fea

$FONTTOOLS feaLib -o FairfaxHD.ttf FairfaxHD_base.fea FairfaxHD_base.ttf
$FONTTOOLS feaLib -o FairfaxPonaHD.ttf FairfaxPonaHD_base.fea FairfaxPonaHD_base.ttf
$FONTTOOLS feaLib -o FairfaxPulaHD.ttf FairfaxPulaHD_base.fea FairfaxPulaHD_base.ttf
$FONTTOOLS feaLib -o FairfaxLogosHD.ttf FairfaxLogosHD_base.fea FairfaxLogosHD_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxHD.ttf FairfaxHaxHD_base.fea FairfaxHaxHD_base.ttf
cp FairfaxSMHD_base.ttf FairfaxSMHD.ttf

rm *_base.fea
rm *_base.ttf

# Inject PUAA table
PUAAFLAGS="czuowbanxkkfeypjqvgsittl --ihatemysalf --halfwidth-and-fullwidth-forms-appendix-a"
$BLOCKS $PUAAFLAGS > Blocks.txt
$UNIDATA $PUAAFLAGS > UnicodeData.txt
$PUAABOOK -D Blocks.txt UnicodeData.txt charts.txt -I FairfaxHD.ttf -O pua.html
$PYPUAA compile -D Blocks.txt UnicodeData.txt -I FairfaxHD.ttf FairfaxPonaHD.ttf FairfaxPulaHD.ttf FairfaxLogosHD.ttf FairfaxHaxHD.ttf FairfaxSMHD.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < FairfaxHD.ttf > FairfaxHD.eot
$TTF2EOT < FairfaxPonaHD.ttf > FairfaxPonaHD.eot
$TTF2EOT < FairfaxPulaHD.ttf > FairfaxPulaHD.eot
$TTF2EOT < FairfaxLogosHD.ttf > FairfaxLogosHD.eot
$TTF2EOT < FairfaxHaxHD.ttf > FairfaxHaxHD.eot
$TTF2EOT < FairfaxSMHD.ttf > FairfaxSMHD.eot

# Create hacked Android version
mkdir Android
$TTFHACK if=FairfaxHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxHD.ttf
$TTFHACK if=FairfaxPonaHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxPonaHD.ttf
$TTFHACK if=FairfaxPulaHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxPulaHD.ttf
$TTFHACK if=FairfaxLogosHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxLogosHD.ttf
$TTFHACK if=FairfaxHaxHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxHaxHD.ttf
$TTFHACK if=FairfaxSMHD.ttf yMin=-544 yMax=1308 of=Android/FairfaxSMHD.ttf

# Create zip
zip FairfaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html
zip FairfaxPonaHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html
zip FairfaxPulaHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html
zip FairfaxLogosHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html
zip FairfaxHaxHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html
zip FairfaxSMHD.zip OFL.txt FairfaxHD.ttf FairfaxHD.eot FairfaxPonaHD.ttf FairfaxPonaHD.eot FairfaxPulaHD.ttf FairfaxPulaHD.eot FairfaxLogosHD.ttf FairfaxLogosHD.eot FairfaxHaxHD.ttf FairfaxHaxHD.eot FairfaxSMHD.ttf FairfaxSMHD.eot Android/* pua.html

# Create lowercase versions
mkdir fairfaxhd
cp FairfaxHD.ttf fairfaxhd/fairfaxhd.ttf
cp FairfaxHD.eot fairfaxhd/fairfaxhd.eot
cp FairfaxHD.zip fairfaxhd/fairfaxhd.zip
cp FairfaxPonaHD.ttf fairfaxhd/fairfaxponahd.ttf
cp FairfaxPonaHD.eot fairfaxhd/fairfaxponahd.eot
cp FairfaxPonaHD.zip fairfaxhd/fairfaxponahd.zip
cp FairfaxPulaHD.ttf fairfaxhd/fairfaxpulahd.ttf
cp FairfaxPulaHD.eot fairfaxhd/fairfaxpulahd.eot
cp FairfaxPulaHD.zip fairfaxhd/fairfaxpulahd.zip
cp FairfaxLogosHD.ttf fairfaxhd/fairfaxlogoshd.ttf
cp FairfaxLogosHD.eot fairfaxhd/fairfaxlogoshd.eot
cp FairfaxLogosHD.zip fairfaxhd/fairfaxlogoshd.zip
cp FairfaxHaxHD.ttf fairfaxhd/fairfaxhaxhd.ttf
cp FairfaxHaxHD.eot fairfaxhd/fairfaxhaxhd.eot
cp FairfaxHaxHD.zip fairfaxhd/fairfaxhaxhd.zip
cp FairfaxSMHD.ttf fairfaxhd/fairfaxsmhd.ttf
cp FairfaxSMHD.eot fairfaxhd/fairfaxsmhd.eot
cp FairfaxSMHD.zip fairfaxhd/fairfaxsmhd.zip
