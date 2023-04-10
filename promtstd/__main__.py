import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Literal, Optional

sys.path.insert(0, str(Path(__file__).parent))

from lib_linter import LintError, StatusError, StatusSuccess, logLinter
from lib_to_html import ParserPromtStdToHTML
from lib_to_json import ParserPromtStdToJson


def main(to_build: Literal["json", "html"] = None, file: Optional[str] = None):
    file_md = None
    if not file:
        parser = ArgumentParser(
            description="Преобразование файла PromtStd.Markdown в формат PromtStd.JSON"
        )
        parser.add_argument("to_build", type=str, help="В какой тип нужно собрать")
        parser.add_argument("file_md", type=str, help="Путь к PromtStd.Markdown")

        args = parser.parse_args()
        file_md = Path(args.file_md)

        if file_md.suffix != ".md":
            logLinter(StatusError.file_no_suffix_md, where_event=file_md)
            raise LintError(StatusError.file_no_suffix_md.value)

    else:
        file_md = Path(file)

    ###
    if to_build == "json":
        r = ParserPromtStdToJson(file_md).parse_file_promt_md_to_json()
        logLinter(StatusSuccess.end_compilation_json, where_event=file_md)

        path_out_file_promt = file_md.with_suffix(".json")

        path_out_file_promt.write_text(r.text)
        logLinter(StatusSuccess.save_to_json_file, where_event=file_md)

    elif to_build == "html":
        r = ParserPromtStdToHTML(file_md).parse_file_promt_md_to_html()
        logLinter(StatusSuccess.end_compilation_html, where_event=file_md)

        path_out_file_promt = file_md.with_suffix(".html")

        path_out_file_promt.write_text(r.text)
        logLinter(StatusSuccess.save_to_json_html, where_event=file_md)

    else:
        logLinter(StatusError.not_allowed_type_to_build, where_event=file_md)
        raise LintError(StatusError.not_allowed_type_to_build.value)


if __name__ == "__main__":
    # main()

    to_build = "html"
    pt = Path(__file__).parent.parent / "examples"
    main(to_build, pt / "Генерация кода на Python.md")
    main(to_build, pt / "Документирование кода.md")
    main(to_build, pt / "Изучение новой темы в IT.md")
    main(to_build, pt / "Написание README большому проекту.md")
    main(to_build, pt / "Оптимизация кода.md")
    main(to_build, pt / "Написать программу на Python.md")
    main(to_build, pt / "Создание промтов вместе с ChatGpt.md")

    ...
