from typing import List, Union

from components import data_source
from components.main.country.graphs import TotalCasesGraph, CasesDailyGraph, \
    DeathsDailyGraph, ActiveCasesTotalGraph, DailyCases

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

CONFIG_PATH = './config.ini'


class Countries(object):
    def __init__(self):
        self.data_source = data_source.PostgresDataSource(CONFIG_PATH)
        self.list_all = self.data_source.get_countries()
        self.current_country_data = \
            self.data_source.get_pandas_dataframe_for_one_country(
                self.list_all[0]
            )
        self.current_country_name = self.list_all[0]

    def set_current_country(self, country: str) -> None:
        self.current_country_data = \
            self.data_source.get_pandas_dataframe_for_one_country(country)
        self.current_country_name = country

    @staticmethod
    def correct_country_name(country: str) -> str:
        if country in ["uk", "us"]:
            return country.upper()
        else:
            name_parts = country.split("_")
            name_parts = [
                part.capitalize() if part not in ["the", "and", "of"] else part
                for part in name_parts
            ]
            return " ".join(name_parts)

    def select_country_dropdown(self):
        dropdown_items = [
            {"label": f"{self.correct_country_name(country)}", "value": country}
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
        labels = self.current_country_data.index
        range_size = len(self.current_country_data.index)
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

    def countries_div(self) -> html.Div:
        return html.Div(id="graphs-div", children=[], className="container")

    def basic_info(self) -> html.Div:
        country = self.current_country_name
        data = self.current_country_data
        cases_total = int(data['coronavirus_cases_linear'].values[-1])
        active_cases = int(data['graph_active_cases_total'].values[-1])
        deaths = int(data['coronavirus_deaths_linear'].values[-1])
        first_case = data.index[data['graph_cases_daily'] != 0][0]
        daily_peak = int(data['graph_cases_daily'].values.max())
        recovered_total = cases_total - active_cases - deaths
        last_data = data.index[-1]

        def metric_and_value_div(
                metric: str, value: Union[str, int]) -> html.Div:
            return html.Div(
                className="col",
                children=[
                    html.H5(
                        className="card-title",
                        children=f"{metric}"
                    ),
                    html.P(
                        children=[
                            f"{value}"
                        ]
                    ),
                ]
            )

        return html.Div(
            className="card text-center",
            children=[
                html.Div(
                    className="card-header text-white bg-primary",
                    children=[
                        html.H5(
                            className="card-title",
                            children=self.correct_country_name(country)
                        ),
                        html.P(
                            style={"margin-bottom": 0},
                            children=[
                                "Basic Information"
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="card-body",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                metric_and_value_div(
                                    metric="Cases Total",
                                    value=cases_total
                                ),
                                metric_and_value_div(
                                    metric="Active Cases",
                                    value=active_cases
                                ),
                                metric_and_value_div(
                                    metric="Deaths",
                                    value=deaths
                                ),
                            ]
                        ),
                        html.Div(
                            className="row",
                            children=[
                                metric_and_value_div(
                                    metric="Recovered",
                                    value=recovered_total
                                ),
                                metric_and_value_div(
                                    metric="First Case",
                                    value=first_case
                                ),
                                metric_and_value_div(
                                    metric="Daily Peak",
                                    value=daily_peak
                                ),
                            ]
                        ),
                        html.P(
                            className="text-muted",
                            style={"margin-bottom": 0},
                            children=[
                                f"Latest data comes from: {last_data}"
                            ]
                        )
                    ]
                ),
                # html.Div(
                #     className="card-footer text-muted",
                #     children=[
                #         f"Latest data comes from: Monday"
                #     ]
                # )
            ]
        )

    def elements_maker(
            self, country: str, graph_type: str, date_range: List[int]):
        print(country, graph_type, date_range)
        self.set_current_country(country)
        df = self.current_country_data
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
            self.basic_info(),
            *graphs_to_include,
        ]
        return elements
