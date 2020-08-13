from components.main.base import  ComponentsData
from components import template
from corona_app import create_app


def main():
    template.bootstrap()
    data = ComponentsData()
    app = create_app(data)
    app.run_server(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
