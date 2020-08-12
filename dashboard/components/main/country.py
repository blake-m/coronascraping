from datetime import datetime
from typing import List, Union, Dict

from components import data_source

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import numpy as np
import pandas as pd

from components.auxiliary import funcs
from components.auxiliary.reusable import labeled_div_with_class_and_id
from components.graphs.figs import INSTALLED_GRAPHS

CONFIG_PATH = './config.ini'
GRAPH_CLASSES = INSTALLED_GRAPHS.values()


class Country(object):
    def __init__(self):
        t1 = datetime.now()
        self.data_source = data_source.PostgresDataSource(CONFIG_PATH)
        self.list_all = self.data_source.get_countries()
        self.detailed_data = self.data_source.get_dataframe_for_all_countries()
        t2 = datetime.now()
        print("COMMON DATA STARTUP TIME:", t2 - t1)

        t1 = datetime.now()
        self.current_country_data = \
            self.data_source.get_dataframe_for_one_country(
                self.list_all[0]
            )
        print("current_country_data\n", self.current_country_data)
        self.current_country_name = self.list_all[0]
        t2 = datetime.now()
        print("COUNTRIES STARTUP TIME: ", t2 - t1)

        t1 = datetime.now()
        self.summary_data = self.get_all_countries_summary()
        t2 = datetime.now()
        print("ALL COUNTRIES STARTUP TIME: ", t2 - t1)

        t1 = datetime.now()
        self.detailed_data = self.data_source.get_dataframe_for_all_countries()
        self.world_data = self.get_world_data()
        print("world_data\n", self.world_data)
        t2 = datetime.now()

        print("ALL COUNTRIES STARTUP TIME: ", t2 - t1)

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

    def set_current_country(self, country: str) -> None:
        print("FIRED (set_current_country)")
        self.current_country_data = \
            self.data_source.get_dataframe_for_one_country(country)
        self.current_country_name = country

    @labeled_div_with_class_and_id(
        label="Country", class_name="col-8 mb-3")
    def select_country_dropdown(self):
        dropdown_items = [
            {"label": f"{self.correct_country_name(country)}", "value": country}
            for country in self.list_all
        ]
        select_country = dbc.Select(
            id="countries_dropdown",
            options=dropdown_items,
            value="poland",  # Explicitly set
            className="custom-select",
        )
        return select_country

    @labeled_div_with_class_and_id(
        label="Graph Type", class_name="col-2")
    def select_graph_type(self, id_: str) -> dbc.RadioItems:
        return dbc.RadioItems(
            options=[
                {"label": "Dedicated", "value": "Dedicated"},
                {"label": "Bar", "value": "Bar"},
                {"label": "Line", "value": "Line"},
            ],
            value="Dedicated",
            id=id_,
            inline=True,
        )

    @labeled_div_with_class_and_id(
        label="Graph Appearance", class_name="col-2")
    def select_graph_width(self, graph_type: str):
        return dbc.Checklist(
            options=[
                {"label": "Wide Graphs", "value": True},
            ],
            value=[],
            id={
                "index": graph_type,
                "type": "graph-width"
            },
            switch=True,
        )

    @labeled_div_with_class_and_id(
        label="Date Range", class_name="col-12")
    def select_date_range(self, scope: str = "country") -> dcc.RangeSlider:
        if scope == "world":
            data = self.world_data
        else:
            data = self.current_country_data
        labels = data.index
        range_size = len(data.index)
        value_range = list(range(range_size))
        min_value = min(value_range)
        max_value = max(value_range)

        mark_values = np.linspace(start=0, stop=max_value, num=10, dtype=int)

        marks = {
            value: funcs.date_to_month_day_format(mark) for value, mark
            in zip(value_range, labels)
            if value in mark_values
        }
        return dcc.RangeSlider(
            id=f'date-range-slider-{scope}',
            min=min_value,
            max=max_value,
            marks=marks,
            step=1,
            value=[min_value, max_value]
        )

    def countries_div(
            self, graph_classes: List[str] = GRAPH_CLASSES) -> html.Div:
        return html.Div(
            id="countries-content",
            children=[
                html.Div(
                    id="basic-info-div",
                    className="container",
                    children=[
                        self.basic_info(),
                    ]
                ),
                html.Div(
                    id={
                        "type": "graphs",
                        "index": "country"
                    },
                    className="container",
                    children=[
                        *[dcc.Loading(
                            id="loading-table",
                            children=[
                                html.Div(
                                    id={
                                        "index": f"{graph.__name__}",
                                        "type": "graph-countries-div",
                                    },
                                    children=html.Div(
                                        style={"min-height": "100px"}
                                    )
                                )
                            ]
                        ) for graph in graph_classes]
                    ]
                )
            ],
            style={"min-height": "500px"},
        )

    def basic_info(self) -> html.Div:
        country = self.current_country_name
        data = self.current_country_data
        not_available_message = "Data Not Available"

        try:
            cases_total = int(data['coronavirus_cases_linear'].values[-1])
        except KeyError:
            cases_total = not_available_message

        try:
            active_cases = int(data['graph_active_cases_total'].values[-1])
        except KeyError:
            active_cases = not_available_message

        try:
            deaths = int(data['coronavirus_deaths_linear'].values[-1])
        except KeyError:
            deaths = not_available_message

        try:
            first_case = funcs.date_to_day_month_year_format(
                data.index[data['graph_cases_daily'] != 0][0])
        except KeyError:
            first_case = not_available_message

        try:
            daily_peak = int(data['graph_cases_daily'].values.max())
        except KeyError:
            daily_peak = not_available_message

        try:
            recovered_total = cases_total - active_cases - deaths
        except TypeError:
            recovered_total = not_available_message

        last_data = funcs.date_to_day_month_year_format(data.index[-1])

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
            ]
        )

    def get_country_basic_info(self, country_data: pd.DataFrame) -> Dict:
        not_available_message = "N/A"
        country_summary = {}
        try:
            country_summary["Cases Total"] = \
                country_data['coronavirus_cases_linear'].values[-1]
        except KeyError:
            country_summary["Cases Total"] = not_available_message

        try:
            country_summary["New Cases"] = \
                country_data['graph_cases_daily'].values[-1]
            country_summary["Daily Peak"] = country_data[
                'graph_cases_daily'].values.max()
        except KeyError:
            country_summary["New Cases"] = not_available_message
            country_summary["Daily Peak"] = not_available_message

        try:
            country_summary["Active Cases"] = \
                country_data['graph_active_cases_total'].values[-1]
        except KeyError:
            country_summary["Active Cases"] = not_available_message

        try:
            country_summary["Deaths"] = \
                country_data['coronavirus_deaths_linear'].values[-1]
        except KeyError:
            country_summary["Deaths"] = not_available_message

        try:
            country_summary["First Case"] = \
                funcs.date_to_day_month_year_format(
                    country_data.index[country_data['graph_cases_daily'] != 0][
                        0])
        except KeyError:
            country_summary["First Case"] = not_available_message

        try:
            country_summary["Recovered Total"] = country_summary[
                                                     "Cases Total"] - \
                                                 country_summary[
                                                     "Active Cases"] - \
                                                 country_summary["Deaths"]
        except TypeError:
            country_summary["Recovered Total"] = not_available_message

        return country_summary

    def get_all_countries_summary(self) -> pd.DataFrame:
        t1 = datetime.now()

        summary_data_list = []
        for country in self.list_all:
            country_data = self.detailed_data[
                self.detailed_data["country"] == country]
            country_data_summarized = {
                "Country": country,
                **self.get_country_basic_info(country_data)
            }
            summary_data_list.append(country_data_summarized)

        df_grouped = pd.DataFrame(summary_data_list)
        df_grouped["Country"] = df_grouped["Country"].apply(
            self.correct_country_name)
        t2 = datetime.now()
        print("get_all_countries_summary TIME: ", t2 - t1)
        return df_grouped

    def get_world_data(self) -> pd.DataFrame:
        grouped_by_day = self.detailed_data.drop("country", axis=1)
        grouped_by_day = grouped_by_day.fillna(0)

        grouped_by_day["date_sortable"] = pd.to_datetime(
            grouped_by_day["date"],
            # format="%Y %b %d"
        )

        grouped_by_day = grouped_by_day. \
            groupby("date_sortable", as_index=False, dropna=False). \
            sum()

        grouped_by_day = grouped_by_day.sort_values(by=["date_sortable"])
        grouped_by_day = grouped_by_day.set_index('date_sortable')
        grouped_by_day.to_excel("GROUPED.xlsx")

        return grouped_by_day

    def world_basic_info(self) -> html.Div:
        div_name = "World"
        data = self.world_data
        not_available_message = "Data Not Available"

        try:
            cases_total = int(data['coronavirus_cases_linear'].values[-1])
        except KeyError:
            cases_total = not_available_message

        try:
            active_cases = int(data['graph_active_cases_total'].values[-1])
        except KeyError:
            active_cases = not_available_message

        try:
            deaths = int(data['coronavirus_deaths_linear'].values[-1])
        except KeyError:
            deaths = not_available_message

        try:
            first_case = data.index[data['graph_cases_daily'] != 0][0]
        except KeyError:
            first_case = not_available_message

        try:
            daily_peak = int(data['graph_cases_daily'].values.max())
        except KeyError:
            daily_peak = not_available_message

        try:
            recovered_total = cases_total - active_cases - deaths
        except TypeError:
            recovered_total = not_available_message

        last_data = funcs.date_to_day_month_year_format(data.index[-1])

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
                            children=self.correct_country_name(div_name)
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
            ]
        )

    def world_div(
            self, graph_classes: List[str] = GRAPH_CLASSES) -> html.Div:
        return html.Div(
            id="world-detail-content",
            children=[
                html.Div(
                    id="basic-info-div",
                    className="container",
                    children=[
                        self.world_basic_info(),
                    ]
                ),
                html.Div(
                    id={
                        "type": "graphs",
                        "index": "world"
                    },
                    className="container",
                    children=[
                        *[dcc.Loading(
                            id="loading-table",
                            children=[
                                html.Div(
                                    id={
                                        "index": f"{graph.__name__}",
                                        "type": "graph-world-div",
                                    },
                                    children=html.Div(
                                        style={"min-height": "100px"}
                                    )
                                )
                            ]
                        ) for graph in graph_classes]
                    ]
                )
            ],
            style={"min-height": "500px"},
        )


def main():
    countries = Country()


if __name__ == "__main__":
    main()
