import os
import re
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def _env_bool(name, default=False):
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


def _wait_for_sqlserver():
    import pyodbc

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "1433")
    user = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "CineGestDb")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    extra_params = os.getenv("DB_EXTRA_PARAMS", "TrustServerCertificate=yes;Encrypt=yes")
    create_if_missing = _env_bool("DB_CREATE_IF_MISSING", False)

    if not re.fullmatch(r"[A-Za-z0-9_-]+", database):
        raise RuntimeError("DB_NAME contiene caracteres no permitidos para el bootstrap seguro.")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host},{port};"
        "DATABASE=master;"
        f"UID={user};PWD={password};"
        f"{extra_params}"
    )

    for attempt in range(30):
        try:
            with pyodbc.connect(connection_string, timeout=3, autocommit=True) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()

                cursor.execute("SELECT DB_ID(?)", database)
                database_id = cursor.fetchone()[0]

                if database_id is None and create_if_missing:
                    cursor.execute(f"CREATE DATABASE [{database}]")
                    cursor.execute("SELECT DB_ID(?)", database)
                    database_id = cursor.fetchone()[0]

                if database_id is None:
                    print(
                        f"SQL Server disponible, pero la base '{database}' no existe "
                        "y DB_CREATE_IF_MISSING está deshabilitado."
                    )
                else:
                    print(f"SQL Server y base '{database}' disponibles.")
                    return
        except pyodbc.Error as exc:
            print(f"Esperando SQL Server ({attempt + 1}/30): {exc}")

        time.sleep(2)

    print("No fue posible preparar la conexión con SQL Server.")
    sys.exit(1)


def _wait_for_django_database():
    import django
    from django.db import connections
    from django.db.utils import OperationalError

    django.setup()

    for attempt in range(30):
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
            print("Base de datos disponible para Django.")
            return
        except OperationalError as exc:
            print(f"Esperando base de datos Django ({attempt + 1}/30): {exc}")
            time.sleep(2)

    print("No fue posible conectar Django a la base de datos.")
    sys.exit(1)


if os.getenv("DATABASE_ENGINE", "sqlite").lower() == "sqlserver":
    _wait_for_sqlserver()

_wait_for_django_database()
