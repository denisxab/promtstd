import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Literal, Optional

sys.path.insert(0, str(Path(__file__).parent))

from lib_linter import LintError, StatusError, StatusSuccess, logLinter
from lib_to_html import ParserPromtStdToHTML
from lib_to_json import ParserPromtStdToJson


def main(to_build: Literal["json", "html", "all"] = None, file: Optional[str] = None):
    file_out = None
    if not file:
        parser = ArgumentParser(
            description="Преобразование файла PromtStd.Markdown в формат PromtStd.JSON"
        )
        parser.add_argument(
            "to_build",
            choices=["json", "html", "all"],
            type=str,
            help="В какой тип нужно собрать",
        )
        parser.add_argument(
            "file_md",
            type=str,
            help="Путь к PromtStd.Markdown",
        )

        args = parser.parse_args()
        to_build = args.to_build
        file_out = Path(args.file_md)

        if file_out.suffix != ".md":
            logLinter(StatusError.file_no_suffix_md, where_event=file_out)
            raise LintError(StatusError.file_no_suffix_md.value)

    else:
        file_out = Path(file)

    ###
    if to_build == "json" or to_build == "all":
        r = ParserPromtStdToJson(file_out).parse_file_promt_md_to_json()
        logLinter(StatusSuccess.end_compilation_json, where_event=file_out)

        path_out_file_promt = (
            file_out.parent / "json" / file_out.with_suffix(".json").name
        )

        path_out_file_promt.parent.mkdir(exist_ok=True)
        path_out_file_promt.write_text(r.text)
        logLinter(StatusSuccess.save_to_json_file, where_event=file_out)

    if to_build == "html" or to_build == "all":
        r = ParserPromtStdToHTML(file_out).parse_file_promt_md_to_html()
        logLinter(StatusSuccess.end_compilation_html, where_event=file_out)

        path_out_file_promt = (
            file_out.parent / "html" / file_out.with_suffix(".html").name
        )

        path_out_file_promt.parent.mkdir(exist_ok=True)
        path_out_file_promt.write_text(r.text)
        logLinter(StatusSuccess.save_to_json_html, where_event=file_out)

    else:
        logLinter(StatusError.not_allowed_type_to_build, where_event=file_out)
        raise LintError(StatusError.not_allowed_type_to_build.value)


if __name__ == "__main__":
    main()

    # to_build = "json"
    # pt = Path(__file__).parent.parent / "examples"
    # main(to_build, pt / "Генерация кода на Python.md")
    # main(to_build, pt / "Документирование кода.md")
    # main(to_build, pt / "Изучение новой темы в IT.md")
    # main(to_build, pt / "Написание README большому проекту.md")
    # main(to_build, pt / "Оптимизация кода.md")
    # main(to_build, pt / "Написать программу на Python.md")
    # main(to_build, pt / "Создание промтов вместе с ChatGpt.md")
