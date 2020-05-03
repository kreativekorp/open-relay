#!/usr/bin/env python

from __future__ import print_function

import sys

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
		for i in range(len(self.chars)):
			self.charindex[self.chars[i].name] = i
			encline = self.chars[i].get('Encoding')
			if encline is not None:
				encline = encline.split(' ')
				unimap[encline[-2]] = str(i)
				encline[-1] = str(i)
				self.chars[i].set(' '.join(encline))
		# Fix references.
		for i in range(len(self.chars)):
			for j in range(len(self.chars[i].properties)-1,-1,-1):
				line = self.chars[i].properties[j]
				if line.startswith('Refer: '):
					line = line.split(' ')
					try:
						line[1] = unimap[line[2]]
						self.chars[i].properties[j] = ' '.join(line)
					except KeyError:
						self.chars[i].properties.pop(j)

	def removeChar(self, name):
		try:
			self.chars.pop(self.charindex.pop(name))
			self.renumber()
		except KeyError:
			pass

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
				elif line == '@@@Renumber':
					self.renumber()
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
	for arg in sys.argv[1:]:
		with open(arg, 'r') as lines:
			sfd.parse(lines)
	sfd.print()

if __name__ == '__main__':
	main()
