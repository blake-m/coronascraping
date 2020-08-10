from components.main.country.country import SingleCountry, Countries, World
from components import template
from corona_app import create_app


template.bootstrap()
single_country = SingleCountry()
world = World()
countries = Countries()
app = create_app(single_country, countries, world)
server = app.server
