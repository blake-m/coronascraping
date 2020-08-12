from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.main import worldtable, world_detail
from components.main.map import worldmap
from components.graphs import figs
from components.main.country import Country
from components.main.map.worldmap import create_map
from components import tabs


def create_app(
        country: Country) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    @app.callback(
        Output("date-range-div-countries", "children"),
        [Input("countries_dropdown", "value"), ],
    )
    def country_elements(country_name: str):
        country.set_current_country(country_name)
        return country.select_date_range()

    # Graphs section ##############################################
    # Callbacks need to be created upfront, hence no dynamic creation

    @app.callback(
        Output(f"{figs.DailyCases.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def country_elements(country_name: str, graph_type: str,
                         date_range: List[int]):
        return [
            figs.DailyCases(country.current_country_data,
                              graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.TotalCasesGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def country_elements(country_name: str, graph_type: str,
                         date_range: List[int]):
        return [
            figs.TotalCasesGraph(country.current_country_data,
                                   graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.CasesDailyGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def country_elements(country_name: str, graph_type: str,
                         date_range: List[int]):
        return [
            figs.CasesDailyGraph(country.current_country_data,
                                   graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.DeathsDailyGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def country_elements(country_name: str, graph_type: str,
                         date_range: List[int]):
        return [
            figs.DeathsDailyGraph(country.current_country_data,
                                    graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.ActiveCasesTotalGraph.__name__}-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def country_elements(country_name: str, graph_type: str,
                         date_range: List[int]):
        return [
            figs.ActiveCasesTotalGraph(country.current_country_data,
                                         graph_type, date_range).get_graph()]

    # WORLD GRAPHS CALLBACKS
    @app.callback(
        Output(f"{figs.DailyCases.__name__}-world-div", "children"),
        [
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def country_elements(graph_type: str,
                         date_range: List[int]):
        return [
            figs.DailyCases(country.world_data, graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.TotalCasesGraph.__name__}-world-div", "children"),
        [
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def country_elements(graph_type: str,
                         date_range: List[int]):
        return [
            figs.TotalCasesGraph(country.world_data, graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.CasesDailyGraph.__name__}-world-div", "children"),
        [
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def country_elements(graph_type: str,
                         date_range: List[int]):
        return [
            figs.CasesDailyGraph(country.world_data, graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.DeathsDailyGraph.__name__}-world-div", "children"),
        [
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def country_elements(graph_type: str,
                         date_range: List[int]):
        return [
            figs.DeathsDailyGraph(country.world_data, graph_type, date_range).get_graph()]

    @app.callback(
        Output(f"{figs.ActiveCasesTotalGraph.__name__}-world-div", "children"),
        [
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def country_elements(graph_type: str,
                         date_range: List[int]):
        return [
            figs.ActiveCasesTotalGraph(country.world_data,
                                         graph_type, date_range).get_graph()]

    ###########################################################################

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return tabs.switch_tab_content(active_tab=active_tab, country=country)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldtable.get_fig(country)

    @app.callback(
        Output("worldmap-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return worldmap.get_fig(country)

    @app.callback(
        Output("countries-content", "children"),
        [
            Input("card-main", "active_tab"),
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ]
    )
    def tab_content(active_tab, country_name, graph_type, date_range):
        print("FIRED", "tab_content")
        return country.countries_div()

    @app.callback(
        Output("graphs-country", "className"),
        [Input("graph_width-country", "value"), ],
    )
    def graph_width(value: []):
        if value:
            return ""
        return "container"

    @app.callback(
        Output("graphs-world", "className"),
        [Input("graph_width-world", "value")],
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
        return create_map(country, projection, data_shown, size)

    ###########################################################################

    @app.callback(
        Output("world-detail-content", "children"),
        [
            Input("card-main", "active_tab"),
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-world", "value"),
            Input("date-range-slider-world", "value"),
        ]
    )
    def tab_content(active_tab, country_name, graph_type, date_range):
        print("FIRED", "tab_content")
        return country.world_div()


    main = html.Div(
        className="",
        children=dbc.Card(
            [
                dbc.CardHeader(
                    tabs.tabs(country),
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
