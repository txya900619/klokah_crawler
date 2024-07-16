import scrapy
from scrapy_playwright.page import PageMethod

from klokah_crawler.items import KlokahCrawlerItem


class CuPracticeSpider(scrapy.Spider):
    name = "cu_practice"

    def start_requests(self):
        urls = [
            (
                dialect_id,
                f"https://web.klokah.tw/extension/cu_practice/index.php?d={dialect_id}&l={lesson_id}&view=article",
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
        )

    def parse(self, response):
        for sentence in response.css("#read-main > div"):
            sentence_text = " ".join(sentence.css("div.word::text").getall())
            translated_text = sentence.css("div.read-sentence.Ch::text").get()
            audio_data_value = sentence.css(".read-play-btn::attr(data-value)").get()
            audio_url = response.css(
                f'audio[data-value="{audio_data_value}"] > source::attr(src)'
            ).get()

            yield KlokahCrawlerItem(
                audio_url=[audio_url],
                text=sentence_text,
                mandarin=translated_text,
                dialect_id=response.meta["dialect_id"],
            )
