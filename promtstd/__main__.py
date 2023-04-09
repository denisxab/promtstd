from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib_linter import LintError, StatusError, StatusSuccess, logLinter
from lib_main import ParserPromtStd


def main(file: Optional[str] = None):
    file_md = None
    if not file:
        parser = ArgumentParser(
            description="Преобразование файла PromtStd.Markdown в формат PromtStd.JSON"
        )
        parser.add_argument("file_md", type=str, help="Путь к PromtStd.Markdown ")

        args = parser.parse_args()
        file_md = Path(args.file_md)

        if file_md.suffix != ".md":
            logLinter(StatusError.file_no_suffix_md, where_event=file_md)
            raise LintError(StatusError.file_no_suffix_md.value)

    else:
        file_md = Path(file)

    ###
    r = ParserPromtStd(file_md).parse_file_promt_md_to_json()
    logLinter(StatusSuccess.end_compilation_json, where_event=file_md)

    path_out_file_promt = file_md.with_suffix(".json")

    path_out_file_promt.write_text(r.text)
    logLinter(StatusSuccess.save_to_json_file, where_event=file_md)


if __name__ == "__main__":
    main()

    # pt = Path(__file__).parent.parent / "examples"
    # main(pt / "Генерация кода на Python.md")
    # main(pt / "Документирование кода.md")
    # main(pt / "Изучение новой темы в IT.md")
    # main(pt / "Написание README большому проекту.md")
    # main(pt / "Оптимизация кода.md")
    # main(pt / "Написать программу на Python.md")
    # main(pt / "Создание промтов вместе с ChatGpt.md")

    ...
