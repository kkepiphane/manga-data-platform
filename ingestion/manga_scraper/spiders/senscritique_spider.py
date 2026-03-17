import scrapy
from datetime import datetime
from ..items.manga_item import MangaItem

class SensCritiqueSpider(scrapy.Spider):

    name = "senscritique"

    start_urls = [
        "https://www.senscritique.com/bd/dragon_ball/88965"
    ]

    def parse(self, response):

        item = MangaItem()

        item["title"] = response.css("h1::text").get()

        item["rating"] = response.css(".sc-1q6h6u8-0::text").get()

        item["genre"] = response.css("a[href*='genre']::text").getall()

        item["source"] = "senscritique"

        item["url"] = response.url

        item["scraped_at"] = datetime.now().isoformat()

        yield item