from typing import Optional, Callable

import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp


def date_to_month_day_format(date_: Timestamp):
    date = pd.to_datetime(date_)
    return f"{date.month_name()[:3]} {date.day}"


def date_to_day_month_year_format(date_: Timestamp):
    date = pd.to_datetime(date_)
    return f"{date.day} {date.month_name()[:3]} {date.year}"


def labeled_div_with_class_and_id(
        label: str, class_name: str = "", div_id: Optional[str] = None
) -> Callable:
    def labeled_div_decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if div_id is not None:
                return html.Div(
                    className=class_name,
                    id=div_id,
                    children=[
                        dbc.Label(
                            label,
                            className="h6"
                        ),
                        function(*args, **kwargs)
                    ]
                )

            return html.Div(
                className=class_name,
                children=[
                    dbc.Label(
                        label,
                        className="h6"
                    ),
                    function(*args, **kwargs)
                ]
            )
        return wrapper
    return labeled_div_decorator
