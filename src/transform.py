from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "cidade",
    "estado",
    "data",
    "temperatura_maxima_c",
    "temperatura_minima_c",
    "temperatura_media_c",
    "precipitacao_mm",
    "tipo_dado",
    "horas_chuva",
    "vento_maximo_kmh",
    "data_coleta",
]


def transform_city_weather(payload: dict) -> pd.DataFrame:
    daily = payload.get("daily", {})

    dataframe = pd.DataFrame(
        {
            "data": daily.get("time", []),
            "temperatura_maxima_c": daily.get("temperature_2m_max", []),
            "temperatura_minima_c": daily.get("temperature_2m_min", []),
            "temperatura_media_c": daily.get("temperature_2m_mean", []),
            "precipitacao_mm": daily.get("precipitation_sum", []),
            "horas_chuva": daily.get("precipitation_hours", []),
            "vento_maximo_kmh": daily.get("wind_speed_10m_max", []),
        }
    )

    dataframe["cidade"] = payload["cidade"]
    dataframe["estado"] = payload["estado"]
    dataframe["data_coleta"] = payload["data_coleta"]
    data_coleta = pd.to_datetime(payload["data_coleta"], errors="coerce").date()
    datas = pd.to_datetime(dataframe["data"], errors="coerce").dt.date
    dataframe["tipo_dado"] = datas.apply(
        lambda data: "historico" if pd.notna(data) and data < data_coleta else "previsao"
    )
    return dataframe[OUTPUT_COLUMNS]


def transform_weather_data(weather_data: list[dict]) -> pd.DataFrame:
    frames = [transform_city_weather(payload) for payload in weather_data]
    if not frames:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    dataframe = pd.concat(frames, ignore_index=True)
    dataframe["data"] = pd.to_datetime(dataframe["data"], errors="coerce").dt.date
    dataframe["data_coleta"] = pd.to_datetime(dataframe["data_coleta"], errors="coerce")

    numeric_columns = [
        "temperatura_maxima_c",
        "temperatura_minima_c",
        "temperatura_media_c",
        "precipitacao_mm",
        "horas_chuva",
        "vento_maximo_kmh",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    dataframe = dataframe.dropna(subset=["data", "temperatura_media_c"])
    dataframe[numeric_columns] = dataframe[numeric_columns].round(2)
    dataframe = dataframe.sort_values(["cidade", "data"]).reset_index(drop=True)
    return dataframe


def save_processed_data(dataframe: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_file, index=False, encoding="utf-8")
