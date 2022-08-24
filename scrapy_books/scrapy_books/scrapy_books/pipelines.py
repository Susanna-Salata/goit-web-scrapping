from itemadapter import ItemAdapter
import sqlite3
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from .model_2 import Book, Base, Quote


class ScrapyBooksPipeline:
    def __init__(self):
        engine = create_engine("sqlite:///library.db")
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.commit()

    def process_item(self, item, spider):
        if type(spider).__name__ == 'quotes':
            quote = Quote(text=item.get('text'),
                          author=item.get('author'),
                          author_details=item.get('author_details'),
                          tag=item.get('tag'))
            self.session.add(quote)
        elif type(spider).__name__ == 'scrapy_books_main':
            book = Book(img_url=item.get('img_url'),
                        rating=item.get('rating'),
                        title=item.get('title'),
                        price=item.get('price'))
            self.session.add(book)

        self.session.commit()

        return item

    def close_connection(self):
        self.session.close()
