from bs4 import BeautifulSoup
import requests


def get(url):
    response_get = requests.get(url)
    if response_get:
        print('connection was successful')
        return response_get
    else:
        print('connection was unsuccessful')
        return None


class AdvertisementParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.select_one('h1.c-product__title')
        if title_tag:
            return title_tag.text.replace('\n', '').replace('\u200c', '').replace(" " * 28, "")

    @property
    def price(self):
        price_tag = self.soup.find('div', class_='js-price-value')
        if price_tag:
            return price_tag.text.replace('\n', '').replace(' ', '')

    @property
    def overview(self):
        overview_tag = self.soup.find('div', class_='js-mask__text')
        if overview_tag:
            return overview_tag.text.replace('\u200c', '').replace('\n', '').replace(" " * 28, "")

    @property
    def get_specs(self):
        specs_list = self.soup.find('article', class_='c-params__border-bottom').findAll('li')
        if specs_list:
            attribute_dict = {}
            for li in specs_list:
                key = li.find('div', class_='c-params__list-key').text
                value = li.find('div', class_='c-params__list-value').text.replace("\n", "").replace(" " * 84, "").replace(
                    " " * 8, "")
                attribute_dict[key] = value
            return attribute_dict
        return None

    @property
    def images(self):
        image_tag = self.soup.find_all('img')
        if image_tag:
            src_list = list()
            link_list = list()
            for src in image_tag:
                src_list.append(src.get('data-src'))
            for li in src_list:
                if li:
                    if li.startswith('https://dkstatics-public.digikala.com/digikala-reviews/'):
                        link_list.append(li)
            return [{'url': li, 'flag': False} for li in link_list]

    def parse(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        product = dict(
            title=self.title, price=self.price,
            overview=self.overview, images=self.images,
            specs=self.get_specs
        )

        return product


if __name__ == '__main__':
    url = 'https://www.digikala.com/product/dkp-6249234'
    response = get(url)
    parse = AdvertisementParser()
    data = parse.parse(response.text)
    for key, value in data.items():
        print(f'{key} : {value}')
        print("$" * 25)
