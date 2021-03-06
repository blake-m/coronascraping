import abc
from typing import Tuple, List, Optional

import dash_core_components as dcc
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go

ROLLING_MEAN_LINE_WIDTH = 4


class BaseGraph(abc.ABC):
    graph = [""]
    graph_name = ""
    title = ""

    def __init__(self,
                 df: pd.DataFrame,
                 graph_type: str,
                 date_range: List[int]):
        self.df = df,
        self.graph_type = graph_type
        self.date_range = date_range

    def check_if_data_available(self) -> bool:
        return self.graph in self.df[0].columns

    def get_x_and_y_axis_data(self) -> Tuple:
        graph_data_df = self.df[0][self.graph]
        x = graph_data_df.index
        y = graph_data_df.values
        return x, y

    def get_x_and_y_axis_selected_range_data(self, x, y):
        # +1 makes the range full and avoids skipping last value
        x_ranged = x[self.date_range[0]: self.date_range[1] + 1]
        y_ranged = y[self.date_range[0]: self.date_range[1] + 1]
        return x_ranged, y_ranged

    @staticmethod
    def get_graph_data_bar(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [go.Bar(
            x=x,
            y=y,
        )]

    @staticmethod
    def get_graph_data_line(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line_width=ROLLING_MEAN_LINE_WIDTH,
        )]

    @staticmethod
    @abc.abstractmethod
    def get_graph_data_dedicated(x, y):
        pass

    def update_figure_layout(self, fig: go.Figure) -> go.Figure:
        fig.update_layout(title_text=f'{self.title}')
        fig.update_layout(legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1
        })
        fig.update_layout(
            margin={
                "l": 20,
                "r": 20,
            },
        )
        return fig

    def get_figure(self, data) -> dcc.Graph:
        fig = go.Figure(data=data)
        fig = self.update_figure_layout(fig)
        graph_ready = dcc.Graph(
            id="country-graph",
            figure=fig
        )
        return graph_ready

    def get_graph(self) -> Optional[dcc.Graph]:
        if self.check_if_data_available():
            x, y = self.get_x_and_y_axis_data()
            x, y = self.get_x_and_y_axis_selected_range_data(x, y)
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
    graph_name = [""]
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

    def get_x_and_y_axis_selected_range_data(self, x, y):
        # +1 makes the range full and avoids skipping last value
        x_ranged = x[self.date_range[0]: self.date_range[1] + 1]
        y_ranged = {}
        for graph in self.graph:
            y_ranged[graph] = y[graph][
                              self.date_range[0]: self.date_range[1] + 1]
        return x_ranged, y_ranged

    @staticmethod
    @abc.abstractmethod
    def get_graph_data_dedicated(
            x, y) -> List[plotly.graph_objs._BaseTraceType]:
        pass

    def get_graph(self) -> Optional[dcc.Graph]:
        if self.check_if_data_available():
            x, y = self.get_x_and_y_axis_data()
            x, y = self.get_x_and_y_axis_selected_range_data(x, y)
            graph_data = self.get_graph_data_dedicated(x, y)
            return self.get_figure(graph_data)
        return None


class BarAndRollingMeanBaseGraph(BaseGraph):
    def get_graph_data_dedicated(
            self, x, y) -> List[plotly.graph_objs._BaseTraceType]:
        rolling_mean_window = 7
        rolling_mean = np.convolve(
            y,
            np.ones((rolling_mean_window,)) / rolling_mean_window, mode='full'
        )

        return [
            go.Bar(
                x=x,
                y=y,
                name=self.graph_name
            ),
            go.Scatter(
                x=x,
                y=rolling_mean,
                mode="lines",
                line_width=ROLLING_MEAN_LINE_WIDTH,
                name=f"Rolling Mean {rolling_mean_window} Days"
            ),
        ]
