import sys
from pathlib import Path

import pytest
from utils import get_file_hash

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib_main import ParserPromtStd

pin = Path(__file__).parent.parent.parent / "examples"


@pytest.mark.parametrize(
    ("file_in", "hash_in", "hash_out"),
    [
        (
            Path("Генерация кода на Python.md"),
            "0c691a5e984f2cc920fbbd7c9c8b3c6f37017ee85e62083466b3e76c30dc7c90",
            "4bed2261583a0fd8dfec0abf1065903bddd5d07f59a1d88d493829840fbfa7f7",
        ),
        (
            Path("Документирование кода.md"),
            "def0b48df8057096faf4be3a4a35959d606466946d8f1aa215535ae301e878ab",
            "8c8c70e7513314bedb416b853bd4b1578a398a82c534216bcb075f3241300062",
        ),
        (
            Path("Оптимизация кода.md"),
            "f8a32191910b89d99f8bf816c7de5143890196944493258751d1d64416ee1f9d",
            "e1d87a57338e4447b6278a1d857ac5b68b19db10cd79abd31d8debe60b55910e",
        ),
        (
            Path("Написание README большому проекту.md"),
            "639efae3c225e19010871d87f9a4e4aaf54b9215215d3b6e985e2acbfdb66897",
            "373c0ff9bbea695bce0efb48f84eff4337731daa94e9c0b324c61458cc9e291e",
        ),
        (
            Path("Написать программу на Python.md"),
            "16d759c4861baaf145f01c0557a001fa813532cd5e1e780ef372d96f7d2646b2",
            "bc5b2707b03165d4d3e427beb1eebaef6796e2a7ca6a2190050d3738d8dbae10",
        ),
        (
            Path("Создание промтов вместе с ChatGpt.md"),
            "7aad7e05aaa03bad52c5fd4626f2c6519114ca6abdde11e9b2daeeee6b9365cc",
            "7065e774d0a958706b20cd0011c0d7f2b8c577d844a94f8cd1ea6a3ed7edbeeb",
        ),
        # ?
        # ? Сюда добавлять новые примеры тестовых файлов
        # ?
    ],
)
def test_parse_promt_md_to_json(file_in: Path, hash_in: str, hash_out: str):
    """
    Тест сборки Markdown в Json

    :param Path file_in: Имя тестового файла в папке `test/in_file` в формате Markdown.
    :param str hash_in: Хеш file_in.
    :param str hash_out: Хеш Json файла.
    """
    path_to_file_promt = pin / file_in
    path_out_file_promt = pin / file_in.with_suffix(".json")

    assert get_file_hash(path_to_file_promt) == hash_in
    assert get_file_hash(path_out_file_promt) == hash_out

    req = ParserPromtStd(select_file=path_to_file_promt).parse_file_promt_md_to_json()

    assert req.text == path_out_file_promt.read_text()
