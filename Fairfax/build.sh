#!/usr/bin/env bash

# Find Bits'n'Picas
if command -v bitsnpicas >/dev/null 2>&1; then
	BITSNPICAS="bitsnpicas"
elif test -f BitsNPicas.jar; then
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

STRFTIME="python ../openrelay-tools/tools/strftime.py"
SITELENPANA="python ../openrelay-tools/tools/sitelenpana.py"
BLOCKS="python ../openrelay-tools/tools/blocks.py"
UNIDATA="python ../openrelay-tools/tools/unicodedata.py"
PUAABOOK="python ../openrelay-tools/tools/puaabook.py"
PYPUAA="python ../openrelay-tools/tools/pypuaa.py"

# Clean
rm -f *_base.* Fairfax*.ttf Fairfax*.eot Fairfax*.zip
rm -rf fairfax

# Generate patched kbitx
$BITSNPICAS convertbitmap -f kbitx \
	-t 0xF800 -d 0x10FF40-0x10FFC0 \
	-spc 0x0021-0x007E -spc 0x00B0 \
	-spc 0x3001-0x3002 -spc uni3001.vs2 -spc uni3002.vs2 \
	-spc 0x300C-0x300F -spc 0x309B-0x309C -spc 0xFF9E-0xFF9F \
	-spc 0xF1900-0xF198F -spc 0xF199C-0xF199D -spc 0xF19A0-0xF19FF \
	-spc uF1910.rand01 -spc uF1910.rand02 -spc uF1910.rand03 -spc uF1910.rand04 \
	-spc 0xF1C40-0xF1C7D -spc 0xF1C80-0xF1C9F \
	-s '20XX[.]XX[.]XX' -r `$STRFTIME '%Y.%m.%d'` \
	-s '20XXXXXX' -r `$STRFTIME '%Y%m%d'` \
	-s '20XX' -r `$STRFTIME '%Y'` \
	-o Fairfax_base.kbitx Fairfax.kbitx \
	-o FairfaxBold_base.kbitx FairfaxBold.kbitx \
	-o FairfaxItalic_base.kbitx FairfaxItalic.kbitx \
	-o FairfaxSerif_base.kbitx FairfaxSerif.kbitx

# Generate fea
$SITELENPANA -f Fairfax_base.kbitx -i ../features/sitelenpona.txt -a ../features/spascii.fea -o ../features/spbase.fea -g glyphs.html -e Fairfax.eot -t Fairfax.ttf
$SITELENPANA -f Fairfax_base.kbitx -i ../features/titipula.txt -a ../features/tpascii.fea -o /dev/null

# Generate ttf
$BITSNPICAS convertbitmap -f ttf \
	-o Fairfax_base.ttf Fairfax_base.kbitx \
	-o FairfaxBold_base.ttf FairfaxBold_base.kbitx \
	-o FairfaxItalic_base.ttf FairfaxItalic_base.kbitx \
	-o FairfaxSerif_base.ttf FairfaxSerif_base.kbitx \
	-s 'Fairfax( Serif)?' -r '$0 Pona' \
	-o FairfaxPona_base.ttf Fairfax_base.kbitx \
	-s ' Pona' -r ' Pula' \
	-o FairfaxPula_base.ttf Fairfax_base.kbitx \
	-s ' Pula' -r ' Hax' \
	-o FairfaxHax_base.ttf Fairfax_base.kbitx \
	-o FairfaxHaxBold_base.ttf FairfaxBold_base.kbitx \
	-o FairfaxHaxItalic_base.ttf FairfaxItalic_base.kbitx \
	-o FairfaxSerifHax_base.ttf FairfaxSerif_base.kbitx \
	-s ' Hax' -r ' SM' -c \
	-o FairfaxSM_base.ttf Fairfax_base.kbitx \
	-o FairfaxSMBold_base.ttf FairfaxBold_base.kbitx \
	-o FairfaxSMItalic_base.ttf FairfaxItalic_base.kbitx \
	-o FairfaxSerifSM_base.ttf FairfaxSerif_base.kbitx

# Add OpenType features
$FONTTOOLS feaLib -o Fairfax.ttf ../features/base.fea Fairfax_base.ttf
$FONTTOOLS feaLib -o FairfaxBold.ttf ../features/base.fea FairfaxBold_base.ttf
$FONTTOOLS feaLib -o FairfaxItalic.ttf ../features/base.fea FairfaxItalic_base.ttf
$FONTTOOLS feaLib -o FairfaxSerif.ttf ../features/base.fea FairfaxSerif_base.ttf
$FONTTOOLS feaLib -o FairfaxPona.ttf ../features/asuki.fea FairfaxPona_base.ttf
$FONTTOOLS feaLib -o FairfaxPula.ttf ../features/atuki.fea FairfaxPula_base.ttf
$FONTTOOLS feaLib -o FairfaxHax.ttf ../features/code.fea FairfaxHax_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxBold.ttf ../features/code.fea FairfaxHaxBold_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxItalic.ttf ../features/code.fea FairfaxHaxItalic_base.ttf
$FONTTOOLS feaLib -o FairfaxSerifHax.ttf ../features/code.fea FairfaxSerifHax_base.ttf
cp FairfaxSM_base.ttf FairfaxSM.ttf
cp FairfaxSMBold_base.ttf FairfaxSMBold.ttf
cp FairfaxSMItalic_base.ttf FairfaxSMItalic.ttf
cp FairfaxSerifSM_base.ttf FairfaxSerifSM.ttf

# Remove intermediate artifacts
rm *_base.kbitx
rm ../features/spascii.fea
rm ../features/spbase.fea
rm ../features/tpascii.fea
rm *_base.ttf

# Inject PUAA table
PUAAFLAGS="czuowbanxkkfeypjqvgsittl --no-sylabica-2013 --sylabica-2017 --pua-a-sylabica-2013"
$BLOCKS $PUAAFLAGS > Blocks.txt
$UNIDATA $PUAAFLAGS > UnicodeData.txt
$PUAABOOK -D Blocks.txt UnicodeData.txt -I Fairfax.ttf -O pua.html
$PYPUAA compile -D Blocks.txt UnicodeData.txt \
	-I Fairfax.ttf FairfaxBold.ttf FairfaxItalic.ttf FairfaxSerif.ttf \
	-I FairfaxPona.ttf FairfaxPula.ttf \
	-I FairfaxHax.ttf FairfaxHaxBold.ttf FairfaxHaxItalic.ttf FairfaxSerifHax.ttf \
	-I FairfaxSM.ttf FairfaxSMBold.ttf FairfaxSMItalic.ttf FairfaxSerifSM.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < Fairfax.ttf > Fairfax.eot
$TTF2EOT < FairfaxBold.ttf > FairfaxBold.eot
$TTF2EOT < FairfaxItalic.ttf > FairfaxItalic.eot
$TTF2EOT < FairfaxSerif.ttf > FairfaxSerif.eot
$TTF2EOT < FairfaxPona.ttf > FairfaxPona.eot
$TTF2EOT < FairfaxPula.ttf > FairfaxPula.eot
$TTF2EOT < FairfaxHax.ttf > FairfaxHax.eot
$TTF2EOT < FairfaxHaxBold.ttf > FairfaxHaxBold.eot
$TTF2EOT < FairfaxHaxItalic.ttf > FairfaxHaxItalic.eot
$TTF2EOT < FairfaxSerifHax.ttf > FairfaxSerifHax.eot
$TTF2EOT < FairfaxSM.ttf > FairfaxSM.eot
$TTF2EOT < FairfaxSMBold.ttf > FairfaxSMBold.eot
$TTF2EOT < FairfaxSMItalic.ttf > FairfaxSMItalic.eot
$TTF2EOT < FairfaxSerifSM.ttf > FairfaxSerifSM.eot

# Create zip
zip Fairfax.zip OFL.txt Fairfax*.ttf Fairfax*.eot pua.html

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
cp FairfaxPona.ttf fairfax/fairfaxpona.ttf
cp FairfaxPona.eot fairfax/fairfaxpona.eot
cp FairfaxPula.ttf fairfax/fairfaxpula.ttf
cp FairfaxPula.eot fairfax/fairfaxpula.eot
cp FairfaxHax.ttf fairfax/fairfaxhax.ttf
cp FairfaxHax.eot fairfax/fairfaxhax.eot
cp FairfaxHaxBold.ttf fairfax/fairfaxhaxbold.ttf
cp FairfaxHaxBold.eot fairfax/fairfaxhaxbold.eot
cp FairfaxHaxItalic.ttf fairfax/fairfaxhaxitalic.ttf
cp FairfaxHaxItalic.eot fairfax/fairfaxhaxitalic.eot
cp FairfaxSerifHax.ttf fairfax/fairfaxserifhax.ttf
cp FairfaxSerifHax.eot fairfax/fairfaxserifhax.eot
cp FairfaxSM.ttf fairfax/fairfaxsm.ttf
cp FairfaxSM.eot fairfax/fairfaxsm.eot
cp FairfaxSMBold.ttf fairfax/fairfaxsmbold.ttf
cp FairfaxSMBold.eot fairfax/fairfaxsmbold.eot
cp FairfaxSMItalic.ttf fairfax/fairfaxsmitalic.ttf
cp FairfaxSMItalic.eot fairfax/fairfaxsmitalic.eot
cp FairfaxSerifSM.ttf fairfax/fairfaxserifsm.ttf
cp FairfaxSerifSM.eot fairfax/fairfaxserifsm.eot
cp Fairfax.zip fairfax/fairfax.zip
