# Despliegue de CineGest

## Requisitos

- Docker Desktop o Docker Engine con Compose.
- Una contraseña robusta para la cuenta `sa` de SQL Server.
- Variables de entorno de producción.

## Variables mínimas

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-value
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=sqlserver
DB_NAME=CineGestDb
DB_USER=sa
DB_PASSWORD=replace-with-a-strong-password
DB_HOST=sqlserver
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_EXTRA_PARAMS=TrustServerCertificate=yes;Encrypt=yes
```

No se debe versionar el archivo `.env`.

## Docker Compose

```bash
docker compose build
docker compose up -d
```

La aplicación queda expuesta en:

```text
http://localhost:8000
```

SQL Server queda expuesto localmente en el puerto `1433` para tareas administrativas.

## Primer usuario administrador

Después de aplicar las migraciones:

```bash
docker compose exec web python manage.py createsuperuser
```

## Verificaciones

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py check --deploy
docker compose exec web python manage.py test
```

## Producción

Antes de exponer el sistema en Internet:

- Usar HTTPS detrás de un reverse proxy o balanceador.
- Definir `DJANGO_DEBUG=False`.
- Configurar `DJANGO_ALLOWED_HOSTS` únicamente con dominios válidos.
- No publicar SQL Server directamente a Internet.
- Aplicar copias de seguridad periódicas a `CineGestDb`.
- Rotar secretos y contraseñas.
- Mantener imágenes Docker y dependencias actualizadas.
