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
rm -f Constructium.sfd-* Constructium.ttf Constructium.eot Constructium.zip ConstructiumTmp.*
rm -rf constructium

# Make timestamped version
python ../bin/sfdpatch.py Constructium.sfd patches/timestamp.txt > ConstructiumTmp.sfd

# Generate ttf
$FONTFORGE -lang=ff -c 'i = 1; while (i < $argc); Open($argv[i]); Generate($argv[i]:r + ".ttf", "", 0); i = i+1; endloop' \
	ConstructiumTmp.sfd
mv ConstructiumTmp.ttf Constructium.ttf
rm ConstructiumTmp.sfd

# Inject PUAA table
python ../bin/blocks.py cwadkkypqvt > Blocks.txt
python ../bin/unicodedata.py cwadkkypqvt > UnicodeData.txt
$BITSNPICAS injectpuaa \
	-D Blocks.txt UnicodeData.txt \
	-I Constructium.ttf
rm Blocks.txt UnicodeData.txt

# Convert to eot
$TTF2EOT < Constructium.ttf > Constructium.eot

# Create zip
zip Constructium.zip OFL.txt Constructium.sfd Constructium.ttf Constructium.eot

# Create lowercase versions
mkdir constructium
cp Constructium.ttf constructium/constructium.ttf
cp Constructium.eot constructium/constructium.eot
cp Constructium.zip constructium/constructium.zip
