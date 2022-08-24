# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapyBooksItem(Item):
    img_url = Field()
    rating = Field()
    title = Field()
    price = Field()
    description = Field()

class QuoteItem(Item):
    text = Field()
    tags = Field()
    author = Field()
    author_details = Field()
