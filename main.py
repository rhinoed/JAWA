# CIT 93 Final Program Project
# JAWA (Just Another Weather App)
# by: Mark Edmunds
# Date 11/2/2023
# This program will allow the user to enter a city and state and return the current weather conditions for that location.

# Import modules
import math
from K import Constants as k
from UserPreferences import UserPreferences as up
from WeatherServices import WeatherServices as ws
from GeocodeCity import Results
from datetime import datetime
from EmptyViews import (EmptyFavorites as ef, EmptyDailyView as edv)
from ModalView import AddFavorite as af
from Alert import Alert as alert
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

# Load the kv files
Builder.load_file("empty_favorites.kv")
Builder.load_file("add_favorite.kv")
Builder.load_file("empty_daily_view.kv")
Builder.load_file("alert.kv")

class Weather(BoxLayout):
    top_menu = ObjectProperty(None)
    weather_output = ObjectProperty(None)
    city = ObjectProperty(None)
    daily_weather = ObjectProperty(None)
    current_weather = ObjectProperty(None)
    favorite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        prefs = up(**up.load())
        self.top_menu.weather_binding = self
        if prefs.saved_location:
            forecast = ws.get_weather_for_location(prefs)
            try:
                self.weather_output = forecast["weather"]
                self.city = forecast["city"]
            except TypeError as te:
                print(f"An error occured geo_loacte returned NONE:{te}")
            self.top_menu.weather_response = self.weather_output
            self.output_weather()
        else:
            self.daily_weather.clear_widgets()
            empty_daily = edv()
            empty_daily.weather_binding = self
            self.daily_weather.add_widget(empty_daily)

        if len(prefs.favorites) == 0:
            self.favorite.clear_widgets()
            empty_favorite = ef()
            empty_favorite.weather_binding = self
            self.favorite.add_widget(empty_favorite)
        elif not prefs.saved_location and len(prefs.favorites) != 0:
            self.get_favorite_weather(prefs.favorites[0])
        
            
    
    def show_add_favorite(self):
        view = af()
        view.weather_binding = self
        view.user_prefs = up(**up.load())
        self.modal_popup = Popup(title="Add Favorite",
                                 content=view,
                                 size_hint=(0.5, 0.5),
                                 title_color=(1, 1, 1, 1,),
                                 separator_color=(.65,.20,.08,1),
                                 auto_dismiss=False)
        view.parent_popup = self.modal_popup
        self.modal_popup.open()
    
    def show_alert(self, message,image):
        view = alert()
        view.message = message
        view.image = image
        self.modal_popup = Popup(title="Alert",
                                 content=view,
                                 size_hint=(0.5, 0.5),
                                 title_color=(1, 1, 1, 1,),
                                 separator_color=(.65,.20,.08,1),
                                 auto_dismiss=True)
        view.parent_popup = self.modal_popup
        self.modal_popup.open()
        
    def search_button_pressed(self, text_input):
        if text_input == "":
            self.top_menu.text_input.hint_text = "You must enter a city"
        else:
            try:
                # get the weather for the city entered
                forcast = ws.get_weather_for(text_input)
            except IndexError as ie:
                print(f"An error occured geo_loacte returned NONE:{ie}")
                raise IndexError("There were no locations returned")

            self.weather_output = forcast["weather"]
            self.city = forcast["city"]
            # clear text input
            self.top_menu.text_input.text = ""
            # write the weather output
            self.output_weather()

    def get_user_preferred_unints(self) -> str:
        units =up(**up.load()).units
        match units:
            case "metric":
                return str(chr(0x2103))
            case "imperial":
                return str(chr(0x2109))
            case _:
                raise ValueError("Invalid unit type")
            
    def get_favorite_weather(self,location):
        forecast = ws.get_weather_for_location(None, location)
        try:
            self.weather_output = forecast["weather"]
            self.city = forecast["city"]
        except TypeError as te:
            print(f"An error occured geo_loacte returned NONE:{te}")
        self.output_weather()

    def output_weather(self):
        user_prefs = up(**up.load())
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
            if self.weather_output.daily != None:
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
    weather_binding = ObjectProperty(None)
    imperial = ObjectProperty(None)
    metric = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_default_units(self, button):
        units = up(**up.load()).units
        if button == units:
            return "down"
        else:
            return "normal"

    def unit_button_pressed(self, unit):
        print(f"Unit button pressed {unit}")
        prefs = up(**up.load())
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
        prefs = up(**up.load())
        if city != "":
            try:
                location = Results(ws.geo_locate(city)).cities[0]
                prefs.set_location(location)
            except IndexError as ie:
                print(f"An error occured geo_loacte returned NONE:{ie}")
        else:
            print("No city provided") 

    def add_button_pressed(self):
        try:    
            self.weather_binding.show_add_favorite()
        except AttributeError as ae:
            print(f"An error occured geo_loacte returned NONE:{ae}")
        except IndexError as ie:
            print(f"An error occured geo_loacte returned NONE:{ie}")
            raise IndexError("There were no locations returned")
       

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
        

class JAWAApp(App):
    def build(self):
        # Set the window size
        Window.size = (1200, 600)
        return Weather()


if __name__ == "__main__":
    # Run the app
    JAWAApp().run()
