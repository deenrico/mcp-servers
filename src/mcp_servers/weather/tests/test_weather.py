import requests
from pydantic import BaseModel, Field, field_validator, model_validator
import pytest
from ..src.weather.weather import (
    get_current_datetime_week_weekday,
    get_stations_names_and_ids,
    get_current_weather,
    get_weather_forecast,
)

from ..src.weather.datamodels import (
    TimeResponse,
    WeatherQuery,
    WeatherForecastQuery,
    WeatherResponse,
    WeatherForecastResponse,
)


# TODO: Implement tests
def test_get_current_datetime_week_weekday():
    assert True
