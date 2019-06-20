#!/usr/bin/env python3

import string
import unicodedata

letters = []
letters += string.ascii_lowercase
letters += [
	'æ','œ',('ẞ', 'ß'), 'þ','ð','ŋ','ĳ','ʒ', 'ə',
	('İ', 'ı'), ('ϴ', None), (None, 'ʼ'), (None, 'ſ')
]

for row in letters:
	if type(row) is str:
		row = (row.upper(), row)
	codes = ["U+%04X" % (ord(c)) for c in row if c]
	names = [unicodedata.name(c) for c in row if c]
	names = [name.replace('LATIN CAPITAL ', '') for name in names]
	names = [name.replace('LATIN SMALL ', '') for name in names]
	unique_names = []
	[unique_names.append(name) for name in names if not name in unique_names]

	print("    ({}, {}), # {} ({})".format(
			repr(row[0]), repr(row[1]),
			', '.join(codes), ', '.join(unique_names)
		))

chars = '&©®™ªº§@'
for c in chars:
	code = "U+%04X" % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {} ({})".format(repr(c), code, name))

chars = ['0⁰₀','1¹₁','2²₂','3³₃','4⁴₄','5⁵₅','6⁶₆','7⁷₇','8⁸₈','9⁹₉']

for c in chars:
	sym = c[0]
	row = (c[1], c[2])
	codes = ["U+%04X" % (ord(c)) for c in (c[0], c[1], c[2])]
	print("    {}: {}, # {}".format(repr(sym), repr(row), ', '.join(codes)))

for c in chars:
	combination = ("◌̂", c[0])
	dst = c[1]
	code = "U+%04X" % (ord(dst))
	print("    {}: {}, # {}".format(repr(combination), repr(dst), code))

for c in chars:
	combination = ("◌̌", c[0])
	dst = c[2]
	code = "U+%04X" % (ord(dst))
	print("    {}: {}, # {}".format(repr(combination), repr(dst), code))

chars = '#%+/<=>\\^_`|~°±¼½×÷‰∓≤≥≠≃≄√∞µ'

for c in chars:
	code = "U+%04X" % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {} ({})".format(repr(c), code, name))

chars = [
('A','α','Α'),
('B','β','Β'),
('G','γ','Γ'),
('D','δ','Δ'),
('E','ε','Ε'),
('Z','ζ','Ζ'),
('H','η','Η'),
('U','θ','Θ'),
('I','ι','Ι'),
('K','κ','Κ'),
('L','λ','Λ'),
('M','μ','Μ'),
('N','ν','Ν'),
('J','ξ','Ξ'),
('O','ο','Ο'),
('P','π','Π'),
('R','ρ','Ρ'),
('S','σ','Σ'),
('W','ς',None),
('T','τ','Τ'),
('Y','υ','Υ'),
('F','φ','Φ'),
('X','χ','Χ'),
('C','ψ','Ψ'),
('V','ω','Ω')]

chars.sort()

for row in chars:
	sym = row[0]
	out = (row[1], row[2])
	codes = ["U+%04X" % (ord(c)) for c in out if c]
	name = unicodedata.name(row[1]).replace('GREEK SMALL LETTER ', '')
	print("    {}: {}, # {} ({})".format(repr(sym), repr(out), ', '.join(codes), name))

chars = '!"\'*,-.:;?¡§·¿‑–—’†‡…'

for c in chars:
	code = "U+%04X" % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {} ({})".format(repr(c), code, name))

chars = '()[]{}«»‹›‚‘“”„'

for c in chars:
	code = "U+%04X" % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {} ({})".format(repr(c), code, name))

chars = '\u0020\u00A0\u202F\u2003'

for c in chars:
	code = '"\\u%04X"' % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {}".format(code, name))


chars = '€$£'

for c in chars:
	code = "U+%04X" % (ord(c))
	name = unicodedata.name(c)
	print("    {}, # {} ({})".format(repr(c), code, name))

chars = [
('B', '฿', None, None, None),
('P', '₱', '₧', '₰', None),
('D', '₫', '₯', None, None),
('L', '₺', '₤', '₾', None),
('W', '₩', None, None, None),
('A', None, '₳', None, None),
('E', '₠', None, None, '¤'),
('C', '¢', '₵', '₢', '₡'),
('T', '₸', '₮', None, None),
('S', '₪', '₷', None, None),
('R', '₽', '₹', '₨', None),
('N', '₦', None, None, None),
('M', '₥', 'ℳ', '₼', None),
('Y', '¥', None, None, None),
('K', '₭', None, None, None),
('G', '₲', None, None, None),
('H', '₴', None, None, None),
('F', 'ƒ', '₣', None, None),
]
chars.sort()

for row in chars:
	sym = row[0]
	out = (row[1], row[2], row[3], row[4])
	codes = ["U+%04X" % (ord(c)) for c in out if c]
	print("    {}: {}, # {}".format(repr(sym), repr(out), ', '.join(codes)))


chars = "◌̀◌́◌̂◌̃◌̄◌̆◌̇◌̈◌̊◌̋◌̌◌̦◌̧◌̨◌̵◌̸◌̏◌̑◌̣◌̱"
for c in chars:
	if c == "◌":
		continue
	visual = "◌" + c
	name = unicodedata.name(c).replace('COMBINING ', '')
	print("    {}, # {}".format(repr(visual), name))
