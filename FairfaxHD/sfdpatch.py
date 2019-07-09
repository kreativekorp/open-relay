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
