from typing import List, Dict

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL

from components.main import worldtable
from components.main.country import CountryComponent
from components.main.map import worldmapcomponents as wm
from components.main.base import ComponentsData
from components import tabs

from components.graphs.figs import INSTALLED_GRAPHS
from components.main.world import WorldComponent
from components.tabs import switch_tab_content


def create_app(data: ComponentsData) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    country = CountryComponent(data)
    world = WorldComponent(data)
    worldmap = wm.WorldMapComponents(data)

    @app.callback(
        Output({"type": "date-range-div", "index": MATCH}, "children"),
        [Input("countries_dropdown", "value")],
        [State({"type": "date-range-div", "index": MATCH}, "id")]
    )
    def update_date_range(country_name: str, state_id: Dict[str, str]):
        data.set_current_country(country_name)
        if state_id["index"] == "country":
            return country.select_date_range()
        else:
            return world.select_date_range()

    @app.callback(
        Output({"type": "graph-world-div", "index": MATCH}, "children"),
        [
            Input({"type": "radio-graph-type", "index": ALL}, "value"),
            Input({"type": "date-range-slider", "index": ALL}, "value"),
        ],
        [
            State({"type": "graph-world-div", "index": MATCH}, "id")
        ]
    )
    def update_world_graphs(graph_type: str, date_range: List[int], state_id):
        graph_class = INSTALLED_GRAPHS[state_id["index"]]
        graph = graph_class(
            data.world, graph_type[0], date_range[0]).get_graph()
        return graph

    @app.callback(
        Output({"type": "graph-country-div", "index": MATCH}, "children"),
        [
            Input("countries_dropdown", "value"),
            Input({"type": "radio-graph-type", "index": ALL}, "value"),
            Input({"type": "date-range-slider", "index": ALL}, "value"),
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
            data.current_country, graph_type[1], date_range[1]).get_graph()
        return graph

    switch_tab_content(app, worldmap, world, country)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_worldtable_loading_spinner(active_tab):
        return worldtable.get_fig(data)

    @app.callback(
        Output("worldmap-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_worldmap_loading_spinner(active_tab):
        return worldmap.get_fig()

    @app.callback(
        Output({"type": "content", "index": MATCH}, "children"),
        [
            Input("card-main", "active_tab"),
            Input("countries_dropdown", "value"),
            Input({"type": "radio-graph-type", "index": MATCH}, "value"),
            Input({"type": "date-range-slider", "index": MATCH}, "value"),
        ],
        [
            State({"type": "content", "index": MATCH}, "id"),
        ]
    )
    def update_countries_content(
            active_tab, country_name, graph_type, date_range, state_id):
        if state_id["index"] == "country":
            return country.content()
        else:
            return world.content()

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
        return worldmap.create_map(projection, data_shown, size)

    main = html.Div(
        className="",
        children=dbc.Card(
            [
                dbc.CardHeader(
                    tabs.tabs(worldmap, world, country),
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
