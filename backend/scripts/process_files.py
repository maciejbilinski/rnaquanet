import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict, FileStorage

from config import STORAGE_DIR


def process_files(files: ImmutableMultiDict[str, FileStorage]):
    for file in files.values():
        if file:
            filename = secure_filename(file.filename)
            os.makedirs(os.path.dirname(f"{STORAGE_DIR}"), exist_ok=True)
            filepath = os.path.join(STORAGE_DIR, filename)
            file.save(filepath)