import abc
from typing import Tuple, List

import dash_core_components as dcc
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go


class BaseGraph(abc.ABC):
    graph = ""
    title = ""

    def __init__(self, df: pd.DataFrame, country: str, graph_type: str):
        self.df = df,
        self.country = country,
        self.graph_type = graph_type

    def check_if_data_available(self) -> bool:
        return self.graph in self.df[0].columns

    def get_x_and_y_axis_data(self) -> Tuple:
        graph_data_df = self.df[0][self.graph]
        x = graph_data_df.index
        y = graph_data_df.values
        return x, y

    @staticmethod
    def get_graph_data_bar(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [go.Bar(
            x=x,
            y=y,
            text=y,
            textposition='auto',
        )]

    @staticmethod
    def get_graph_data_line(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [go.Scatter(
            x=x,
            y=y,
            text=y,
            mode="lines+markers",
            textposition=['top right'],
        )]

    @staticmethod
    @abc.abstractmethod
    def get_graph_data_dedicated(x, y):
        pass

    def get_figure(self, data):
        fig = go.Figure(data=data)
        fig.update_layout(title_text=f'{self.title}')
        graph_ready = dcc.Graph(
            id=f"{self.country}-{self.graph}",
            figure=fig
        )
        return graph_ready

    def get_graph(self):
        if self.check_if_data_available():
            x, y = self.get_x_and_y_axis_data()
            if self.graph_type == "Bar":
                graph_data = self.get_graph_data_bar(x, y)
            elif self.graph_type == "Line":
                graph_data = self.get_graph_data_line(x, y)
            elif self.graph_type == "Dedicated":
                graph_data = self.get_graph_data_dedicated(x, y)
            return self.get_figure(graph_data)
        return None


class TotalCasesGraph(BaseGraph):
    graph = "coronavirus_cases_linear"
    title = "TOTAL CASES"

    @staticmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [
            go.Scatter(
                x=x,
                y=y,
                text=y,
                mode="lines+markers",
                textposition=['top right'],
            ),
            go.Bar(
                x=x,
                y=y,
                text=y,
                textposition='auto',
            )
        ]


class TotalCasesGraph(BaseGraph):
    graph = "coronavirus_cases_linear"
    title = "TOTAL CASES"

    @staticmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [
            go.Scatter(
                x=x,
                y=y,
                text=y,
                mode="lines+markers",
                textposition=['top right'],
            ),
            go.Bar(
                x=x,
                y=y,
                text=y,
                textposition='auto',
            )
        ]


class CasesDailyGraph(BaseGraph):
    graph = "graph_cases_daily"
    title = "CASES DAILY"

    @staticmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        n = 7
        # TODO(blake): reimplement rolling mean - it seems to be wrong
        rolling_mean = np.cumsum(y, dtype=float)
        rolling_mean[n:] = rolling_mean[n:] - rolling_mean[:-n]
        rolling_mean = rolling_mean[n - 1:] / n

        return [
            go.Scatter(
                x=x,
                y=rolling_mean,
                text=y,
                mode="lines+markers",
                textposition=['top right'],
            ),
            go.Bar(
                x=x,
                y=y,
                text=y,
                textposition='auto',
            )
        ]
