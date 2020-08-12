import dash_core_components as dcc
import dash_html_components as html

from components.main.country import Country


def get_fig(countries: Country) -> html.Div:
    df = countries.summary_data

    return html.Div(
        children=[

        ]
    )





children = [
    dcc.Loading(
        id="loading-table",
        children=[
            html.Div(
                id='world-detail-content',
                style={"min-height": "500px"},
            )
        ],
    )

]
