import shutil

def prepare_catalogs(mappings: list[dict]) -> None:
    """
    Prepares the catalogs.

    Args:
        mappings: a list of dictionaries containing 'src' and 'dest' keys
        specifying the files
    Returns:
        None
    """
    for mapping in mappings:
        src = mapping['src']
        dest = mapping['dest']
        shutil.move(src, dest)
