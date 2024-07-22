from dataclasses import dataclass
from typing import List

from datetime import datetime

# @dataclass
# class Names:
#     en: str =
#     ru: str
#     pl: str
#     lt: str
#     ta: str
#     uk: str
#     zh: str
#     ar: str
#     ja: str
#
#
#     def __post_init__(self, **kwargs):
#         # Handle unknown keys by adding them to the class
#         for key, value in kwargs.items():
#             setattr(self, key, value)


@dataclass
class City:
    name: str
    lat: float
    lon: float
    country: str
    state: str = ""
    local_names: dict = None



@dataclass
class Results:
    cities: list[City]

    def __post_init__(self):
        self.cities = [City(**obj) for obj in self.cities]
