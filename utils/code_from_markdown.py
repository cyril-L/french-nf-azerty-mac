#!/usr/bin/env python

"""Executes Python blocks embedded in a Markdown file.

Pass a Markdown file as argument to execute its embedded code.
Symlink along a Markdown file to allow its content to be imported.

literate_content.md
literate_content.py@ -> code_from_markdown.py
main.py

literate_content.md:
```python
foo = "Hello"
```

main.py:
from literate_content import foo
print(foo)
"""

__author__ = 'cyril@lugan.fr (Cyril Lugan)'
__license__ = "MIT"

import sys
import re

if len(sys.argv) == 2:
    markdown_file = sys.argv[1]
else:
    markdown_file = re.sub(r"\.py$", ".md", __file__)

with open(markdown_file, 'r') as f:
    markdown_contents = f.read()
    python_block = re.compile(r'^```python(.*?)^```', re.MULTILINE | re.DOTALL)
    for match in re.finditer(python_block, markdown_contents):
        python_code = match.group(1)
        exec(python_code)
