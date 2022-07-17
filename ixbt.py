from datetime import datetime, timedelta
import requests
import json
from bs4 import BeautifulSoup

from base_class import BaseParser


class IxbtParser(BaseParser):
    """Парсер для сайта ixbt.com"""

    def collect_data(self, date_from: datetime, date_to: datetime) -> str:
        """
        Метод для парсинга информации за некоторый промежуток времени.
        :param date_from: дата начала сбора информации.
        :param date_to: дата окончания сбора информации.
        :return: текстовый ответ для пользователя
        """
        dates = [date_from + timedelta(days=x) for x in range((date_to - date_from).days + 1)]

        result = list()

        for date in dates:
            result += self._get_data(date)
            print(f"[+] Получены новости за {date.strftime('%d.%m.%Y')}")

        self._save_data(result)

        return f"[SUCCESS] Новости за период {date_from.strftime('%d.%m.%Y')} - " \
               f"{date_to.strftime('%d.%m.%Y')} собраны в файл {self.filename}"

    def _get_data(self, date: datetime) -> list:
        """
        Метод для сбора новостей за определенный день.
        :param date: день, за который нужно получить новости.
        :return: список новостей.
        """
        temp_result = list()
        day, month, year = date.strftime("%d-%m-%Y").split("-")

        url = self.url.format(year=year, month=month, day=day)

        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, "lxml")

        items = soup.find_all("div", class_="item no-padding")

        for item in items:
            item_dct = {
                "title": item.find("div", class_="b-article__header").find("h2").text.strip(),

                "subtitle": item.find("div", class_="b-article__header").find("h4").text.strip(),

                "url": item.find("div", class_="comment_content").get("data-url"),

                "time": f'{day}.{month}.{year} {item.find("span", class_="time_iteration_icon").text.strip()}',

                "text": " ".join(
                    [p.text.strip().replace("&nbsp;", "") for p in item.find("div", class_="item__text").find_all("p")])
            }

            tags = item.find("p", class_="b-article__tags__list")
            sources = item.find("p", class_="b-article__source__list")

            if tags is None:
                item_dct["tags"] = []

            else:
                item_dct["tags"] = [tag.text for tag in tags.find_all("a")]

            if sources is None:
                item_dct["sources"] = []

            else:
                item_dct["sources"] = [source.text for source in sources.find_all("a")]

            temp_result.append(item_dct)

        return temp_result
