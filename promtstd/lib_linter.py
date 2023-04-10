"""Файл для соблюдения синтаксиса promtstd"""


from enum import Enum
from os import getenv
from pathlib import Path, PosixPath

end_color = "\033[0m"

isAnsi = False
# Проверяем, что терминал поддерживает ANSI-цвета
if getenv("TERM") == "xterm-color":
    isAnsi = True


class StatusPromtStd(Enum):
    ...

    def log_level() -> str:
        ...


class StatusWarning(StatusPromtStd):
    not_h1_meta_header = "Не указана глава с мета информацией (# meta)"
    not_h1_base_promt = "Не указана глава с базовым промтом(# base_promt)"
    not_body_base_promt = "В главе (# base_promt) не указана текст с базовым промтом. Помните о том что код блок с промтом должен иметь тип `promt`"
    not_h1_tools______ = "Не указана глава с доп промтами (# tools)"
    not_body_tools = "В главе (# tools) не указана текст."
    not_body_promt_tools = "В главе (# tools) не указана текст с промтом. Помните о том что код блок с промтом должен иметь тип `promt`"
    not_h1_expl_______ = "Не указана глава с примерами (# expl)"

    def log_level():
        return "WARNING"

    def color():
        return "\033[93m"


class StatusSuccess(StatusPromtStd):
    end_compilation_json = "Конец компиляции в json"
    save_to_json_file = "Сохранение в файл json"
    end_compilation_html = "Конец компиляции в html"
    save_to_json_html = "Сохранение в файл html"

    def log_level():
        return "SUCCESS"

    def color():
        return "\033[32m"


class StatusError(StatusPromtStd):
    file_no_suffix_md = "Переданный файл не имеет расширение `.md`"
    not_allowed_type_to_build = "Недопустимый тим для сборки"

    def log_level():
        return "ERROR"

    def color():
        return "\033[31m"


def logLinter(status: StatusPromtStd, add_text: str = "", where_event: str | Path = ""):
    """
    Вывести лог информацию

    :param status: Статус сообщения
    :param add_text: Дополнительные текст
    """
    if type(where_event) == PosixPath:
        where_event = where_event.name

    if isAnsi:
        print(
            f"[{status.__class__.log_level()}:{status.name}]\t{where_event} | {add_text if add_text else status.value}"
        )

    else:
        print(
            f"{status.__class__.color()}[{status.__class__.log_level()}:{status.name}]{end_color}\t {where_event} | {add_text if add_text else status.value}"
        )


class LintError(BaseException):
    ...
