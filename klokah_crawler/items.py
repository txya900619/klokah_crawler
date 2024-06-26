# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class KlokahCrawlerItem:
    audio_url: list[str]
    text: str
    mandarin: str
    dialect_id: int
    audio_meta: list[dict] = None


@dataclass
class KlokahCrawlerSaveItem:
    text: str
    mandarin: str
    dialect: str
    audio_path: str = None
