import scrapy
from ..items import ScrapyBooksItem
import requests
from bs4 import BeautifulSoup

RATE_TO_NUMBER = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }


class ScrapyBooksMainSpider(scrapy.Spider):
    name = 'scrapy_books_main'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    index_url = 'http://books.toscrape.com/'

    def parse(self, response):
        book = ScrapyBooksItem()
        item_xpath = "//article[@class='product_pod']"
        items = response.xpath(item_xpath)
        next_xpath = "//*[contains(@class, 'next')]//a/@href"
        next_page_pre = response.xpath(next_xpath).extract()
        description_xpath = "//article[@class='product_page']/p//text()"
        decription = response.xpath(description_xpath)

        img_url_xpath = ".//*[contains(@class, 'image_container')]//img/@src"
        rating_xpath = ".//*[contains(@class, 'star-rating')]/@class"
        title_xpath = ".//h3/a/@title"
        price_xpath = ".//*[contains(@class, 'price_color')]//text()"

        details_xpath = './/h3/a/@href'

        if items:
            for item in items:
                # print(item.extract())
                book['img_url'] = f'{self.index_url}{item.xpath(img_url_xpath).extract()[0]}'
                rating_class = item.xpath(rating_xpath).extract()[0].split()[1]
                book['rating'] = RATE_TO_NUMBER.get(rating_class)
                book['title'] = item.xpath(title_xpath).extract()[0]
                book['price'] = float(item.xpath(price_xpath).extract()[0].removeprefix('£'))

                details_url = item.xpath(details_xpath).extract()
                description_text = ""
                if details_url:
                    details_url = f'{self.index_url}{details_url[0]}'
                    html_doc = requests.get(details_url)
                    if html_doc.status_code == 200:
                        soup = BeautifulSoup(html_doc.content, 'lxml')
                        description_text = soup.find('article', attrs={'class': 'product_page'}).p
                        print(description_text)

                yield book

        if next_page_pre:
            next_page = f'{self.index_url}catalogue/{next_page_pre[0].split("/")[-1]}'
            yield scrapy.Request(url=next_page)
