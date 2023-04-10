# meta

- for:
  - ChatGPT
- use:
  - Первое сообщение
- tags:
  - Python
  - Code

# doc

Этот промт используется для написание документации к коду. В частности для языка программирования Python

# base_promt

```promt
Напиши докстригки к этому {ЧемуДокументация}. В ответ отправь только имя класса/метода и его докстринг:

{{CODE}}
```

- CODE ~ Код которому нужно написать документацию
- ЧемуДокументация ~ К чему нужно писать документацию
  - Класс
  - Метод
  - [x] Класс и метод
  - Атрибуты

# tools

Тут будет список вспомогательных промтов. Например которые логично использовать совместно с основным промтом

```promt
Продолжи свой ответ, с того места где ты закончил прошлый
```

```promt
Напиши снова главу: {{ИмяГлавы}}
```

- ИмяГлавы ~ Название главы

# expl

## Пример написание документация для тестов

```python
class SubdivisionSearchApiViewTests(APITestCaseAuthorization):
    def setUp(self):
        super().setUp()
        self.url = reverse("subdivisionsearch")

    def test_list_subdivisions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0], SubdivisionSerializer(self.subdivision).data
        )
        self.assertEqual(
            response.data["results"][1], SubdivisionSerializer(self.subdivision2).data
        )

    def test_create_subdivision(self):
        new_data = {
            "department": self.department.id,
            "name": "Отделение 3",
            "start_date": "2023-03-01",
        }
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subdivision.objects.filter(name=new_data["name"]).exists())

    def test_filter_subdivisions_by_department(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0], SubdivisionSerializer(self.subdivision).data
        )
        self.assertEqual(
            response.data["results"][1], SubdivisionSerializer(self.subdivision2).data
        )

    def test_filter_subdivisions_by_date(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0], SubdivisionSerializer(self.subdivision).data
        )
        self.assertEqual(
            response.data["results"][1], SubdivisionSerializer(self.subdivision2).data
        )
```

### Пример 1

Класс: SubdivisionSearchApiViewTests

Докстринг класса:
Тесты для представления API поиска подразделений

Метод: setUp

Докстринг метода:
Переопределение метода setUp для настройки тестового окружения

Метод: test_list_subdivisions

Докстринг метода:
Тест для проверки получения списка подразделений

Метод: test_create_subdivision

Докстринг метода:
Тест для проверки создания нового подразделения

Метод: test_filter_subdivisions_by_department

Докстринг метода:
Тест для проверки фильтрации подразделений по отделу

Метод: test_filter_subdivisions_by_date

Докстринг метода:
Тест для проверки фильтрации подразделений по дате

### Пример 2

Класс: SubdivisionSearchApiViewTests
Докстринг: Класс для тестирования API поиска подразделений.

Метод: setUp
Докстринг: Настраивает тестовый случай перед каждым тестом.

Метод: test_list_subdivisions
Докстринг: Тест проверяет получение списка всех подразделений.

Метод: test_create_subdivision
Докстринг: Тест проверяет создание нового подразделения.

Метод: test_filter_subdivisions_by_department
Докстринг: Тест проверяет фильтрацию подразделений по департаменту.

Метод: test_filter_subdivisions_by_date
Докстринг: Тест проверяет фильтрацию подразделений по дате.

## Пример написания документации для кода с логикой

```python
import json
import re

from lib_re import RePromt
from lib_types import (
    PromtBasePromt,
    PromtCodeBlock,
    PromtHeder,
    PromtMeta,
    PromtToolsPromt,
)


def parse_header_md_to_obj(promt_header: str) -> PromtHeder:
    """Распарсить главу с прмотом"""
    # Убрать комментарии из текста
    promt_header = RePromt.clear_comments.sub("", promt_header)

    name = RePromt.search_h1.search(promt_header)["name_promt"].strip()
    meta_raw = RePromt.meta_h2.search(promt_header)["meta_text"].strip()
    des = RePromt.des_h2.search(promt_header)["doc_text"].strip()
    base_promt_raw = RePromt.base_promt_h2.search(promt_header)[
        "base_promt_text"
    ].strip()
    examples_raw = RePromt.examples_promt_h3.search(promt_header)[
        "examples_promt_text"
    ].strip()
    tools_promt_raw = RePromt.tools_promt_h2.search(promt_header)[
        "tools_promt_text"
    ].strip()
    ###
    # meta_raw
    #
    meta_obj = {
        m["key"]: RePromt.md_list.findall(m["values"])
        for m in RePromt.meta_parse_body.finditer(meta_raw)
    }
    meta = PromtMeta(
        for_=meta_obj.get("for", tuple()),
        use=meta_obj.get("use", tuple()),
        group=meta_obj.get("group", tuple()),
        tags=meta_obj.get("tags", tuple()),
    )
    ###
    #
    # base_promt_raw
    #
    base_promt_obj = RePromt.promt_code_block.search(base_promt_raw)
    base_promt = PromtBasePromt(
        promt=PromtCodeBlock(
            text_promt=base_promt_obj["code"],
            templates={
                m["key"]: m["value"].strip()
                for m in RePromt.md_dict.finditer(base_promt_obj["templates"])
            }
            if base_promt_obj["templates"]
            else "",
        ),
        examples=tuple(
            m["code"] for m in RePromt.examples_code_block.finditer(examples_raw)
        ),
    )
    ###
    #
    # tools_promt_raw
    #
    tools_promt = PromtToolsPromt(
        promts=tuple(
            PromtCodeBlock(
                text_promt=m["code"],
                templates={
                    m2["key"]: m2["value"].strip()
                    for m2 in RePromt.md_dict.finditer(m["templates"])
                }
                if m["templates"]
                else "",
            )
            for m in RePromt.promt_code_block.finditer(tools_promt_raw)
        )
    )

    p = PromtHeder(
        name=name, meta=meta, des=des, base_promt=base_promt, tools_promt=tools_promt
    )

    return p


def parse_promt_md_to_json(promt_text: str) -> str:
    """Распарсить весь Markdown файл с промтами
    и вызвать для каждого промта функцию parse_header_md_to_obj

    promt_text: Прмоты в Markdown формате
    return: Промты в Json формате
    """

    arr_promts: PromtHeder = []

    h1_last: re.Match = None

    for h1_now in RePromt.search_h1.finditer(promt_text):
        h1_now: re.Match

        if h1_last:
            promt_header = promt_text[h1_last.span()[0] : h1_now.span()[0]]
            arr_promts.append(parse_header_md_to_obj(promt_header))
        h1_last = h1_now

    if h1_last:
        promt_header = promt_text[h1_last.span()[0] :]
        arr_promts.append(parse_header_md_to_obj(promt_header))

    r = json.dumps(arr_promts, ensure_ascii=False, indent=4)
    return r
```

### Пример 1

Функция: parse_header_md_to_obj
Докстринг: Распарсить раздел с промптом из Markdown и преобразовать его в объект.

Функция: parse_promt_md_to_json
Докстринг: Распарсить весь Markdown файл с промптами, вызвать для каждого промта функцию parse_header_md_to_obj и преобразовать результат в JSON формат.
