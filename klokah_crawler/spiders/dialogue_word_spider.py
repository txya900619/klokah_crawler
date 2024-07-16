import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class DialogueWordSpider(scrapy.Spider):
    name = "dialogue_word"

    def start_requests(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/dialogue/json/SN112{dialect_id:02}.json",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for lesson_name, lesson_tid_list in response["S2"].items():
            if lesson_name in ["group", "L9", "L10", "L11", "L12"]:
                continue
            yield scrapy.Request(
                url=f"https://web.klokah.tw/text/read_embed.php?tid={lesson_tid_list[1]}&mode=1",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_read_embed,
            )

        for lesson_name, lesson_tid_list in response["S3"].items():
            if lesson_name in ["group", "L9", "L10", "L11", "L12"]:
                continue
            yield scrapy.Request(
                url=f"https://web.klokah.tw/text/read_embed.php?tid={lesson_tid_list[1]}&mode=1",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_read_embed,
            )

    def parse_read_embed(self, response):
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
