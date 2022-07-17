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

    def __init__(self, url: str):
        """
        Конструктор класса BaseParser.
        :param url: адрес сайта для парсинга.
        """
        self.__url = url

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

    @abstractmethod
    def collect_data(self, date_from: datetime, date_to: datetime) -> str:
        """
        Метод для парсинга информации за некоторый промежуток времени.
        :param date_from: дата начала сбора информации.
        :param date_to: дата окончания сбора информации.
        """
        pass
