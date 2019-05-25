#!/usr/bin/env python3

import tempfile
import subprocess
import unicodedata
import sys
import os

def usage():
	sys.exit(
		"Prints unicode chars present in a file but not the other\n"
		"Usage: {} file1 file2".format(sys.argv[0]))

if len(sys.argv) != 3:
	usage()

file1 = sys.argv[1]
file2 = sys.argv[2]

def text_file_charset(path):
	with open(path) as f:
		return set(f.read())

def pdf_file_charset(path):
	with tempfile.NamedTemporaryFile() as tmp:
		subprocess.run(["pdftotext", path, tmp.name])
		return text_file_charset(tmp.name)

def file_charset(path):
	_, ext = os.path.splitext(path)
	if ext == '.pdf':
		return pdf_file_charset(path)
	else:
		return text_file_charset(path)

def print_char(c):
	code = "U+%04X" % (ord(c))
	try:
		name = unicodedata.name(c)
	except ValueError:
		name = '?'
	print('{}\t{}\t{}'.format(c, code, name))

file1_charset = file_charset(file1)
file2_charset = file_charset(file2)

print('Chars in {} but not in {}:'.format(file1, file2))
for c in sorted(file1_charset.difference(file2_charset)):
	print_char(c)

print('Chars in {} but not in {}:'.format(file2, file1))
for c in sorted(file2_charset.difference(file1_charset)):
	print_char(c)