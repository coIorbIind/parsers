from abc import abstractmethod


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseParser(metaclass=MetaSingleton):
    """Базовый класс для парсеров различных сайтов"""

    # __metaclass__ = MetaSingleton

    def __init__(self, url: str,):
        """
        Конструктор класса BaseParser.
        :param url: адрес сайта для парсинга.
        """
        self.__url = url

    def __str__(self):
        return f"Парсер для сайта {self.__url}."

    @abstractmethod
    def parse(self):
        pass
