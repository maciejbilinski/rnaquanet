from pathlib import Path


def get_base_dir():
    return str(Path(__file__).resolve().parent)

