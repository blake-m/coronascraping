from components.main.base import ComponentsData, CountryAndWorldComponentsBase

CONFIG_PATH = './config.ini'
NOT_AVAILABLE_MESSAGE = "Data N/A"


class WorldComponent(CountryAndWorldComponentsBase):
    def __init__(self, data: ComponentsData):
        super().__init__(data)
        self.content_type = "world"
