import dash_core_components as dcc
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go





from components.main.country.country import DATA_SOURCE

df = px.data.gapminder().query("year==2007")
# df.to_excel("excel_TEST.xlsx")
#
#
# df = DATA_SOURCE.get_pandas_dataframe_for_one_country("poland")

fig = px.choropleth(df, locations="iso_alpha",
                    # color="graph_cases_daily", # lifeExp is a column of gapminder
                    color="lifeExp",
                    # hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)

# fig = go.Figure(data=fig)
# # fig.update_layout(title_text=f'{self.title}')
# graph_ready = dcc.Graph(
#     id=f"123123123TEST",
#     figure=fig
# )

children = [
    dcc.Graph(figure=fig)
]
