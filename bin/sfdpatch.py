#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
from psname import psName, psResolve, psUnicode
import re
import sys

def dicttime(now=datetime.now()):
	iso = now.isocalendar()
	hour12 = now.hour % 12
	if hour12 == 0:
		hour12 = 12
	U = int(now.strftime('%U'), 10)
	W = int(now.strftime('%W'), 10)
	return {
		'a': now.strftime('%a'),
		'A': now.strftime('%A'),
		'b': now.strftime('%b'),
		'B': now.strftime('%B'),
		'c': now.strftime('%c'),
		'C': now.year / 100,
		'Ch': (now.year / 100) / 10,
		'Cl': (now.year / 100) % 10,
		'd': now.day,
		'dh': now.day / 10,
		'dl': now.day % 10,
		'D': now.strftime('%m/%d/%y'),
		'e': now.day,
		'eh': now.day / 10,
		'el': now.day % 10,
		'E': now.strftime('%d/%m/%y'),
		'f': now.microsecond,
		'F': now.strftime('%Y-%m-%d'),
		'g': iso[0] % 100,
		'gh': (iso[0] % 100) / 10,
		'gl': (iso[0] % 100) % 10,
		'G': iso[0],
		'h': now.strftime('%h'),
		'H': now.hour,
		'Hh': now.hour / 10,
		'Hl': now.hour % 10,
		'i': now.hour % 12,
		'ih': (now.hour % 12) / 10,
		'il': (now.hour % 12) % 10,
		'I': hour12,
		'Ih': hour12 / 10,
		'Il': hour12 % 10,
		'j': int(now.strftime('%j'), 10),
		'J': iso[0] / 100,
		'Jh': (iso[0] / 100) / 10,
		'Jl': (iso[0] / 100) % 10,
		'k': now.hour,
		'kh': now.hour / 10,
		'kl': now.hour % 10,
		'K': now.microsecond % 1000,
		'l': hour12,
		'lh': hour12 / 10,
		'll': hour12 % 10,
		'L': now.microsecond / 1000,
		'm': now.month,
		'mh': now.month / 10,
		'ml': now.month % 10,
		'M': now.minute,
		'Mh': now.minute / 10,
		'Ml': now.minute % 10,
		'n': '\n',
		'N': '\r\n',
		'p': now.strftime('%p'),
		'P': now.strftime('%P'),
		'r': now.strftime('%r'),
		'R': now.strftime('%R'),
		's': int(now.strftime('%s'), 10),
		'S': now.second,
		'Sh': now.second / 10,
		'Sl': now.second % 10,
		't': '\t',
		'T': now.strftime('%T'),
		'u': now.isoweekday(),
		'U': U,
		'Uh': U / 10,
		'Ul': U % 10,
		'v': iso[2],
		'V': iso[1],
		'Vh': iso[1] / 10,
		'Vl': iso[1] % 10,
		'w': now.weekday(),
		'W': W,
		'Wh': W / 10,
		'Wl': W % 10,
		'x': now.strftime('%x'),
		'X': now.strftime('%X'),
		'y': now.year % 100,
		'yh': (now.year % 100) / 10,
		'yl': (now.year % 100) % 10,
		'Y': now.year,
		'z': now.strftime('%z'),
		'Z': now.strftime('%Z'),
	}

class SfdChar:
	def __init__(self, name):
		self.name = name
		self.properties = []

	def append(self, prop):
		self.properties.append(prop)

	def remove(self, prop):
		try:
			self.properties.remove(prop)
		except ValueError:
			pass

	def set(self, prop):
		kv = prop.split(': ', 1)
		if len(kv) > 1:
			k = kv[0] + ': '
			for i in range(len(self.properties)):
				if self.properties[i].startswith(k):
					self.properties[i] = prop
					return i
		i = len(self.properties)
		self.properties.append(prop)
		return i

	def get(self, key):
		k = key + ': '
		for i in range(len(self.properties)):
			if self.properties[i].startswith(k):
				return self.properties[i]
		return None

	def getSplines(self):
		splines = []
		inSplineSet = False
		for prop in self.properties:
			if prop == 'EndSplineSet':
				inSplineSet = False
			elif prop == 'SplineSet':
				inSplineSet = True
			elif inSplineSet:
				splines.append(prop)
		return splines

	def removeSplines(self, includingMarkers=False):
		newProps = []
		inSplineSet = False
		for prop in self.properties:
			if prop == 'EndSplineSet':
				inSplineSet = False
				if not includingMarkers:
					newProps.append(prop)
			elif prop == 'SplineSet':
				inSplineSet = True
				if not includingMarkers:
					newProps.append(prop)
			elif not inSplineSet:
				newProps.append(prop)
		self.properties = newProps

	def appendSplines(self, splines):
		newProps = []
		for prop in self.properties:
			if prop == 'EndSplineSet':
				if splines is not None:
					for spline in splines:
						newProps.append(spline)
					splines = None
			newProps.append(prop)
		if splines is not None:
			newProps.append('SplineSet')
			for spline in splines:
				newProps.append(spline)
			newProps.append('EndSplineSet')
		self.properties = newProps

	def print(self):
		print('StartChar: ' + self.name)
		for prop in self.properties:
			print(prop)
		print('EndChar')

class Sfd:
	def __init__(self, version='3.0'):
		self.version = version
		self.properties = []
		self.encsize = 0
		self.chars = []
		self.charindex = {}

	def append(self, prop):
		self.properties.append(prop)

	def remove(self, prop):
		try:
			self.properties.remove(prop)
		except ValueError:
			pass

	def set(self, prop):
		kv = prop.split(': ', 1)
		if len(kv) > 1:
			k = kv[0] + ': '
			for i in range(len(self.properties)):
				if self.properties[i].startswith(k):
					self.properties[i] = prop
					return i
		i = len(self.properties)
		self.properties.append(prop)
		return i

	def get(self, key):
		k = key + ': '
		for i in range(len(self.properties)):
			if self.properties[i].startswith(k):
				return self.properties[i]
		return None

	def charIndex(self, name, create=False):
		try:
			return self.charindex[name]
		except KeyError:
			if create:
				i = len(self.chars)
				self.chars.append(SfdChar(name))
				self.charindex[name] = i
				return i
			return -1

	def renumber(self):
		unimap = {}
		ordmap = {}
		slotcp = 0x110000
		for i in range(len(self.chars)):
			self.charindex[self.chars[i].name] = i
			encline = self.chars[i].get('Encoding')
			if encline is not None:
				encline = encline.split(' ')
				if not encline[-2].startswith('-'):
					unimap[encline[-2]] = str(i)
				if not encline[-1].startswith('-'):
					ordmap[encline[-1]] = str(i)
				encline[-1] = str(i)
				if encline[-2].startswith('-'):
					encline[-3] = str(slotcp)
					slotcp += 1
				self.chars[i].set(' '.join(encline))
		# Fix references.
		for i in range(len(self.chars)):
			for j in range(len(self.chars[i].properties)-1,-1,-1):
				line = self.chars[i].properties[j]
				if line.startswith('Refer: '):
					line = line.split(' ')
					if line[2] in unimap:
						line[1] = unimap[line[2]]
						self.chars[i].properties[j] = ' '.join(line)
					elif line[1] in ordmap:
						line[1] = ordmap[line[1]]
						self.chars[i].properties[j] = ' '.join(line)
					else:
						self.chars[i].properties.pop(j)
				elif line.startswith('Kerns2: '):
					line = line.split(' ')
					isRef = True
					for k in range(1, len(line)):
						if line[k].endswith('"') or line[k].endswith('}'):
							isRef = True
						elif line[k].startswith('"') or line[k].startswith('{'):
							isRef = False
						elif isRef:
							line[k] = ordmap[line[k]]
							isRef = False
					self.chars[i].properties[j] = ' '.join(line)

	def removeChar(self, name):
		names = name.split(' ')
		for i in range(len(self.chars)-1,-1,-1):
			if self.chars[i].name in names:
				self.charindex.pop(self.chars[i].name)
				self.chars.pop(i)
		self.renumber()

	def sortByCodePoint(self):
		def getCodePoint(ch):
			encline = ch.get('Encoding')
			if encline is not None:
				encline = encline.split(' ')
				if not encline[-2].startswith('-'):
					return (0, int(encline[-2]), ch.name)
				if '.' in ch.name:
					cp = psUnicode(ch.name.split('.')[0])
					if cp >= 0:
						return (1, cp, ch.name)
				if not encline[-1].startswith('-'):
					return (2, int(encline[-1]), ch.name)
			return (99, -1, ch.name)
		self.chars.sort(key=getCodePoint)
		self.renumber()

	def strictMonospace(self):
		wline = None
		spidx = self.charIndex('space')
		if spidx >= 0:
			wline = self.chars[spidx].get('Width')
		if wline is None:
			wline = 'Width: 0'
		for i in range(len(self.chars)-1,-1,-1):
			if self.chars[i].get('Width') != wline:
				self.charindex.pop(self.chars[i].name)
				self.chars.pop(i)
			else:
				# Remove glyph substitution references.
				for j in range(len(self.chars[i].properties)-1,-1,-1):
					if '2: ' in self.chars[i].properties[j]:
						self.chars[i].properties.pop(j)
		self.renumber()

	def subsetRemap(self, sr):
		newChars = []
		for o, n in sr:
			ocp, ogn = psResolve(n if o is None else o)
			ncp, ngn = psResolve(o if n is None else n)
			oci = self.charIndex(ogn)
			if oci >= 0:
				oldChar = self.chars[oci]
				newChar = SfdChar(ngn)
				for prop in oldChar.properties:
					newChar.append(prop)
				newChar.set('Encoding: %d %d %d' % (ncp, ncp, len(newChars)))
				newChars.append(newChar)
		self.chars = newChars
		self.renumber()

	def sitelenPonaRename(self):
		for i in range(len(self.chars)-1,-1,-1):
			if self.chars[i].name.startswith('NameMe.'):
				baseName = None
				formName = None
				for prop in self.chars[i].properties:
					if prop.startswith('Refer: '):
						cp = int(prop.split(' ')[2])
						if cp == 0xFFA50:
							formName = '.cartouche'
						elif cp == 0xFFA51:
							formName = '.extension'
						else:
							baseName = psName(cp)
				if baseName is not None and formName is not None:
					self.charindex.pop(self.chars[i].name)
					self.charindex[baseName + formName] = i
					self.chars[i].name = baseName + formName

	def print(self):
		print('SplineFontDB: ' + self.version)
		for prop in self.properties:
			print(prop)
		print('BeginChars: %d %d' % (self.encsize, len(self.chars)))
		for ch in self.chars:
			print('')
			ch.print()
		print('EndChars')
		print('EndSplineFont')

	def parse(self, lines):
		ci = -1
		for line in lines:
			line = line.rstrip()
			if len(line) == 0:
				pass
			elif ci < 0:
				if line == 'EndSplineFont':
					pass
				elif line == 'EndChars':
					pass
				elif line.startswith('StartChar: '):
					ci = self.charIndex(line[11:], True)
				elif line.startswith('BeginChars: '):
					encsize = int(line[12:].split(' ', 1)[0])
					if self.encsize < encsize:
						self.encsize = encsize
				elif line.startswith('SplineFontDB: '):
					self.version = line[14:]
				elif line.startswith('---StartChar: '):
					self.removeChar(line[14:])
				elif line == '@@@StrictMonospace':
					self.strictMonospace()
				elif line == '@@@SortByCodePoint':
					self.sortByCodePoint()
				elif line == '@@@Renumber':
					self.renumber()
				elif line.startswith('++%'):
					self.append(datetime.now().strftime(line[3:]))
				elif line.startswith('--%'):
					self.remove(datetime.now().strftime(line[3:]))
				elif line.startswith('==%'):
					self.set(datetime.now().strftime(line[3:]))
				elif line.startswith('+++'):
					self.append(line[3:])
				elif line.startswith('---'):
					self.remove(line[3:])
				elif line.startswith('==='):
					self.set(line[3:])
				else:
					self.append(line)
			else:
				if line == 'EndChar':
					ci = -1
				elif line.startswith('@@%AppendSplines '):
					for name in (line[17:] % dicttime()).split(' '):
						scidx = self.charIndex(name)
						if scidx >= 0:
							splines = self.chars[scidx].getSplines()
							self.chars[ci].appendSplines(splines)
				elif line.startswith('@@@AppendSplines '):
					for name in line[17:].split(' '):
						scidx = self.charIndex(name)
						if scidx >= 0:
							splines = self.chars[scidx].getSplines()
							self.chars[ci].appendSplines(splines)
				elif line.startswith('@@@RemoveSplines '):
					self.chars[ci].removeSplines(int(line[17:]) > 0)
				elif line == '@@@RemoveSplines':
					self.chars[ci].removeSplines()
				elif line.startswith('+++'):
					self.chars[ci].append(line[3:])
				elif line.startswith('---'):
					self.chars[ci].remove(line[3:])
				elif line.startswith('==='):
					self.chars[ci].set(line[3:])
				else:
					self.chars[ci].append(line)

def main():
	sfd = Sfd()
	parseOpts = True
	argType = 'file'
	def parseFile(f):
		print(('Patching %s...' % f), file=sys.stderr)
		with open(f, 'r') as lines:
			sfd.parse(lines)
	def parseSubsetRemap(f):
		print(('Patching %s...' % f), file=sys.stderr)
		with open(f, 'r') as lines:
			for line in lines:
				line = line.split('#')[0].strip()
				if line:
					line = re.split(r'\s+', line)
					f0 = line[0] if len(line) > 0 else None
					f1 = line[1] if len(line) > 1 else None
					yield f0, f1
	for arg in sys.argv[1:]:
		if parseOpts and arg.startswith('-'):
			if arg == '--':
				parseOpts = False
			elif arg == '-f' or arg == '--file':
				argType = 'file'
			elif arg == '-c' or arg == '--command':
				argType = 'command'
			elif arg == '-r' or arg == '--removeChar':
				argType = 'removeChar'
			elif arg == '-sr' or arg == '--subsetRemap':
				argType = 'subsetRemap'
			elif arg == '-n' or arg == '--renumber':
				sfd.renumber()
			elif arg == '-s' or arg == '--sortByCodePoint':
				sfd.sortByCodePoint()
			elif arg == '-m' or arg == '--strictMonospace':
				sfd.strictMonospace()
			elif arg == '-sp' or arg == '--sitelenPonaRename':
				sfd.sitelenPonaRename()
			elif arg == '--marks':
				for ch in sfd.chars:
					zw = False
					hg = False
					for prop in ch.properties:
						if prop == 'Width: 0':
							zw = True
						if prop == 'SplineSet':
							hg = True
						if prop.startswith('Refer: '):
							hg = True
					if zw and hg:
						print(ch.name)
				sys.exit()
			elif arg.startswith('-f='):
				parseFile(arg[3:])
			elif arg.startswith("--file="):
				parseFile(arg[7:])
			elif arg.startswith('-c='):
				sfd.parse(arg[3:].split(';'))
			elif arg.startswith('--command='):
				sfd.parse(arg[10:].split(';'))
			elif arg.startswith('-r='):
				sfd.removeChar(arg[3:])
			elif arg.startswith('--removeChar='):
				sfd.removeChar(arg[13:])
			elif arg.startswith('-sr='):
				sfd.subsetRemap(parseSubsetRemap(arg[4:]))
			elif arg.startswith('--subsetRemap='):
				sfd.subsetRemap(parseSubsetRemap(arg[14:]))
			else:
				print(('Unknown option: %s' % arg), file=sys.stderr)
		elif argType == 'subsetRemap':
			sfd.subsetRemap(parseSubsetRemap(arg))
		elif argType == 'removeChar':
			sfd.removeChar(arg)
		elif argType == 'command':
			sfd.parse(arg.split(';'))
		else:
			parseFile(arg)
	sfd.print()

if __name__ == '__main__':
	main()
