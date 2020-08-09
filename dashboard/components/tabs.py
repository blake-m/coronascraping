import dash_bootstrap_components as dbc
import dash_html_components as html

from components.main.country.country import SingleCountry
from components.main.map.worldmap import set_projection, set_data_shown, \
    set_size


def tabs(countries: SingleCountry):
    return dbc.Tabs(
        [
            dbc.Tab(
                label="World Map",
                tab_id="tab-1",
                children=html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="card p-3 text-body",
                            children=[
                                html.Div(
                                    className="row align-text-top",
                                    children=[
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Type of Data",
                                                    className="h6"
                                                ),
                                                set_data_shown(),
                                            ]
                                        ),
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Map Projection Type",
                                                    className="h6"
                                                ),
                                                set_projection(),
                                            ]
                                        ),
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Map Size",
                                                    className="h6"
                                                ),
                                                set_size(),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ),
            dbc.Tab(
                label="World Table",
                tab_id="tab-2",
            ),
            dbc.Tab(
                label="Countries",
                tab_id="tab-3",
                children=html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="card p-3 text-body",
                            children=[
                                html.Div(
                                    className="row align-text-top",
                                    children=[
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Country",
                                                    className="h6"
                                                ),
                                                countries.select_country_dropdown()
                                    ]
                                        ),
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Graph Appearance",
                                                    className="h6"
                                                ),
                                                countries.select_graph_width()
                                            ]
                                        ),
                                        html.Div(
                                            className="col-4",
                                            children=[
                                                dbc.Label(
                                                    "Graph Type",
                                                    className="h6"
                                                ),
                                                countries.select_graph_type(),
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className="row align-text-top",
                                    children=[
                                        html.Div(
                                            className="col-12 mt-3",
                                            id="date-range-div",
                                            children=[
                                                dbc.Label(
                                                    "Date Range",
                                                    className="h6"
                                                ),
                                                countries.select_date_range()
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ),
        ],
        id="card-main",
        card=True,
        active_tab="tab-1",
    )

    # def switch_tab_content(active_tab, countries: Countries):
    #     if active_tab == "tab-1":
    #         return worldmap.children
    #     if active_tab == "tab-2":
    #         return worldtable.children
    #     if active_tab == "tab-3":
    #         return countries.countries_div([
    #         graphs.DailyCases,
    #         graphs.TotalCasesGraph,
    #         graphs.CasesDailyGraph,
    #         graphs.DeathsDailyGraph,
    #         graphs.ActiveCasesTotalGraph,
    #     ])
