import pandas as pd
from typing import List
from database import DatabaseCell, database
from pathlib import Path


def export_tables_to_csv(tables: List):
    data = []
    for table in tables:
        database_cell = DatabaseCell(table=table, data={})
        result = database.read(database_cell=database_cell)
        data.append(result)
    csv = []
    for item in data:
        df = pd.DataFrame(item)
        csv.append(df.to_csv())
    export_directory = Path(__file__).parent.parent.resolve() / "exports"
    export_directory.mkdir(parents=True, exist_ok=True)
    for index, csv_file in enumerate(csv):
        path = export_directory / f"{tables[index]}.csv"
        with open(str(path), "w") as f:
            f.write(csv_file)
