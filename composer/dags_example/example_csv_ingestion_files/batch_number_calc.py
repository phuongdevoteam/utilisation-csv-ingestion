from pathlib import Path

def bn_func(metadata) -> str:
    '''Calculate batch number which will be used as a temporary table name and will also be inserted'''
    file_stem = Path(metadata['file_name']).stem
    return file_stem