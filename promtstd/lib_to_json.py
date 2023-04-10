from typing import Optional

from lib_linter import StatusWarning, logLinter
from lib_main import ParserPromtStd
from lib_re import RePromt
from lib_types import (
    JsonText,
    PromtBasePromt,
    PromtCodeBlock,
    PromtCodeBlockVars,
    PromtExamples,
    PromtMeta,
    PromtObj,
    PromtToolsPromt,
)


class ParserPromtStdToJson(ParserPromtStd):
    def parse_file_promt_md_to_json(self) -> JsonText:
        """
        Разбирает файл Markdown и конвертирует его в формат JSON, на основе стандарта promtstd.

        :return: Текст в формате JSON.
        """
        return self.parse_text_promt_md_to_json(
            self.select_file.read_text(encoding="utf-8"),
            str(self.select_file.name),
            str(self.select_file.parent.name),
        )

    def parse_text_promt_md_to_json(
        self, promt_text: str, promt_name: str, promt_group_name: str
    ) -> JsonText:
        """
        Разбирает текстовый файл Markdown с промптами и создает объект PromtObj.

        :param promt_name: Имя промпта.
        :param promt_group_name: Имя какой группе относиться промпт.
        :param promt_text: Текст промпта в формате Markdown.
        :return: Объект JsonText.
        """

        # Убрать комментарии из текста
        promt_text = RePromt.md_comment.sub("", promt_text)

        name = promt_name

        # Парсинг мета-данных
        meta = self._parse_meta(promt_text, promt_group_name)

        if doc := RePromt.doc_h1.search(promt_text):
            doc = doc["doc_text"].strip()

        # Парсинг основного промпта
        base_promt = self._parse_base_promt(promt_text)

        # Парсинг промптов инструментов
        tools_promt = self._parse_tools_promt(promt_text)

        # Парсинг примеров
        examples = self._parse_examples(promt_text)

        p = PromtObj(
            name=name,
            meta=meta,
            doc=doc,
            base_promt=base_promt,
            tools_promt=tools_promt,
            expl=examples,
        )

        return JsonText(p)

    #
    ##
    ###
    #### Низкоуровневые методы
    ###
    ##
    #

    def _parse_promt_code_block_vars(
        self, text_promt: str, text_vars: str
    ) -> list[PromtCodeBlockVars]:
        """
        Разбирает текстовую строку и создает объекты PromtCodeBlockVars.

        :param code: Текст промта
        :param text_vars: Текстовая строка с описанием переменных промпта.
        :return: Список объектов PromtCodeBlockVars.
        """

        res: list[PromtCodeBlockVars] = []
        vars_find: set[str] = set()
        if text_vars:
            # Итерация по найденным переменным описания промпта
            for m in RePromt.promt_code_block_vars.finditer(text_vars):
                name = m["name"].strip()
                doc = m["doc"]
                allowed = []
                default = None

                # Итерация по разрешенным значениям переменной
                for m in RePromt.md_list.finditer(m["allowed"]):
                    # Поиск значения по умолчанию среди разрешенных значений
                    if m["is_select"]:
                        default = m["item"]
                    allowed.append(m["item"])

                # Создание объекта PromtCodeBlockVars и добавление его в список
                res.append(
                    PromtCodeBlockVars(
                        name=name,
                        doc=doc,
                        default=default,
                        allowed=allowed,
                    )
                )
                vars_find.add(name)

        # Добавляем в список переменных, и те переменные которые не имеют описание
        for var_no_doc in RePromt.promt_inner_vars.finditer(text_promt):
            if var_no_doc["name"] not in vars_find:
                res.append(
                    PromtCodeBlockVars(
                        name=var_no_doc["name"],
                        doc=None,
                        default=None,
                        allowed=None,
                    )
                )

        return res

    def _parse_meta(
        self, promt_text: str, promt_group_name: str
    ) -> Optional[PromtMeta]:
        """
        Разбирает текстовую строку и создает объект PromtMeta с мета-данными о промпте.

        :param promt_text: Текстовая строка с мета-данными промпта.
        :param promt_group_name: Имя какой группе относиться промпт.
        :return: Объект PromtMeta.
        """

        if meta_raw := RePromt.meta_h1.search(promt_text):
            meta_raw = meta_raw["meta_text"].strip()
            # Создание словаря meta_obj с ключами и соответствующими им списками значений
            meta_obj = {
                m["key"]: [x["item"] for x in RePromt.md_list.finditer(m["values"])]
                for m in RePromt.meta_parse_body.finditer(meta_raw)
            }
            # Создание объекта PromtMeta с использованием данных из meta_obj
            meta = PromtMeta(
                for_=meta_obj.get("for", tuple()),
                use=meta_obj.get("use", tuple()),
                group=promt_group_name,
                tags=meta_obj.get("tags", tuple()),
                version=meta_obj.get("version", None),
            )
            return meta
        else:
            logLinter(StatusWarning.not_h1_meta_header, where_event=self.select_file)

    def _parse_base_promt(self, promt_text: str) -> Optional[PromtBasePromt]:
        """
        Разбирает текстовую строку и создает объект PromtBasePromt с основным промптом.

        :param promt_text: Текстовая строка с основным промптом.
        :return: Объект PromtBasePromt.
        """
        if base_promt_raw := RePromt.base_promt_h1.search(promt_text):
            # Извлечение основного промпта из текста
            base_promt_raw = base_promt_raw["base_promt_text"].strip()

            # Поиск кодового блока промпта в тексте
            base_promt_obj = RePromt.promt_code_block.search(base_promt_raw)

            if base_promt_obj:
                # Парсинг переменных кодового блока промпта
                promt_code_block_vars = self._parse_promt_code_block_vars(
                    base_promt_obj["code"], base_promt_obj["templates"]
                )

                # Создание объекта PromtBasePromt с полученными данными
                base_promt = PromtBasePromt(
                    promt=PromtCodeBlock(
                        text_promt=base_promt_obj["code"],
                        vars=promt_code_block_vars,
                    )
                )

                return base_promt
            else:
                logLinter(
                    StatusWarning.not_body_base_promt, where_event=self.select_file
                )

        else:
            logLinter(StatusWarning.not_h1_base_promt, where_event=self.select_file)

    def _parse_tools_promt(self, promt_text: str) -> Optional[PromtToolsPromt]:
        """
        Разбирает текстовую строку и создает объект PromtToolsPromt с промптами инструментов.

        :param promt_text: Текстовая строка с промптами инструментов.
        :return: Объект PromtToolsPromt.
        """
        if tools_promt_raw := RePromt.tools_promt_h1.search(promt_text):
            tools_promt_raw = tools_promt_raw["tools_promt_text"].strip()

            promts: list[PromtCodeBlock] = []
            for m in RePromt.tools_promt_h2.finditer(tools_promt_raw):
                if not m["body"]:
                    logLinter(
                        StatusWarning.not_body_tools, where_event=self.select_file
                    )

                m2 = None
                for m2 in RePromt.promt_code_block.finditer(m["body"]):
                    promts.append(
                        PromtCodeBlock(
                            about_promt=m["name"],
                            text_promt=m2["code"],
                            vars=self._parse_promt_code_block_vars(
                                m2["code"], m2["templates"]
                            ),
                        )
                    )
                if not m2:
                    logLinter(
                        StatusWarning.not_body_promt_tools, where_event=self.select_file
                    )

            tools_promt = PromtToolsPromt(promts=promts)
            return tools_promt
        else:
            logLinter(StatusWarning.not_h1_tools______, where_event=self.select_file)

    def _parse_examples(self, promt_text: str) -> list[PromtExamples]:
        """
        Разбирает текстовую строку и создает список объектов PromtExamples с примерами промпта.

        :param promt_text: Текстовая строка с примерами промпта.
        :return: Список объектов PromtExamples.
        """
        if examples_raw := RePromt.examples_promt_h1.search(promt_text):
            examples_raw = examples_raw["examples_promt_text"].strip()
            expl = []

            for m in RePromt.examples_in_h2.finditer(examples_raw):
                _name = m["name"]
                in_text = m["doc"]
                out_text = {}
                for m2 in RePromt.examples_out_h3.finditer(m["out"]):
                    out_text[m2["name"]] = m2["body"]

                expl.append(
                    PromtExamples(
                        name=_name,
                        in_text=in_text,
                        out_text=out_text,
                    )
                )

            return expl
        else:
            logLinter(StatusWarning.not_h1_expl_______, where_event=self.select_file)
