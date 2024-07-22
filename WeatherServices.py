import os
import requests
from GeocodeCity import Results
from OneCallModel import WeatherData
from UserPreferences import UserPreferences


class WeatherServices:
    user_prefs = UserPreferences(**UserPreferences.load())
    api_key = os.environ.get('OPEN_WEATHER_API_KEY')
    units = user_prefs.units
    state_code = ""
    country_code = user_prefs.location.country
    limit = 3

    def __init__(self):
        raise NotImplementedError("This class cannot be instantiated")

    @classmethod
    def geo_locate(cls, city):
        user_prefs = UserPreferences(**UserPreferences.load())
        request = requests.get(
            f"https://api.openweathermap.org/geo/1.0/direct?q={city},{cls.state_code},{cls.country_code}&limit={cls.limit}&appid={cls.api_key}")
        print(request)
        if request.status_code == 200:
            return request.json()
        else:
            raise ValueError("The request did not return a valid location")


    @classmethod
    def get_weather_for(cls, city):
        """Returns a WeatherData object for the given city"""
        user_prefs = UserPreferences(**UserPreferences.load())
        try:
            location = Results(cls.geo_locate(city)).cities[0]
            one_call = f"https://api.openweathermap.org/data/3.0/onecall?lat={location.lat}&lon={location.lon}&units={user_prefs.units}&appid={cls.api_key}"
            request = requests.get(one_call).json()
            print(request)
            return {
                    "city": location,
                    "weather": WeatherData(**request)
                    }

        except ValueError as ve:
            print(ve)
