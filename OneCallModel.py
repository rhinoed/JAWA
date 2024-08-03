from dataclasses import dataclass
from typing import List

class Snow:
    ...

@dataclass
class Weather:
    id: int
    main: str
    description: str
    icon: str


@dataclass
class CurrentWeather:
    dt: int
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    weather: List[Weather]
    wind_gust: float = None
    snow: dict = None
    rain: dict = None

    def __post_init__(self):
        self.weather = [Weather(**obj) for obj in self.weather]


@dataclass
class MinutelyForecast:
    dt: int
    precipitation: int

@dataclass
class HourlyForecast:
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[Weather]
    pop: float
    rain: dict = None
    snow: dict = None

    def __post_init__(self):
        self.weather = [Weather(**obj) for obj in self.weather]


@dataclass
class DailyTemperature:
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


@dataclass
class DailyFeelsLike:
    day: float
    night: float
    eve: float
    morn: float


@dataclass
class DailyForecast:
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    summary: str
    temp: DailyTemperature
    feels_like: DailyFeelsLike
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[Weather]
    clouds: int
    pop: float
    rain: float = None
    snow: float = None
    uvi: float = None
    

    def __post_init__(self):
        self.temp = DailyTemperature(**self.temp)
        self.feels_like = DailyFeelsLike(**self.feels_like)
        self.weather = [Weather(**obj) for obj in self.weather]


@dataclass
class Alert:
    sender_name: str
    event: str
    start: int
    end: int
    description: str
    tags: List[str]

    def __post_init__(self):
        self.tags = [str(tag) for tag in self.tags]

@dataclass
class WeatherData:
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: CurrentWeather
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]
    minutely: List[MinutelyForecast] = None
    alerts: List[Alert] = None

    def __post_init__(self):
        self.current = CurrentWeather(**self.current)
        self.minutely = [MinutelyForecast(**obj) for obj in self.minutely]
        self.hourly = [HourlyForecast(**obj) for obj in self.hourly]
        self.daily = [DailyForecast(**obj) for obj in self.daily]
        if self.alerts != None:
            print(self.alerts)
            self.alerts = [Alert(**obj) for obj in self.alerts]
