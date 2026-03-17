import scrapy
from datetime import datetime
from ..items.manga_item import MangaItem

class TopitoSpider(scrapy.Spider):

    name = "topito"

    start_urls = [
        "https://www.topito.com/top-meilleurs-mangas-shonen"
    ]

    def parse(self, response):

        titles = response.css("h2::text").getall()

        for title in titles:

            item = MangaItem()

            item["title"] = title.strip()

            item["source"] = "topito"

            item["url"] = response.url

            item["scraped_at"] = datetime.now().isoformat()

            yield item