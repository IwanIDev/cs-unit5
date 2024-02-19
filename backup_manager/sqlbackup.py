from database import database
from pathlib import Path
import logging


def sql_backup(path: Path) -> None:
    backup_path = path / 'backup.sql'
    backup = database.backup()
    with open(backup_path, 'w') as f:
        f.write(backup)
