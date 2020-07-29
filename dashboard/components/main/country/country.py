from typing import List

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from components import data_source
from components.main.country.graphs import TotalCasesGraph, CasesDailyGraph, \
    DeathsDailyGraph, ActiveCasesTotalGraph, DailyCases

CONFIG_PATH = './config.ini'


class Countries(object):
    def __init__(self):
        self.data_source = data_source.PostgresDataSource(CONFIG_PATH)
        self.list_all = self.data_source.get_countries()
        self.current = self.data_source.get_pandas_dataframe_for_one_country(
            self.list_all[0])

    def set_current_country(self, country: str) -> None:
        self.current = self.data_source.get_pandas_dataframe_for_one_country(
            country)

    def select_country_dropdown(self):
        dropdown_items = [
            {"label": f"{country}", "value": country}
            for country in self.list_all
        ]

        select_country = dbc.Select(
            id="countries_dropdown",
            options=dropdown_items,
            value=self.list_all[0],
            className="custom-select",
        )
        return select_country

    def select_graph_type(self):
        return dbc.RadioItems(
            options=[
                {"label": "Dedicated", "value": "Dedicated"},
                {"label": "Bar", "value": "Bar"},
                {"label": "Line", "value": "Line"},
            ],
            value="Dedicated",
            id="radio_graph_type",
            inline=True,
        )

    def select_date_range(self):
        labels = self.current.index
        range_size = len(self.current.index)
        value_range = list(range(range_size))
        print("value_range", value_range)
        min_value = min(value_range)
        max_value = max(value_range)
        print(min_value, max_value)
        print(min_value, type(max_value))
        marks = {
            value: mark for value, mark
            in zip(value_range, labels)
            if value % 15 == 0
        }
        return dcc.RangeSlider(
            id='date-range-slider',
            min=min_value,
            max=max_value,
            marks=marks,
            step=1,
            value=[min_value, max_value]
        )

    def countries_div(self):
        return html.Div(id="graphs-div", children=[], className="container")

    def elements_maker(
            self, country: str, graph_type: str, date_range: List[int]):
        print(country, graph_type, date_range)
        self.set_current_country(country)
        df = self.current
        print(df.columns)
        graphs_to_include_classes = [
            DailyCases,
            TotalCasesGraph,
            CasesDailyGraph,
            DeathsDailyGraph,
            ActiveCasesTotalGraph,
        ]
        graphs_to_include = [
            graph_class(df, country, graph_type, date_range).get_graph()
            for graph_class in graphs_to_include_classes
        ]

        # Clean out graphs that returned None
        graphs_to_include = [
            graph for graph in graphs_to_include if graph is not None]

        elements = [
            # TODO(blake): implement a div with basic info
            html.H3(f"Total Cases: {'214214123'}"),
            *graphs_to_include,
        ]
        return elements
