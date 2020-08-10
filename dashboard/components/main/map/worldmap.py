import os

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

import plotly.express as px

from components.main.country.country import Countries

ISO_CODES_PATH = os.path.join(*[
    "components", "main", "map", "countries_codes_and_coordinates.csv"])


def set_projection():
    return dbc.RadioItems(
        options=[
            {"label": "Orthographic", "value": "orthographic"},
            {"label": "Natural Earth", "value": "natural earth"},
            {"label": "Equirectangular", "value": "equirectangular"},
        ],
        value="orthographic",
        id="radio-set-projection",
        inline=True,
    )


def set_data_shown():
    return dbc.Select(
        options=[
            {"label": "Cases Total", "value": "Cases Total"},
            {"label": "Daily Peak", "value": "Daily Peak"},
            {"label": "New Cases", "value": "New Cases"},
            {"label": "Active Cases", "value": "Active Cases"},
            {"label": "Deaths", "value": "Deaths"},
            {"label": "Recovered Total", "value": "Recovered Total"},
        ],
        value="Cases Total",
        id="select-set-data-shown",
    )


def set_size():
    return dbc.RadioItems(
        options=[
            {"label": "Small", "value": 500},
            {"label": "Medium", "value": 700},
            {"label": "Big", "value": 1200},
        ],
        value=500,
        id="radio-set-size",
        inline=True,
    )


def create_map(countries: Countries, projection,
               data_shown, size) -> px.choropleth:
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
    iso_codes_df["Alpha-3 code"] = iso_codes_df["Alpha-3 code"].apply(
        lambda string: string.replace('"', ''))
    iso_codes_df["Alpha-3 code"] = iso_codes_df["Alpha-3 code"].apply(
        lambda string: string.replace(' ', ''))
    df_joined = pd.merge(df, iso_codes_df, on="Country", how="left")

    print(df_joined.head())
    bootstrap_colors = {
        "primary": "#007bff",
        "table-primary": "#b8daff",
        "text-muted": "#6c757d",
    }

    fig = px.choropleth(
        df_joined,
        locations="Alpha-3 code",
        color=data_shown,  # lifeExp is a column of gapminder
        hover_name="Country",
        # column to add to hover information
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(projection_type=projection)
    fig.update_layout(height=size)
    return fig


def get_fig(countries: Countries) -> html.Div:
    default_projection = "orthographic"
    default_data_shown = "Cases Total"
    default_size = 700
    return html.Div(
        className="",
        children=[
            dcc.Graph(
                id="worldmap-graph",
                figure=create_map(countries, default_projection,
                                  default_data_shown, default_size))
        ]
    )


children = [
    dcc.Loading(
        id="loading-table",
        children=[
            html.Div(
                id='worldmap-content',
                style={
                    "min-height": "500px",
                    # 'height': '1200px'
                },
            )
        ],
    )
]
