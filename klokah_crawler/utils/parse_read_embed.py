from klokah_crawler.items import KlokahCrawlerItem


def parse_read_embed(response):
    for sentence in response.css("#read-main > div"):
        sentence_text = " ".join(sentence.css("div.word::text").getall())
        translated_text = sentence.css("div.read-sentence.Ch::text").get()
        audio_data_value = sentence.css(".read-play-btn::attr(data-value)").get()
        audio_url = response.css(
            f'audio[data-value="{audio_data_value}"] > source::attr(src)'
        ).get()

        if translated_text is None or len(translated_text) == 0:
            continue

        yield KlokahCrawlerItem(
            audio_url=[audio_url],
            text=sentence_text,
            mandarin=translated_text,
            dialect_id=response.meta["dialect_id"],
        )
