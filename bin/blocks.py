#!/usr/bin/env python

from __future__ import print_function
import sys

args = ''.join(sys.argv[1:])

# cf
if 'c' in args: # uCsur
	print ("""
E000..E07F; Tengwar
E080..E0FF; Cirth
E100..E14F; Engsvanyali
E150..E1AF; Kinya
E1B0..E1CF; Ilianore
E1D0..E1FF; Syai
E200..E26F; Verdurian
E270..E28F; Aui
E290..E2BF; Amman-Iar
E2C0..E2CF; Streich
E2D0..E2FF; Xaini
E300..E33F; Mizarian
E340..E35F; Zirinka
E360..E37F; Sarkai
E380..E3AF; Thelwik
E3B0..E3FF; Olaetyan
E400..E42F; Niskloz
E430..E44F; Kazat Akkorou
E450..E46F; Kazvarad
E470..E48F; Zarkhand
E490..E4BF; Rozhxh
E4C0..E4EF; Serivelna
E4F0..E4FF; Kelwathi
E500..E51F; Saklor
E520..E54F; Rynnan
E550..E57F; Alzetjan
E580..E59F; Telarasso
E5A0..E5BF; Ssuraki
E5C0..E5DF; Gargoyle
E5E0..E5FF; Ophidian
E600..E62F; Ferengi
E630..E64F; Seussian Latin Extensions
E650..E67F; Sylabica
E680..E6CF; Ewellic
E6D0..E6EF; Amlin
E6F0..E73F; Unifon Extended
E740..E76F; Unifon
E770..E77F; Solresol
E780..E7FF; Visible Speech
E800..E82F; Monofon
E830..E88F; Dni
E890..E8DF; Aurebesh
E8E0..E8FF; Tonal
E900..E97F; Glaitha-A
E980..E9FF; Glaitha-B
EA00..EA9F; Lhenazi
EAA0..EAFF; Wanya
EB00..EB3F; Orokin
EB40..EB5F; Standard Galactic
EB60..EB9F; Braille Extended
EBA0..EBDF; Cistercian Numerals
EBE0..EBEF; Lapointe Hexadecimal Numerals
EBF0..EBFF; Martin Hexadecimal Numerals
EC00..EC2F; Cylenian
EC30..EC6F; Syrrin
EC70..ECEF; Graflect
ECF0..ECFF; Whitaker Hexadecimal Numerals
ED00..ED3F; Deini
ED40..ED7F; Niji
ED80..EDAF; Iranic
EDB0..EDDF; Tassarunese
EDE0..EDEF; Zese
EDF0..EDFF; Grawlixes
""")

# fs
if 'z' in args: # Zvbi
	print('EE00..EE7F; Block Sextants (Compatible with ZVBI)')

# fs
if 'u' in args: # Unscii
	print('EE80..EEFF; Block Sextants (Compatible with Unscii)')

# fs
if 'o' in args: # Octets
	print('EF00..EFFF; Hex Byte Pictures')

# cf
if 'w' in args: # kamakaWi
	if 'm' in args: # Modular
		raise ValueError('cannot have both w and m')
	print('F000..F1FF; Kamakawi')

# s
if 'm' in args: # Modular
	if 'w' in args: # kamakaWi
		raise ValueError('cannot have both w and m')
	print('F000..F0FF; Modular Font Elements')
	print('F100..F1FF; Modular Font Elements Extended')

# fs
if 'b' in args: # Blocks
	print("""
F200..F20F; Box Drawing Extended
F210..F23F; Fill Patterns
F240..F27F; Shade Quadrants
F280..F2BF; Sixel Graphics
F2C0..F2FF; Block Sextants
F300..F3FF; Block Octants
F400..F43F; C1 Control Pictures
""")

# cf
if 'a' in args: # Ath
	print('F4C0..F4EF; Ath')

# f
if 'n' in args: # Nishikiteki
	print('F500..F54F; Kodo Symbols')
	print('F550..F55F; Mathematical Symbols Appendix')

# cf
if 'n' in args or 'd' in args: # Nishikiteki/Duodecimal
	print('F560..F56F; Camp Duodecimal Numerals')

# f
if 'n' in args: # Nishikiteki
	print('F570..F57F; Tally Marks')
	print('F580..F58F; Geomantic Figures')

# fs
if 'x' in args: # commander X16
	print('F590..F5BF; C64-OS Symbols')
	print('F5C0..F5FF; Commander X16 Symbols')

# cfs
if 'k' in args: # Kreative
	print('F600..F61F; Kreative Software Private Use-F6')

# f
if 'f' in args: # Fairfax
	print('F620..F67F; Fairfax Presentation Variants-A')

# fs
if 'e' in args: # mousEtext
	print('F680..F69F; Apple MouseText Characters')

# f
if 'f' in args: # Fairfax
	print('F6A0..F6FF; Fairfax Presentation Variants-B')

# cfs
if 'k' in args: # Kreative
	print('F700..F7FF; Kreative Software Private Use-F7')
	print('F800..F89F; Kreative Software Private Use-F8')

# cf
if 'c' in args: # uCsur
	print('F8A0..F8CF; Aiha')

# cfs
if 'c' in args or 'h' in args: # uCsur/tlhinganHol
	print('F8D0..F8FF; Klingon')

# cf
if 'c' in args: # uCsur
	print("""
F0000..F0E6F; Kinya Syllables
F0E70..F16AF; Pikto
F16B0..F16DF; Derani
F1700..F18FF; Semtog
F1900..F19FF; Sitelen Pona
F1B00..F1C3F; Shidinn
F1C40..F1C7F; Titi Pula
""")

# cf
if 'p' in args: # Presentationforms
	print('FA700..FA71F; Modifier Tone Letter Presentation Forms')
	print('FA720..FA7FF; Latin Presentation Forms')

# cf
if 'y' in args: # bettYboop
	print('FB000..FB00F; Betty Boop')

# cf
if 'p' in args: # Presentationforms
	print("""
FE000..FE07F; Tengwar Presentation Forms
FE400..FE42F; Niskloz Presentation Forms
FE5E0..FE5FF; Ophidian Presentation Forms
FE680..FE6CF; Ewellic Presentation Forms
""")

# cfs
if 'k' in args: # Kreative
	print('FF000..FF02F; Kreative Software Private Use-FF0')
	if 'kk' in args:
		print('FF030..FF09F; Domino Tiles Extended')
		print('FF0A0..FF0DF; Powerline Symbols')
		print('FF0E0..FF0FF; Rayalaka Color Symbols')
	print('FF100..FF1FF; Kreative Software Private Use-FF1')

# cf
if 'j' in args: # tahano veno (aJeri)
	print('FF380..FF3BF; Tahano Veno')

# cf
if 'q' in args: # QolumbiareQords
	print('FF3C0..FF3FF; Aliphbepf')

# cf
if 'v' in args: # Voynich
	print('FF400..FF51F; Voynich')

# cf
if 'g' in args: # jurGenschmidt
	print('FF600..FF64F; Jurgenschmidt')

# cf
if 'p' in args: # Presentationforms
	print('FF6B0..FF6DF; Derani Presentation Forms')

# fs
if 's' in args: # SevenSegment
	print('FF700..FF7FF; Seven-Segment Display Patterns')

# cfs
if 'i' in args and 'k' in args: # pIco-eIght, Kreative
	print('FF800..FF80F; PICO-8 Symbols')
	print('FF810..FF89F; Number Forms Appendix')
elif 'i' in args: # pIco-eIght
	print('FF800..FF81F; PICO-8 Symbols')
elif 'k' in args: # Kreative
	print('FF810..FF89F; Number Forms Appendix')

# cf
if 'p' in args: # Presentationforms
	print('FF8A0..FF8CF; Aiha Presentation Forms')

# cf
if 't' in args: # Tokipona
	if 'tt' in args:
		print('FF900..FFABF; Sitelen Pona Presentation Forms-A')
		print('FFAC0..FFBFF; Sitelen Pona Presentation Forms-B')
	else:
		print('FF900..FFABF; Sitelen Pona Presentation Forms')

# fs
if 'l' in args: # Legacycomputing
	print('FFC00..FFCFF; Symbols for Legacy Computing Appendix')

# cf
if 't' in args: # Tokipona
	if 'tt' in args:
		print('FFD00..FFDFF; Sitelen Pona Presentation Forms-C')
