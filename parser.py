import random

import requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://animego.org/search/'


class FoundedObject:
    def __init__(self, name, url, image_url):
        self.name = name
        self.url = url
        self.image_url = image_url


class Parser:
    @classmethod
    def find(cls, search_type, query) -> FoundedObject:
        resp = requests.get(BASE_URL + f'{search_type}?q={"+".join(query.split())}')

        soup = bs(resp.text, 'html.parser')

        grid_items = soup.findAll('div', class_='animes-grid-item')

        items = []

        for item in grid_items:
            title = item.find('div', class_='card-title').find('a')
            image = item.find('div', class_='animes-grid-item-picture').find('div', class_='anime-grid-lazy')

            url = title['href']
            text = title['title']

            items.append(FoundedObject(name=text, url=url, image_url=image['data-original']))

        return random.choice(items)

    @classmethod
    def find_anime(cls, query) -> FoundedObject:
        return cls.find('anime', query)

    @classmethod
    def find_manga(cls, query) -> FoundedObject:
        return cls.find('manga', query)
