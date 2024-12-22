from clients.accuweather_client import AccuWeatherClient
from typing import Any, Dict, List, Optional, Union
from utils import (
    check_bad_weather,
    format_ten_day_weather_response,
    format_five_day_weather_response,
    format_weather_response,
)


def get_one_day_weather_by_coordinates(latitude: Optional[float], longitude: Optional[float]) -> Union[Dict[str, Any], Dict[str, str]]:
    if latitude is None or longitude is None:
        return {"error": "Latitude and/or longitude not provided"}

    client = AccuWeatherClient()

    location = client.get_location_by_position(latitude, longitude)
    if location is None:
        return {"error": "Failed to retrieve location with the provided data"}

    weather = client.get_one_day_weather_by_location_key(location["Key"])
    if weather is None:
        return {"error": "Failed to retrieve weather with the provided data"}

    formatted_weather = format_weather_response(weather)
    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    weather_conditions = check_bad_weather(formatted_weather)
    formatted_weather["weather_conditions"] = weather_conditions
    formatted_weather["latitude"] = latitude
    formatted_weather["longitude"] = longitude

    return formatted_weather


def get_one_day_weather_by_city(city: Optional[str]) -> Union[Dict[str, Any], Dict[str, str]]:
    if city is None:
        return {"error": "City not provided"}

    client = AccuWeatherClient()

    locations = client.get_location_by_search(city)
    if not locations:
        return {"error": "Failed to retrieve location with the provided data"}

    location = locations[0]

    weather = client.get_one_day_weather_by_location_key(location["Key"])
    if weather is None:
        return {"error": "Failed to retrieve weather with the provided data"}

    formatted_weather = format_weather_response(weather)
    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    weather_conditions = check_bad_weather(formatted_weather)
    formatted_weather["weather_conditions"] = weather_conditions
    formatted_weather["latitude"] = location["GeoPosition"]["Latitude"]
    formatted_weather["longitude"] = location["GeoPosition"]["Longitude"]

    return formatted_weather


def get_five_day_weather_by_city(city: Optional[str]) -> Union[List[Any], Dict[str, str], None]:
    if city is None:
        return {"error": "City not provided"}

    client = AccuWeatherClient()

    locations = client.get_location_by_search(city)
    if not locations:
        return {"error": "Failed to retrieve location with the provided data"}

    location = locations[0]

    weather_data = client.get_five_day_weather_by_location_key(location["Key"])

    if weather_data is None:
        return {"error": "Failed to retrieve 5-day weather forecast"}

    formatted_weather = format_five_day_weather_response(weather_data)

    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    formatted_weather["latitude"] = location["GeoPosition"]["Latitude"]
    formatted_weather["longitude"] = location["GeoPosition"]["Longitude"]

    return formatted_weather


def get_five_day_weather_by_location(latitude: Optional[float], longitude: Optional[float]) -> Union[List[Any], Dict[str, str], None]:
    if latitude is None or longitude is None:
        return {"error": "Latitude and/or longitude not provided"}

    client = AccuWeatherClient()

    location = client.get_location_by_position(latitude, longitude)
    if location is None:
        return {"error": "Failed to retrieve location with the provided data"}

    location_key = location["Key"]
    weather_data = client.get_five_day_weather_by_location_key(location_key)

    if weather_data is None:
        return {"error": "Failed to retrieve 5-day weather forecast"}

    formatted_weather = format_five_day_weather_response(weather_data)

    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    formatted_weather["latitude"] = latitude
    formatted_weather["longitude"] = longitude

    return formatted_weather


def get_ten_day_weather_by_city(city: Optional[str]) -> Union[List[Any], Dict[str, str], None]:
    if city is None:
        return {"error": "City not provided"}

    client = AccuWeatherClient()

    locations = client.get_location_by_search(city)
    if not locations:
        return {"error": "Failed to retrieve location with the provided data"}

    location = locations[0]

    weather_data = client.get_ten_day_weather_by_location_key(location["Key"])

    if weather_data is None:
        return {"error": "Failed to retrieve 10-day weather forecast"}

    formatted_weather = format_ten_day_weather_response(weather_data)

    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    formatted_weather["latitude"] = location["GeoPosition"]["Latitude"]
    formatted_weather["longitude"] = location["GeoPosition"]["Longitude"]

    return formatted_weather


def get_ten_day_weather_by_location(latitude: Optional[float], longitude: Optional[float]) -> Union[List[Any], Dict[str, str], None]:
    if latitude is None or longitude is None:
        return {"error": "Latitude and/or longitude not provided"}

    client = AccuWeatherClient()

    location = client.get_location_by_position(latitude, longitude)
    if location is None:
        return {"error": "Failed to retrieve location with the provided data"}

    location_key = location["Key"]
    weather_data = client.get_ten_day_weather_by_location_key(location_key)

    if weather_data is None:
        return {"error": "Failed to retrieve 10-day weather forecast"}

    formatted_weather = format_ten_day_weather_response(weather_data)

    if formatted_weather is None:
        return {"error": "Failed to process weather data from API"}

    formatted_weather["latitude"] = latitude
    formatted_weather["longitude"] = longitude

    return formatted_weather
