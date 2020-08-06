from components.main.country.country import Countries
from components import template
from corona_app import create_app


def main():
    template.bootstrap()
    countries = Countries()
    app = create_app(countries)
    app.run_server(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
