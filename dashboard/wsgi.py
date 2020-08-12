from components.main.country import Country
from components import template
from corona_app import create_app


template.bootstrap()
template.bootstrap()
country = Country()
app = create_app(country)
server = app.server
