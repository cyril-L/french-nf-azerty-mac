#!/usr/bin/env python3

"""Utils used to execute Python blocks embedded in a Markdown files.
"""

__author__ = 'cyril@lugan.fr (Cyril Lugan)'
__license__ = "MIT"

import sys
import re
import itertools

def parse_as_table(table_str, row_separator='|', line_separator='\n', strip=' '):
    table = []
    for line in table_str.split(line_separator):
        if not row_separator in line:
            continue
        line = re.sub("^.*?{}".format(re.escape(row_separator)), '', line)
        line = re.sub("{0}(?!.*{0})$".format(re.escape(row_separator)), '', line)
        line = [cell.strip(strip) for cell in line.split(row_separator)]
        line = [cell if cell != '' else None for cell in line]
        table.append(line)
    return table

def parse_as_list(table_str, row_separator='|', line_separator='\n', strip=' '):
    return  list(itertools.chain.from_iterable(
        parse_as_table(table_str, row_separator, line_separator)))

def python_blocks_in_markdown(filename):
    with open(filename, 'r') as file:
        block_starting = re.compile(r'^```python')
        block_ending = re.compile(r'^```')
        block = None
        block_lineno = None
        for lineno, line in enumerate(file, 1):
            if block is None and re.match(block_starting, line):
                block = []
                block_lineno = lineno
            elif block is not None:
                if not re.match(block_ending, line):
                    block.append(line)
                else:
                    try:
                        yield "\n".join(block)
                    except:
                        sys.stderr.write(
                            "Error while parsing block in {}, line {}\n"
                            .format(filename, block_lineno))
                        raise
                    block = None
