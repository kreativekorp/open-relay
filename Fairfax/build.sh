#!/usr/bin/env bash

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

# Clean
rm -f *_base.* Fairfax*.ttf Fairfax*.eot Fairfax*.zip
rm -rf fairfax

# Generate ttf
$BITSNPICAS convertbitmap \
	-f ttf -t 0xF800 -d 0x10FF40-0x10FFC0 \
	-s '20XX[.]XX[.]XX' -r `python ../bin/strftime.py '%Y.%m.%d'` \
	-s '20XXXXXX' -r `python ../bin/strftime.py '%Y%m%d'` \
	-s '20XX' -r `python ../bin/strftime.py '%Y'` \
	-o Fairfax_base.ttf Fairfax.kbitx \
	-o FairfaxBold_base.ttf FairfaxBold.kbitx \
	-o FairfaxItalic_base.ttf FairfaxItalic.kbitx \
	-o FairfaxSerif_base.ttf FairfaxSerif.kbitx \
	-s 'Fairfax( Serif)?' -r '$0 Pona' \
	-o FairfaxPona_base.ttf Fairfax.kbitx \
	-s ' Pona' -r ' Pula' \
	-o FairfaxPula_base.ttf Fairfax.kbitx \
	-s ' Pula' -r ' Hax' \
	-o FairfaxHax_base.ttf Fairfax.kbitx \
	-o FairfaxHaxBold_base.ttf FairfaxBold.kbitx \
	-o FairfaxHaxItalic_base.ttf FairfaxItalic.kbitx \
	-o FairfaxSerifHax_base.ttf FairfaxSerif.kbitx \
	-s ' Hax' -r ' SM' -c \
	-o FairfaxSM_base.ttf Fairfax.kbitx \
	-o FairfaxSMBold_base.ttf FairfaxBold.kbitx \
	-o FairfaxSMItalic_base.ttf FairfaxItalic.kbitx \
	-o FairfaxSerifSM_base.ttf FairfaxSerif.kbitx

# Add OpenType features (Bits'n'Picas cannot do this itself)
python ../bin/sitelenpona.py -a ../features/asuki.txt -t ../features/atuki.txt -e ../features/extendable.txt -j ../features/joiners.txt -g Fairfax.kbitx
cat ../features/languages.fea ../features/sequences.fea joiners.fea ../features/variants.fea extendable.fea ../features/extensions.fea > Fairfax_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea asuki.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxPona_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea atuki.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxPula_base.fea
cat ../features/languages.fea ../features/sequences.fea joiners.fea ../features/ligatures.fea ../features/variants.fea extendable.fea ../features/extensions.fea > FairfaxHax_base.fea
rm asuki.fea atuki.fea extendable.fea joiners.fea

$FONTTOOLS feaLib -o Fairfax.ttf Fairfax_base.fea Fairfax_base.ttf
$FONTTOOLS feaLib -o FairfaxBold.ttf Fairfax_base.fea FairfaxBold_base.ttf
$FONTTOOLS feaLib -o FairfaxItalic.ttf Fairfax_base.fea FairfaxItalic_base.ttf
$FONTTOOLS feaLib -o FairfaxSerif.ttf Fairfax_base.fea FairfaxSerif_base.ttf
$FONTTOOLS feaLib -o FairfaxPona.ttf FairfaxPona_base.fea FairfaxPona_base.ttf
$FONTTOOLS feaLib -o FairfaxPula.ttf FairfaxPula_base.fea FairfaxPula_base.ttf
$FONTTOOLS feaLib -o FairfaxHax.ttf FairfaxHax_base.fea FairfaxHax_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxBold.ttf FairfaxHax_base.fea FairfaxHaxBold_base.ttf
$FONTTOOLS feaLib -o FairfaxHaxItalic.ttf FairfaxHax_base.fea FairfaxHaxItalic_base.ttf
$FONTTOOLS feaLib -o FairfaxSerifHax.ttf FairfaxHax_base.fea FairfaxSerifHax_base.ttf
cp FairfaxSM_base.ttf FairfaxSM.ttf
cp FairfaxSMBold_base.ttf FairfaxSMBold.ttf
cp FairfaxSMItalic_base.ttf FairfaxSMItalic.ttf
cp FairfaxSerifSM_base.ttf FairfaxSerifSM.ttf

rm *_base.fea
rm *_base.ttf

# Inject PUAA table
python ../bin/blocks.py czuowbanxkkfeypjqvgsittl > Blocks.txt
python ../bin/unicodedata.py czuowbanxkkfeypjqvgsittl > UnicodeData.txt
$BITSNPICAS injectpuaa \
	-D Blocks.txt UnicodeData.txt \
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
zip Fairfax.zip OFL.txt Fairfax*.ttf Fairfax*.eot

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
