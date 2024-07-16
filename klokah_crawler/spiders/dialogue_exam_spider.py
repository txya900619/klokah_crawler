import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class DialogueExamSpider(scrapy.Spider):
    name = "dialogue_exam"

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
            if lesson_name == "group":
                continue

            exam_index = 2
            if lesson_name in ["L9", "L10", "L11", "L12"]:
                exam_index = 1
            yield scrapy.Request(
                url=f"https://web.klokah.tw/text/php/getSentence.php?tid={lesson_tid_list[exam_index]}",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_get_sentence,
            )

        for lesson_name, lesson_tid_list in response["S3"].items():
            if lesson_name == "group":
                continue

            exam_index = 2
            if lesson_name in ["L9", "L10", "L11", "L12"]:
                exam_index = 1
            yield scrapy.Request(
                url=f"https://web.klokah.tw/text/php/getSentence.php?tid={lesson_tid_list[exam_index]}",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_get_sentence,
            )

    def parse_get_sentence(self, response):
        dialect_id = response.meta["dialect_id"]
        for sentence in response.json():
            audio_path = sentence["mp3"]
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/text/{audio_path}"],
                text=sentence["ab"],
                mandarin=sentence["ch"],
                dialect_id=dialect_id,
            )
