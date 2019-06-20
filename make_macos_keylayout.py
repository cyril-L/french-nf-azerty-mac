#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
import re

from references import nf_z71_300 as nf
from references import iso_cei_9995_11 as iso9995_11
from references import iso_cei_9995_1 as iso9995_1

# The keylayout file format is described in Apple Technical Note TN2056.
# https://developer.apple.com/library/archive/technotes/tn2056/_index.html
#
# Here we start from a reference layout provided by Ukulele, mainly to keep
# mappings for keys outside the alphanumeric section, which are not defined
# in NF Z71-300.
#
# We need to strip some entities that ElementTree won’t parse, like &#x0008;
# Those will be set back before writing to disk.

with open('./references/macos/French.keylayout', 'r') as f:
    keylayout = f.read()
keylayout = keylayout.replace('&#x', '#x')
keylayout = ET.fromstring(keylayout)

# Redefines metadata

# TODO id uniqueness + bundle consistency?
keylayout.attrib['id'] = "-10798"
keylayout.attrib['name'] = "French - NF"
keylayout.attrib['maxout'] = "2"

# Redefines our modifier keymap selections.
# It tells which keymap is selected depending on modifier combinations.
#
# <modifierMap id="commonModifiers" defaultIndex="0">
#   <keyMapSelect mapIndex="0">
#       <modifier keys="command? anyControl?"/>
#   </keyMapSelect>
#   <keyMapSelect mapIndex="1">
#       <modifier keys="anyShift command? anyControl?"/>
#   </keyMapSelect>
#  [...]
# </modifierMap>

modifier_map = keylayout.find("modifierMap")
for key_map_select in list(modifier_map):
    modifier_map.remove(key_map_select)

for index, keys in [
        ('0', "command? anyControl?"), # Default layer
        ('1', "anyShift command? anyControl?"), # Shift pressed
        ('2', "anyOption command? anyControl?"), # AltGr pressed
        ('3', "anyShift anyOption command? anyControl?"), # AltGr + Shift pressed
        # Same sequence with Caps Lock toggled
        ('4', "caps command? anyControl?"),
        ('5', "anyShift caps command? anyControl?"),
        ('6', "caps anyOption command? anyControl?"),
        ('7', "anyShift caps anyOption command? anyControl?"),
]:
    key_map_select = ET.SubElement(modifier_map, "keyMapSelect", mapIndex=index)
    ET.SubElement(key_map_select, "modifier", keys=keys)

# Redefines actions.
#
# Actions are defined when a key can output different chars when
# preceeded by a dead key. We identify them with the char output
# when no state is selected.
#
# <action id="s">
#   <when output="s" state="none"/>
#   <when output="s̀" state="◌̀"/>
#   <when output="ś" state="◌́"/>
#   [...]
#   <when output="σ" state="◌µ"/>
#   <when output="₪" state="◌¤"/>
#   <when output="ſ" state="◌Eu"/>
#  </action>

# Compute greek combinations
# Defined by mapping a capital latin letter to both cases of greek letters

actions = keylayout.find("actions")
for action in list(actions):
    actions.remove(action)

combinations = {}

for other in [
        iso9995_11.special_chars_from_dead_keys,
        nf.latin_letters_with_diacritics,
        nf.special_chars_from_diacritics,
]:
    combinations.update(other)

def add_combination_by_key(dead_key, key, mappings):
    for i, keymap in enumerate([
            nf.azerty_group1_level1,
            nf.azerty_group1_level2,
            nf.azerty_group2_level1,
            nf.azerty_group2_level2,
    ]):
        if len(mappings) > i and mappings[i]:
            combinations[(dead_key, keymap[key])] = mappings[i]

latin_letter_keys = {v: k for k, v in nf.azerty_group1_level2.items()}
def add_combination_by_letter(dead_key, upper_letter, mappings):
    key = latin_letter_keys[upper_letter]
    add_combination_by_key(dead_key, key, mappings)

for latin_upper, currency_symbols in nf.extended_currency_symbols.items():
    add_combination_by_letter('◌¤', latin_upper, currency_symbols)

for latin_upper, greek_letters in nf.greek_letters.items():
    add_combination_by_letter('◌µ', latin_upper, greek_letters)

for latin_upper, extended_letters in nf.extended_latin_letters.items():
    add_combination_by_letter('◌Eu', latin_upper, extended_letters)

for key, extended_symbols in nf.extended_latin_symbols.items():
    add_combination_by_key('◌Eu', key, extended_symbols)
    extended_lower, extended_upper = extended_symbols

for space in [' ', '\u00A0']:
    for dead_key in nf.supported_diacritics:
        combinations[(dead_key, space)] = iso9995_11.get_spacing_clone(dead_key)
    combinations[('◌¤', space)] = '¤'
    combinations[('◌µ', space)] = 'µ'
    combinations[('◌Eu', space)] = 'Eu'

def xpath_str(s):
    return ('"{}"' if "'" in s else "'{}'").format(s)

def add_action_state(action_id, state, output=None, nxt=None):
    action = actions.find(".//action[@id = {}]".format(xpath_str(action_id)))
    if not action:
        action = ET.SubElement(actions, "action", id=action_id)
    when = ET.SubElement(action, "when", state=state)
    if output:
        when.attrib['output'] = output
    if nxt:
        when.attrib['next'] = nxt

for combination, output in combinations.items():
    state, action = combination
    if not '◌' in output: # Do not support chained dead keys for now
        add_action_state(action, state, output=output)

for dead_key in nf.supported_diacritics + ['◌µ', '◌¤', '◌Eu']:
    add_action_state(dead_key, 'none', nxt=dead_key)

for action in list(actions.findall("action")):
    if not '◌' in action.attrib['id']:
        add_action_state(action.attrib['id'], 'none', output=action.attrib['id'])

# Redefines terminators.
#
# Terminators are characters output when a dead key have been pressed,
# but no combinations where defined with the following key.
#
# <terminators>
#   <when state="◌̀" output="`"/>
#   <when state="◌́" output="´"/>
#   <when state="◌̂" output="^"/>
#   <when state="◌̃" output="~"/>
#   <when state="◌̄" output="¯"/>
#   [...]
# </terminators>

terminators = keylayout.find("terminators")
for terminator in list(terminators):
    terminators.remove(terminator)

def add_terminator(terminators, state, output):
    when = ET.SubElement(terminators, "when", state=state)
    when.attrib['output'] = output

for dead_key in nf.supported_diacritics:
    add_terminator(terminators, dead_key, iso9995_11.get_spacing_clone(dead_key))

add_terminator(terminators, '◌µ', 'µ')
add_terminator(terminators, '◌¤', '¤')
add_terminator(terminators, '◌Eu', 'Eu')

# Redefines keymaps
#
# - Save default outputs from Ukulele for non alphanumeric keys
# - Map keylaout alphanumeric keycodes to ISO keycodes.
# - Generate keymaps for Caps Lock, using Shift to revert its
#   when hit together.

level1_defaults = OrderedDict()
level2_defaults = OrderedDict()

def parse_key_map(index):
    key_map = OrderedDict()
    for key in keylayout.findall(".//keyMap[@index='{}']/key".format(index)):
        if 'output' in key.attrib:
            out = key.attrib['output']
        else:
            out = key.attrib['action']
        key_map[key.attrib['code']] = out
    return key_map

level1_defaults = parse_key_map('0')
level2_defaults = parse_key_map('1')

key_map_set = keylayout.find("keyMapSet")
for key_map in list(key_map_set):
    key_map_set.remove(key_map)

alnum_keycodes = {
    '0':  'C01', '1':  'C02', '2':  'C03', '3':  'C04', '4':  'C06',
    '5':  'C05', '6':  'B01', '7':  'B02', '8':  'B03', '9':  'B04',
    '10': 'E00', '11': 'B05', '12': 'D01', '13': 'D02', '14': 'D03',
    '15': 'D04', '16': 'D06', '17': 'D05', '18': 'E01', '19': 'E02',
    '20': 'E03', '21': 'E04', '22': 'E06', '23': 'E05', '24': 'E12',
    '25': 'E09', '26': 'E07', '27': 'E11', '28': 'E08', '29': 'E10',
    '30': 'D12', '31': 'D09', '32': 'D07', '33': 'D11', '34': 'D08',
    '35': 'D10', '37': 'C09', '38': 'C07', '39': 'C11', '40': 'C08',
    '41': 'C10', '42': 'C12', '43': 'B08', '44': 'B10', '45': 'B06',
    '46': 'B07', '47': 'B09', '49': 'A03', '50': 'B00',
}

def make_caps_lock_keyset(level1, level2, is_shift_pressed):
    layer = level1.copy() if not is_shift_pressed else level2.copy()
    for key in iso9995_1.alphanumeric_keys:
        if level2[key] in nf.azerty_caps_lock:
            if not is_shift_pressed:
                layer[key] = level2[key]
            else:
                layer[key] = level1[key]
    return layer

azerty_group1_level1_maj = make_caps_lock_keyset(
    nf.azerty_group1_level1, nf.azerty_group1_level2, False)

azerty_group1_level2_maj = make_caps_lock_keyset(
    nf.azerty_group1_level1, nf.azerty_group1_level2, True)

azerty_group2_level1_maj = make_caps_lock_keyset(
    nf.azerty_group2_level1, nf.azerty_group2_level2, False)

azerty_group2_level2_maj = make_caps_lock_keyset(
    nf.azerty_group2_level1, nf.azerty_group2_level2, True)

for index, defaults, nf_layout in [
        ('0', level1_defaults, nf.azerty_group1_level1),
        ('1', level2_defaults, nf.azerty_group1_level2),
        ('2', level1_defaults, nf.azerty_group2_level1),
        ('3', level2_defaults, nf.azerty_group2_level2),
        ('4', level1_defaults, azerty_group1_level1_maj),
        ('5', level2_defaults, azerty_group1_level2_maj),
        ('6', level1_defaults, azerty_group2_level1_maj),
        ('7', level2_defaults, azerty_group2_level2_maj),
]:
    key_map = ET.SubElement(key_map_set, "keyMap", index=index)
    for key in defaults:
        if key in alnum_keycodes:
            out = nf_layout[alnum_keycodes[key]]
        else:
            out = defaults[key]
        if actions.find(".//action[@id = {}]".format(xpath_str(out))):
            ET.SubElement(key_map, "key", code=key, action=out)
        else:
            ET.SubElement(key_map, "key", code=key, output=out)

# Output the result, setting back stripped entities and 1.1 xml header
# Named entities are not supported in keylayout files

keylayout = ET.tostring(keylayout, encoding='utf8', method='xml').decode('utf-8')
keylayout = keylayout.replace('#x', '&#x')
for entity, code in [
        ('&quot;', '&#x0022;'),
        ('&amp;',  '&#x0026;'),
        ('&apos;', '&#x0027;'),
        ('&lt;',   '&#x003C;'),
        ('&gt;',   '&#x003E;'),
]:
    keylayout = keylayout.replace(entity, code)

keylayout = re.sub(
    r"^<\?xml.+\?>",
    '<?xml version="1.1" encoding="UTF-8"?>\n' +
    '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">\n' +
    '<!--Released under MIT License. Copyright (c) 2019 Cyril Lugan-->',
    keylayout
)
print(keylayout)