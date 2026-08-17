# Modelo de dominio de CineGest

Este documento define la base funcional y relacional de CineGest antes de implementar los módulos de negocio.

## Objetivos

- Permitir una renta con uno o varios artículos.
- Mantener trazabilidad de clientes, empleados, usuarios y operaciones.
- Evitar eliminaciones físicas de información de negocio.
- Separar catálogos, inventario y transacciones.
- Preparar el proyecto para Microsoft SQL Server.

## Entidades principales

### Usuario
Modelo personalizado de Django para autenticación. Roles iniciales: `ADMINISTRADOR` y `EMPLEADO`.

### TipoArticulo
Catálogo para clasificar Películas, CD de música, Libros u otros medios.

### Genero
Catálogo de géneros relacionados con artículos.

### Idioma
Catálogo de idiomas disponibles.

### PersonaElenco
Representa actores, directores u otros participantes.

### Articulo
Contenido administrado por CineGest. Incluye título, tipo, idioma, precio por día, días de renta, recargo tardío, descripción y estado.

Relaciones principales:
- TipoArticulo 1:N Articulo
- Idioma 1:N Articulo
- Articulo N:M Genero
- Articulo N:M PersonaElenco mediante ArticuloElenco

### ArticuloElenco
Tabla intermedia para guardar el rol de una persona dentro de un artículo, por ejemplo Actor, Director, Productor, Autor o Intérprete.

### InventarioItem
Representa cada unidad física disponible para renta. Estados: `DISPONIBLE`, `RENTADO`, `MANTENIMIENTO`, `RETIRADO`.

### Cliente
Incluye nombre, cédula/RNC, tipo de persona, email, teléfono, límite de crédito y estado.

Reglas:
- Cédula/RNC única cuando sea informada.
- Un cliente inactivo no puede iniciar nuevas rentas.
- El límite de crédito no puede ser negativo.

### Empleado
Incluye usuario asociado, nombre, cédula, tanda laboral, comisión, fecha de ingreso y estado.

### Renta
Cabecera de una transacción. Estados: `ABIERTA`, `PARCIALMENTE_DEVUELTA`, `DEVUELTA`, `CANCELADA`.

Una renta pertenece a un cliente y a un empleado, y contiene uno o varios detalles.

### DetalleRenta
Representa cada unidad física incluida en una renta. Conserva el precio utilizado en la transacción, cantidad de días, fechas de devolución y recargos.

### Auditoria
Registra usuario, acción, entidad, identificador, datos anteriores/nuevos, IP y fecha.

## Relaciones principales

```text
Usuario ─────── 0..1 Empleado
                     │
Cliente 1 ────────── N Renta 1 ────────── N DetalleRenta N ────────── 1 InventarioItem
                                                                             │
                                                                             N
                                                                             │
                                                                             1
                                                                          Articulo
                                                                         /   |   \
                                                               TipoArticulo Idioma Genero

Articulo N ────────── N PersonaElenco mediante ArticuloElenco
```

## Reglas de negocio iniciales

1. Toda renta debe tener un cliente activo y un empleado activo.
2. Una renta debe contener al menos un detalle.
3. Solo unidades `DISPONIBLE` pueden rentarse.
4. El precio se copia al detalle para conservar el histórico.
5. Los recargos se calculan con fecha esperada, fecha real y tarifa tardía.
6. Las transacciones no se eliminan físicamente.
7. Catálogos y maestros usan activación/inactivación.
8. Operaciones sensibles generan auditoría.
9. Zona horaria: `America/Santo_Domingo`.
10. Secretos y credenciales se gestionan mediante variables de entorno.

## Apps Django previstas

```text
apps/
├── core
├── accounts
├── dashboard
├── catalogos
├── clientes
├── empleados
├── articulos
├── rentas
└── reportes
```

## Criterio de cierre de Fase 1

- Modelo de dominio documentado.
- Estructura modular definida.
- Base reutilizable para timestamps y eliminación lógica.
- Usuario personalizado definido antes de las migraciones de negocio.
