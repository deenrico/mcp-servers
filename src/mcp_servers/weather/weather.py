import requests
import json
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
import logging
import polars as pl
import re
from datamodels import (
    TimeResponse,
    WeatherQuery,
    WeatherForecastQuery,
    WeatherResponse,
    WeatherForecastResponse,
)

logger = logging.getLogger(__name__)

mcp = FastMCP("weather")


@mcp.tool(name="Fetch time information")
def get_current_datetime_week_weekday() -> str:
    f"""Tool to retrieve the current date and time as well as the weekday and calendar week.

    Returns:
        TimeResponse: Returns a parsable JSON string following this schema: {TimeResponse}
    """.strip()

    today = datetime.now()

    response = TimeResponse(
        current_datetime=today.strftime("%Y-%m-%dT%H:%M+01:00"),
        current_weekday=today.strftime("%A"),
        current_calendar_week=today.strftime("%U"),
    )

    return response.model_dump_json()


@mcp.tool(name="Get weather station information")
async def get_stations_names_and_ids(location_name: str) -> str:
    """
    Tool to get the latest station information of the German Weather Service (DWD).
    
    Most importantly, matches location names longitude and latitude, which can then be 
    used to query the BrightSky API for weather data, using longitude and latitude as inputs.

    Args:
        location_name (str): Location name to search for in the station list.
        
    Returns:
        str: A JSON parsable string containing the station location as longitude and latitude.
    """.strip()
    try:
        stations = requests.get(
            url="https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_rich.txt?view=nasPublication"
        )

    except Exception as e:
        return f"""
        The GET request seems to fail with exception {e}.
        """.strip()

    try:
        # Need to reconstruct the data bc the txt file is not in a standard format,
        # which will confuse LLM trying to parse it.
        station_dict = {
            element: []
            for element in stations.text.splitlines()[1].split()
            if element != "HFG_NFG"  # Not needed and messes up alignment
        }

    except Exception as e:
        return f"""
        Could not extract headers with exception {e}.
        """.strip()

    logger.debug(f"Empty station dict: \n\n{station_dict}")

    # Reconstruct the station information by splitting on lines and then on spaces
    reconstructed_stations = []

    for relevant_station in [
        station for station in stations.text.splitlines() if location_name in station
    ]:
        reconstructed_station = []

        for i, element in enumerate(re.split("  +", relevant_station)):
            # "If" needed as 1st col (station name) sometimes contains spaces
            # and I don't want to split on those
            if i == 0:
                reconstructed_station.append(element)
            else:
                for i in element.split():
                    reconstructed_station.append(i)

        if len(reconstructed_station) == 11:
            del reconstructed_station[7]

        reconstructed_stations.append(reconstructed_station)

    logger.debug(f"Reconstructed stations: \n\n{reconstructed_stations}")

    # Populate the station_dict
    for station in reconstructed_stations:
        for i, element in enumerate(station):
            key = list(station_dict)[i]
            station_dict[key].append(element)

    logger.debug(f"Filled station dict: \n\n{station_dict}")

    # Using Polars df.to_dicts() to make it a nice JSON parsable for LLM
    df = (
        (
            pl.LazyFrame(station_dict)
            .with_columns(
                pl.col("STAT_NAME").str.strip_chars(),
                pl.col("STAT_ID").cast(pl.Int64),
                pl.col("STAT").str.strip_chars(),
                pl.col("BR_HIGH").cast(pl.Float64),
                pl.col("LA_HIGH").cast(pl.Float64),
                pl.col("HS").cast(pl.Int64),
                pl.col("BL").str.strip_chars(),
                pl.col("ENDE").str.to_date(format="%d.%m.%Y"),
            )
            .rename(
                {
                    "STAT": "wmo_station_id",
                    "STAT_NAME": "station_name",
                    "BR_HIGH": "latitude_in_degrees",
                    "LA_HIGH": "longitude_in_degrees",
                    "ENDE": "last_weather_recording_date",
                    "BL": "state_location_abbreviation",
                }
            )
            .drop(pl.col("KE", "STAT_ID", "HS", "BEGINN"))
            .filter(
                pl.col("last_weather_recording_date")
                >= datetime.now().date() - timedelta(days=3)
            )
            # Needed re-cast to dump it as JSON
            .with_columns(pl.col("last_weather_recording_date").cast(pl.String))
        )
        .collect()
        .to_dicts()
    )

    logger.info(json.dumps(df))

    return json.dumps(df)


# TODO: Enforce / Validate response schema
@mcp.tool(name="Fetch current weather")
async def get_current_weather(
    weather_query: WeatherQuery,
    api_endpoint: str = "https://api.brightsky.dev/current_weather",
) -> str | WeatherResponse:
    f"""
    Tool to fetch the current weather data from the BrightSky API, which is a REST API
    for the German Weather Service (DWD).
    The weather_query can either contain latitude and longitude, or the wmo_station_id, but not both.
    
    The input should follow this schema (not enforced):
    {WeatherQuery.model_json_schema()}

    The response from the API follows this schema (not enforced):
    {WeatherResponse.model_json_schema()}
    """
    try:
        response = requests.get(
            url=api_endpoint,
            params=weather_query.model_dump(exclude_none=True),
            headers={"Accept": "application/json"},
        )

        logger.info(f"Weather API response status code: {response.status_code}")
        logger.info(f"Weather API response content: {response.text}")

        # TODO: Validate WeatherResponse and separate exception check from API call before dumping
        return json.loads(response.text)

    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")

        return f"""
                Error: Unable to reach the weather API endpoint or parse its response. 
                
                Exception: {e}
                """


@mcp.tool(name="Get weather forecast")
async def get_weather_forecast(
    weather_query: WeatherForecastQuery | str,
    api_endpoint: str = "https://api.brightsky.dev/weather",
) -> WeatherForecastResponse | str:
    """Tool to retrieve an (hourly) weather forecast for a given location upto a specified
    forecast horizont.

    Args:
        weather_query (WeatherForecastQuery | str): The weather query including the start and end dates as
                                              well as the longitude and latitude of the location. 
        api_endpoint (str): The brightsky API endpoint to call the weather forecast.

    Returns:
        WeatherForecastResponse | str: The weather forecast for a given TimeFrame
    """.strip()

    try:
        response = requests.get(
            url=api_endpoint,
            params=weather_query.model_dump(exclude_none=True),
            headers={"Accept": "application/json"},
        )

        logger.info(f"Weather API response status code: {response.status_code}")
        logger.info(f"Weather API response content: {response.text}")

        return json.loads(response.text)

    except Exception as e:
        return f"API request failed with error {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
