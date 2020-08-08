import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


from components.main.country.country import Countries

ISO_CODES_PATH = "components\main\map\countries_codes_and_coordinates.csv"


def get_fig(countries: Countries) -> html.Div:
    df = countries.summary_data
    # TODO(blake): make some constant
    df = df.loc[
        (df["Country"] != "Channel Islands")
        & (df["Country"] != "Curacao")
        & (df["Country"] != "Saint Barthelemy")
        & (df["Country"] != "Saint Martin")
        & (df["Country"] != "Sint Maarten")
        & (df["Country"] != "Saint")
        ]
    iso_codes_df = pd.read_csv(ISO_CODES_PATH)
    iso_codes_df = iso_codes_df[["Country", "Alpha-3 code"]]
    iso_codes_df["Alpha-3 code"] = iso_codes_df["Alpha-3 code"].apply(lambda string: string.replace('"', ''))
    df_joined = pd.merge(df, iso_codes_df, on="Country", how="left")

    print(df_joined)

    df_joined.to_excel("text.xlsx")

    bootstrap_colors = {
        "primary": "#007bff",
        "table-primary": "#b8daff",
        "text-muted": "#6c757d",
    }

    fig = go.Figure(
        data=go.Choropleth(
            locations=df_joined['Alpha-3 code'],
            locationmode='country names',
            z=df_joined['Cases Total'],
            text=df_joined['Country'],
            colorscale='Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix='$',
            colorbar_title='GDP<br>Billions US$',
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    # df = pd.read_csv(
    #     'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
    #
    # fig = go.Figure(data=go.Choropleth(
    #     locations=df['CODE'],
    #     z=df['GDP (BILLIONS)'],
    #     text=df['COUNTRY'],
    #     colorscale='Blues',
    #     autocolorscale=False,
    #     reversescale=True,
    #     marker_line_color='darkgray',
    #     marker_line_width=0.5,
    #     colorbar_tickprefix='$',
    #     colorbar_title='GDP<br>Billions US$',
    # ))
    #
    # fig.update_layout(
    #     title_text='2014 Global GDP',
    #     geo=dict(
    #         showframe=False,
    #         showcoastlines=False,
    #         projection_type='equirectangular'
    #     ),
    #     annotations=[dict(
    #         x=0.55,
    #         y=0.1,
    #         xref='paper',
    #         yref='paper',
    #         text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
    #             CIA World Factbook</a>',
    #         showarrow=False
    #     )]
    # )
    # print(df)

    return html.Div(
        className="container",
        children=[
            dcc.Graph(figure=fig)
        ]
    )


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
