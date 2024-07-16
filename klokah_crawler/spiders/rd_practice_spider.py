import scrapy
from scrapy_playwright.page import PageMethod

from klokah_crawler.utils.parse_read_embed import parse_read_embed


class RdPracticeSpider(scrapy.Spider):
    name = "rd_practice"

    def start_requests(self):
        urls = [
            (
                dialect_id,
                f"https://web.klokah.tw/extension/rd_practice/index.php?d={dialect_id}&l={lesson_id}&view=article",
            )
            for lesson_id in range(1, 31)
            for dialect_id in [i for i in range(1, 44) if i != 12]
        ]
        for dialect_id, url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.get_iframe_url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "#text-frame"),
                    ],
                    "dialect_id": dialect_id,
                },
            )

    def get_iframe_url(self, response):
        yield scrapy.Request(
            url=response.css("#text-frame::attr(src)").get(),
            meta={"dialect_id": response.meta["dialect_id"]},
            callback=parse_read_embed,
        )
