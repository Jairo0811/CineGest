# Configuración de Microsoft SQL Server

CineGest permite mantener SQLite para arranque local y activar SQL Server mediante variables de entorno.

## Requisitos en Windows

- Microsoft SQL Server 2022 o superior.
- SQL Server Management Studio.
- Microsoft ODBC Driver 18 for SQL Server.
- Python 3.13 y entorno virtual del proyecto.

## Instalar dependencias Python

```powershell
python -m pip install -r requirements.txt
```

## Crear el archivo local `.env`

Copiar `.env.example` como `.env`:

```powershell
Copy-Item .env.example .env
```

Para SQL Server, configurar:

```dotenv
DATABASE_ENGINE=sqlserver
DB_NAME=CineGestDb
DB_USER=sa
DB_PASSWORD=CAMBIAR_PASSWORD
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_EXTRA_PARAMS=TrustServerCertificate=yes;Encrypt=yes
```

El archivo `.env` está excluido de Git y nunca debe contenerse en commits.

## Crear la base de datos

Desde SQL Server Management Studio:

```sql
CREATE DATABASE CineGestDb;
GO
```

## Crear migraciones iniciales

Después de instalar dependencias y antes de crear datos:

```powershell
python manage.py makemigrations accounts
python manage.py migrate
```

## Crear administrador

```powershell
python manage.py createsuperuser
```

## Validar configuración

```powershell
python manage.py check
python manage.py runserver
```

Login:

```text
http://127.0.0.1:8000/accounts/login/
```

Administrador Django:

```text
http://127.0.0.1:8000/admin/
```

## Volver temporalmente a SQLite

Cambiar en `.env`:

```dotenv
DATABASE_ENGINE=sqlite
```

Esto facilita el desarrollo inicial sin eliminar la configuración profesional de SQL Server.
