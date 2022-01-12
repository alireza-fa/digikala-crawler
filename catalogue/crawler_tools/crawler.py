from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from catalogue.crawler_tools.config import START_PAGE, END_PAGE, COUNT, URL
from catalogue.crawler_tools.data_save import AdvertisementParser
from catalogue.models import ProductLink, Product, ProductAttribute, ProductImageLink


class CrawlerBase(ABC):
    def __init__(self):
        self.count = COUNT
        self.start_page = START_PAGE
        self.end_page = END_PAGE

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass

    def get(self, url):
        response_get = requests.get(url)
        if response_get:
            print(f'connection was successful\tpage number : {self.start_page}')
            self.count += 1
            return response_get
        else:
            print('connection was unsuccessful')
            return None


class LinkCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.url = URL

    @staticmethod
    def find_links(html_doc):
        html = BeautifulSoup(html_doc, 'html.parser')
        hrefs = html.findAll('div', class_='c-product-box__content--row')
        links = []
        for href in hrefs:
            links.append('https://www.digikala.com' + href.find('a').get('href'))
        return links

    def crawl_links(self, url):
        crawl = True
        links_list = list()
        while crawl:
            if self.end_page <= self.start_page:
                crawl = False
            response = self.get(url.format(str(self.start_page)))
            self.start_page += 1
            new_links = self.find_links(response.text)
            if new_links:
                print(new_links)
                links_list.extend(new_links)
            else:
                crawl = False

        return links_list

    def start(self):
        links = self.crawl_links(self.url)
        self.store(data=links)
        return 'crawler link was is successfully done'

    def store(self, data):
        for link in data:
            try:
                li = ProductLink.objects.create(url=link)
                print(li.url)
            except:
                pass


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementParser()

    def __load_links(self):
        return ProductLink.objects.filter(flag=False)

    def start(self):
        for link in self.links:
            if not link.flag:
                response = self.get(link.url)
                if response is not None:
                    data = self.parser.parse(response.text)
                    self.store(data)
                    link.flag = True
                    link.save()

    def store(self, data):
        product = Product.objects.create(
            title=data['title'], price=data['price'], description=data['overview']
        )
        for image in data['images']:
            ProductImageLink.objects.create(
                url=image['url']
            )
        for key, value in data['specs'].items():
            ProductAttribute.objects.create(
                product=product, title=key, value=value
            )
        print('crawling is successfully')
        
