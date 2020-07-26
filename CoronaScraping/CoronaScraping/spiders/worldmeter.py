import abc

import js2xml
import lxml.etree
from parsel import Selector
import scrapy
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse

from CoronaScraping import config


# TODO(blake): remember to add year to dates


class BaseSpider(scrapy.Spider, abc.ABC):
    name = 'base'

    def __init__(self, path_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config.ConfigData(path_config)

    def start_requests(self):
        requests = [scrapy.Request(url, self.parse)
                    for url in self.config.start_urls]
        yield from requests


class CountryGraphsDataExtractingSpider(BaseSpider):
    name = "country_graphs_data_extracting_spider"

    def __init__(self, path_config, *args, **kwargs):
        super().__init__(path_config, *args, **kwargs)

    def parse(self, response):
        yield from self.parse_country_links(response)

    def parse_country_links(self, response: HtmlResponse) -> Request:
        table = response.css(self.config.countries_table)
        all_link_tags = table.css('a')
        country_links = [link.attrib['href'] for link in all_link_tags]

        for country_link in country_links:
            full_country_link = response.urljoin(country_link)
            current_country = country_link.split('/')[1]
            yield scrapy.Request(full_country_link,
                                 callback=self.parse_country,
                                 cb_kwargs={"country": current_country})
            # TODO(blake): remove break - it's here just to make the requests quicker
            # break

    def parse_js_scripts(self, response):
        all_scripts = response.css(self.config.all_js_scripts).getall()

        for js_script in all_scripts:
            xml = lxml.etree.tostring(js2xml.parse(js_script),
                                      encoding='unicode')
            yield Selector(text=xml)

    def parse_graph_data(self, selector):
        graph_type = selector.css(self.config.graph_type).getall()[0]
        x_axis = selector.xpath(self.config.x_axis).getall()
        y_axis = selector.xpath(self.config.y_axis).getall()
        return graph_type, x_axis, y_axis

    @staticmethod
    def form_graph_data_dict(x_axis, y_axis):
        return {f"{x}": y for x, y in list(zip(x_axis, y_axis))}

    def check_if_is_chart_script(self, selector):
        for identifier in selector.css('identifier'):
            try:
                if identifier.attrib['name'] == self.config.chart_indicator:
                    return True
            except KeyError:
                pass
        return False

    def parse_country(self, response: HtmlResponse, country: str) -> Request:
        graphs = {}
        for selector in self.parse_js_scripts(response):
            if self.check_if_is_chart_script(selector):
                graph_type, x_axis, y_axis = self.parse_graph_data(
                    selector=selector)
                graphs[f"{graph_type}"] = self.form_graph_data_dict(
                    x_axis, y_axis)
        print(f"{country}: {graphs}")
        yield {f"{country}": graphs}
