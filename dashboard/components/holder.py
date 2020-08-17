from components.main.base import ComponentsData
from components.main.country import CountryComponents
from components.main.map.worldmap import WorldMapComponents
from components.main.world import WorldComponents
from components.main.worldtable import WorldTableComponents


class ComponentsHolder(object):
    def __init__(self, data: ComponentsData) -> None:
        self.data = data
        self.country = CountryComponents(data)
        self.world = WorldComponents(data)
        self.worldmap = WorldMapComponents(data)
        self.worldtable = WorldTableComponents(data)
