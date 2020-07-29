from typing import List

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from components import data_source
from components.main.country.graphs import TotalCasesGraph, CasesDailyGraph, \
    DeathsDailyGraph, ActiveCasesTotalGraph, DailyCases

CONFIG_PATH = './config.ini'
DATA_SOURCE = data_source.PostgresDataSource(CONFIG_PATH)
COUNTRIES = DATA_SOURCE.get_countries()

dropdown_items = [{"label": f"{country}", "value": country} for
                  country in COUNTRIES]

select_country = dbc.Select(
    id="countries_dropdown",
    options=dropdown_items,
    value=COUNTRIES[0],
    className="custom-select",
)

select_graph_type = dbc.RadioItems(
    options=[
        {"label": "Dedicated", "value": "Dedicated"},
        {"label": "Bar", "value": "Bar"},
        {"label": "Line", "value": "Line"},
    ],
    value="Dedicated",
    id="radio_graph_type",
    inline=True,
)

select_date_range = dcc.RangeSlider(
    id='date-range-slider',
    min=0,
    max=20,
    step=0.5,
    value=[5, 15]
),

countries_div = html.Div(id="graphs-div", children=[], className="container")


def country_elements_maker(
        country: str, graph_type: str, date_range: List[int]):
    print(country, graph_type, date_range)
    df = DATA_SOURCE.get_pandas_dataframe_for_one_country(country)
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
