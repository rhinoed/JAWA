# Modal View for the application
# August 2024
# Mark Edmunds

# Import the necessary libraries
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class AddFavorite(BoxLayout):
    weather_binding = ObjectProperty(None)
    user_prefs = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_then_dismiss(self, input_text):
        try:
            # get the weather data for the city
            self.weather_binding.search_button_pressed(input_text)
            # add the city to the favorites
            self.user_prefs.add_to_favorites(self.weather_binding.city)
        except IndexError as ie:
            self.parent.title = f"An error occurred while adding favorite: {ie}"
            print(f"An error occurred while adding favorite: {ie}")
        
        # output the weather this is actually done twice once when `search_button_pressed` is called and again here
        # this is done to ensure the favorites are updated
        if input_text != "":
            self.weather_binding.output_weather()
        self.parent_popup.dismiss()   