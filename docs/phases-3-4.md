# Fases 3 y 4 — Módulos de negocio

Este bloque implementa el modelo funcional de catálogos, clientes, empleados, artículos, inventario y elenco sobre la arquitectura definida en las Fases 1 y 2.

## Fase 3 — Catálogos, clientes y empleados

### Catálogos
- `TipoArticulo`
- `Genero`
- `Idioma`
- Activación/inactivación heredada de `BaseCatalogModel`.
- Administración mediante Django Admin.

### Clientes
- Persona física o jurídica.
- Cédula/RNC única.
- Email y teléfono opcionales.
- Límite de crédito no negativo.
- Activación/inactivación sin eliminación física.

### Empleados
- Asociación opcional uno-a-uno con el usuario de Django.
- Cédula única.
- Tanda laboral.
- Comisión entre 0 % y 100 %.
- Fecha de ingreso.
- Activación/inactivación.

## Fase 4 — Artículos, inventario y elenco

### Artículos
- Tipo de artículo e idioma protegidos ante eliminación.
- Relación N:M con géneros.
- Tarifas de renta y recargo no negativas.
- Días de renta configurables.

### Elenco
- Personas con nombre legal y nombre artístico opcional.
- Relación N:M con artículos mediante `ArticuloElenco`.
- Roles: actor/actriz, director/a, productor/a, autor/a, intérprete u otro.
- Restricción única por artículo, persona y rol.

### Inventario
Cada unidad física se registra mediante `InventarioItem` con código único y uno de los estados:

- `DISPONIBLE`
- `RENTADO`
- `MANTENIMIENTO`
- `RETIRADO`

Esta separación permite que un mismo título tenga múltiples copias físicas con disponibilidad independiente.

## Validación local pendiente

Después de actualizar la rama:

```powershell
python -m pip install -r requirements.txt
python manage.py makemigrations catalogos clientes empleados articulos
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

Validar además los CRUD administrativos en `/admin/` para catálogos, clientes, empleados, artículos, elenco e inventario.

## Criterio de cierre

Las fases se consideran cerradas cuando:

1. `makemigrations` no genera errores.
2. `migrate` se aplica correctamente en SQLite y posteriormente SQL Server.
3. `python manage.py check` no reporta incidencias.
4. Los modelos pueden crearse y editarse desde Django Admin.
5. Las restricciones de unicidad y rangos numéricos funcionan como se espera.
