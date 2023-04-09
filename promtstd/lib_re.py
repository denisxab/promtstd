from re import compile


class RePromt:
    """Класс который хранит регулярные выражения"""

    #
    ## Для парсинга Markdown
    #
    # ? Заголовок первого уровня
    h1_pattern = r"((?:\n|\A)#{{1}} {header}\n)(?P<{group_name}>(.*\s*(?!#{{1}} ))+)"
    # ? Комментарии в Markdown
    md_comment = compile(r"%[^%]+%")
    # ? Парсинг markdown словарей
    md_dict = compile(r"- (?P<key>[\w\d_ -]+)~(?P<value>[^\n]+)\n?")
    # ? Парсинг markdown списка
    md_list = compile(r"- (?P<is_select>\[x\] )?(?P<item>[^\n]+)")
    # ? Найти выбранные элементы списка
    md_select_in_list = compile(r"- \[x\] (?P<name>[^\n]+)\n")
    #
    ## Для парсинга стандарта promtstd
    #
    # ? Поиск заголовка с мета информацией
    meta_h1 = compile(h1_pattern.format(header="meta", group_name="meta_text"))
    # ? Распарсить текст мета данных
    meta_parse_body = compile(r"- (?P<key>\w+): *\n(?P<values>(?:[\t ]+- [^\n]+\n?)+)")
    # ? Поиск заголовка с описанием
    doc_h1 = compile(h1_pattern.format(header="doc", group_name="doc_text"))
    # ? Поиск заголовка с основным промтом
    base_promt_h1 = compile(
        h1_pattern.format(header="base_promt", group_name="base_promt_text")
    )
    # ? Поиск заголовка с вспомогательными промтами
    tools_promt_h1 = compile(
        h1_pattern.format(header="tools", group_name="tools_promt_text")
    )
    # ? Поиск заголовков с описанием вспомогательного промта
    tools_promt_h2 = compile(
        r"(?:(?:\A|\n)#{2} (?P<name>[^\n]+)\n+)?(?P<body>(?:.\s*(?!#{2} ))+)"
    )
    # ? Поиск блоков с promt
    promt_code_block = compile(
        r"(?:`{3}promt\n(?P<code>(?:.\s*(?!`{3}))+)\n`{3}\s*)(?P<templates>(?:- [\w\d_ -]+~[^\n]+\n?((?:[\t ]+- [^\n]+\n?)*))+)?"
    )
    # ? Поиск переменных в коде промта
    promt_inner_vars = compile(r"{{(?P<name>[^}]+)}}")
    # ? Парсинг переменных
    promt_code_block_vars = compile(
        r"(?:- (?P<name>[\w\d_ -]+)~(?P<doc>[^\n]+)\n?(?P<allowed>(?:[\t ]+- [^\n]+\n?)*))"
    )
    # ? Поиск заголовка с в котором находятся все примеры
    examples_promt_h1 = compile(
        h1_pattern.format(header="expl", group_name="examples_promt_text")
    )
    # ? Поиск заголовка с конкретным примером
    examples_in_h2 = compile(
        r"(?:\A|\n)#{2} (?P<name>[^\n]+)\n(?P<doc>(?:.*\s*(?!#{3} ))+)(?P<out>(?:.*\s*(?!#{2} ))+)"
    )
    # ? Поиск заголовков с ответами на конкретный пример
    examples_out_h3 = compile(r"#{3} (?P<name>[^\n]+)\n(?P<body>(.*\s*(?!#{3} ))+)")
