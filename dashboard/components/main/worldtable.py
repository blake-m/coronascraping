import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

from components import template


def get_fig():
    template.bootstrap()

    df = px.data.iris()  # iris is a pandas DataFrame
    fig = px.scatter(df, x="sepal_width", y="sepal_length")

    map = dcc.Graph(
        id='example-graph-1',
        figure=fig
    )
    return map


children = [
    dcc.Loading(
        id="loading-table",
        children=[
            html.Div(
                id='worldtable-content',
                style={"min-height": "500px"},
            )
        ],
        type="circle",
    )
]
