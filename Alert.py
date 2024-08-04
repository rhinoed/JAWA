#
#
#
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class Alert(BoxLayout):
    message = StringProperty("")
    image = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class critical_weather_alert(Alert):
    instructions = StringProperty("")
    weather_icon = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "Critical Alert"
        self.image = "images/critical.png"