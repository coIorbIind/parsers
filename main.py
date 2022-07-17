from art import tprint
from datetime import datetime

from mosru import MosRuParser
from ixbt import IxbtParser


def input_date():
    """Функция для ввода даты"""
    while True:
        try:
            date = datetime.strptime(input(), "%d.%m.%Y")

            if date > datetime.today():
                raise ValueError
            break

        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")

    return date


def create_parsers():
    """Функция для инициализации массива парсеров"""
    parsers = list()
    parsers.append(IxbtParser(url="https://www.ixbt.com/news/{year}/{month}/{day}/?show=tape", filename="ixbt.json"))
    parsers.append(MosRuParser(url="https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/articles?",
                               filename="mosru.json"))

    return parsers


def main():
    """Функция для взаимодействия с пользователем"""
    parsers = create_parsers()

    tprint("PARSERS", font='tarty4')
    print("=" * 43)

    print("Для сбора новостей с сайта ixbt.com введите .......1")
    print("Для сбора новостей с сайта mos.ru введите .........2")
    print("=" * 52)

    while True:
        try:
            pars_id = int(input())

            if pars_id not in [1, 2]:
                raise ValueError
            break

        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")

    print("Введите дату начала сбора информации в формате день.месяц.год")
    date_from = input_date()

    print("Введите дату окончания сбора информации в формате день.месяц.год")
    date_to = input_date()
    print("=" * 52)

    result = parsers[pars_id - 1].collect_data(date_from, date_to)
    print("=" * 52)

    print(result)


if __name__ == '__main__':
    main()
