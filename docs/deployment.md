# Despliegue de CineGest

## Requisitos

- Docker Desktop o Docker Engine con Compose.
- Una contraseña robusta para la cuenta `sa` de SQL Server.
- Variables de entorno de producción.
- HTTPS mediante reverse proxy o balanceador cuando el servicio sea público.

## Variables mínimas

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-value-at-least-32-characters
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=cinegest.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://cinegest.example.com
DJANGO_SECURE_SSL_REDIRECT=True
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

Cuando `DJANGO_DEBUG=False`, CineGest rechaza el arranque si `DJANGO_SECRET_KEY` conserva un valor de desarrollo o si `DJANGO_ALLOWED_HOSTS` está vacío.

## Docker Compose

```bash
docker compose build
docker compose up -d
```

En desarrollo local la aplicación queda expuesta en:

```text
http://localhost:8000
```

El `docker-compose.yml` publica SQL Server en el puerto `1433` para facilitar tareas locales. En producción se recomienda eliminar ese mapeo de puertos y permitir acceso a SQL Server únicamente desde la red interna de la aplicación.

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

## Validación automatizada de SQL Server

La integración continua incluye un trabajo independiente con SQL Server 2022 y Microsoft ODBC Driver 18. Ese trabajo:

1. inicia una instancia limpia de SQL Server;
2. espera hasta que la conexión esté disponible;
3. verifica que no existan migraciones pendientes de generar;
4. ejecuta las migraciones;
5. ejecuta `python manage.py check`;
6. ejecuta toda la suite de pruebas sobre SQL Server;
7. ejecuta `python manage.py check --deploy` con `DJANGO_DEBUG=False`.

Un cambio no debe considerarse listo para producción si falla cualquiera de las dos rutas de CI: SQLite o SQL Server.

## Producción

Antes de exponer el sistema en Internet:

- Usar HTTPS detrás de un reverse proxy o balanceador.
- Definir `DJANGO_DEBUG=False`.
- Utilizar una clave `DJANGO_SECRET_KEY` aleatoria y exclusiva del entorno.
- Configurar `DJANGO_ALLOWED_HOSTS` únicamente con dominios válidos.
- Configurar `DJANGO_CSRF_TRUSTED_ORIGINS` con orígenes HTTPS explícitos.
- Mantener `DJANGO_SECURE_SSL_REDIRECT=True` salvo que la terminación TLS requiera una configuración equivalente en infraestructura.
- No publicar SQL Server directamente a Internet.
- Aplicar copias de seguridad periódicas a `CineGestDb`.
- Rotar secretos y contraseñas.
- Mantener imágenes Docker y dependencias actualizadas.
