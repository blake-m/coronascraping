import dash_html_components as html
import dash_bootstrap_components as dbc

from components import data_source
from components.main.country.graphs import TotalCasesGraph, CasesDailyGraph, \
    DeathsDailyGraph, ActiveCasesTotalGraph

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

countries_div = html.Div(id="graphs-div", children=[], className="container")


def country_graphs_maker(value_country, value_graph):
    print(value_country, value_graph)
    df = DATA_SOURCE.get_pandas_dataframe_for_one_country(value_country)
    print(df.columns)
    graphs = [
        # TODO(blake): implement a div with basic info
        html.H3(f"Total Cases: {'214214123'}"),
        TotalCasesGraph(df, value_country, value_graph).get_graph(),
        CasesDailyGraph(df, value_country, value_graph).get_graph(),
        DeathsDailyGraph(df, value_country, value_graph).get_graph(),
        ActiveCasesTotalGraph(df, value_country, value_graph).get_graph(),

    ]
    graphs = [graph for graph in graphs if graph is not None]

    return graphs
