from components.main.base import ComponentsData
from components import template
from corona_app import create_app

template.bootstrap()
data = ComponentsData()
app = create_app(data)
server = app.server
