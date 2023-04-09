import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def get_file_hash(file_path, algorithm="sha256"):
    """Получить хеш файла"""
    hash_algorithm = hashlib.new(algorithm)
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()
