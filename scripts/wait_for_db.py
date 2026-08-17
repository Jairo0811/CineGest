import os
import sys
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
from django.db import connections
from django.db.utils import OperationalError


django.setup()

for attempt in range(30):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
        print("Base de datos disponible.")
        sys.exit(0)
    except OperationalError as exc:
        print(f"Esperando base de datos ({attempt + 1}/30): {exc}")
        time.sleep(2)

print("No fue posible conectar a la base de datos.")
sys.exit(1)
