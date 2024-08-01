# CIT 93 Final Program Project
# JAWA (Just Another Weather App)
# by: Mark Edmunds
# Date 11/2/2023
# This program will allow the user to enter a city and state and return the current weather conditions for that location.

# Import modules
import math
import UserPreferences
from K import Constants as k
from WeatherServices import WeatherServices
from GeocodeCity import Results
from datetime import datetime
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.core.window import Window


class Weather(BoxLayout):
    top_menu = ObjectProperty(None)
    weather_output = ObjectProperty(None)
    city = ObjectProperty(None)
    daily_weather = ObjectProperty(None)
    current_weather = ObjectProperty(None)
    favorite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        if prefs.saved_location:
            forecast = WeatherServices.get_weather_for_location(prefs)
            self.weather_output = forecast["weather"]
            self.city = forecast["city"]
            self.top_menu.weather_response = self.weather_output
            self.output_weather()
        
    def search_button_pressed(self, text_input):
        if text_input == "":
            self.top_menu.text_input.hint_text = "You must enter a city"
        else:
            print(f"Search button pressed {text_input}")
            forcast = WeatherServices.get_weather_for(text_input)
            # clear text input
            self.top_menu.text_input.text = ""
            self.weather_output = forcast["weather"]
            self.city = forcast["city"]
            self.top_menu.weather_response = self.weather_output
            # write the weather output
            self.output_weather()
            print(self.weather_output)

    def get_user_preferred_unints(self) -> str:
        units = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load()).units
        match units:
            case "metric":
                return str(chr(0x2103))
            case "imperial":
                return str(chr(0x2109))
            case _:
                raise ValueError("Invalid unit type")
            
    def get_favorite_weather(self,location):
        forecast = WeatherServices.get_weather_for_location(None, location)
        self.weather_output = forecast["weather"]
        self.city = forecast["city"]
        self.output_weather()

    def output_weather(self):
        user_prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        units = user_prefs.units
        if self.weather_output == None:
            raise ValueError("No weather data to display")
        else:
            # Current weather
            # Set temperature
            self.current_weather.current_temp_label.text = str(
                f"{math.floor(self.weather_output.current.temp)} {self.get_user_preferred_unints()}"
            )
            # Set the city name
            self.current_weather.current_city_label.text = self.city.name
            # Set the alert label if there is an alert
            self.current_weather.current_alert_label = "" if self.weather_output.alerts == None else f"⚠️ {self.weather_output.alerts[0].event}"
            
            # Set the current weather icon
            self.current_weather.current_weather_icon = f"icons/{k.get_icon_for_condition(
                self.weather_output.current.weather[0].id,
                self.weather_output.current.dt,
                self.weather_output.current.sunset,
                self.weather_output.current.sunrise
            )}"
            # Set the current weather description
            self.current_weather.current_weather_description_label = self.weather_output.current.weather[0].main
            # Current weather details
            # Set sunrise
            self.current_weather.current_sunrise_label.text = datetime.fromtimestamp(
                self.weather_output.current.sunrise).strftime('%-I:%M %p')
            # Set sunset
            self.current_weather.current_sunset_label.text = datetime.fromtimestamp(
                self.weather_output.current.sunset).strftime('%-I:%M %p')
            # Set humidity
            self.current_weather.current_humidity_label.text = f"{str(self.weather_output.current.humidity)} {k.weather_units["humidity"]}"
            # Set pressure
            self.current_weather.current_pressure_label.text = k.convert_pressure(units, int(self.weather_output.current.pressure))
            # Set wind speed
            self.current_weather.current_wind_label.text = f"{str(self.weather_output.current.wind_speed)} {k.weather_units[f"{units}_wind_speed"]}"
            # Set visibility
            self.current_weather.current_visibility_label.text = f"{self.weather_output.current.visibility} {k.weather_units["metric_visability"]}" if units == "metric" else k.convert_visability(self.weather_output.current.visibility)
            # Clear the existing daily view section
            self.daily_weather.clear_widgets()
            # Iterate over daily forecast to create the daily weather section
            for day in self.weather_output.daily:
                # Create view
                view = DailyWeather()
                view.day_label = DailyWeather.get_day_from_timestamp(day.dt)
                view.daily_temp_label = str(f"{math.floor(day.temp.max)}{self.get_user_preferred_unints()}")
                view.daily_description_label = day.weather[0].main
                icon = f"{day.weather[0].icon}@2x.png"
                view.daily_weather_icon = f"icons/{icon}"
                # Add view to window
                self.daily_weather.add_widget(view)
            # Create favorite view
            if len(user_prefs.favorites) != 0:
                self.favorite.clear_widgets()
                for location in user_prefs.favorites:
                    view = Favorite()
                    view.favorite_location = location
                    view.favorite_city_label = f"{location.name}, {k.get_state_code(location.state)}" if location.state != None else f"{location.name}, {location.country}"
                    # creae a binding object to the weather class instance
                    view.weather_binding = self
                    self.favorite.add_widget(view)
            else:
                self.favorite.clear_widgets()
                self.remove_widget(self.ids.favorite)
        


class CurrentWeather(BoxLayout):
    
    current_temp_label = ObjectProperty(None)
    current_city_label = ObjectProperty(None)
    current_sunrise_label = ObjectProperty(None)
    current_sunset_label = ObjectProperty(None)
    current_humidity_label = ObjectProperty(None)
    current_wind_label = ObjectProperty(None)
    current_pressure_label = ObjectProperty(None)
    current_visibility_label = ObjectProperty(None)
    current_weather_icon = StringProperty("")
    current_alert_label = StringProperty("")
    current_weather_description_label = StringProperty("")


class TopMenu(BoxLayout):
    text_input = ObjectProperty(None)
    weather_response = ObjectProperty(None)
    imperial = ObjectProperty(None)
    metric = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_default_units(self, button):
        units = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load()).units
        if button == units:
            return "down"
        else:
            return "normal"

    def unit_button_pressed(self, unit):
        print(f"Unit button pressed {unit}")
        prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        match unit:
            case "metric":
                prefs.units = unit
                self.metric.state = "down"
            case "imperial":
                prefs.units = unit
                self.imperial.state = "down"

            case _:
                raise ValueError("Invalid unit type")
        prefs.save()

    def set_location_pressed(self, city: str):
        prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        if city != "":
            location = Results(WeatherServices.geo_locate(city)).cities[0]
            prefs.set_location(location)
        else:
            print("No city provided") 

    def add_button_pressed(self, city: str):
        prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        if city != "":
            location = Results(WeatherServices.geo_locate(city)).cities[0]
            prefs.add_to_favorites(location)
            print(self.weather_response)
        else:
            print("No city provided")

class DailyWeather(BoxLayout):
    day_label = StringProperty("")
    daily_weather_icon = StringProperty("")
    daily_temp_label = StringProperty("")
    daily_description_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_day_from_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%A,  %d")

class Favorite(BoxLayout):
    favorite_location = ObjectProperty(None)
    favorite_forecast = ObjectProperty(None)
    weather_binding = ObjectProperty(None)
    favorite_city_label = StringProperty("")
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        
    def disable_favorite(self):
        user_prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        
        
    
    def get_favorite_weather(self):
        #forecast = WeatherServices.get_weather_for_location(None,self.favorite_location)
        #self.favorite_forecast = forecast["weather"]
        print(self.favorite_location.name)
        

class JAWAApp(App):
    def build(self):
        Window.size = (1200, 600)
        return Weather()


if __name__ == "__main__":
    JAWAApp().run()
