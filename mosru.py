import json
from datetime import datetime
import requests
import time
from random import random

from bs4 import BeautifulSoup
from urllib3.exceptions import ProtocolError

from base_class import BaseParser


class MosRuParser(BaseParser):

    def __init__(self, url: str, filename: str):
        """
        Конструктор класса MosRuParser.
        :param url: адрес сайта для парсинга.
        :param filename: название файла для сохранения новостей.
        """
        super().__init__(url, filename)
        self.params = {
            "fields": ",".join(["id", "full_text", "title", "published_at"]),
            "per-page": 50,
            "sort": "-date"
        }

    def collect_data(self, date_from: datetime, date_to: datetime) -> str:
        """
        Метод для парсинга информации за некоторый промежуток времени.
        :param date_from: дата начала сбора информации.
        :param date_to: дата окончания сбора информации.
        :return: текстовый ответ для пользователя
        """
        self.params["from"] = date_from.strftime("%Y-%m-%d+00:00:00")
        self.params["to"] = date_to.strftime("%Y-%m-%d+23:59:59")

        url = self._create_url()

        page_count = self._get_page_count(url)  # получаем число страниц с данными

        result = list()

        for page_num in range(1, page_count + 1):
            result += self._get_data(page_num=page_num, url=url)  # собираем данные с каждой страницы
            time.sleep(random() * 1.5 + 0.5)  # немного ждем, чтобы не нагружать сервер запросами
            print(f"[+] Получено {page_num} из {page_count} страниц")

        self._save_data(result)

        return f"[SUCCESS] Новости за период {date_from.strftime('%d.%m.%Y')} - " \
               f"{date_to.strftime('%d.%m.%Y')} собраны в файл {self.filename}"

    def _get_data(self, page_num, url):
        """
        Метод для извлечения информации о статьях.
        :param url: url адрес сайта
        :param page_num: номер страницы.
        :return: None
        """
        page_url = url + f"&page={page_num}"  # подставляем номер страницы в параметры запроса

        # Отправляем запрос на сайт, если нет ответа, ждем в течение 15 секунд
        try:
            response = requests.get(page_url)

        except ProtocolError:
            time.sleep(15)
            response = requests.get(page_url)

        if response.ok:
            data = response.json()  # если данные успешно получены, собираем информацию с ответа сервера

            items = data.get("items")  # забираем все новости

            # Извлекаем текст из всех тегов статьи
            for item in items:
                item["full_text"] = BeautifulSoup(item["full_text"], "lxml").text

            return items

    def _create_url(self) -> str:
        """
        Метод для создания ссылки по определенным параметрам.
        :return: url адрес нужной страницы
        """
        temp_url = self.url
        for k, v in self.params.items():
            temp_url += f"{k}={v}&"

        temp_url = temp_url[:-1]

        return temp_url

    @staticmethod
    def _get_page_count(url: str) -> int:
        """
        Метод для получения количества всех страниц.
        :return: количество страниц с записями
        """
        response = requests.get(url)  # отправляем запрос на сайт

        if response.ok:
            data = response.json()  # если ответ успешно получен, извлекаем из него данные

            meta = data.get("_meta")  # находим метаданные

            page_count = meta.get("pageCount")  # извлекаем число страниц

            return page_count

        return 0
