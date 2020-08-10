from components.main.country.country import SingleCountry, Countries, World
from components import template
from corona_app import create_app


def main():
    template.bootstrap()
    single_country = SingleCountry()
    countries = Countries()
    world = World()
    app = create_app(single_country, countries, world)
    app.run_server(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
