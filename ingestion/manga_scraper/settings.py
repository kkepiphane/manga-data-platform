ITEM_PIPELINES = {
   'manga_scraper.pipelines.json_pipeline.JsonPipeline': 300,
}

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

USER_AGENT = "manga-data-platform-bot"

BOT_NAME = "manga_scraper"

SPIDER_MODULES = ["manga_scraper.spiders"]
NEWSPIDER_MODULE = "manga_scraper.spiders"