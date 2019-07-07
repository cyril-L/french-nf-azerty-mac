# ISO/CEI 9995-1

Information technology — Keyboard layouts for text and office systems — Part 1: General principles governing keyboard layouts.

## Disclaimer

This document contains notes taken while developing a keyboard driver implementing the [NF Z71-300](#nf-z71-300) standard about French keyboard layouts for office systems.

This document is not a reference, it might contain errors and approximations.

## Physical division and reference grid

The keyboard is divided in the following sections and zones:

- Alphanumeric section: letters, punctuation and digits, along with surrounding function keys.
  - Alphanumeric zone: keys producing characters, it includes the space bar and does not include the Tabulation and Enter keys.
  - Function zones: surrounding the alphanumeric zone on the left and right.
- Numeric section: numeric keypad.
  - Numeric zone: digits and decimal separator.
  - Function zone : Enter, Numeric Lock and operators.
- Editing and function section: all the remaining parts, like arrow keys, line and page navigation and function keys.

A reference grid identifies each key by a combination of a letter (indicating the row) and two digits (indicating the column):

```python
# TODO Not sure about the function zone identifiers

alphanumeric_section_keys = """
║E00║E01║E02║E03║E04║E05║E06║E07║E08║E09║E10║E11║E12║    E14║
║D00  ║D01║D02║D03║D04║D05║D06║D07║D08║D09║D10║D11║D12║
║C00   ║C01║C02║C03║C04║C05║C06║C07║C08║C09║C10║C11║C12║ C13║
║B99 ║B00║B01║B02║B03║B04║B05║B06║B07║B08║B09║B10║       B11║
║A99 ║A00 ║A02 ║           A03          ║ A08║ A10║ A11║ A12║
"""

alphanumeric_zones = """
║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║░░░░░░░║
║░░░░░║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║
║░░░░░░║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║░░░░║
║░░░░║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║░░░░░░░░░░║
║░░░░║░░░░║░░░░║                        ║░░░░║░░░░║░░░░║░░░░║
"""
```

Layouts are represented as a grid to be more concise and visual. The following snippet is used to convert this data to Python lists.

```python
import re

def layout_to_list(layout):
    # Merges lines
    newlines = re.compile(r'║\s*\n\s*║', re.MULTILINE)
    layout = re.sub(newlines, '║', layout)
    # Removes any leading and trailing whitespaces
    layout = layout.strip()
    # Removes leading and trailing separators
    layout = layout.strip('║')
    return [key.strip(' ') for key in layout.split('║')]
```

```python
# List of alphanumeric section keys
alphanumeric_section_keys = layout_to_list(alphanumeric_section_keys)

alphanumeric_key_is_fn = dict(zip(
    alphanumeric_section_keys,
    ["░" in key for key in layout_to_list(alphanumeric_zones)]))

# List of alphanumeric zone keys
alphanumeric_keys = [key
    for key, is_fn in alphanumeric_key_is_fn.items()
    if not is_fn]

# List of alphanumeric function zone keys
alphanumeric_function_keys = [key
    for key, is_fn in alphanumeric_key_is_fn.items()
    if is_fn]
```

## References

<a name="ref"></a>[ISO/CEI 9995-1](https://www.iso.org/standard/51645.html): Information technology — Keyboard layouts for text and office systems — Part 1: General principles governing keyboard layouts. 2009.

<a name="nf-z71-300"></a>[NF Z71-300](https://www.boutique.afnor.org/norme/nf-z71-300/interfaces-utilisateurs-dispositions-de-clavier-bureautique-francais/article/901594/fa188960): Norme AFNOR Z71-300. Interfaces utilisateurs - Dispositions de clavier bureautique français. 2019.