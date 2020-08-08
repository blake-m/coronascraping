import dash_bootstrap_components as dbc
import dash_html_components as html

from components.main import worldtable, worldmap
from components.main.country import graphs
from components.main.country.country import Countries


def tabs(countries: Countries):
    return dbc.Tabs(
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
                                        className="col-7",
                                        children=[
                                            countries.select_country_dropdown()]
                                    ),
                                    html.Div(
                                        className="col-2",
                                        children=countries.select_graph_width()
                                    ),
                                    html.Div(
                                        className="col-3",
                                        children=[countries.select_graph_type()]
                                    )]
                            ),
                            html.Div(
                                className="row align-items-center",
                                children=[
                                    html.Div(
                                        className="col-12 mt-3",
                                        id="date-range-div",
                                        children=countries.select_date_range()
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
        active_tab="tab-3",
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
