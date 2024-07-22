#
#
#
#
import os
import json
from dataclasses import dataclass, asdict
from typing import List
from GeocodeCity import City
from K import Constants as k



@dataclass
class UserLocation:
    name: str
    lat: float
    lon: float
    country: str
    state: str
    state_code_usa: str


@dataclass
class UserPreferences:
    units: str
    saved_location: bool
    location: UserLocation
    favorites: List[City]

    def __post_init__(self):
        self.location = UserLocation(**self.location)
        self.favorites = [City(**city) for city in self.favorites]


    @classmethod
    def load(cls):
        with open("user_preferences.json", "r") as prefs:
            try:
                return json.load(prefs)
            except FileExistsError as fileEr:
                print(fileEr)
            except PermissionError as perEr:
                print(perEr)

    def save(self):
        if type(self) != UserPreferences:
            raise TypeError("Must be of type UserPreferences")
        else:
            with open("user_preferences.json", "w") as prefs:
                try:
                    print(self.units)
                    json.dump(asdict(self), prefs, indent=4)
                except PermissionError as perEr:
                    print(perEr)

    def add_to_favorites(self, fav):
        if len(self.favorites) == 10:
            raise MaxFavoritesError
        else:
            self.favorites.append(fav)
            self.save()

    def set_location(self, city: City):
        """Set the user's location to the given city
        :param city: City object"""
        if type(city) != City:
            raise TypeError("method set location expects argument of type City")
        else:
            self.saved_location = True
            self.location.name = city.name
            self.location.lat = city.lat
            self.location.lon = city.lon
            self.location.state = city.state
            self.location.country = city.country
            self.location.state_code_usa = k.get_state_code(city.state)
            self.save()





class MaxFavoritesError(Exception):
    """Raised when the user tries to add more than 10 favorites"""
    # creat message for the exception
    def __init__(self, message="You can only have 10 favorites"):
        self.message = message
        super().__init__(self.message)