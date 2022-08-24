import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    index_url = 'http://quotes.toscrape.com/'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        quote_item = QuoteItem()
        item_xpath = "//*[contains(@class, 'quote')]"
        items = response.xpath(item_xpath)
        next_xpath = "//*[contains(@class, 'next')]//a/@href"
        next_page_pre = response.xpath(next_xpath).extract()

        text_xpath = ".//*[contains(@class, 'text')]//text()"
        author_xpath = ".//*[contains(@class, 'author')]//text()"
        author_details_xpath = ".//*[contains(@class, 'author')]//a/@href"
        tags_xpath = ".//*[contains(@class, 'tag')]//text()"

        for item in items:
            print(item.extract())
            quote_item['text'] = ' '.join(item.xpath(text_xpath).extract()).replace('"', '').replace('\n', ' ').replace('“', '').replace('”', '').replace(r'\n            ', ' ')
            # print(f">>>>>>> {quote_item['text']}")
            quote_item['author'] = item.xpath(author_xpath).extract()[0]
            # print(f">>>>>>> {quote_item['author']}")
            quote_item['author_details'] = item.xpath(author_details_xpath).extract()
            exceptions = ['\n', '\nTags:\n', '\n\n']
            tags = [t.replace(r'\n', '').replace(' ','') for t in item.xpath(tags_xpath).extract()]
            tags = [t for t in tags if t not in exceptions]
            quote_item['tags'] = tags
            yield quote_item

        if next_page_pre:
            next_page = f'{self.index_url}{next_page_pre[0]}'.replace('.com//', '.com/')
            print(f'>>>>>>>>> next page: {next_page}')
            yield scrapy.Request(url=next_page)



