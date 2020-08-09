from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.main import worldtable
from components.main.map import worldmap
from components.main.country import graphs
from components.main.country.country import SingleCountry, Countries
from components.main.map.worldmap import create_map
from components.tabs import tabs


def create_app(
        single_country: SingleCountry, countries: Countries) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    @app.callback(
        Output("date-range-div", "children"),
        [Input("countries_dropdown", "value"), ],
    )
    def country_elements(country: str):
        single_country.set_current_country(country)
        return single_country.select_date_range()

    # Graphs section ##############################################
    # Callbacks need to be created upfront, hence no dynamic creation
    graph_classes = [
        graphs.DailyCases,
        graphs.TotalCasesGraph,
        graphs.CasesDailyGraph,
        graphs.DeathsDailyGraph,
        graphs.ActiveCasesTotalGraph,
    ]

    @app.callback(
        Output(f"{graphs.DailyCases.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def country_elements(country: str, graph_type: str,
                         date_range: List[int]):
        return [
            graphs.DailyCases(single_country.current_country_data, country,
                              graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{graphs.TotalCasesGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def country_elements(country: str, graph_type: str,
                         date_range: List[int]):
        return [
            graphs.TotalCasesGraph(single_country.current_country_data, country,
                                   graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{graphs.CasesDailyGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def country_elements(country: str, graph_type: str,
                         date_range: List[int]):
        return [
            graphs.CasesDailyGraph(single_country.current_country_data, country,
                                   graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{graphs.DeathsDailyGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def country_elements(country: str, graph_type: str,
                         date_range: List[int]):
        return [
            graphs.DeathsDailyGraph(single_country.current_country_data,
                                    country,
                                    graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{graphs.ActiveCasesTotalGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def country_elements(country: str, graph_type: str,
                         date_range: List[int]):
        return [
            graphs.ActiveCasesTotalGraph(single_country.current_country_data,
                                         country,
                                         graph_type, date_range).get_graph()]

    ###########################################################################

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        if active_tab == "tab-1":
            return worldmap.children
        if active_tab == "tab-2":
            return worldtable.children
        if active_tab == "tab-3":
            return single_country.countries_div(graph_classes)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldtable.get_fig(countries)

    @app.callback(
        Output("worldmap-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldmap.get_fig(countries)

    @app.callback(
        Output("countries-content", "children"),
        [
            Input("card-main", "active_tab"),
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ]
    )
    def tab_content(active_tab, country, graph_type, date_range):
        print("FIRED", "tab_content")
        return single_country.countries_div(graph_classes)

    @app.callback(
        Output("graphs", "className"),
        [Input("graph_width", "value"), ],
    )
    def graph_width(value: []):
        if value:
            return ""
        return "container"

    # Worldmap callbacks

    @app.callback(
        Output("worldmap-graph", "figure"),
        [
            Input("radio-set-projection", "value"),
            Input("select-set-data-shown", "value"),
            Input("radio-set-size", "value"),
        ],
    )
    def set_worldmap(projection: str, data_shown: str, size: int):
        return create_map(countries, projection, data_shown, size)

    ###########################################################################

    main = html.Div(
        className="",
        children=dbc.Card(
            [
                dbc.CardHeader(
                    tabs(single_country),
                    className="card-header text-white bg-primary",
                ),
                dbc.CardBody(
                    className="align-middle",
                    children=html.Div(
                        id="card-content",
                        className="container-fluid",
                    )
                ),
            ],
        )
    )

    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(
        className="bg-light p-3",
        style={
            "min-height": "100vh",
        },
        children=[main]
    )
    return app
