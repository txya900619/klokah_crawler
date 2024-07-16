for spider in readingtext liveturorial twelve twelve_word readnews sp_junior sp_senior ps_practice con_practice con_practice_word rd_practice rd_practice_word cu_practice cu_practice_word dialogue dialogue_word essay essay_word pbc mode
do
    scrapy crawl $spider -O results/$spider.json:jsonlines --logfile logs/$spider.log
done