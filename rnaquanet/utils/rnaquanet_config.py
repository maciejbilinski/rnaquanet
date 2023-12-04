import yaml
import os
from .dataclasses import ConfigData, ConfigNetwork

class RnaquanetConfig:
    name: str
    tools_path: str
    verbose: bool
    data: ConfigData
    network: ConfigNetwork
    def __init__(self, path: str, override: dict = {}):
        with open(path, "r") as stream:
            try:
                result = yaml.safe_load(stream)
                result = RnaquanetConfig._merge_dicts(result, override)
                self.name = result['name']
                self.tools_path = os.path.join(os.getcwd(), result['tools_path'])
                self.verbose = result['verbose']
                self.data = ConfigData(result['data'])
                self.network = ConfigNetwork(result['network'])
            except yaml.YAMLError as exc:
                e = Exception(exc)
                e.add_note('Cannot load config file')
                raise e
            except TypeError as exc:
                e = Exception(exc)
                e.add_note('Config file has incorrect structure')
                raise e
    
    @staticmethod
    def _merge_dicts(yml, override):
        result = {}
        for key in set(override.keys()) | set(yml.keys()):
            override_value = override.get(key)
            yml_value = yml.get(key)

            if isinstance(override_value, dict) and isinstance(yml_value, dict):
                result[key] = RnaquanetConfig._merge_dicts(yml_value, override_value)
            elif override_value is not None:
                result[key] = override_value
            elif yml_value is not None:
                result[key] = yml_value

        return result