"""Executes code from it Markdown sibling.

It allows variables defined in the Markdown file to be imported and used
elsewhere.
"""

from kbdrefs.literate import python_blocks_in_markdown
import re

MARKDOWN_FILE = re.sub(r"\.py$", ".md", __file__)

for block in python_blocks_in_markdown(MARKDOWN_FILE):
    exec(block)
