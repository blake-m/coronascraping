from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH

from components.main import worldtable
from components.main.map import worldmap
from components.main.details import Components
from components.main.map.worldmap import create_map
from components import tabs

from components.graphs.figs import INSTALLED_GRAPHS


def create_app(country: Components) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    @app.callback(
        Output("date-range-div-countries", "children"),
        [Input("countries_dropdown", "value")],
    )
    def update_date_range(country_name: str):
        country.data.set_current_country(country_name)
        return country.select_date_range()

    @app.callback(
        Output({"type": "graph-country-div", "index": MATCH}, "children"),
        [
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ],
        [
            State({"type": "graph-country-div", "index": MATCH}, "id")
        ]
    )
    def update_country_graphs(country_name: str, graph_type: str,
                              date_range: List[int], state_id):
        print("state", state_id)
        print("INSTALLED_GRAPHS", INSTALLED_GRAPHS)

        graph_class = INSTALLED_GRAPHS[state_id["index"]]
        graph = graph_class(
            country.data.current_country_data, graph_type, date_range).get_graph()
        return graph

    @app.callback(
        Output({"type": "graph-world-div", "index": MATCH}, "children"),
        [
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ],
        [
            State({"type": "graph-world-div", "index": MATCH}, "id")
        ]
    )
    def update_world_graphs(graph_type: str, date_range: List[int], state_id):
        graph_class = INSTALLED_GRAPHS[state_id["index"]]
        graph = graph_class(
            country.data.world, graph_type, date_range).get_graph()
        return graph

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_tab_content(active_tab):
        return tabs.switch_tab_content(active_tab=active_tab, country=country)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_worldtable_loading_spinner(active_tab):
        return worldtable.get_fig(country.data)

    @app.callback(
        Output("worldmap-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_worldmap_loading_spinner(active_tab):
        return worldmap.get_fig(country.data)

    @app.callback(
        Output({"type": "content", "index": MATCH}, "children"),
        [
            Input("card-main", "active_tab"),
            Input("countries_dropdown", "value"),
            Input("radio-graph-type-country", "value"),
            Input("date-range-slider-country", "value"),
        ],
        [
            State({"type": "content", "index": MATCH}, "id"),
        ]
    )
    def update_countries_content(
            active_tab, country_name, graph_type, date_range, state_id):
        print("FIRED", "tab_content")
        print("state_id", state_id)
        if state_id["index"] == "country":
            return country.main_div("country")
        else:
            return country.main_div("world")

    @app.callback(
        Output({"type": "graphs", "index": MATCH}, "className"),
        [Input({"type": "graph-width", "index": MATCH}, "value")],
    )
    def update_graph_width(value: []):
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
    def update_worldmap_content(projection: str, data_shown: str, size: int):
        return create_map(country.data, projection, data_shown, size)

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
