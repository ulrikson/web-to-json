from bs4 import BeautifulSoup
import requests
import json


class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = self.__get_soup()
        self.content = {}

    def convert_to_json(self):
        self.__get_headers()
        self.__get_links()

        with open("test.json", "w", encoding="utf-8") as file:
            json.dump(self.content, file, indent=4, ensure_ascii=False)

    def __get_soup(self):
        html = requests.get(self.url).content
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def __get_links(self):
        self.content["links"] = []

        for link in self.soup.find_all("a"):
            try:
                self.content["links"].append(link["href"])
            except KeyError:
                continue

    def __get_headers(self):
        self.content["headers"] = {}

        for i in range(1, 7):
            title = "h" + str(i)
            header = [link.text for link in self.soup.find_all(title)]
            self.content["headers"][title] = header
