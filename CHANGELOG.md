# Changelog

Todos los cambios relevantes de CineGest se documentan en este archivo.

## [1.0.0] - Pendiente de publicación

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
- Docker, Gunicorn, WhiteNoise y Microsoft ODBC Driver 18.

### Seguridad

- Secretos fuera del código mediante `.env`.
- Protección CSRF de Django.
- Autenticación obligatoria en las vistas operativas.
- Cookies seguras y HSTS cuando `DEBUG=False`.
- Operaciones de renta y devolución encapsuladas en transacciones de base de datos.
