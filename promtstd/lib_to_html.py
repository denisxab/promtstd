import re
from pathlib import Path

import markdown
from lib_main import ParserPromtStd
from lib_re import RePromt
from lib_types import HTMLText
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter
from sass import compile


class ParserPromtStdToHTML(ParserPromtStd):
    def __init__(self, select_file: Path) -> None:
        super().__init__(select_file)

        # Создание экземпляра класса Markdown
        self.md = markdown.Markdown(
            extensions=[
                # добавляет возможность использования блоков кода, ограниченных символами ```.
                "fenced_code",
                # заменяет переносы строк на тег <br>.
                "nl2br",
                # добавляет поддержку улучшенного форматирования текста.
                "pymdownx.betterem",
                # добавляет возможность экранирования всех символов.
                "pymdownx.escapeall",
                # добавляет автоматическое преобразование ссылок в HTML-ссылки.
                "pymdownx.magiclink",
                # добавляет возможность использования блоков кода с различными языками программирования.
                "pymdownx.superfences",
                #
                ##
                ###
                ##
                #
                # Создание экземпляра расширения TOC с указанием места для вставки оглавления
                TocExtension(marker="[TOC]", title="Оглавление"),
            ],
            output_format="html5",
        )
        # Папка с CSS
        dir_css = Path(__file__).parent / "from_html" / "css"

        # CSS стили
        self.css_style = "{bootstrap}{base_style}{codehigligt}".format(
            # Стили bootstrap
            bootstrap=(dir_css / "bootstrap.css").read_text(),
            # Базовые стили
            base_style=compile(filename=str((dir_css / "base_style.scss"))),
            # Стили для подсветки кода
            codehigligt=HtmlFormatter(style="monokai").get_style_defs(".highlight"),
        ).replace("\n", "")

    def parse_text_promt_md_to_html(
        self, promt_text: str, promt_name: str, promt_group_name: str
    ) -> HTMLText:
        """
        Разбирает текстовый файл Markdown с промптами и создает объект PromtObj.

        :param promt_name: Имя промпта.
        :param promt_group_name: Имя какой группе относиться промпт.
        :param promt_text: Текст промпта в формате Markdown.
        :return: Объект HTMLText.
        """

        # Убрать комментарии из текста
        promt_text = RePromt.md_comment.sub("", promt_text)
        # Увеличиваем количество пробелов у списка, чтобы он считался вложенным для python-markdown
        promt_text = re.sub(" {1,3}-", "    -", promt_text)
        # Вставляем оглавление
        promt_text = f"[TOC]\n\n{promt_text}"

        # Конвертация текста в HTML
        html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Promtstd</title>
    <style>{css}</style>
</head>
<body>
    <div class="markdown-body">
        {body}
    </div>
</body>
</html>"""[
            1:
        ].format(
            css=self.css_style,
            body=self.md.convert(promt_text),
        )
        return HTMLText(html)

    def parse_file_promt_md_to_html(self) -> HTMLText:
        """
        Разбирает файл Markdown и конвертирует его в формат HTML, на основе стандарта promtstd.

        :return: Текст в формате JSON.
        """
        return self.parse_text_promt_md_to_html(
            self.select_file.read_text(encoding="utf-8"),
            str(self.select_file.name),
            str(self.select_file.parent.name),
        )
