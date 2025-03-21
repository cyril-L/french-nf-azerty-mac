#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
import re

from kbdrefs import nf_z71_300 as nf
from kbdrefs import iso_cei_9995_11 as iso9995_11
from kbdrefs import iso_cei_9995_1 as iso9995_1

# The keylayout file format is described in Apple Technical Note TN2056.
# https://developer.apple.com/library/archive/technotes/tn2056/_index.html
#
# Here we start from a reference layout provided by Ukulele, mainly to keep
# mappings for keys outside the alphanumeric section, which are not defined
# in NF Z71-300.
#
# We need to strip some entities that ElementTree won’t parse, like &#x0008;
# Those will be set back before writing to disk.

with open('./kbdrefs/macos/French.keylayout', 'r') as f:
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

# Do not enter AltGr layouts if Cmd or Ctrl is pressed to avoid breaking shortcuts
# For instance, we want [Cmd][Alt][Shift][V], not [Cmd][Alt][Shift][˛]
for index, keys in [
        ('0', "command? anyControl?"), # Default layer
        ('1', "anyShift command? anyControl?"), # Shift pressed
        ('2', "anyOption"), # AltGr pressed.
        ('3', "anyShift anyOption"), # AltGr + Shift pressed
        # Same sequence with Caps Lock toggled
        ('4', "caps command? anyControl?"),
        ('5', "anyShift caps command? anyControl?"),
        ('6', "caps anyOption"),
        ('7', "anyShift caps anyOption"),
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
combinations.update(iso9995_11.special_chars_combinations)
combinations.update(nf.azerty_combinations)

for space in [' ', '\u00A0']:
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
azerty_with_caps = {}

for key, chars in nf.azerty_layout.items():
    g1l1, g1l2, g2l1, g2l2 = chars
    g1l1_caps = g1l2 if g1l2 in nf.azerty_caps_lock else g1l1
    g1l2_caps = g1l1 if g1l2 in nf.azerty_caps_lock else g1l2
    g2l1_caps = g2l2 if g2l2 in nf.azerty_caps_lock else g2l1
    g2l2_caps = g2l1 if g2l2 in nf.azerty_caps_lock else g2l2
    azerty_with_caps[key] = (
        g1l1, g1l2, g2l1, g2l2,
        g1l1_caps, g1l2_caps, g2l1_caps, g2l2_caps)

for index in range(8):
    key_map = ET.SubElement(key_map_set, "keyMap", index=str(index))
    if index % 2 == 0:
        defaults = level1_defaults
    else:
        defaults = level2_defaults
    for key in defaults:
        if key in alnum_keycodes:
            out = azerty_with_caps[alnum_keycodes[key]][index]
        else:
            out = defaults[key]
        # TODO check what to do when no char defined
        if out == None:
            out = ''
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