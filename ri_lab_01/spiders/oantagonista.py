# -*- coding: utf-8 -*-
import scrapy
import json
import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    allowed_domains = ['oantagonista.com']
    start_urls = []
    start_page = 1
    limit_date = datetime.datetime(2019,1,1)

    def __init__(self, *a, **kw):
        super(OantagonistaSpider, self).__init__(*a, **kw)
        with open('seeds/oantagonista.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        def checkDate(response, lowerLimit):
            currentDate = response.css('time.entry-date ::attr(datetime)').get()
            currentDate = currentDate.split(' ')[0].split('-')

            date =  datetime.datetime(int(currentDate[-3]), int(currentDate[-2]), int(currentDate[-1]))

            return date > lowerLimit

        if (checkDate(response, self.limit_date) and self.start_page <= 2):
            for quote in response.css('div.container-post-home'):
                yield {
                    'title': quote.css('a.article_link h2::text').get(),
                    'date': quote.css('a.article_link span time::text').get(),
                    'section': quote.css('a.article_link span span::text').get(),
                    'author': quote.css('a.article_link span div::text').get(),
                    'text': quote.css('a.article_link p::text').get(),
                    'url': quote.css('a.article_link::attr("href")').get()
                }
            nextPage = self.start_urls[0] + 'pagina/' + str(self.start_page) +'/?ajax'
            self.start_page = self.start_page + 1

            page = response.url.split("/")[-2]
            filename = 'quotes-%s.html' % page
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)

            yield scrapy.Request(nextPage, callback=self.parse)
        #
        #
        #
