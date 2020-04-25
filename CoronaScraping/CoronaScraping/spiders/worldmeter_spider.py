from typing import List

import js2xml
import lxml.etree
from parsel import Selector

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.http.request import Request


class WorldMeterSpider(scrapy.Spider):
    name = 'worldmeter'

    start_urls = [
        'https://www.worldometers.info/coronavirus/'
    ]

    def parse(self, response: HtmlResponse) -> Request:
        table = response.css('#main_table_countries_today')
        all_link_tags = table.css('a')
        country_links = [link.attrib['href'] for link in all_link_tags]

        for country_link in country_links:
            full_country_link = response.urljoin(country_link)
            current_country = country_link.split('/')[1]
            yield scrapy.Request(full_country_link,
                                 callback=self.parse_country,
                                 cb_kwargs={"country": current_country})

        # yield from response.follow_all(all_link_tags,
        #                                callback=self.parse_country)

    def parse_country(self, response: HtmlResponse, country: str) -> Request:
        all_scripts = response.css(
            'script[type="text/javascript"]::text').getall()

        for i, js_script in enumerate(all_scripts):
            xml = lxml.etree.tostring(js2xml.parse(js_script),
                                      encoding='unicode')
            selector = Selector(text=xml)
            all_ = selector.getall()
            folder = "/home/blake/PycharmProjects/Coronavirus/scripts/new/"
            with open(f'{folder}{country}-script-{i}.xml', 'a') as file:
                for script in all_:
                    file.write(script)




