# Empty Views for the application
# August 2024
# Mark Edmunds

# Import the necessary modules
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Empty Favorites view
class EmptyFavorites(BoxLayout):
    weather_binding = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def add_favorite_button_pressed(self):
        # display a modal view to add a favorite
        self.weather_binding.show_add_favorite()

# Empty DailyWeather view
class EmptyDailyView(BoxLayout):
    weather_binding = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    