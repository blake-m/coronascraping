import dash_core_components as dcc

import plotly.express as px

from components import template

template.bootstrap()


df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

map = dcc.Graph(
    id='example-graph-1',
    figure=fig
)

children = [
    map
]

