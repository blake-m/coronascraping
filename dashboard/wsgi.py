from components.main.base import CountryAndWorldComponentsBase
from components import template
from corona_app import create_app


template.bootstrap()
template.bootstrap()
country = CountryAndWorldComponentsBase()
app = create_app(country)
server = app.server
