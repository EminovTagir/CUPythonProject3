import logging
import requests
from typing import Any, Dict, Optional
from config import config


class AccuWeatherClient:
    def __init__(self) -> None:
        self.api_key: str = config.accu_weather_api_key
        self.base_url: str = "http://dataservice.accuweather.com/"

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        url: str = f"{self.base_url}{endpoint}"
        params = params or {}
        params["apikey"] = self.api_key
        try:
            response: requests.Response = requests.get(url, params=params)
            logging.info(f"Request to {response.url}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.info(f"Request error: {e}")
            return None

    def get_location_by_position(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        endpoint: str = "locations/v1/cities/geoposition/search"
        params: Dict[str, Any] = {"q": f"{latitude},{longitude}"}

        result: Optional[Dict[str, Any]] = self._make_request(endpoint, params)
        logging.info("Location obtained by geoposition")
        return result

    def get_location_by_search(self, search: str) -> Optional[Dict[str, Any]]:
        endpoint: str = "locations/v1/cities/search"
        params: Dict[str, Any] = {"q": search}

        result: Optional[Dict[str, Any]] = self._make_request(endpoint, params)
        logging.info("Location obtained by search")
        return result

    def get_one_day_weather_by_location_key(self, location_key: str) -> Optional[Dict[str, Any]]:
        endpoint: str = f"forecasts/v1/daily/1day/{location_key}"
        params: Dict[str, Any] = {"details": True, "metric": True}

        result: Optional[Dict[str, Any]] = self._make_request(endpoint, params)
        logging.info("Weather obtained by location key")
        return result

    def get_five_day_weather_by_location_key(self, location_key: str) -> Optional[Dict[str, Any]]:
        endpoint: str = f"forecasts/v1/daily/5day/{location_key}"
        params: Dict[str, Any] = {"details": True, "metric": True}

        result: Optional[Dict[str, Any]] = self._make_request(endpoint, params)
        logging.info("Weather obtained by location key")
        return result

    def get_ten_day_weather_by_location_key(self, location_key: str) -> Optional[Dict[str, Any]]:
        endpoint: str = f"forecasts/v1/daily/10day/{location_key}"
        params: Dict[str, Any] = {"details": True, "metric": True}

        result: Optional[Dict[str, Any]] = self._make_request(endpoint, params)
        logging.info("Weather obtained by location key")
        return result
