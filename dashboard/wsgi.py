from components.main.details import Components
from components import template
from corona_app import create_app


template.bootstrap()
template.bootstrap()
country = Components()
app = create_app(country)
server = app.server
