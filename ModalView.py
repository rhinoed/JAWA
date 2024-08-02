# Modal View for the application
# August 2024
# Mark Edmunds

# Import the necessary libraries
from kivy.uix.boxlayout import BoxLayout

class AddFavorite(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dismiss(self):
        self.parent_popup.dismiss()   