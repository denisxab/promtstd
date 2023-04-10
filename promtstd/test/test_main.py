import sys
from pathlib import Path

import pytest
from utils import get_file_hash

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib_to_json import ParserPromtStdToJson

pin = Path(__file__).parent.parent.parent / "examples"


@pytest.mark.parametrize(
    ("file_in", "hash_in", "hash_out"),
    [
        (
            Path("Генерация кода на Python.md"),
            "b750e2b8be69fce810051c369638653e260c7187f91f1d4eac63fda7c4a3aac2",
            "4bed2261583a0fd8dfec0abf1065903bddd5d07f59a1d88d493829840fbfa7f7",
        ),
        (
            Path("Документирование кода.md"),
            "6911e545648182adf0791192d0301540cd7699b64f5dc42a57f0abc161de9212",
            "8c8c70e7513314bedb416b853bd4b1578a398a82c534216bcb075f3241300062",
        ),
        (
            Path("Оптимизация кода.md"),
            "23621f774ba51a8e811e56e4880bf7709d94294a7444dc83fa24a3ea24f3ea14",
            "e1d87a57338e4447b6278a1d857ac5b68b19db10cd79abd31d8debe60b55910e",
        ),
        (
            Path("Написание README большому проекту.md"),
            "66e2268fdb2c99992cf287b3419b9623858a7f13ab3087ebfd585d48506d61b4",
            "85a6cf90ea1d8b0019a7785e116d7f9cf81bbd5aa1d55cdd413b683a86e5e309",
        ),
        (
            Path("Написать программу на Python.md"),
            "49ab111fe296b0fa0ac700bfb678c9c24aff2f58f436ceb4a4e8b75244813891",
            "bc5b2707b03165d4d3e427beb1eebaef6796e2a7ca6a2190050d3738d8dbae10",
        ),
        (
            Path("Создание промтов вместе с ChatGpt.md"),
            "13565a0d94fc8ee52038c74cf5e248c3ec0eb1e668b175ecb12b8ad759f0234b",
            "9bbf0eeea796c29c093ceb90581558fac97022aee3e76e9e304e857ec08e618a",
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
    path_out_file_promt = pin / "json" / file_in.with_suffix(".json")

    assert get_file_hash(path_to_file_promt) == hash_in
    assert get_file_hash(path_out_file_promt) == hash_out

    req = ParserPromtStdToJson(
        select_file=path_to_file_promt
    ).parse_file_promt_md_to_json()

    assert req.text == path_out_file_promt.read_text()
