# Parsers

## Проект по сбору новостей

### На данный момент поддерживается сбор новостей с сайтов ixbt.com и mos.ru

## Установка
  1. Клонировать репозиторий
  ```
  git clone https://github.com/coIorbIind/parsers.git
  ```
  2. Создать виртуальное окружение
  ```
  python -m venv venv
  ```
  3. Активировать виртуальное окружение
  ```
  venv\Scripts\activate.bat - для Windows
  source venv/bin/activate - для Linux и MacOS
  ```
  4. Установить необходимые зависимости
  ```
  pip install -r requirements.txt
  ```
  5. Запустить проект
  ```
  python main.py
  ```
  
 ## Пример использования
  1. Запуск
  ```
  python main.py
  ```
  2. Выбрать один из пунктов в меню
  3. Ввести дату начала и окончания сбора новостей
  
  ![image](https://user-images.githubusercontent.com/91391687/179394903-b7ec25af-adb3-4af3-9eb1-3b746fde6668.png)
  
  После окончания парсинга вы увидите json файл с новостями в текущей директории.
  
   ```
  .
  ├── parsers
  |   ├── .gitignore
  |   ├── base_class.py
  |   ├── ixbt.py
  |   ├── main.py
  |   ├── mosru.py
  |   └── requirements.txt
  ```
  
  Структура файла ixbt.json
  ```json
  [
    {
          "title": "заголовок",
          "subtitle": "подзаголовок",
          "url": "url адрес",
          "time": "время публикации",
          "text": "текст статьи",
          "tags": [
              "список тегов"
          ],
          "sources": [
              "список источников"
          ]
    }
   ]
  ```
  Структура файла mosru.json
  ```json
  [
    {
        "id": "id новости",
        "title": "заголовок",
        "published_at": "время публикации",
        "full_text": "текст статьи"
    }
  ]
  ```  
