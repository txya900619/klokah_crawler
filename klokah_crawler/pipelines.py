# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

from klokah_crawler.dialect_id_map import DIALECT_ID_MAP
from klokah_crawler.items import KlokahCrawlerItem, KlokahCrawlerSaveItem


class PostDownloadPipeline:
    def process_item(self, item, spider):
        storage_folder = get_project_settings().get("FILES_STORE")

        if not isinstance(item, KlokahCrawlerItem):
            if "audio_meta" in item:
                audio_path = item["audio_meta"][0]["path"]
                if not os.path.isabs(storage_folder):
                    storage_folder = os.path.join(
                        os.getcwd(), storage_folder.replace("./", "")
                    )
            return item

        adapter = ItemAdapter(item)
        audio_path = None
        if adapter.get("audio_meta") and len(adapter["audio_meta"]) > 0:
            audio_path = adapter["audio_meta"][0]["path"]

            if not os.path.isabs(storage_folder):
                storage_folder = os.path.join(
                    os.getcwd(), storage_folder.replace("./", "")
                )
            audio_path = os.path.join(storage_folder, audio_path)

        return KlokahCrawlerSaveItem(
            text=adapter["text"],
            mandarin=adapter["mandarin"],
            audio_path=audio_path,
            dialect=DIALECT_ID_MAP[str(adapter["dialect_id"])],
            raw_text=adapter["raw_text"],
        )
