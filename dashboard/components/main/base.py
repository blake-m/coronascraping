import abc
from datetime import datetime
from typing import List, Dict

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import numpy as np
import pandas as pd

from components import data_source
from components.auxiliary import funcs
from components.auxiliary.reusable import labeled_div_with_class_and_id, \
    print_startup_time
from components.graphs.figs import INSTALLED_GRAPHS

CONFIG_PATH = './config.ini'
NOT_AVAILABLE_MESSAGE = "Data N/A"


class ComponentsData(object):
    @print_startup_time("ALL COMPONENTS DATA")
    def __init__(self):
        @print_startup_time("COMMON DATA")
        def init_common_data():
            self.source = data_source.PostgresDataSource(CONFIG_PATH)
            self.all_countries_names_list = self.source.get_countries()
            self.all_counries = self.source.get_dataframe_for_all_countries()

        @print_startup_time("CURRENT SINGLE COUNTRY DATA")
        def init_current_single_country_data():
            self.current_country = \
                self.source.get_dataframe_for_one_country(
                    self.all_countries_names_list[0])
            self.current_country_name = self.all_countries_names_list[0]

        @print_startup_time("WORLD DATA")
        def init_world_data():
            self.summary_data = self.get_all_countries_summary()
            self.all_counries = self.source.get_dataframe_for_all_countries()
            self.world = self.get_world_data()

        init_common_data()
        init_current_single_country_data()
        init_world_data()

    def set_current_country(self, country: str) -> None:
        self.current_country = \
            self.source.get_dataframe_for_one_country(country)
        self.current_country_name = country

    def get_all_countries_summary(self) -> pd.DataFrame:
        t1 = datetime.now()

        summary_data_list = []
        for country in self.all_countries_names_list:
            country_data = self.all_counries[
                self.all_counries["country"] == country]
            country_data_summarized = {
                "Country": country,
                **self.get_country_basic_info_dict(country_data)
            }
            summary_data_list.append(country_data_summarized)

        df_grouped = pd.DataFrame(summary_data_list)
        df_grouped["Country"] = df_grouped["Country"].apply(
            funcs.correct_country_name)
        t2 = datetime.now()
        print("get_all_countries_summary TIME: ", t2 - t1)
        return df_grouped

    def get_world_data(self) -> pd.DataFrame:
        grouped_by_day = self.all_counries.drop("country", axis=1)
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
        # grouped_by_day.to_excel("GROUPED.xlsx")

        return grouped_by_day

    @staticmethod
    def get_cases_total_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data['coronavirus_cases_linear'].values[-1]
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_active_cases_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data['graph_active_cases_total'].values[-1]
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_new_cases_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data['graph_cases_daily'].values[-1]
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_deaths_total_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data['coronavirus_deaths_linear'].values[-1]
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_first_case_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            first_case_raw = data.index[data['graph_cases_daily'] != 0][0]
            return funcs.date_to_day_month_year_format(first_case_raw)
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_daily_peak_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data['graph_cases_daily'].values.max()
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_recovered_total_or_no_data_message(data: pd.DataFrame) -> str:
        try:
            return data.index[data['graph_cases_daily'] != 0][0]
        except KeyError:
            return NOT_AVAILABLE_MESSAGE

    @staticmethod
    def get_latest_data(data: pd.DataFrame) -> str:
        return funcs.date_to_day_month_year_format(data.index[-1])

    def get_country_basic_info_dict(self, data: pd.DataFrame) -> Dict:
        summary_dict = {
            "Cases Total": self.get_cases_total_or_no_data_message(data),
            "Daily Peak": self.get_daily_peak_or_no_data_message(data),
            "New Cases": self.get_new_cases_or_no_data_message(data),
            "Active Cases": self.get_active_cases_or_no_data_message(data),
            "Deaths": self.get_deaths_total_or_no_data_message(data),
            "First Case": self.get_first_case_or_no_data_message(data),
            "Latest Data": self.get_latest_data(data),
        }

        try:
            summary_dict["Recovered Total"] = (
                    summary_dict["Cases Total"]
                    - summary_dict["Active Cases"]
                    - summary_dict["Deaths"]
            )
        except TypeError:
            summary_dict["Recovered Total"] = NOT_AVAILABLE_MESSAGE

        return summary_dict


class ComponentsBase(abc.ABC):
    def __init__(self, data: ComponentsData):
        self.data = data


class CountryAndWorldComponentsBase(ComponentsBase, abc.ABC):
    def __init__(self, data: ComponentsData):
        super().__init__(data)
        self.graph_classes = INSTALLED_GRAPHS.values()
        self.content_type: str = ""

    @labeled_div_with_class_and_id(label="Graph Type", class_name="col-2")
    def select_graph_type(self) -> dbc.RadioItems:
        return dbc.RadioItems(
            options=[
                {"label": "Dedicated", "value": "Dedicated"},
                {"label": "Bar", "value": "Bar"},
                {"label": "Line", "value": "Line"},
            ],
            value="Dedicated",
            id={
                "type": "radio-graph-type",
                "index": self.content_type,
            },
            inline=True,
        )

    @labeled_div_with_class_and_id(
        label="Graph Appearance", class_name="col-2")
    def select_graph_width(self):
        return dbc.Checklist(
            options=[
                {"label": "Wide Graphs", "value": True},
            ],
            value=[],
            id={
                "index": self.content_type,
                "type": "graph-width"
            },
            switch=True,
        )

    @labeled_div_with_class_and_id(label="Date Range", class_name="col-12")
    def select_date_range(self) -> dcc.RangeSlider:
        if self.content_type == "world":
            data = self.data.world
        else:
            data = self.data.current_country
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
            id={
                "type": 'date-range-slider',
                "index": self.content_type
            },
            min=min_value,
            max=max_value,
            marks=marks,
            step=1,
            value=[min_value, max_value]
        )

    def date_range_div(self):
        class_name = "col-12" if self.content_type == "country" else "col-8"
        return html.Div(
            className=class_name,
            id={
                "type": "date-range-div",
                "index": self.content_type,
            },
            children=[
                self.select_date_range()
            ]
        )

    def basic_info(self) -> html.Div:
        if self.content_type == "country":
            div_label = self.data.current_country_name
            data = self.data.current_country
        elif self.content_type == "world":
            div_label = self.content_type
            data = self.data.world
        summary_dict = self.data.get_country_basic_info_dict(data)

        def metric_and_value_div(metric: str) -> html.Div:
            return html.Div(
                className="col",
                children=[
                    html.H5(
                        className="card-title",
                        children=metric
                    ),
                    html.P(children=summary_dict[metric]),
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
                            children=funcs.correct_country_name(div_label)
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
                                ),
                                metric_and_value_div(
                                    metric="Active Cases",
                                ),
                                metric_and_value_div(
                                    metric="Deaths",
                                ),
                            ]
                        ),
                        html.Div(
                            className="row",
                            children=[
                                metric_and_value_div(
                                    metric="Recovered Total",
                                ),
                                metric_and_value_div(
                                    metric="First Case",
                                ),
                                metric_and_value_div(
                                    metric="Daily Peak",
                                ),
                            ]
                        ),
                        html.P(
                            className="text-muted",
                            style={"margin-bottom": 0},
                            children=[
                                f"Latest data comes from: "
                                f"{summary_dict['Latest Data']}"
                            ]
                        )
                    ]
                ),
            ]
        )

    def children(self):
        return [
            html.Div(
                id={
                    "type": "content",
                    "index": self.content_type
                },
                children=[],
                style={"min-height": "500px"},
            )
        ]

    def graph_divs_list(self) -> List[dcc.Loading]:
        return [
            dcc.Loading(
                id="loading-table",
                children=[
                    html.Div(
                        id={
                            "index": f"{graph.__name__}",
                            "type": f"graph-{self.content_type}-div",
                        },
                        children=html.Div(
                            style={"min-height": "100px"}
                        )
                    )
                ]
            ) for graph in self.graph_classes
        ]

    def content(self) -> List[html.Div]:
        return [
            html.Div(
                id="basic-info-div",
                className="container",
                children=[self.basic_info()]
            ),
            html.Div(
                id={
                    "type": "graphs",
                    "index": self.content_type
                },
                className="container",
                children=[*self.graph_divs_list()]
            )
        ]
