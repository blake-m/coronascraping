from typing import List, Dict, Optional

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL

from components.main.country import CountryComponents
from components.main.base import ComponentsData
from components import tabs

from components.graphs.figs import INSTALLED_GRAPHS
from components.main.map.worldmap import WorldMapComponents
from components.main.world import WorldComponents
from components.main.worldtable import WorldTableComponents
from components.tabs import switch_tab_content


def create_all_components_dict(data):
    country = CountryComponents(data)
    world = WorldComponents(data)
    worldmap = WorldMapComponents(data)
    worldtable = WorldTableComponents(data)

    return dict(
        country=country,
        world=world,
        worldmap=worldmap,
        worldtable=worldtable
    )


def create_app(data: ComponentsData) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    country = CountryComponents(data)
    world = WorldComponents(data)
    worldmap = WorldMapComponents(data)
    worldtable = WorldTableComponents(data)

    all_components = dict(
        country=country,
        world=world,
        worldmap=worldmap,
        worldtable=worldtable
    )

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
        Output({"type": "graph-div", "index": MATCH}, "children"),
        [
            Input("countries_dropdown", "value"),
            Input({"type": "radio-graph-type", "index": ALL}, "value"),
            Input({"type": "date-range-slider", "index": ALL}, "value"),
        ],
        [
            State({"type": "graph-div", "index": MATCH}, "id"),
            State({"type": "radio-graph-type", "index": ALL}, "id"),
            State({"type": "date-range-slider", "index": ALL}, "id"),
        ]
    )
    def update_country_graphs(
            country_name: str,
            graph_type: str,
            date_range: List[int],
            graph_div_id: List[Dict],
            graph_type_radio_id_list: List[Dict],
            date_range_slider_id_list: List[Dict]) -> Optional[dcc.Graph]:
        def get_list_index_of_world_and_country_data_in_id_list(
                id_list: List[Dict]):
            if "world" == id_list[0]["index"]:
                world_data_index, country_data_index = 0, 1
            else:
                world_data_index, country_data_index = 1, 0
            return world_data_index, country_data_index

        world_data_index_in_date_range_slider_id_list, \
        country_data_index_in_date_range_slider_id_list = \
            get_list_index_of_world_and_country_data_in_id_list(
                date_range_slider_id_list)

        world_data_index_in_graph_type_radio_id_list, \
        country_data_index_in_graph_type_radio_id_list = \
            get_list_index_of_world_and_country_data_in_id_list(
                graph_type_radio_id_list)

        content_type_and_graph_name: str = graph_div_id["index"]
        if content_type_and_graph_name.startswith("World"):
            graph_name = content_type_and_graph_name.replace("World", "")
            graph_class = INSTALLED_GRAPHS[graph_name]
            graph = graph_class(
                data.world,
                graph_type[world_data_index_in_graph_type_radio_id_list],
                date_range[world_data_index_in_date_range_slider_id_list]
            ).get_graph()
        else:
            graph_name = content_type_and_graph_name.replace("Country", "")
            graph_class = INSTALLED_GRAPHS[graph_name]
            graph = graph_class(
                data.current_country,
                graph_type[country_data_index_in_graph_type_radio_id_list],
                date_range[country_data_index_in_date_range_slider_id_list]
            ).get_graph()
        return graph

    switch_tab_content(app, all_components)

    # Loading spinners callbacks
    @app.callback(
        Output("worldtable-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def update_worldtable_loading_spinner(active_tab):
        return worldtable.get_fig()

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
                    tabs.tabs(all_components),
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
