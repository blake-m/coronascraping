import dash_core_components as dcc

import plotly.express as px

from components import template

template.bootstrap()

df = px.data.gapminder().query("year==2007")
# df.to_excel("excel_TEST.xlsx")
#
#
# df = DATA_SOURCE.get_pandas_dataframe_for_one_country("poland")

fig = px.choropleth(df, locations="iso_alpha",
                    # color="graph_cases_daily", # lifeExp is a column of gapminder
                    color="lifeExp",
                    # hover_name="country", # column to add to hover information
                    # color_continuous_scale=px.colors.sequential.Plasma
                    )

fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

# fig = go.Figure(data=fig)
# # fig.update_layout(title_text=f'{self.title}')
# graph_ready = dcc.Graph(
#     id=f"123123123TEST",
#     figure=fig
# )

children = [
    dcc.Graph(figure=fig)
]
