from collections import Callable
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html

from components.graphs.figs import INSTALLED_GRAPHS
from components.holder import ComponentsHolder

from components.main.country import CountryComponents
from components.main.map.worldmap import WorldMapComponents
from components.main.world import WorldComponents

GRAPH_CLASSES = INSTALLED_GRAPHS.values()


def main_tab(label: str) -> Callable:
    """Returns a dbc.Tab for dbc.Tabs."""
    tab_id = label.split(" ")
    tab_id.insert(0, "tab")
    tab_id = "-".join(tab_id)
    tab_id = tab_id.lower()

    # This nested function definitions are needed to allow the
    # main_tab_decorator to take arguments
    def main_tab_decorator(function: Callable) -> Callable:
        def wrapper(*args) -> dbc.Tab:
            rows_of_column_divs = function(*args)
            return dbc.Tab(
                label=label,
                tab_id=f"{tab_id}",
                children=html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="card p-3 text-body",
                            children=[
                                html.Div(
                                    className="row align-text-top",
                                    children=row
                                ) for row in rows_of_column_divs
                            ]
                        )
                    ]
                )
            )

        return wrapper

    return main_tab_decorator


@main_tab(label="World Map")
def world_map_content(worldmap: WorldMapComponents) -> List[List[html.Div]]:
    first_row = [
        worldmap.set_data_shown(),
        worldmap.set_projection(),
        worldmap.set_size(),
    ]
    return [first_row]


@main_tab(label="World Detail")
def world_detail_content(world: WorldComponents) -> List[List[html.Div]]:
    first_row = [
        world.select_graph_type(),
        world.select_graph_width(),
        world.date_range_div()
    ]
    return [first_row]


@main_tab(label="Countries")
def countries_content(country: CountryComponents) -> List[List[html.Div]]:
    first_row = [
        country.select_country_dropdown(),
        country.select_graph_type(),
        country.select_graph_width(),
    ]
    second_row = [
        country.date_range_div()
    ]
    return [
        first_row,
        second_row
    ]


def tabs(components_holder: ComponentsHolder) -> dbc.Tabs:
    return dbc.Tabs(
        id="card-main",
        card=True,
        active_tab="tab-world-map",
        children=[
            world_map_content(components_holder.worldmap),
            world_detail_content(components_holder.world),
            dbc.Tab(
                label="World Table",
                tab_id="tab-world-table",
            ),
            countries_content(components_holder.country),
        ]
    )
