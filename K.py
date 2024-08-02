from datetime import datetime as dt
import math
class Constants():
    weather_units = {
            "imperial_wind_speed": "MPH",
            "metric_wind_speed": "m/s",
            "pressure": "hPa",
            "imperial_pressure": "inHg",
            "metric_pressure": "mmHg",
            "humidity": "%",
            "imperial_visability": "miles",
            "metric_visability": "meters"
        }
    
    user_location_init_dict = {
            "name": "", "lat": 0.0,
            "lon": 0.0, "country": "",
            "state": "",
            "state_code_usa": ""
        }
    user_pref_init_dict = {
            "units": "imperial",
            "saved_location": False,
            "location": user_location_init_dict,
            "favorites": []
        }
    def __init__(self) -> None:
        raise NotImplementedError("This class cannot be instantiated")
    @staticmethod
    def convert_visability(meters: int) -> str:
        miles = meters / 1609.344
        return str(f"{math.floor(miles)} {Constants.weather_units["imperial_visability"]}")
    
    @staticmethod
    def convert_pressure(unints: str, pressure: int) -> str:
        match unints:
            # Convert pressure to imperial
            case "imperial":
                # limit the decimal places to 2
                return f"{round(pressure * 0.02953, 2)} {Constants.weather_units["imperial_pressure"]}"
            # Convert pressure to metric
            case "metric":
                return f"{round(pressure * 0.750064)} {Constants.weather_units["metric_pressure"]}"
    
    
    @staticmethod
    def get_code_class(code: str) -> str:
        match int(code):
            case 800:
                return "800"
            case 801:
                return "801"
            case 802:
                return "802"
            case code if code >= 803 or code <= 815:
                return "80x"
            case code if code >= 700 or code <= 715:
                return "7xx"
            case code if code >= 600 or code <= 615:
                return "6xx"
            case code if code >= 500 or code <= 509:
                return "50x"
            case 511:
                return "511"
            case code if code >= 512 or code <= 515:
                return "5xx"
            case code if code >= 300 or code <= 315:
                return "3xx"
            case code if code >= 200 or code <= 215:
                return "2xx"
    @staticmethod
    def get_icon_for_condition(code: str, time_of_day: str, sunset: str, sunrise: str) -> str:
        code_class = Constants.get_code_class(code)
        icon_dict_list = [
                        {"code_class": "800", "description": "clear sky", "day":"01d@2x.png", "night":"01n@2x.png"},
                        {"code_class": "801", "description": "few clouds", "day":"02d@2x.png", "night":"02n@2x.png"},
                        {"code_class": "802", "description": "scattered clouds", "day":"03d@2x.png", "night":"03n@2x.png"},
                        {"code_class": "80x", "description": "broken/overcast", "day":"04d@2x.png", "night":"04n@2x.png"},
                        {"code_class": "7xx", "description": "atmosphere", "day":"50d@2x.png", "night":"50n@2x.png"},
                        {"code_class": "6xx", "description": "snow", "day":"13d@2x.png", "night":"13n@2x.png"},
                        {"code_class": "50x", "description": "rain", "day":"10d@2x.png", "night":"10n@2x.png"},
                        {"code_class": "511", "description": "frezzing rain", "day":"13d@2x.png", "night":"13n@2x.png"},
                        {"code_class": "5xx", "description": "rain", "day":"09d@2x.png", "night":"09n@2x.png"},
                        {"code_class": "3xx", "description": "drizzle", "day":"09d@2x.png", "night":"09n@2x.png"},
                        {"code_class": "2xx", "description": "thunderstorm", "day":"11d@2x.png", "night":"11n@2x.png"},
                        ]
        local_time = dt.fromtimestamp(time_of_day)
        time_of_sunset = dt.fromtimestamp(sunset)
        time_of_sunrise = dt.fromtimestamp(sunrise)
        night_or_day = "night" if local_time < time_of_sunrise or local_time > time_of_sunset else "day"
        for group in icon_dict_list:
            if group["code_class"] == code_class:
                return group[night_or_day]

    
    @staticmethod
    def get_state_code(name_of_state: str, key="name") -> str:
        state_codes = [
                    {"name":"Alabama","abbreviation":"AL"},
                    {"name":"Alaska","abbreviation":"AK"},
                    {"name":"Arizona","abbreviation":"AZ"},
                    {"name":"Arkansas","abbreviation":"AR"},
                    {"name":"California","abbreviation":"CA"},
                    {"name":"Colorado","abbreviation":"CO"},
                    {"name":"Connecticut","abbreviation":"CT"},
                    {"name":"Delaware","abbreviation":"DE"},
                    {"name":"Florida","abbreviation":"FL"},
                    {"name":"Georgia","abbreviation":"GA"},
                    {"name":"Hawaii","abbreviation":"HI"},
                    {"name":"Idaho","abbreviation":"ID"},
                    {"name":"Illinois","abbreviation":"IL"},
                    {"name":"Indiana","abbreviation":"IN"},
                    {"name":"Iowa","abbreviation":"IA"},
                    {"name":"Kansas","abbreviation":"KS"},
                    {"name":"Kentucky","abbreviation":"KY"},
                    {"name":"Louisiana","abbreviation":"LA"},
                    {"name":"Maine","abbreviation":"ME"},
                    {"name":"Maryland","abbreviation":"MD"},
                    {"name":"Massachusetts","abbreviation":"MA"},
                    {"name":"Michigan","abbreviation":"MI"},
                    {"name":"Minnesota","abbreviation":"MN"},
                    {"name":"Mississippi","abbreviation":"MS"},
                    {"name":"Missouri","abbreviation":"MO"},
                    {"name":"Montana","abbreviation":"MT"},
                    {"name":"Nebraska","abbreviation":"NE"},
                    {"name":"Nevada","abbreviation":"NV"},
                    {"name":"New Hampshire","abbreviation":"NH"},
                    {"name":"New Jersey","abbreviation":"NJ"},
                    {"name":"New Mexico","abbreviation":"NM"},
                    {"name":"New York","abbreviation":"NY"},
                    {"name":"North Carolina","abbreviation":"NC"},
                    {"name":"North Dakota","abbreviation":"ND"},
                    {"name":"Ohio","abbreviation":"OH"},
                    {"name":"Oklahoma","abbreviation":"OK"},
                    {"name":"Oregon","abbreviation":"OR"},
                    {"name":"Pennsylvania","abbreviation":"PA"},
                    {"name":"Rhode Island","abbreviation":"RI"},
                    {"name":"South Carolina","abbreviation":"SC"},
                    {"name":"South Dakota","abbreviation":"SD"},
                    {"name":"Tennessee","abbreviation":"TN"},
                    {"name":"Texas","abbreviation":"TX"},
                    {"name":"Utah","abbreviation":"UT"},
                    {"name":"Vermont","abbreviation":"VT"},
                    {"name":"Virginia","abbreviation":"VA"},
                    {"name":"Washington","abbreviation":"WA"},
                    {"name":"West Virginia","abbreviation":"WV"},
                    {"name":"Wisconsin","abbreviation":"WI"},
                    {"name":"Wyoming","abbreviation":"WY"}
                   ]
        for state in state_codes:
            if state[key] == name_of_state:
                return state["abbreviation"]