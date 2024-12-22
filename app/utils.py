from typing import Dict, Optional, Any, List

def check_bad_weather(data: Dict[str, Any]) -> str:
    temperature = data["temperature"]
    wind_speed = data["wind_speed"]
    rain_probability = data["rain_probability"]

    if temperature < 0 or temperature > 35 or wind_speed > 50 or rain_probability > 70:
        return "Unfavorable"

    return "Favorable"


def format_weather_response(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        return {
            "temperature": data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"],
            "humidity": data["DailyForecasts"][0]["Day"]["RelativeHumidity"]["Average"],
            "wind_speed": data["DailyForecasts"][0]["Day"]["Wind"]["Speed"]["Value"],
            "rain_probability": data["DailyForecasts"][0]["Day"]["PrecipitationProbability"],
        }
    except KeyError:
        return None


def format_five_day_weather_response(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    forecasts = data.get("DailyForecasts", [])
    formatted_data: List[Dict[str, Any]] = []

    for day in forecasts:
        try:
            day_data = {
                "date": day["Date"],
                "temperature": day["Temperature"]["Maximum"]["Value"],
                "humidity": day["Day"]["RelativeHumidity"]["Average"],
                "wind_speed": day["Day"]["Wind"]["Speed"]["Value"],
                "rain_probability": day["Day"]["PrecipitationProbability"],
            }
            day_data["weather_conditions"] = check_bad_weather(day_data)
            formatted_data.append(day_data)
        except KeyError:
            return None

    return {"data": formatted_data}


def format_ten_day_weather_response(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    forecasts = data.get("DailyForecasts", [])[:10]
    formatted_data: List[Dict[str, Any]] = []

    for day in forecasts:
        try:
            day_data = {
                "date": day["Date"],
                "temperature": day["Temperature"]["Maximum"]["Value"],
                "humidity": day["Day"]["RelativeHumidity"]["Average"],
                "wind_speed": day["Day"]["Wind"]["Speed"]["Value"],
                "rain_probability": day["Day"]["PrecipitationProbability"],
            }
            day_data["weather_conditions"] = check_bad_weather(day_data)
            formatted_data.append(day_data)
        except KeyError:
            return None

    return {"data": formatted_data}
