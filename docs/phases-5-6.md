# Fases 5 y 6 — Cierre funcional de CineGest

## Fase 5 — Rentas, devoluciones y dashboard

### Rentas

- Una renta contiene uno o varios `DetalleRenta`.
- Solo se permiten clientes y empleados activos.
- Solo pueden rentarse unidades de inventario en estado `DISPONIBLE`.
- La creación usa una transacción de base de datos y bloqueo `select_for_update` para reducir condiciones de carrera.
- El precio y los días de renta se copian al detalle para conservar el histórico.
- Al registrar una renta, cada unidad pasa a `RENTADO`.

### Devoluciones

- Cada detalle puede devolverse de manera independiente.
- Una renta puede quedar `PARCIAL` si aún existen unidades pendientes.
- Cuando todas las unidades se devuelven, la renta pasa a `DEVUELTA`.
- El recargo se calcula según los días de atraso y la tarifa tardía vigente en el artículo.
- Una unidad devuelta vuelve a `DISPONIBLE`.

### Dashboard

Incluye indicadores de clientes, empleados, artículos, inventario disponible, rentas abiertas, recargos, últimas rentas y artículos más rentados.

## Fase 6 — Reportes, calidad y producción

### Reportes

- Filtros por rango de fechas y estado.
- Exportación de rentas a Excel mediante OpenPyXL.
- Exportación de rentas a PDF mediante ReportLab.

### Calidad

- Pruebas del servicio de renta y devolución.
- Pipeline de GitHub Actions con Python 3.13.
- Generación y aplicación de migraciones en CI.
- `manage.py check`, pruebas y `collectstatic` obligatorios en CI.

### Producción

- Gunicorn como servidor WSGI.
- WhiteNoise para archivos estáticos.
- Cookies seguras y HSTS al ejecutar con `DEBUG=False`.
- Dockerfile con Microsoft ODBC Driver 18 para conectividad con SQL Server.

## Validación de cierre

Antes del release estable se deben cumplir todos estos puntos:

1. Versionar las migraciones generadas por Django.
2. CI en verde.
3. Validar una renta de varios artículos.
4. Validar devolución parcial y total.
5. Validar recargo tardío.
6. Validar exportaciones PDF y Excel.
7. Validar conexión con Microsoft SQL Server.
8. Ejecutar `python manage.py check --deploy` con configuración de producción.
