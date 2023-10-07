import random

import requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://animego.org/search/'


class FoundedObject:
    def __init__(self, name, url, image_url, original_name, rating):
        self.name = name
        self.url = url
        self.image_url = image_url
        self.original_name = original_name
        self.rating = rating

    def preview(self):
        return f'{self.name} {self.rating} \n{self.original_name}'


class Parser:
    @classmethod
    def find(cls, search_type, query, k: int = 5) -> list[FoundedObject]:
        resp = requests.get(BASE_URL + f'{search_type}?q={"+".join(query.split())}')

        soup = bs(resp.text, 'html.parser')

        grid_items = soup.findAll('div', class_='animes-grid-item')

        items = []

        for item in grid_items:
            title = item.find('div', class_='card-title').find('a')
            image = item.find('div', class_='animes-grid-item-picture').find('div', class_='anime-grid-lazy')

            url = title['href']
            text = title['title']
            rating = item.find('div', class_='p-rate-flag__text').contents[0] if search_type != 'manga' else ''
            original_name = item.find('div', class_='text-gray-dark-6 small mb-1 d-none d-sm-block').find(
                'div').contents[0]  if search_type != 'manga' else ''

            items.append(FoundedObject(name=text, url=url, image_url=image['data-original'], rating=rating,
                                       original_name=original_name))

        return random.choices(items, k=k if k < len(items) else len(items))

    @classmethod
    def find_anime(cls, query) -> list[FoundedObject]:
        return cls.find('anime', query)

    @classmethod
    def find_manga(cls, query) -> list[FoundedObject]:
        return cls.find('manga', query)
