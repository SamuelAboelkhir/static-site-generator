def markdown_to_blocks(markdown: str):
    # Trying something pythonic
    # Empty strings "" are falsy so an if "" will be skipped
    return [
        block_final
        for block in markdown.split("\n\n")
        if (block_final := block.strip())
    ]
