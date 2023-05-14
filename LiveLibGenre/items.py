# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):
    name = scrapy.Field()
    #author = scrapy.Field()
    url = scrapy.Field()
    genre = scrapy.Field()


class BookCard(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    type_book = scrapy.Field()
    description = scrapy.Field()
    genres_from_book = scrapy.Field()
    main_genre = scrapy.Field()
    number_of_pages = scrapy.Field()
    language = scrapy.Field()
    age_limit = scrapy.Field()
    publisher = scrapy.Field()
    publication_year = scrapy.Field()
    circulations = scrapy.Field()
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()
    number_of_users_read = scrapy.Field()
    number_of_users_planning = scrapy.Field()
    ISBN = scrapy.Field()
    sourceLink = scrapy.Field()
    parsing_date = scrapy.Field()
    