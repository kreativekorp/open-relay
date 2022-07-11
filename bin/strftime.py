#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
import sys

def main():
	now = datetime.now()
	for arg in sys.argv[1:]:
		print(now.strftime(arg))

if __name__ == '__main__':
	main()
