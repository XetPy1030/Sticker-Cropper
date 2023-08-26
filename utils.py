import os
from typing import List


def collect_files(dir: str, extensions: List[str]) -> list:
    """
    Collect all files in dir
    """
    files = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.split('.')[-1] in extensions:
                files.append(os.path.join(root, filename))

    return files
