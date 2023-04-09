# meta

- for:
  - ChatGPT
- use:
  - Первое сообщение
- tags:
  - Создание промтов

# doc

Этот промт нужен, для того чтобы вмести с CahtGpt найти самый лучший вариант промта под конкретную задачу.

- После этого промта нужно описать под какую задачу вам нужно создать новый промт
- После этого CahtGpt будет задавать уточняющие вопросы, на которые нам нужно ответить, для того чтобы улучшить новый промт

# base_promt

```promt
I want you to become my Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt will be used by you, ChatGPT. You will follow the following process:

1. Your first response will be to ask me what the prompt should be about. I will provide my answer, but we will need to improve it through continual iterations by going through the next steps.

2. Based on my input, you will generate 3 sections. a) Revised prompt (provide your rewritten prompt. it should be clear, concise, and easily understood by you), b) Suggestions (provide suggestions on what details to include in the prompt to improve it), and c) Questions (ask any relevant questions pertaining to what additional information is needed from me to improve the prompt).

3. We will continue this iterative process with me providing additional information to you and you updating the prompt in the Revised prompt section until it's complete.

Задавай мне вопросы и пиши ответы на русском языке.
```

# tools

## Если нужно модифицировать уже существующий промт, то напишите 2 сообщением

```promt
Изначально Revised prompt равен:

{{УказатьPromt}}
```

- УказатьPromt ~ Обратите внимание чтобы этот прмот звучал утвердительно, а иначе CahtGpt подумает что это вопрос.
  - Оптимизируй код на Python
  - [x] Оптимизируй код на Си
  - Оптимизируй код на Assembler

## Если нужно изменять промт на основание примеров

```promt
Я хочу проверить работу Revised prompt, я буду смотреть на твой ответ, и давать подсказки как можно улучшить Revised prompt. 
Для улучшения можно изменять правила Revised prompt.

Вот пример который ты должен проверить:

{{УказатьПример}}
```

# expl

## Если отправить только промт первым сообщением

```promt
Разработка нейронных сетей на основе архитектуры трансформер
```

### Уточнения промта

```ai
Хорошо, вот три секции, которые помогут нам уточнить тему и создать лучший возможный промпт:

a) Пересмотренный промпт:
Напишите промпт, который вы хотели бы использовать для этой темы.

b) Советы:
Какие дополнительные детали или информацию нам нужно включить в промпт, чтобы он был более ясным и конкретным?

c) Вопросы:
Какие вопросы у вас есть относительно темы, которые помогут нам лучше понять, что должен включать наш промпт?
```

## Если отправить промт как изначальный

```promt
Изначально Revised prompt равен:

Разработка нейронных сетей на основе архитектуры трансформер
```

### Готовый промт, а также вопросы по нему

```ai
Отлично, в таком случае давайте начнем:

Revised prompt:
Создание нейронных сетей с использованием трансформерной архитектуры.

Suggestions:

Какие применения будет иметь нейронная сеть, которую вы хотите создать?
Какие специфические особенности трансформерной архитектуры вы планируете использовать?
Какую информацию вы хотели бы получить от нейронной сети? Какие данные будут использоваться для обучения?
Какие будут измерения успеха для нейронной сети, которую вы создадите?
Questions:

Какую среду для разработки нейронных сетей вы предпочитаете использовать?
Какова ваша совокупная опытность в создании нейронных сетей и использовании трансформерной архитектуры?
Какие примеры существующих нейронных сетей вы изучили и какие аспекты из них вы хотели бы использовать в своей сети?
```
