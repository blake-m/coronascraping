from components.main.country.country import SingleCountry, Countries
from components import template
from corona_app import create_app


template.bootstrap()
single_country = SingleCountry()
countries = Countries()
app = create_app(single_country, countries)
server = app.server
