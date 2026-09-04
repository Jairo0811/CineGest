# Fase 7 — Production Validation & Portfolio Release

La Fase 7 cierra CineGest como entrega profesional de portafolio sobre la base funcional de las Fases 1–6.

## Objetivos

- Validar automáticamente la aplicación sobre Microsoft SQL Server 2022.
- Resolver deuda técnica en el módulo de reportes.
- Endurecer la configuración de producción.
- Ampliar la cobertura automatizada de los endpoints de reportes.
- Dejar definido el criterio de cierre para `v1.0.0`.

## 1. Corrección crítica de reportes

Se detectaron marcadores de conflicto Git sin resolver en `apps/reportes/views.py`. El módulo fue reemplazado por una estructura separada:

```text
apps/reportes/
├── exporters.py   # PDF y Excel
├── services.py    # filtros y consultas
├── tests.py       # pruebas HTTP y exportaciones
├── urls.py
└── views.py       # controladores HTTP delgados
```

El cambio elimina lógica de presentación y generación de archivos del controlador HTTP.

## 2. Validación SQL Server en CI

GitHub Actions ejecuta ahora dos trabajos independientes:

1. `SQLite validation`
   - migraciones;
   - `django check`;
   - suite completa;
   - `collectstatic`.

2. `SQL Server 2022 integration`
   - contenedor oficial de SQL Server 2022;
   - Microsoft ODBC Driver 18;
   - espera activa hasta disponibilidad de la base de datos;
   - verificación de migraciones;
   - migraciones reales contra SQL Server;
   - `django check`;
   - suite completa sobre SQL Server;
   - `django check --deploy` con configuración de producción.

Esta validación sustituye el estado anterior de «SQL Server preparado, validación física pendiente» por una comprobación reproducible en CI.

## 3. Hardening de producción

Cuando `DJANGO_DEBUG=False`, CineGest exige:

- `DJANGO_SECRET_KEY` explícito, robusto y distinto de los valores de desarrollo;
- al menos un valor en `DJANGO_ALLOWED_HOSTS`.

También se incorporan:

- `DJANGO_CSRF_TRUSTED_ORIGINS`;
- `DJANGO_SECURE_SSL_REDIRECT`;
- cookies de sesión seguras y `HttpOnly`;
- HSTS en producción;
- `SECURE_CONTENT_TYPE_NOSNIFF`;
- `strict-origin-when-cross-origin` como política de referrer;
- `X_FRAME_OPTIONS = DENY`.

## 4. Cobertura adicional

La suite de reportes valida:

- autenticación obligatoria;
- renderizado del índice;
- filtro por estado;
- tolerancia a fechas inválidas;
- generación XLSX válida;
- generación PDF válida.

## 5. Criterio de cierre de `v1.0.0`

La versión `v1.0.0` puede declararse estable cuando el PR de esta fase cumpla simultáneamente:

- CI SQLite verde;
- CI SQL Server 2022 verde;
- `check --deploy` sin errores bloqueantes;
- ausencia de marcadores de conflicto en código versionado;
- documentación de despliegue actualizada;
- PR fusionado a `main`.

Después de este cierre, CineGest se considera un proyecto académico/profesional terminado y mantenido principalmente con fines de portafolio, correcciones y actualizaciones de seguridad.
