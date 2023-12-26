import json
import os
import pathlib
from typing import Union

from vodafone_station.util import CallableValue


class Config:

    def __init__(self, config: Union[dict, os.PathLike, str], defaults: Union[dict, os.PathLike, str] = None):
        if defaults is None:
            defaults = pathlib.Path(pathlib.Path(__file__).parent, "default_config.json").absolute()
        self.config = self.load_config(config)
        self.defaults = self.load_config(defaults)

    @staticmethod
    def load_config(config: Union[dict, os.PathLike, str]) -> dict:
        if not isinstance(config, dict):
            with open(config, "r") as f:
                return json.load(f)
        else:
            return config

    @staticmethod
    def _get_value_with_previous(config: dict, previous: list[str], name: str):
        for key in previous:
            config = config[key]
        return config[name]

    def get_value_with_previous(self, previous: list[str], name: str):
        try:
            return self._get_value_with_previous(self.config, previous, name)
        except KeyError:
            if not self.defaults:
                raise
            return self._get_value_with_previous(self.defaults, previous, name)

    def get_value(self, name: str):
        name_parts = name.split("_")
        concat_name_parts = []
        previous = []
        value = None
        error = None

        for name_part in name_parts:
            try:
                concat_name_parts.append(name_part)
                name = "_".join(concat_name_parts)
                value = self.get_value_with_previous(previous, name)
                previous.append(name)
                concat_name_parts = []
                error = None
            except TypeError:
                pass
            except KeyError as error_obj:
                error = error_obj

        if error:
            raise error
        return value

    def __getattr__(self, name: str):
        name = name.replace("get_", "").replace("is_", "")
        value = self.get_value(name)
        return CallableValue(value)
