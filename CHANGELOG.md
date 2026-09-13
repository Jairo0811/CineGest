# Changelog

Todos los cambios relevantes de CineGest se documentan en este archivo.

## [1.0.0] - 2026-09-13

### Añadido

- Arquitectura modular en Django.
- Usuario personalizado con roles Administrador y Empleado.
- Configuración mediante variables de entorno.
- Compatibilidad con SQLite para desarrollo y Microsoft SQL Server para la versión profesional.
- Catálogos de tipos de artículos, géneros e idiomas.
- Gestión de clientes y empleados.
- Gestión de artículos, elenco e inventario por unidad física.
- Rentas con múltiples artículos.
- Devoluciones parciales y totales con recargos tardíos.
- Dashboard ejecutivo.
- Reportes filtrables con exportación PDF y Excel.
- Interfaz Bootstrap responsiva para dashboard, rentas y reportes.
- Pruebas automatizadas del flujo principal.
- GitHub Actions CI.
- Validación de integración continua sobre SQL Server 2022 con Microsoft ODBC Driver 18.
- Pruebas HTTP y de generación de archivos para el módulo de reportes.
- Docker, Gunicorn, WhiteNoise y Microsoft ODBC Driver 18.

### Cambiado

- El módulo de reportes se divide en `views`, servicios de consulta y exportadores para reducir acoplamiento y facilitar mantenimiento.
- La documentación de despliegue incorpora variables y criterios explícitos de producción.
- El pipeline CI separa la validación rápida con SQLite de la integración real con SQL Server 2022.
- Django 5.2 LTS se actualiza a `5.2.17`, último patch de seguridad disponible al momento del congelamiento.

### Corregido

- Eliminados marcadores de conflicto Git que habían quedado versionados en `apps/reportes/views.py`.
- Los filtros de fecha inválidos en reportes dejan de propagarse directamente al ORM.
- `staticfiles/` generado por `collectstatic` queda excluido del control de versiones.

### Seguridad

- Secretos fuera del código mediante `.env`.
- Protección CSRF de Django.
- Autenticación obligatoria en las vistas operativas.
- Cookies seguras y HSTS cuando `DEBUG=False`.
- Operaciones de renta y devolución encapsuladas en transacciones de base de datos.
- Bloqueo del arranque en producción cuando se conserva una clave secreta de desarrollo o no existen hosts permitidos.
- Soporte de `DJANGO_CSRF_TRUSTED_ORIGINS` y redirección HTTPS configurable.
- `SECURE_CONTENT_TYPE_NOSNIFF`, política de referrer estricta y protección contra framing.

### Cierre de versión

`v1.0.0` queda declarada como línea base estable de portafolio tras completar en verde la validación SQLite, la integración SQL Server 2022 y `django check --deploy`. A partir de este punto, CineGest queda congelado para nuevas funcionalidades y solo recibirá correcciones necesarias, mantenimiento técnico y actualizaciones de seguridad.
