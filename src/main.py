import argparse
import sys

from src.config import (
    CITIES,
    DATABASE_FILE,
    FORECAST_DAYS,
    LOG_FILE,
    METRICS_FILE,
    PROCESSED_WEATHER_FILE,
    RAW_WEATHER_FILE,
)
from src.extract import fetch_weather_data, save_raw_data
from src.load import load_weather_data
from src.logger import setup_logger
from src.metrics import calculate_weather_metrics, save_metrics
from src.transform import save_processed_data, transform_weather_data


def run_pipeline(forecast_days: int = FORECAST_DAYS) -> None:
    logger = setup_logger(LOG_FILE)
    logger.info("Pipeline de clima iniciado")

    weather_data = fetch_weather_data(CITIES, logger, forecast_days)
    save_raw_data(weather_data, RAW_WEATHER_FILE, logger)

    dataframe = transform_weather_data(weather_data)
    save_processed_data(dataframe, PROCESSED_WEATHER_FILE)
    logger.info("Dados tratados salvos: %s linhas", len(dataframe))

    load_weather_data(dataframe, DATABASE_FILE)
    logger.info("Dados carregados no SQLite: %s", DATABASE_FILE)

    metrics = calculate_weather_metrics(DATABASE_FILE)
    save_metrics(metrics, METRICS_FILE)
    logger.info("Métricas salvas: %s linhas", len(metrics))

    logger.info("Pipeline de clima finalizado")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ETL de clima: Open-Meteo para SQLite.")
    parser.add_argument(
        "--forecast-days",
        type=int,
        default=FORECAST_DAYS,
        choices=range(1, 17),
        metavar="1-16",
        help=f"Quantidade de dias de previsão. Padrão: {FORECAST_DAYS}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_pipeline(args.forecast_days)
    except Exception as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
