from time import sleep
from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from components.main import worldmap, worldtable
from components.main.country import graphs
from components.tabs import tabs


def create_app(countries):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    main = dbc.Card(
        [
            dbc.CardHeader(tabs(countries)),
            dbc.CardBody(
                className="align-middle",
                children=html.Div(
                    id="card-content",
                    className="container-fluid",
                )
            ),
        ]
    )

    @app.callback(
        Output("date-range-div", "children"),
        [Input("countries_dropdown", "value"),],
    )
    def country_elements(country: str):
        countries.set_current_country(country)
        return countries.select_date_range()

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
            graphs.DailyCases(countries.current_country_data, country,
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
            graphs.TotalCasesGraph(countries.current_country_data, country,
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
            graphs.CasesDailyGraph(countries.current_country_data, country,
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
            graphs.DeathsDailyGraph(countries.current_country_data, country,
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
            graphs.ActiveCasesTotalGraph(countries.current_country_data,
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
            return countries.countries_div(graph_classes)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldtable.get_fig()

    @app.callback(
        Output("worldmap-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldmap.get_fig()

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
        return countries.countries_div(graph_classes)

    @app.callback(
        Output("graphs", "className"),
        [Input("graph_width", "value"),],
    )
    def graph_width(value: []):
        if value:
            return ""
        return "container"

    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(children=[main])
    return app
