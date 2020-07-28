import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output


import elements
from tabs import worldmap, worldtable


CONFIG_PATH = 'config.ini'

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

data_source = elements.JSONDataSource(CONFIG_PATH)
countries = data_source.get_countries()

dropdown_items = [{"label": f"{country}", "value": country} for
                  country in countries]

select_country = dbc.Select(
    id="countries_dropdown",
    options=dropdown_items,
    value=countries[0],
    className="custom-select",
)

select_graph_type = dbc.RadioItems(
    options=[
        {"label": "Bar", "value": "Bar"},
        {"label": "Line", "value": "Line"},
    ],
    value="Bar",
    id="radio_graph_type",
    inline=True,
)

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="World Map",
                        tab_id="tab-1",
                        # tabClassName="ml-auto",
                        # labelClassName="text-success"
                    ),
                    dbc.Tab(
                        label="World Table",
                        tab_id="tab-2",
                    ),
                    dbc.Tab(
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
                        label="Countries",
                        tab_id="tab-3",
                    ),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.Div(id="card-content",
                              className="container-fluid card-text")),
    ]
)

countries_div = html.Div(id="graphs-div", children=[], className="container")
children = [
    # select,
    card,
]

test_div = html.Div(children=children)


@app.callback(
    Output("graphs-div", "children"),
    [Input("countries_dropdown", "value"),
     Input("radio_graph_type", "value")]
)
def country_graphs(value_country, value_graph):
    print(value_country, value_graph)
    country = elements.Country(data_source, value_country)
    df = country.data
    graph_types = df.columns
    graphs = []
    for graph in graph_types:
        graph_data_df = df[graph]
        x = graph_data_df.index
        y = graph_data_df.values
        data = None
        if value_graph == "Bar":
            data = [go.Bar(
                x=x,
                y=y,
                text=y,
                textposition='auto',
            )]
        elif value_graph == "Line":
            data = [go.Scatter(
                x=x,
                y=y,
                text=y,
                mode="lines+markers",
                textposition=['top right'],
            )]
        fig = go.Figure(data=data)
        fig.update_layout(title_text=f'{graph}')
        graph_ready = dcc.Graph(
            id=f"{value_country}-{graph}",
            figure=fig
        )
        graphs.append(graph_ready)
    return graphs


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-1":
        return worldmap.children
    if active_tab == "tab-2":
        return worldtable.children
    if active_tab == "tab-3":
        return countries_div


app.config.suppress_callback_exceptions = True
app.layout = test_div

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
