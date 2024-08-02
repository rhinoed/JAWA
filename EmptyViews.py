# Empty Views for the application
# August 2024
# Mark Edmunds

# Import the necessary modules
from kivy.uix.boxlayout import BoxLayout

class EmptyFavorites(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def add_favorite_button_pressed(self):
        print("Add Favorite Button Pressed")
    