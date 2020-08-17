from typing import Dict, Callable, List, Optional

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH, ALL

from components.graphs.figs import INSTALLED_GRAPHS
from components.holder import ComponentsHolder


class Callbacks(object):
    def __init__(self, app: dash.Dash, holder: ComponentsHolder) -> None:
        self.app = app
        self.holder = holder

    def switch_tab_content(self) -> Callable:
        @self.app.callback(
            Output("card-content", "children"),
            [Input("card-main", "active_tab")]
        )
        def switch_tab_content(active_tab):
            if active_tab == "tab-world-map":
                return self.holder.worldmap.children()
            elif active_tab == "tab-world-detail":
                return self.holder.world.children()
            elif active_tab == "tab-world-table":
                return self.holder.worldtable.children()
            elif active_tab == "tab-countries":
                return self.holder.country.children()
        return switch_tab_content

    def update_date_range_slider(self) -> Callable:
        @self.app.callback(
            Output({"type": "date-range-div", "index": MATCH}, "children"),
            [Input("countries_dropdown", "value")],
            [State({"type": "date-range-div", "index": MATCH}, "id")]
        )
        def update_date_range_slider(country_name: str,
                                     state_id: Dict[str, str]):
            self.holder.data.set_current_country(country_name)
            if state_id["index"] == "country":
                return self.holder.country.select_date_range()
            else:
                return self.holder.world.select_date_range()

        return update_date_range_slider

    def update_country_graphs(self):
        @self.app.callback(
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

            content_type_and_graph_name = graph_div_id["index"]
            if content_type_and_graph_name.startswith("World"):
                graph_name = content_type_and_graph_name.replace("World", "")
                graph_class = INSTALLED_GRAPHS[graph_name]
                graph = graph_class(
                    self.holder.data.world,
                    graph_type[world_data_index_in_graph_type_radio_id_list],
                    date_range[world_data_index_in_date_range_slider_id_list]
                ).get_graph()
            else:
                graph_name = content_type_and_graph_name.replace("Country", "")
                graph_class = INSTALLED_GRAPHS[graph_name]
                graph = graph_class(
                    self.holder.data.current_country,
                    graph_type[country_data_index_in_graph_type_radio_id_list],
                    date_range[country_data_index_in_date_range_slider_id_list]
                ).get_graph()
            return graph
        return update_country_graphs

    def update_worldtable_loading_spinner(self):
        @self.app.callback(
            Output("worldtable-content", "children"),
            [Input("card-main", "active_tab")]
        )
        def update_worldtable_loading_spinner(active_tab):
            return self.holder.worldtable.get_fig()
        return update_worldtable_loading_spinner

    def update_worldmap_loading_spinner(self):
        @self.app.callback(
            Output("worldmap-content", "children"),
            [Input("card-main", "active_tab")]
        )
        def update_worldmap_loading_spinner(active_tab):
            return self.holder.worldmap.get_fig()
        return update_worldmap_loading_spinner

    def update_countries_content(self):
        @self.app.callback(
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
                return self.holder.country.content()
            else:
                return self.holder.world.content()
        return update_countries_content

    def update_graph_width(self):
        @self.app.callback(
            Output({"type": "graphs", "index": MATCH}, "className"),
            [Input({"type": "graph-width", "index": MATCH}, "value")],
        )
        def update_graph_width(value: []):
            if value:
                return ""
            return "container"
        return update_graph_width

    def update_worldmap_content(self):
        @self.app.callback(
            Output("worldmap-graph", "figure"),
            [
                Input("radio-set-projection", "value"),
                Input("select-set-data-shown", "value"),
                Input("radio-set-size", "value"),
            ],
        )
        def update_worldmap_content(projection: str, data_shown: str, size: int):
            return self.holder.worldmap.create_map(projection, data_shown, size)
        return update_worldmap_content
