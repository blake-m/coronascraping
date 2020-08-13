from typing import Optional, Callable

from datetime import datetime


import dash_bootstrap_components as dbc
import dash_html_components as html


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


def print_startup_time(action_name: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            t1 = datetime.now()
            function(*args, **kwargs)
            t2 = datetime.now()
            print(f"{action_name} STARTUP TIME:", t2 - t1)
        return wrapper
    return decorator
