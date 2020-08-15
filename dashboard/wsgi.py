import logging

from components.main.base import ComponentsData
from components import template
from corona_app import create_app

template.bootstrap()
data = ComponentsData()
app = create_app(data)
server = app.server


@server.route("/reload_data")
def reload_data():
    data.__init__()
    logging.info("ALL DATA RELOADED")
    return "ALL DATA RELOADED"
