from typing import Dict, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class WeatherStation(BaseModel):
    station_name: str = Field(
        ...,
        description="""
        The station name location. E.g. "Hamburg".
        """.strip(),
    )
    wmo_station_id: str = Field(
        ...,
        description="""
        WMO station ID, typically five alphanumeric characters.
        """.strip(),
    )
    latitude_in_degrees: float = Field(
        ...,
        description="""
        "Latitude of the weather station in decimal degrees."
        """.strip(),
    )
    longitude_in_degrees: float = Field(
        ...,
        description="""
        "Latitude of the weather station in decimal degrees."
        """.strip(),
    )
    state_location_abbreviation: str = Field(
        ...,
        description="""
        The state abbreviation. Possible values (and their meanings) are:
            "BB": "Brandenburg",
            "BE": "Berlin",
            "BW": "Baden-Württemberg",
            "BY": "Bayern",
            "HB": "Bremen",
            "HE": "Hessen",
            "HH": "Hamburg",
            "MV": "Mecklenburg-Vorpommern",
            "NI": "Niedersachsen",
            "NW": "Nordrhein-Westfalen",
            "RP": "Rheinland-Pfalz",
            "SH": "Schleswig-Holstein",
            "SL": "Saarland",
            "SN": "Sachsen",
            "ST": "Sachsen-Anhalt",
            "TH": "Thüringen",
            "T":  "Tirol"
        """.strip(),
    )
    last_weather_recording_date: str = Field(
        ...,
        description="""
        This is the general station information update.
        Not to be confused with the last current weather information.
        It just means this was the last time the station was updated in the
        station list.
        """.strip(),
    )


class WeatherQuery(BaseModel):
    lat: float | None = Field(
        description="""
        Latitude of the location. If specified, you need to also specify longitude.
        Should not be given together with the WMO station ID""".strip()
    )
    lon: float | None = Field(
        description="""
        Longitude of the location. If specified, you need to also specify latitude.
        Should not be given together with the WMO station ID""".strip()
    )
    # TODO: wmo_stations are less reliable than longitude, latitude since some stations are
    #       specialized and don't give current weather data, leading to ValidationErrors
    # wmo_station_id: list[str, int] | None = Field(None,
    #     description="WMO station ID. If longitude and latitude are given, this parameter should be None."
    #     )


class WeatherForecastQuery(BaseModel):
    date: str = Field(
        default=datetime.now().strftime("%Y-%m-%dT%H:%M+01:00"),
        description="""
        Timestamp of first weather record (or forecast) to retrieve, in ISO 8601 format. 
        May contain time and/or UTC offset. Usually the current date (and time).
        Needs to be of format: "%Y-%m-%d" or "%Y-%m-%dT%H:%M+01:00"
        """.strip(),
        examples=["'2025-10-29T11:31+01:00'"],
    )
    last_date: str | None = Field(
        default=None,
        description="""
        Timestamp of last weather record (or forecast) to retrieve, in ISO 8601 format. 
        Will default to date + 1 day.
        """.strip(),
        examples=["2025-10-30T11:31+01:00"],
    )
    lat: float | None = Field(
        description="""
        Latitude of the location. If specified, you need to also specify longitude.
        Should not be given together with the WMO station ID""".strip()
    )
    lon: float | None = Field(
        description="""
        Longitude of the location. If specified, you need to also specify latitude.
        Should not be given together with the WMO station ID""".strip()
    )


class CurrentWeatherRecord(BaseModel):
    timestamp: datetime = Field(description="The current date and timestamp.")
    cloud_cover: float | None = Field(
        description="""
        The amount of current otal cloud cover at timestamp in percent, where: 
        - 0-10 percent is "clear" or "sunny"
        - 10-30 percent is "mostly sunny"
        - 30-70 percent is "partly sunny" or "partly cloudy"
        - 70-90 percent is "mostly cloudy" or "mostly overcast"
        - 80-100 percent is "cloudy" or "completely overcast"
        """.strip()
    )
    condition: str | None = Field(
        description="""
        Current weather condition as a one-word summary.
        Unlike the numerical parameters, this field is not taken 
        as-is from the raw data (because it does not exist), 
        but is calculated from different fields in the raw data as 
        a best effort.
        """.strip()
    )
    icon: str | None = Field(
        description="""
        Icon alias suitable for the current weather conditions. 
        Unlike the numerical parameters, this field is not taken as-is 
        from the raw data (because it does not exist), but is calculated from 
        different fields in the raw data as a best effort. 
        Not all values are available for all source types.
        """
    )
    relative_humidity: int | None = Field(
        description="Current relative humidity in percent."
    )
    temperature: float | None = Field(
        description="Current real temperature in degrees Celsius"
    )
    visibility: int | None
    precipitation_10: float | None = Field(
        description="Precipitation sum over the last 10 minutes in mm."
    )
    precipitation_30: float | None = Field(
        description="Precipitation sum over the last 30 minutes in mm."
    )
    precipitation_60: float | None = Field(
        description="Precipitation sum over the last 60 minutes in mm."
    )
    solar_10: float | None = Field(
        description="Solar radiation over the last 10 minutes in W/m²."
    )
    solar_30: float | None = Field(
        description="Solar radiation over the last 30 minutes in W/m²."
    )
    solar_60: float | None = Field(
        description="Solar radiation over the last 60 minutes in W/m²."
    )
    sunshine_30: int | None = Field(
        description="Sunshine duration over the last 30 minutes in minutes."
    )
    sunshine_60: int | None = Field(
        description="Sunshine duration over the last 60 minutes in minutes."
    )
    wind_direction_10: int | None = Field(
        description="Wind direction at 10 meters height in degrees."
    )
    wind_direction_30: int | None = Field(
        description="Wind direction at 30 meters height in degrees."
    )
    wind_direction_60: int | None = Field(
        description="Wind direction at 60 meters height in degrees."
    )
    wind_speed_10: float | None = Field(
        description="Wind speed at 10 meters height in m/s."
    )
    wind_speed_30: float | None = Field(
        description="Wind speed at 30 meters height in m/s."
    )
    wind_speed_60: float | None = Field(
        description="Wind speed at 60 meters height in m/s."
    )
    wind_gust_direction_10: int | None = Field(
        description="Wind gust direction at 10 meters height in degrees."
    )
    wind_gust_direction_30: int | None = Field(
        description="Wind gust direction at 30 meters height in degrees."
    )
    wind_gust_direction_60: int | None = Field(
        description="Wind gust direction at 60 meters height in degrees."
    )
    wind_gust_speed_10: float | None = Field(
        description="Wind gust speed at 10 meters height in m/s."
    )
    wind_gust_speed_30: float | None = Field(
        description="Wind gust speed at 30 meters height in m/s."
    )
    wind_gust_speed_60: float | None = Field(
        description="Wind gust speed at 60 meters height in m/s."
    )


class Source(BaseModel):
    id: int = Field(description="Bright Sky source ID. Only relevant for dev purposes.")
    dwd_station_id: str | None = Field(
        description="DWD weather station ID, if available."
    )
    wmo_station_id: str | None = Field(
        description="WMO weather station ID, if available."
    )
    station_name: str | None = Field(
        description="Name of the weather station, if available. Example: Munich"
    )
    observation_type: str | None = Field(
        description="""
        Type of the weather station, if available. Available values are:
        historical, current, synop, forecast
        """.strip()
    )
    first_record: datetime | None = Field(
        description="""
        Timestamp of first available record for this source.
        Only relevant for historical sources and for dev purposes.
        """.strip()
    )
    last_record: datetime | None = Field(
        description="""
        Timestamp of last available record for this source.
        Only relevant for historical sources and for dev purposes.
        """.strip()
    )
    lat: float | None = Field(
        description="Latitude of the weather station in decimal degrees, if available."
    )
    lon: float | None = Field(
        description="Longitude of the weather station in decimal degrees, if available."
    )
    height: float | None = Field(description="Height of the weather station in meters.")
    distance: int | None = Field(
        description="""
        Distance of weather station to the requested lat and lon 
        (if given), in meters.""".strip()
    )


class WeatherResponse(BaseModel):
    weather: CurrentWeatherRecord
    sources: list[Source]


class TimeResponse(BaseModel):
    current_datetime: str | datetime = Field(description="The current date and time")
    current_weekday: str = Field(
        description="The name of the weekday for the current datetime"
    )
    current_calendar_week: int | None = Field(
        description="The current calendar week for the current datetime"
    )


class WeatherForecastRecord(BaseModel):
    """A weather observation for one time stamp."""

    timestamp: str = Field(
        description="ISO 8601‑formatted timestamp of this weather record.",
        examples=["2023-08-07T12:30:00+00:00"],
    )
    source_id: int | None = Field(
        None,
        description="BrightSky source ID for this record.",
        examples=[238685],
    )

    cloud_cover: float | None = Field(
        None,
        description="Total cloud cover at timestamp (percentage, 0‑100).",
        examples=[12.1],
    )
    condition: str | None = Field(
        None,
        description=(
            "Human‑readable weather conditions derived from the raw data.\n\n"
            "Allowed values: dry, fog, rain, sleet, snow, hail, thunderstorm."
        ),
        examples=["rain"],
    )

    dew_point: float | None = Field(
        None,
        description="Dew point at timestamp (°C), measured 2 m above ground.",
        examples=[-2.5],
    )
    icon: str | None = Field(
        None,
        description=(
            "Icon alias suitable for the current weather conditions "
            "(derived, not raw).\n\n"
            "Allowed values: clear-day, clear-night, partly-cloudy-day, "
            "partly‑cloudy-night, cloudy, fog, wind, rain, sleet, snow, hail, thunderstorm."
        ),
        examples=["rain"],
    )

    pressure_msl: float | None = Field(
        None,
        description=(
            "Atmospheric pressure at timestamp, reduced to mean sea level (hPa)."
        ),
        examples=[1015.1],
    )
    relative_humidity: int | None = Field(
        None,
        description="Relative humidity at timestamp (%).",
        examples=[40],
    )
    temperature: float | None = Field(
        None,
        description="Air temperature at timestamp (°C), 2 m above ground.",
        examples=[10.6],
    )
    visibility: int | None = Field(
        None,
        description="Visibility at timestamp (metres).",
        examples=[3621],
    )

    fallback_source_ids: Dict[str, int] | None = Field(
        None,
        description=(
            "Mapping of meteorological parameters to the source IDs "
            "that were used to fill missing values."
        ),
        examples=[{"pressure_msl": 11831, "wind_speed_30": 11831}],
    )

    precipitation: float | None = Field(
        None,
        description="Total precipitation during previous 60 min (mm).",
        examples=[1.8],
    )
    solar: float | None = Field(
        None,
        description="Solar irradiation during previous 60 min (kWh/m²).",
        examples=[0.563],
    )
    sunshine: int | None = Field(
        None,
        description="Sunshine duration during previous 60 min (minutes).",
        examples=[58],
    )

    wind_direction: int | None = Field(
        None,
        description=(
            "Mean wind direction during previous hour, 10 m above ground (°)."
        ),
        examples=[70],
    )
    wind_speed: float | None = Field(
        None,
        description="Mean wind speed during previous hour, 10 m above ground (m/s).",
        examples=[12.6],
    )
    wind_gust_direction: int | None = Field(
        None,
        description=(
            "Direction of maximum wind gust during previous hour 10 m above ground (°)."
        ),
        examples=[50],
    )
    wind_gust_speed: float | None = Field(
        None,
        description=(
            "Speed of maximum wind gust during previous hour 10 m above ground (m/s)."
        ),
        examples=[33.5],
    )

    precipitation_probability: int | None = Field(
        None,
        description="Probability (>0.1 mm) of precipitation in the previous hour (%).",
        examples=[46],
    )
    precipitation_probability_6h: int | None = Field(
        None,
        description=(
            "Probability (>0.2 mm) of precipitation in the previous "
            "6 hours (%). Only available at 0, 6, 12, 18 UTC."
        ),
        examples=[75],
    )


class WeatherForecastSource(BaseModel):
    """Metadata for a weather source that contributed to the payload."""

    id: int = Field(
        ...,
        description="BrightSky source ID.",
        examples=[6007],
    )
    dwd_station_id: str | None = Field(
        None,
        description="DWD weather station ID (5‑char code).",
        examples=["01766"],
    )
    wmo_station_id: str | None = Field(
        None,
        description="WMO weather station ID (5‑char code).",
        examples=["10315"],
    )
    station_name: str | None = Field(
        None,
        description="DWD weather station name.",
        examples=["Münster/Osnabrück"],
    )

    observation_type: str | None = Field(
        None,
        description=("Type of source data."),
        examples=["historical", "current", "synop", "forecast"],
    )
    first_record: str | None = Field(
        None,
        description="<date‑time> timestamp of the first available record for this source.",
        examples=["2010-01-01T00:00+02:00"],
    )
    last_record: str | None = Field(
        None,
        description="<date‑time> timestamp of the latest available record.",
        examples=["2023-08-07T12:40+02:00"],
    )

    lat: float | None = Field(
        None,
        description="Station latitude, decimal degrees.",
        examples=[52.1344],
    )
    lon: float | None = Field(
        None,
        description="Station longitude, decimal degrees.",
        examples=[7.6969],
    )
    height: float | None = Field(
        None,
        description="Station height above sea level (m).",
        examples=[47.8],
    )
    distance: int | None = Field(
        None,
        description="Distance of the station to the requested lat/lon in metres.",
        examples=[1234],
    )


class WeatherForecastResponse(BaseModel):
    """Full BrightSky API response."""

    weather: List[WeatherForecastRecord] = Field(
        description="Array of hourly weather records.",
    )
    sources: List[WeatherForecastSource] = Field(
        description="Metadata for the source(s) that provided the data.",
    )
