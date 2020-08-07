import textwrap
from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.main import worldmap, worldtable
from components.main.country.graphs import DailyCases, TotalCasesGraph, \
    CasesDailyGraph, DeathsDailyGraph, ActiveCasesTotalGraph
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
        [
            Input("countries_dropdown", "value"),
        ],
    )
    def country_elements(country: str):
        countries.set_current_country(country)
        return countries.select_date_range()

    graph_classes = [
        "DailyCases",
        "TotalCasesGraph",
        "CasesDailyGraph",
        "DeathsDailyGraph",
        "ActiveCasesTotalGraph",
    ]

    for graph_class in graph_classes:
        exec(textwrap.dedent(
            f"""
            @app.callback(
            Output(f"{graph_class}-div", "children"),
                [
                    Input("countries_dropdown", "value"),
                    Input("radio_graph_type", "value"),
                    Input("date-range-slider", "value"),
                ]
            )
            def country_elements(country: str, graph_type: str,
                                 date_range: List[int]):
                return [
                    {graph_class}(countries.current_country_data, country,
                                           graph_type, date_range).get_graph()]
                """
            )
        )

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        # TODO(blake): export it back to tabs module
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
        return countries.countries_div(graph_classes)

    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(children=[main])
    return app
