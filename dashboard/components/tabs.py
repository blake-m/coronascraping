from collections import Callable
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html

from components.graphs.figs import INSTALLED_GRAPHS

from components.main import worldtable
from components.main.details import Components
from components.main.map import worldmap

GRAPH_CLASSES = INSTALLED_GRAPHS.values()


def main_tab(label: str) -> Callable:
    """Returns a dbc.Tab for dbc.Tabs."""
    tab_id = label.split(" ")
    tab_id.insert(0, "tab")
    tab_id = "-".join(tab_id)
    tab_id = tab_id.lower()
    print("tab_id\n", tab_id)

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
def world_map_content() -> List[List[html.Div]]:
    first_row = [
        worldmap.set_data_shown(),
        worldmap.set_projection(),
        worldmap.set_size(),
    ]
    return [first_row]


@main_tab(label="World Detail")
def world_detail_content(country: Components) -> List[List[html.Div]]:
    first_row = [
        country.select_graph_type("world"),
        country.select_graph_width("world"),
        country.date_range_div(content_type="world")
    ]

    return [
        first_row,
    ]


@main_tab(label="Countries")
def countries_content(country: Components) -> List[List[html.Div]]:
    first_row = [
        country.select_country_dropdown(),
        country.select_graph_type("country"),
        country.select_graph_width("country"),
    ]
    second_row = [
        country.date_range_div(content_type="country")
    ]
    return [
        first_row,
        second_row
    ]


def tabs(countries: Components) -> dbc.Tabs:
    return dbc.Tabs([
        world_map_content(),
        world_detail_content(countries),
        dbc.Tab(
            label="World Table",
            tab_id="tab-world-table",
        ),
        countries_content(countries),
    ],
        id="card-main",
        card=True,
        active_tab="tab-world-map",
    )


def switch_tab_content(active_tab: str, country: Components) -> html.Div:
    if active_tab == "tab-world-map":
        return worldmap.children
    elif active_tab == "tab-world-detail":
        return country.main_div("world")
    elif active_tab == "tab-world-table":
        return worldtable.children
    elif active_tab == "tab-countries":
        return country.main_div("country")
