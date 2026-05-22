import sqlite3
from pathlib import Path

import pandas as pd


def load_weather_data(dataframe: pd.DataFrame, database_file: Path) -> None:
    database_file.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_file) as connection:
        dataframe.to_sql("clima_diario", connection, if_exists="replace", index=False)
