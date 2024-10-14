import yaml
from schedule.settings import STRINGS_FILE


class StringLoader:
    yaml_string_path = STRINGS_FILE

    @classmethod
    def load_strings(cls):
        with open(cls.yaml_string_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    @classmethod
    def get_string(cls, key, default=None):
        keys = key.split('.')
        value = cls.load_strings()
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
