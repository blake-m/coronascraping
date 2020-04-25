import js2xml
import lxml.etree
import scrapy
from parsel import Selector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse


# TODO(blake): remember to add year to dates

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

    def parse_country(self, response: HtmlResponse, country: str) -> Request:
        all_scripts = response.css(
            'script[type="text/javascript"]::text').getall()

        graphs = []
        for js_script in all_scripts:
            xml = lxml.etree.tostring(js2xml.parse(js_script),
                                      encoding='unicode')
            selector = Selector(text=xml)

            # scripts forming a chart have this identifier name in them
            chart_indicator = 'Highcharts'
            is_chart_script = False
            for identifier in selector.css('identifier'):
                try:
                    if identifier.attrib['name'] == chart_indicator:
                        is_chart_script = True
                        break
                except KeyError:
                    pass

            if is_chart_script:
                graph_type, x_axis, y_axis = self.extract_graph_data(
                    selector=selector)
                graph = {
                    f"{graph_type}": {
                        f"{x}": y for x, y in list(zip(x_axis, y_axis))
                    }
                }
                graphs.append(graph)

        yield {f"{country}": graph for graph in graphs}

    def extract_graph_data(self, selector):
        graph_type = selector.css('arguments string::text').getall()[0]
        x_axis = selector.xpath(
            '//property[contains(@name, "categories")]//string/text()').getall()
        y_axis = selector.xpath(
            '//property[contains(@name, "data")]//number/@value').getall()
        return graph_type, x_axis, y_axis
