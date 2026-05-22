from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATABASE_DIR = PROJECT_ROOT / "database"
LOG_DIR = PROJECT_ROOT / "logs"

RAW_WEATHER_FILE = RAW_DATA_DIR / "clima_raw.json"
PROCESSED_WEATHER_FILE = PROCESSED_DATA_DIR / "clima_tratado.csv"
METRICS_FILE = PROCESSED_DATA_DIR / "metricas_clima.csv"
DATABASE_FILE = DATABASE_DIR / "clima.db"
LOG_FILE = LOG_DIR / "etl_clima.log"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
PAST_DAYS = 7
FORECAST_DAYS = 7
TIMEZONE = "America/Sao_Paulo"

CITIES = [
    {"cidade": "São Paulo", "estado": "SP", "latitude": -23.5505, "longitude": -46.6333},
    {"cidade": "Rio de Janeiro", "estado": "RJ", "latitude": -22.9068, "longitude": -43.1729},
    {"cidade": "Belo Horizonte", "estado": "MG", "latitude": -19.9167, "longitude": -43.9345},
    {"cidade": "Brasília", "estado": "DF", "latitude": -15.7939, "longitude": -47.8828},
    {"cidade": "Curitiba", "estado": "PR", "latitude": -25.4296, "longitude": -49.2713},
    {"cidade": "Recife", "estado": "PE", "latitude": -8.0476, "longitude": -34.8770},
]

DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",
    "precipitation_hours",
    "wind_speed_10m_max",
]
