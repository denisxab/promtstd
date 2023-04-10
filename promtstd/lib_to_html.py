from pathlib import Path
from typing import Optional

import markdown
from lib_linter import StatusWarning, logLinter
from lib_main import ParserPromtStd
from lib_re import RePromt
from lib_types import HTMLText


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
                # добавляет возможность использования блоков кода с различными языками программирования.
                "pymdownx.superfences",
                # добавляет автоматическое преобразование ссылок в HTML-ссылки.
                "pymdownx.magiclink",
                #
                ##
                ###
                ##
                #
                # подсвечивает синтаксис блоков кода.
                "codehilite",
                # "markdown.extensions.codehilite",
                # добавляет подсветку синтаксиса кода с помощью Pygments.
                # "pymdownx.highlight",
            ],
            output_format="html5",
        )
        dirs = Path(__file__).parent
        self.css_style = (dirs / "bootstrap.css").read_text() + (
            dirs / "css.css"
        ).read_text()

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
