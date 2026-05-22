import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from src.config import DAILY_VARIABLES, FORECAST_DAYS, OPEN_METEO_URL, TIMEZONE


def build_weather_url(city: dict, forecast_days: int = FORECAST_DAYS) -> str:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": TIMEZONE,
        "forecast_days": forecast_days,
    }
    return f"{OPEN_METEO_URL}?{urlencode(params)}"


def fetch_weather_for_city(
    city: dict,
    logger: logging.Logger,
    forecast_days: int = FORECAST_DAYS,
) -> dict:
    city_name = city["cidade"]
    logger.info("Buscando dados de clima: %s", city_name)

    url = build_weather_url(city, forecast_days)
    with urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    payload["cidade"] = city["cidade"]
    payload["estado"] = city["estado"]
    payload["latitude_consulta"] = city["latitude"]
    payload["longitude_consulta"] = city["longitude"]
    payload["data_coleta"] = datetime.now().replace(microsecond=0).isoformat()
    return payload


def fetch_weather_data(
    cities: list[dict],
    logger: logging.Logger,
    forecast_days: int = FORECAST_DAYS,
) -> list[dict]:
    weather_data = []

    for city in cities:
        weather_data.append(fetch_weather_for_city(city, logger, forecast_days))

    logger.info("Extração concluída: %s cidades consultadas", len(weather_data))
    return weather_data


def save_raw_data(weather_data: list[dict], output_file: Path, logger: logging.Logger) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(weather_data, file, ensure_ascii=False, indent=2)

    logger.info("Arquivo raw salvo: %s", output_file)
