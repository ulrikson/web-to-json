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
        self.__get_imgs()
        self.__get_links()
        self.__get_text()

        with open("test.json", "w", encoding="utf-8") as file:
            json.dump(self.content, file, indent=4, ensure_ascii=False)

    def __get_soup(self):
        response = requests.get(self.url)
        print(response.status_code)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def __get_headers(self):
        self.content["headers"] = {}

        for i in range(1, 7):
            title = "h" + str(i)
            header = [link.text for link in self.soup.find_all(title)]
            self.content["headers"][title] = header

    def __get_links(self):
        self.content["links"] = []

        for url in self.soup.find_all("a"):
            try:
                link = self.__get_exact_url(url["href"])
                self.content["links"].append(link)
            except KeyError:
                continue

    def __get_imgs(self):
        self.content["imgs"] = []

        for img in self.soup.find_all("img"):
            try:
                link = self.__get_exact_url(img["src"])
                self.content["imgs"].append(link)
            except KeyError:
                continue

    def __get_exact_url(self, link):
        return self.url + link if link[0] == "/" else link

    def __get_text(self):
        self.content["text"] = []

        for element in self.soup.find_all("p"):
            self.content["text"].append(element.text)
