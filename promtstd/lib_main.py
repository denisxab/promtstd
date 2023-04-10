from pathlib import Path


class ParserPromtStd:
    def __init__(self, select_file: Path) -> None:
        """
        :param select_file: Путь к файлу промпта.
        """
        # Имя файла который сейчас обрабатывается
        self.select_file: Path = select_file
