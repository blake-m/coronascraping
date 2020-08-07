import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

from components import template


def get_fig():
    template.bootstrap()
    df = px.data.gapminder().query("year==2007")
    fig = px.choropleth(df, locations="iso_alpha",
                        color="lifeExp",
                        )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return dcc.Graph(figure=fig)


children = [
    dcc.Loading(
        id="loading-table",
        children=[
            html.Div(
                id='worldmap-content',
                style={"min-height": "500px"},
            )
        ],
        type="cube",
    )
]
