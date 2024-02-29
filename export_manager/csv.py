import pandas as pd
from typing import List
from database import DatabaseCell, database
from pathlib import Path


def export_tables_to_csv(tables: List, path: Path):
    path.resolve()
    data = []
    for table in tables:
        database_cell = DatabaseCell(table=table, data={})
        result = database.read(database_cell=database_cell)
        data.append(result)
    csv = []
    for item in data:
        df = pd.DataFrame(item)
        csv.append(df.to_csv())
    for index, csv_file in enumerate(csv):
        file_path = path / f"{tables[index]}.csv"
        with open(str(file_path), "w") as f:
            f.write(csv_file)
