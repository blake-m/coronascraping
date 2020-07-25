import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# from dashboard import elements

# countries = elements.CountriesAvailable
#
# country_graphs = []
# for column in df.columns:
#     pass
#
# children = [
#     html.Div(id="graphs-div")
# ]
#
#
# @app.callback(
#     Output("graphs-div", "children"), [Input("card-tabs", "active_tab")]
# )
# def country_graphs(active_tab):
#     if active_tab == "tab-1":
#         return worldmap.children
#     if active_tab == "tab-2":
#         return worldtable.children
#     if active_tab == "tab-3":
#         return country.children
