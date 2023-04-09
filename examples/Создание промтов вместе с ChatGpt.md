
# base_promt

Этот промт нужен, для того чтобы вмести с CahtGpt найти самый лучший вариант промта под конкретную задачу.

- После этого промта нужно описать под какую задачу вам нужно создать нвоый промт
- После этого CahtGpt будет задавать уточняющие вопросы, на которые нам нужно ответить, для того чтобы улучшить новый промт

```promt
I want you to become my Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt will be used by you, ChatGPT. You will follow the following process:

1. Your first response will be to ask me what the prompt should be about. I will provide my answer, but we will need to improve it through continual iterations by going through the next steps.

2. Based on my input, you will generate 3 sections. a) Revised prompt (provide your rewritten prompt. it should be clear, concise, and easily understood by you), b) Suggestions (provide suggestions on what details to include in the prompt to improve it), and c) Questions (ask any relevant questions pertaining to what additional information is needed from me to improve the prompt).

3. We will continue this iterative process with me providing additional information to you and you updating the prompt in the Revised prompt section until it's complete.

Задавай мне вопросы и пиши ответы на русском языке
```

# tools

## Если нужно модифицировать уже существующий промт, то напишите 2 сообщением

```promt
Изначально Revised prompt равен: 

{{Указать_пример}}
```

## Если нужно изменять промт на основание примеров

```promt
Я хочу проверить работу Revised prompt, я буду давать смотреть на твой ответ и давать подсказки как можно улучшить Revised prompt. Для улучшения можно изменять правила Revised prompt. Вот пример который ты должен проверить:

{{Указать_пример}}
```
