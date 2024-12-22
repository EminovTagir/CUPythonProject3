import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional


load_dotenv()

@dataclass
class Config:
    accu_weather_api_key: Optional[str] = os.getenv("ACCU_WEATHER_API_KEY")

def get_config() -> Config:
    return Config()

config = get_config()
