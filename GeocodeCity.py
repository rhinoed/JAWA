from dataclasses import dataclass

@dataclass
class City:
    name: str
    lat: float
    lon: float
    country: str
    state: str = ""
    state_code_usa: str = None
    local_names: dict = None



@dataclass
class Results:
    cities: list[City]

    def __post_init__(self):
        self.cities = [City(**obj) for obj in self.cities]
