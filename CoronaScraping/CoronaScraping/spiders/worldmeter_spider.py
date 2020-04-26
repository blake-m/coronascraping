from abc import abstractmethod, ABC
import json

import js2xml
import lxml.etree
import scrapy
from parsel import Selector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse


# TODO(blake): remember to add year to dates

class BaseSpider(scrapy.Spider, ABC):
    name: str

    def __init__(self, path_selector_config: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path_selector_config, 'r') as file:
            self.selector_config = json.load(file)

    def start_requests(self):
        requests = [scrapy.Request(url, self.parse)
                    for url in self.selector_config['start_urls']]
        yield from requests

    @abstractmethod
    def parse(self, response):
        pass


class WorldMeterSpider(BaseSpider):
    name = "worldmeter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsers = (
            self.parse_country_links,
        )
        self.countries_table = self.selector_config['countries_table']
        # scripts forming a chart have this identifier name in them
        self.all_js_scripts = self.selector_config['all_js_scripts']
        self.chart_indicator = self.selector_config['chart_indicator']
        self.graph_type = self.selector_config['graph_type']
        self.x_axis = self.selector_config['x_axis']
        self.y_axis = self.selector_config['y_axis']

    def parse(self, response: HtmlResponse) -> Request:
        """"""
        for parser in self.parsers:
            yield from parser(response)

    def parse_country_links(self, response: HtmlResponse) -> Request:
        table = response.css(self.countries_table)
        all_link_tags = table.css('a')
        country_links = [link.attrib['href'] for link in all_link_tags]

        for country_link in country_links:
            full_country_link = response.urljoin(country_link)
            current_country = country_link.split('/')[1]
            yield scrapy.Request(full_country_link,
                                 callback=self.parse_country,
                                 cb_kwargs={"country": current_country})

    def parse_js_scripts(self, response):
        all_scripts = response.css(self.all_js_scripts).getall()

        for js_script in all_scripts:
            xml = lxml.etree.tostring(js2xml.parse(js_script),
                                      encoding='unicode')
            yield Selector(text=xml)

    def parse_graph_data(self, selector):
        graph_type = selector.css(self.graph_type).getall()[0]
        x_axis = selector.xpath(self.x_axis).getall()
        y_axis = selector.xpath(self.y_axis).getall()
        return graph_type, x_axis, y_axis

    @staticmethod
    def form_graph_data_dict(x_axis, y_axis):
        return {f"{x}": y for x, y in list(zip(x_axis, y_axis))}

    def check_if_is_chart_script(self, selector):
        for identifier in selector.css('identifier'):
            try:
                if identifier.attrib['name'] == self.chart_indicator:
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
        yield {f"{country}": graphs}
