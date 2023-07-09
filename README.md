# modsen

# Практического задание python

## Задание

Необходимо написать очень простой поисковик по текстам документов. Данные хранятся в БД по желанию, поисковый индекс в эластике.
Ссылка на тестовый массива данных: ./posts.csv. 

__Структура БД:__

- `id` - уникальный для каждого документа;
- `rubrics` - массив рубрик;
- `text` - текст документа;
- `created_date` - дата создания документа.


__Структура Индекса:__

- `iD` - id из базы;
- `text` - текст из структуры БД.


__Необходимые методы:__

- сервис должен принимать на вход произвольный текстовый запрос, искать по тексту документа в индексе и возвращать первые 20 документов со всем полями БД, упорядоченные по дате создания;
- удалять документ из БД и индекса по полю  `id`.

__Технические требования:__

- любой python фреймворк кроме Django и DRF;
- `README` с гайдом по поднятию;
- `docs.json` - документация к сервису в формате openapi.

__Программа максимум:__

- функциональные тесты;
- сервис работает в Docker;
- асинхронные вызовы.


---

# Как поднять

запустить main.py и всё