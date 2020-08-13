import dash_bootstrap_components as dbc

from components.auxiliary import funcs
from components.auxiliary.reusable import labeled_div_with_class_and_id
from components.main.base import ComponentsData, CountryAndWorldComponentsBase

CONFIG_PATH = './config.ini'
NOT_AVAILABLE_MESSAGE = "Data N/A"


class CountryComponent(CountryAndWorldComponentsBase):
    def __init__(self, data: ComponentsData):
        super().__init__(data)
        self.content_type = "country"

    @labeled_div_with_class_and_id(label="Country", class_name="col-8 mb-3")
    def select_country_dropdown(self):
        dropdown_items = [
            {"label": f"{funcs.correct_country_name(country)}",
             "value": country}
            for country in self.data.all_countries_names_list
        ]
        select_country = dbc.Select(
            id="countries_dropdown",
            options=dropdown_items,
            value="poland",  # Explicitly set
            className="custom-select",
        )
        return select_country
