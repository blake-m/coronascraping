import dash_core_components as dcc
import dash_html_components as html
import dash_table

from components.main.world import WorldComponents


class WorldTableComponents(WorldComponents):
    def get_fig(self) -> html.Div:
        df = self.data.summary_data
        bootstrap_colors = {
            "primary": "#007bff",
            "table-primary": "#b8daff",
            "text-muted": "#6c757d",
        }

        return html.Div(
            children=[
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {"name": column, "id": column} for column in df.columns
                    ],
                    data=df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",

                    style_header={
                        'backgroundColor': bootstrap_colors["primary"],
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'border': '0',
                        'backgroundColor': 'white',
                        'color': bootstrap_colors["text-muted"],
                        'font-family': 'sans-serif',
                        'padding': '1px 25px'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': bootstrap_colors["table-primary"]
                        }
                    ],
                    style_as_list_view=True,
                    style_table={
                        'overflowX': 'auto',
                        'overflowY': 'auto',
                    }
                )
            ]
        )

    @staticmethod
    def children():
        return [
            dcc.Loading(
                id="loading-table",
                children=[
                    html.Div(
                        id='worldtable-content',
                        style={"min-height": "500px"},
                    )
                ],
            )
        ]
