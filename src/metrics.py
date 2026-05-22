import sqlite3
from pathlib import Path

import pandas as pd


METRICS_QUERY = """
SELECT
    cidade,
    estado,
    COUNT(*) AS dias_analisados,
    ROUND(AVG(temperatura_media_c), 2) AS temperatura_media_c,
    ROUND(MAX(temperatura_maxima_c), 2) AS maior_temperatura_c,
    ROUND(MIN(temperatura_minima_c), 2) AS menor_temperatura_c,
    ROUND(SUM(precipitacao_mm), 2) AS precipitacao_total_mm,
    SUM(CASE WHEN precipitacao_mm > 0 THEN 1 ELSE 0 END) AS dias_com_chuva
FROM clima_diario
GROUP BY cidade, estado
ORDER BY temperatura_media_c DESC;
"""


def calculate_weather_metrics(database_file: Path) -> pd.DataFrame:
    with sqlite3.connect(database_file) as connection:
        return pd.read_sql_query(METRICS_QUERY, connection)


def save_metrics(dataframe: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_file, index=False, encoding="utf-8")
