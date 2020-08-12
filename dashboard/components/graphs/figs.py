from typing import List, Dict

import inspect
import sys

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go

from components.graphs import base

ROLLING_MEAN_LINE_WIDTH = 4


class DailyCases(base.AdvancedBaseGraph):
    graph = [
        "graph_cases_daily",
        "cases_cured_daily",
        "graph_deaths_daily",
    ]
    graph_name = [
        "New Cases",
        "Cases Cured",
        "Deaths",
    ]
    title = "DAILY CASES STACKED"

    def get_graph_data_dedicated(
            self,
            x: pd.core.indexes.base.Index,
            y: Dict[str, np.array]
    ) -> List[plotly.graph_objs._BaseTraceType]:
        graphs = []

        for graph_type, graph_name in zip(y, self.graph_name):
            y_loaded = y[graph_type]
            graphs.append(
                go.Bar(
                    x=x,
                    y=y_loaded,
                    name=graph_name,
                )
            )
        return graphs

    def update_figure_layout(self, fig: go.Figure) -> go.Figure:
        fig_updated = super().update_figure_layout(fig)
        fig_updated.update_layout(barmode='stack')
        return fig_updated


class TotalCasesGraph(base.BaseGraph):
    graph = "coronavirus_cases_linear"
    graph_name = ""
    title = "TOTAL CASES"

    def get_graph_data_dedicated(
            self, x, y) -> List[plotly.graph_objs._BaseTraceType]:
        return [
            go.Bar(
                x=x,
                y=y,
                name=self.graph_name,
            )
        ]


class CasesDailyGraph(base.BarAndRollingMeanBaseGraph):
    graph = "graph_cases_daily"
    graph_name = "New Cases"
    title = "CASES DAILY"


class DeathsDailyGraph(base.BarAndRollingMeanBaseGraph):
    graph = "graph_deaths_daily"
    graph_name = "Deaths"
    title = "DEATHS DAILY"


class ActiveCasesTotalGraph(base.BarAndRollingMeanBaseGraph):
    graph = "graph_active_cases_total"
    graph_name = "Active Cases"
    title = "ACTIVE CASES TOTAL"


class CuredDailyGraph(base.BarAndRollingMeanBaseGraph):
    graph = "cases_cured_daily"
    graph_name = "Cases Cured"
    title = "CASES CURED DAILY"


clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
INSTALLED_GRAPHS = {cls[1].__name__: cls[1] for cls in clsmembers}

print("INSTALLED_GRAPHS", INSTALLED_GRAPHS)
