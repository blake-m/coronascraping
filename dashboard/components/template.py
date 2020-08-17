import plotly.graph_objects as go
import plotly.io as pio


def bootstrap():
    """Set CSS template to be used by Dash."""
    pio.templates["bootstrap"] = go.layout.Template({
        "layout": {
            "colorway": [
                "#007bff",  # primary
                "#ffc107",  # warning
                "#dc3545",  # danger
                "#17a2b8",  # info
                "#6c757d",  # secondary
                "#28a745",  # success
                "#f8f9fa",  # light
                "#343a40",  # dark
            ]
        }
    })

    pio.templates.default = "plotly_white+bootstrap"
