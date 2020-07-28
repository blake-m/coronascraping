import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.main.country.country import country_graphs_maker
from components.tabs import tabs, switch_tab_content


def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    main = dbc.Card(
        [
            dbc.CardHeader(tabs),
            dbc.CardBody(
                html.Div(
                    id="card-content",
                    className="container-fluid card-text"
                )
            ),
        ]
    )

    @app.callback(
        Output("graphs-div", "children"),
        [Input("countries_dropdown", "value"),
         Input("radio_graph_type", "value")]
    )
    def country_graphs(value_country, value_graph):
        return country_graphs_maker(value_country, value_graph)

    @app.callback(
        Output("card-content", "children"),
        [Input("card-main", "active_tab")]
    )
    def tab_content(active_tab):
        return switch_tab_content(active_tab)

    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(children=[main])
    return app
