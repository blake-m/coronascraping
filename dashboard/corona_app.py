from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State

from components.tabs import tabs, switch_tab_content


def create_app(countries):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    main = dbc.Card(
        [
            dbc.CardHeader(tabs(countries)),
            dbc.CardBody(
                className="align-middle",
                children=dcc.Loading(
                    id='card-body-loading',
                    fullscreen=True,
                    children=[html.Div(
                        id="card-content",
                        className="container-fluid card-text"
                    )]
                )
            ),
        ]
    )

    @app.callback(
        Output("graphs-div", "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio_graph_type", "value"),
            Input("date-range-slider", "value"),
        ],
    )
    def country_elements(country: str, graph_type: str, date_range: List[int]):
        return countries.elements_maker(country, graph_type, date_range)

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return switch_tab_content(active_tab, countries)

    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(children=[main])
    return app
