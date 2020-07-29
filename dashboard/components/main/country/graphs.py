import abc
from typing import Tuple, List, Dict

import dash_core_components as dcc
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go


class BaseGraph(abc.ABC):
    graph = [""]
    title = ""

    def __init__(self,
                 df: pd.DataFrame,
                 country: str,
                 graph_type: str,
                 date_range: List[int]):
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
            id={
                "type": "country-graph",
                "index": f"{self.country}-{self.graph}"
            },
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


class AdvancedBaseGraph(BaseGraph):
    graph = [""]
    title = ""

    def check_if_data_available(self) -> bool:
        return all([graph in self.df[0].columns for graph in self.graph])

    def get_x_and_y_axis_data(self) -> Tuple:
        y_axes = {}
        df = self.df[0]  # Quick fix to a weird error
        for graph in self.graph:
            graph_data_df = df[graph]
            y_axes[graph] = graph_data_df.values
        x = df.index
        return x, y_axes

    @staticmethod
    @abc.abstractmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        pass

    @abc.abstractmethod
    def get_figure(self, data):
        pass

    def get_graph(self):
        if self.check_if_data_available():
            x, y = self.get_x_and_y_axis_data()
            graph_data = self.get_graph_data_dedicated(x, y)
            return self.get_figure(graph_data)
        return None


class DailyCases(AdvancedBaseGraph):
    graph = ["graph_deaths_daily", "cases_cured_daily", "graph_cases_daily"]
    title = "DAILY CASES STACKED"

    @staticmethod
    def get_graph_data_dedicated(
            x: pd.core.indexes.base.Index,
            y: Dict[str, np.array]
    ) -> List[plotly.graph_objs._BaseTraceType]:
        graphs = []
        print("X", type(x))
        print("Y", type(y))
        print("Y", type(y["graph_deaths_daily"]))
        print("X", x)
        print("Y", y)
        n = 7
        window = len(x) - n

        for graph_name in y:
            y_loaded = y[graph_name]
            y_loaded = y_loaded[window:]
            x_loaded = x[window:]
            graphs.append(
                go.Bar(
                    x=x_loaded,
                    y=y_loaded,
                    text=y_loaded,
                    textposition='auto',
                    name=graph_name,
                )
            )
        return graphs

    def get_figure(self, data):
        fig = go.Figure(data=data)
        fig.update_layout(title_text=f'{self.title}')
        fig.update_layout(barmode='stack')
        graph_ready = dcc.Graph(
            id={
                "type": "country-graph",
                "index": f"{self.country}-{self.graph}"
            },
            figure=fig
        )
        return graph_ready


class TotalCasesGraph(BaseGraph):
    graph = "coronavirus_cases_linear"
    title = "TOTAL CASES"

    @staticmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [
            go.Bar(
                x=x,
                y=y,
                text=y,
                textposition='auto',
            )
        ]

    def get_figure(self, data):
        fig = go.Figure(data=data)
        fig.update_layout(title_text=f'{self.title}')
        graph_ready = dcc.Graph(
            id={
                "type": "country-graph",
                "index": f"{self.country}-{self.graph}"
            },
            figure=fig
        )
        return graph_ready


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


class DeathsDailyGraph(BaseGraph):
    graph = "graph_deaths_daily"
    title = "DEATHS DAILY"

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


class ActiveCasesTotalGraph(BaseGraph):
    graph = "graph_active_cases_total"
    title = "ACTIVE CASES TOTAL"

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


class CuredDailyGraph(BaseGraph):
    graph = "cases_cured_daily"
    title = "CASES CURED DAILY"

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
