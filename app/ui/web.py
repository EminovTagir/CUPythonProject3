from flask import Blueprint, render_template, request
from typing import Any, Dict

from services.weather import (
    get_one_day_weather_by_city,
    get_one_day_weather_by_coordinates,
)

bp = Blueprint("weather", __name__)


@bp.route("/", methods=["GET", "POST"])
def route() -> Any:
    if request.method == "GET":
        return render_template("route.html")

    elif request.method == "POST":
        start_city: str = request.form.get("startCity", "")
        end_city: str = request.form.get("endCity", "")

        start_city_weather: Dict[str, Any] = get_one_day_weather_by_city(start_city)
        end_city_weather: Dict[str, Any] = get_one_day_weather_by_city(end_city)

        if "error" in start_city_weather:
            return render_template("route.html", **start_city_weather)

        if "error" in end_city_weather:
            return render_template("route.html", **end_city_weather)

        return render_template(
            "route.html",
            start_city=start_city,
            end_city=end_city,
            start_weather=start_city_weather,
            end_weather=end_city_weather,
        )
