import json
from abc import abstractmethod
from datetime import datetime


class MetaSingleton(type):
    """Метакласс, определяющий поведение singleton'a"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseParser(metaclass=MetaSingleton):
    """Базовый класс для парсеров различных сайтов"""

    def __init__(self, url: str, filename: str):
        """
        Конструктор класса BaseParser.
        :param url: адрес сайта для парсинга.
        :param filename: название файла для сохранения новостей.
        """
        self.__url = url
        self.__filename = filename

    def __str__(self):
        """Строковое представление объекта"""
        return f"Парсер для сайта {self.__url}."

    def __repr__(self):
        """Строковое представление объекта"""
        return f"Парсер для сайта {self.__url}."

    @property
    def url(self):
        """Getter для url"""
        return self.__url

    @url.setter
    def url(self, new_url):
        """Setter для url"""
        self.__url = new_url

    @property
    def filename(self):
        """Getter для filename"""
        return self.__filename

    @filename.setter
    def filename(self, new_filename):
        """Setter для filename"""
        self.__filename = new_filename

    @abstractmethod
    def collect_data(self, date_from: datetime, date_to: datetime) -> str:
        """
        Метод для парсинга информации за некоторый промежуток времени.
        :param date_from: дата начала сбора информации.
        :param date_to: дата окончания сбора информации.
        """
        pass

    def _save_data(self, items: list) -> None:
        """
        Метод для записи данных в файл.
        :param items: список новостей для записи.
        """
        with open(self.__filename, "w", encoding='utf8') as file:
            json.dump(items, file, indent=4, ensure_ascii=False)
