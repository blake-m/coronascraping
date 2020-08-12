from components.main.country import Country
from components import template
from corona_app import create_app


def main():
    template.bootstrap()
    country = Country()
    app = create_app(country)
    app.run_server(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
