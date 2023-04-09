from collections import OrderedDict
from json import dumps
from typing import Optional


class JsonText:
    """
    Представляет текст в формате JSON.
    """

    def __init__(self, promts) -> None:
        self.text = dumps(promts, ensure_ascii=False, indent=4)


class PromtMeta(OrderedDict):
    """Мета информация об промте"""

    # В какой AI используется
    for_: tuple[str]
    # В каком месте AI используется%
    use: tuple[str]
    # Имя какой группе относиться промпт
    group: tuple[str]
    # Какой тег у этого промта
    tags: tuple[str]
    # Версия стандарта promtstd
    version: float

    def __repr__(self):
        return f"PromtMeta(for_={self.for_}, use={self.use}, group={self.group}, tags={self.tags})"


class PromtExamples(OrderedDict):
    """Примеры использования промта"""

    # Имя примера
    name: str
    # Пример запроса
    in_text: str
    # Примеры ответов
    out_text: dict[str, str]

    def __repr__(self):
        return f"PromtExamples(examples={self.examples})"


class PromtCodeBlockVars(OrderedDict):
    """Хранит описание переменных"""

    # Имя переменной
    name: str
    # Описание переменной
    doc: str
    # Выбранное значение по умолчанию
    default: str
    # Доступные значения по умолчанию
    allowed: list[str]


class PromtCodeBlock(OrderedDict):
    """Хранение промта вмести с шаблонными ключами"""

    # Необязательная информация о промте
    about_promt: Optional[str]
    # Текст промта
    text_promt: str
    # Шаблонные ключи
    vars: list[PromtCodeBlockVars]

    def __repr__(self):
        return f"PromtCodeBlock(text_promt='{self.text_promt}', templates={self.vars})"


class PromtBasePromt(OrderedDict):
    """Основной промт"""

    promt: PromtCodeBlock

    def __repr__(self):
        return f"PromtBasePromt(promt={self.promt}, examples={self.examples})"


class PromtToolsPromt(OrderedDict):
    """Вспомогательные промты"""

    promts: tuple[PromtCodeBlock]

    def __repr__(self):
        return f"PromtToolsPromt(promts={self.promts})"


class PromtObj(OrderedDict):
    """
    Хранит всю информацию о промпте, включая мета-данные, основной промпт,
    промпты инструментов и примеры.
    """

    # Имя промта
    name: str
    # Мета инфомарция о промте
    meta: PromtMeta
    # Описание промта
    doc: str
    # Базовый промт
    base_promt: PromtBasePromt
    # Вспомогательные промты
    tools: PromtToolsPromt
    # Примеры использования промта
    expl: list[PromtExamples]

    def __repr__(self):
        return f"PromtHeder(name='{self.name}', meta={self.meta}, des='{self.doc}', base_promt={self.base_promt}, tools_promt={self.tools})"
