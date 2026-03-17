import scrapy

class MangaItem(scrapy.Item):

    title = scrapy.Field()

    genre = scrapy.Field()

    rating = scrapy.Field()

    source = scrapy.Field()

    url = scrapy.Field()

    scraped_at = scrapy.Field()