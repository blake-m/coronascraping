import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from components.callbacks import Callbacks
from components.holder import ComponentsHolder
from components.main.base import ComponentsData
from components import tabs


def create_app(data: ComponentsData) -> dash.Dash:
    """Creates (and returns) the Dash App instance and all the basic
    requirements for its working.

    Dash Callbacks need to be defined upfront, therefore their definitions are
    called here upfront.

    Main Div (html component) for the app is defined and attached to app in this
    function.

    Arguments:
        data - all data for the app is preloaded from the database at the launch
            of the app and is then kept in memory for faster manipulation. It is
            possible due to its low volume. All the components created in the
            Dash app use this data.
    """
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    components_holder = ComponentsHolder(data)
    callbacks = Callbacks(app, components_holder)

    callbacks.switch_tab_content()
    callbacks.update_date_range_slider()
    callbacks.update_country_graphs()
    callbacks.update_worldtable_loading_spinner()
    callbacks.update_worldmap_loading_spinner()
    callbacks.update_countries_content()
    callbacks.update_graph_width()
    callbacks.update_worldmap_content()

    main = html.Div(
        className="",
        children=dbc.Card(
            [
                dbc.CardHeader(
                    tabs.tabs(components_holder),
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
