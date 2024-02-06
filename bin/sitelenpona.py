#!/usr/bin/env python

from __future__ import print_function
from psname import psName, psNames
import re
import sys

class AsukiLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip(), 1)
		self.outputPsName = fields[0]
		self.inputPsNames = psNames(fields[1])
		self.sortKey = (-len(self.inputPsNames), fields[1])
		rule = 'sub %s by %s;' % (' '.join(self.inputPsNames), self.outputPsName)
		self.subRule = rule if self.comment is None else '%s  # %s' % (rule, self.comment)
		rule = 'sub %s space by %s;' % (' '.join(self.inputPsNames), self.outputPsName)
		self.subRuleSpace = rule if self.comment is None else '%s  # %s' % (rule, self.comment)

def readAsukiSource(filename):
	asuki = {}
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				a = AsukiLine(index, line)
				if a.sortKey[0] not in asuki:
					asuki[a.sortKey[0]] = {}
				asuki[a.sortKey[0]][a.sortKey[1]] = a
				index += 1
	return asuki

def writeAsukiFeatures(filename, asuki):
	with open(filename, 'w') as f:
		f.write('feature liga {\n\n')
		for sk0 in sorted(asuki.keys()):
			f.write('  # Sequences of length %d (%d + space)\n' % (1-sk0, -sk0))
			for sk1 in sorted(asuki[sk0].keys()):
				f.write('  %s\n' % asuki[sk0][sk1].subRuleSpace)
			f.write('\n')
			f.write('  # Sequences of length %d\n' % -sk0)
			for sk1 in sorted(asuki[sk0].keys()):
				f.write('  %s\n' % asuki[sk0][sk1].subRule)
			f.write('\n')
		f.write('} liga;\n')

def readSFDGlyphNames(filename):
	glyphNames = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if line.startswith('StartChar: '):
				line = line.split(' ', 1)[1]
				glyphNames.append(line)
	return glyphNames

def readKbitxGlyphNames(filename):
	glyphNames = []
	with open(filename, 'r') as f:
		for line in f:
			m = re.search('<g ([un])="([^\"]+)"', line)
			if m:
				if m.group(1) == 'u':
					glyphNames.append(psName(int(m.group(2))))
				if m.group(1) == 'n':
					glyphNames.append(m.group(2))
	return glyphNames

def readGlyphNames(filename):
	if filename.endswith('.sfd'):
		return readSFDGlyphNames(filename)
	if filename.endswith('.kbitx'):
		return readKbitxGlyphNames(filename)
	raise ValueError(filename)

def kijeExtensionTriples(glyphNames):
	for gn in glyphNames:
		ext = '%s.kijext' % gn
		end = '%s.kijend' % gn
		if ext in glyphNames and end in glyphNames:
			yield gn, ext, end

class ExtendableLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip())
		self.base = fields[0] if len(fields) > 0 and fields[0][0] != '-' else None
		self.forward = fields[1] if len(fields) > 1 and fields[1][0] != '-' else None
		self.reverse = fields[2] if len(fields) > 2 and fields[2][0] != '-' else None
		self.both = fields[3] if len(fields) > 3 and fields[3][0] != '-' else None
		self.kijeReverse = fields[4] if len(fields) > 4 and fields[4][0] != '-' else None
		self.kijeBoth = fields[5] if len(fields) > 5 and fields[5][0] != '-' else None

	def wrap(self, text, additional=None):
		if text is not None:
			if self.comment is not None:
				if additional is not None:
					return '%s  # %s, %s' % (text, self.comment, additional)
				return '%s  # %s' % (text, self.comment)
			if additional is not None:
				return '%s  # %s' % (text, additional)
		return text

def readExtendableSource(filename):
	extendable = []
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				e = ExtendableLine(index, line)
				extendable.append(e)
				index += 1
	return extendable

def forwardExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.forward is not None:
			yield e.wrap(e.base), e.wrap(e.forward)
	for e in extendable:
		if e.reverse is not None and e.both is not None:
			yield e.wrap(e.reverse, 'reverse-extended'), e.wrap(e.both, 'reverse-extended')
	for e in extendable:
		if e.kijeReverse is not None and e.kijeBoth is not None:
			yield e.wrap(e.kijeReverse, 'reverse-extended'), e.wrap(e.kijeBoth, 'reverse-extended')

def reverseExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.reverse is not None:
			yield e.wrap(e.base), e.wrap(e.reverse)
	for e in extendable:
		if e.forward is not None and e.both is not None:
			yield e.wrap(e.forward, 'extended'), e.wrap(e.both, 'extended')

def kijeExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.kijeReverse is not None:
			yield e.wrap(e.base), e.wrap(e.kijeReverse)
	for e in extendable:
		if e.forward is not None and e.kijeBoth is not None:
			yield e.wrap(e.forward, 'extended'), e.wrap(e.kijeBoth, 'extended')

def writeExtendableFeatures(filename, glyphNames, extendable):
	with open(filename, 'w') as f:
		f.write('# all glyphs that can be included in a cartouche\n')
		f.write('@spCartoucheless = [%s];\n\n' % ' '.join(gn.rsplit('.', 1)[0] for gn in glyphNames if gn.endswith('.cartouche')))
		f.write('# corresponding glyphs with cartouche extension\n')
		f.write('@spCartouche = [%s];\n\n' % ' '.join(gn for gn in glyphNames if gn.endswith('.cartouche')));
		f.write('# all glyphs that can be included in a long glyph\n')
		f.write('@spExtensionless = [%s];\n\n' % ' '.join(gn.rsplit('.', 1)[0] for gn in glyphNames if gn.endswith('.extension')))
		f.write('# corresponding glyphs with long glyph extension\n')
		f.write('@spExtension = [%s];\n\n' % ' '.join(gn for gn in glyphNames if gn.endswith('.extension')))
		f.write('# sitelen pona ideographs that can be made long on the right side\n')
		f.write('@spExtendable = [\n%s];\n\n' % ''.join('  %s\n' % a for a, e in forwardExtendablePairs(extendable)))
		f.write('# corresponding glyphs made long on the right side\n')
		f.write('@spExtended = [\n%s];\n\n' % ''.join('  %s\n' % e for a, e in forwardExtendablePairs(extendable)))
		f.write('# sitelen pona ideographs that can be made long on the left side\n')
		f.write('@spReverseExtendable = [\n%s];\n\n' % ''.join('  %s\n' % a for a, e in reverseExtendablePairs(extendable)))
		f.write('# corresponding glyphs made long on the left side\n')
		f.write('@spReverseExtended = [\n%s];\n\n' % ''.join('  %s\n' % e for a, e in reverseExtendablePairs(extendable)))
		f.write('# reverse long glyph extension for kijetesantakalu\n')
		f.write('@spKijeExtensionless = [%s];\n' % ' '.join(gn for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtension = [%s];\n' % ' '.join(ext for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtensionEnd = [%s];\n' % ' '.join(end for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtendable = [\n%s];\n' % ''.join('  %s\n' % a for a, e in kijeExtendablePairs(extendable)))
		f.write('@spKijeExtended = [\n%s];\n' % ''.join('  %s\n' % e for a, e in kijeExtendablePairs(extendable)))

class JoinerLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip(), 1)
		self.outputPsName = fields[0]
		self.inputSource = fields[1]
		self.inputSourceItems = [fields[1]]
		self.inputSourceDelim = None
		self.inputSourceJoiner = None
		for delim, joiner in [('-','uni200D'),('+','uni200D'),('^','uF1995'),('*','uF1996')]:
			if delim in fields[1]:
				self.inputSourceItems = fields[1].split(delim)
				self.inputSourceDelim = delim
				self.inputSourceJoiner = joiner

	def subRule(self, nimi, includeComment=True):
		joiner = ' %s ' % self.inputSourceJoiner
		names = [i[1:] if i[0] == '\\' else nimi[i] for i in self.inputSourceItems]
		rule = 'sub %s by %s;' % (joiner.join(names), self.outputPsName)
		return rule if self.comment is None or not includeComment else '%s  # %s' % (rule, self.comment)

	def sortKey(self, nimi):
		return (
			(
				-len(self.inputSourceItems),
				self.inputSourceJoiner != 'uni200D',
				None if self.comment is None else '+' in self.comment
			),
			self.subRule(nimi, False)
		)

def readJoinerSource(filename, joiners=None, nimi=None):
	if joiners is None:
		joiners = {}
	if nimi is None:
		nimi = {}
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				j = JoinerLine(index, line)
				if j.inputSourceDelim is None:
					nimi[j.inputSource] = j.outputPsName
				elif j.inputSourceDelim != '+':
					sk = j.sortKey(nimi)
					if sk[0] not in joiners:
						joiners[sk[0]] = {}
					if sk[1] not in joiners[sk[0]]:
						joiners[sk[0]][sk[1]] = j
				index += 1
	return joiners, nimi

def writeJoinerFeatures(filename, joiners, nimi):
	with open(filename, 'w') as f:
		f.write('feature liga {\n\n')
		for sk0 in sorted(joiners.keys()):
			if sk0[2]:
				pass
			elif sk0[1]:
				f.write('  # Sequences of length %d, using stacking or scaling joiners\n' % -sk0[0])
			else:
				f.write('  # Sequences of length %d, using zero width joiners\n' % -sk0[0])
			for sk1 in sorted(joiners[sk0].keys()):
				f.write('  %s\n' % joiners[sk0][sk1].subRule(nimi))
			f.write('\n')
		f.write('} liga;\n')

def main(args):
	# Default arguments
	asukiSrc = 'asuki.txt'
	asukiOut = 'asuki.fea'
	atukiSrc = 'atuki.txt'
	atukiOut = 'atuki.fea'
	extendableSrc = 'extendable.txt'
	extendableOut = 'extendable.fea'
	joinerSrc = 'joiners.txt'
	joinerOut = 'joiners.fea'
	glyphNameSrc = None
	# Parse arguments
	argType = None
	for arg in args:
		if argType is not None:
			if argType == '-a':
				asukiSrc = arg
			if argType == '-A':
				asukiOut = arg
			if argType == '-t':
				atukiSrc = arg
			if argType == '-T':
				atukiOut = arg
			if argType == '-e':
				extendableSrc = arg
			if argType == '-E':
				extendableOut = arg
			if argType == '-j':
				joinerSrc = arg
			if argType == '-J':
				joinerOut = arg
			if argType == '-g':
				glyphNameSrc = arg
			argType = None
		elif arg.startswith('-'):
			if arg in ['-a', '-A', '-t', '-T', '-e', '-E', '-j', '-J', '-g']:
				argType = arg
			else:
				print(('Unknown option: %s' % arg), file=sys.stderr)
		else:
			glyphNameSrc = arg
	# Build
	if glyphNameSrc is None:
		print('No source font provided', file=sys.stderr)
	else:
		asuki = readAsukiSource(asukiSrc)
		writeAsukiFeatures(asukiOut, asuki)
		atuki = readAsukiSource(atukiSrc)
		writeAsukiFeatures(atukiOut, atuki)
		glyphNames = readGlyphNames(glyphNameSrc)
		extendable = readExtendableSource(extendableSrc)
		writeExtendableFeatures(extendableOut, glyphNames, extendable)
		joiners, nimi = readJoinerSource(asukiSrc)
		joiners, nimi = readJoinerSource(joinerSrc, joiners, nimi)
		writeJoinerFeatures(joinerOut, joiners, nimi)

if __name__ == '__main__':
	main(sys.argv[1:])
