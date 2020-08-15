import abc
import json


class ConfigData:
    def __init__(self, selector_config: dict):
        self.selector_config = selector_config
        self.create_instance_attributes()

    def create_instance_attributes(self):
        for key, value in self.selector_config.items():
            if type(value) is str:
                exec(f"self.{key} = '{value}'")
            else:
                exec(f"self.{key} = {value}")
            # TODO(blake): remove this print
