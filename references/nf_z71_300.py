from references.utils import python_blocks_in_markdown

for block in python_blocks_in_markdown(__file__):
    exec(block)
