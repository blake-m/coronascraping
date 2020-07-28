import dash_bootstrap_components as dbc
import dash_html_components as html

from components.main import worldtable, worldmap
from components.main.country.country import countries_div, \
    select_country, \
    select_graph_type

tabs = dbc.Tabs(
    [
        dbc.Tab(
            label="World Map",
            tab_id="tab-1",
        ),
        dbc.Tab(
            label="World Table",
            tab_id="tab-2",
        ),
        dbc.Tab(
            label="Countries",
            tab_id="tab-3",
            children=[
                html.Br(),
                html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="row align-items-center",
                            children=[
                                html.Div(
                                    className="col-sm-8",
                                    children=[select_country]
                                ),
                                html.Div(
                                    className="col-sm-4",
                                    children=[select_graph_type]
                                )
                            ]
                        )
                    ]
                )
            ],

        ),
    ],
    id="card-main",
    card=True,
    active_tab="tab-1",
)


def switch_tab_content(active_tab):
    if active_tab == "tab-1":
        return worldmap.children
    if active_tab == "tab-2":
        return worldtable.children
    if active_tab == "tab-3":
        return countries_div
