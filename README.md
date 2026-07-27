# 🎬 CineGest - Sistema de Gestión para Video Club

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,django,html,css,bootstrap&perline=5" />
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=vscode,git,github&perline=3" />
</p>

<p align="center">
  <strong>La solución inteligente para la gestión de Video Clubs.</strong><br>
  Desarrollado con Python, Django y SQLite, con una futura migración a Microsoft SQL Server.
</p>

---

# 📖 Descripción

**CineGest** es un sistema web orientado a la administración integral de un Video Club.

La aplicación permite gestionar tipos de artículos, géneros, idiomas, artículos, clientes, empleados y procesos de renta y devolución, centralizando las operaciones principales de un negocio dedicado al alquiler de películas, música, libros y otros recursos audiovisuales.

El proyecto se encuentra en proceso de evolución hacia una versión más moderna, segura, escalable y preparada para formar parte de un portafolio profesional.

**CineGest** forma parte de una colección de proyectos académicos desarrollados en la **Universidad APEC (UNAPEC)**, tomando como referencia el listado de proyectos propuestos por el profesor **Juan Pablo Valdez Reyes**.

---

# 🎓 Origen del Proyecto

La versión académica original fue desarrollada durante el **primer cuatrimestre de 2026** como proyecto final de la asignatura **Desarrollo de Software con Tecnología Open Source I (ISO-610)**, impartida por el profesor **Omar de la Cruz** en la **Universidad APEC (UNAPEC)**.

El proyecto original fue realizado en equipo utilizando **Python, Django y SQLite**.

La versión actual, denominada **CineGest**, toma dicho trabajo como base de inspiración y tiene como objetivo transformarlo en una solución más profesional mediante mejoras en arquitectura, experiencia de usuario, seguridad, validaciones, base de datos, reportes y nuevas funcionalidades.

Repositorio del proyecto académico original: [MDGreenCode/GestionVideoClub](https://github.com/MDGreenCode/GestionVideoClub)

---

# 👥 Equipo del Proyecto Académico Original

| Integrante | Matrícula |
|------------|-----------|
| Carlos Jesús Bobea Mejía | A00091229 |
| Mario David Pichardo Vásquez | A00114273 |
| Francis Jairo Matías Rosario | A00115261 |
| Pieranyela José Carrasco Rodríguez | A00116415 |
| Jenrry Monegro Rosario | A00116621 |

El proyecto académico original fue desarrollado por el equipo anterior. 

**Mario David Pichardo Vásquez** fue el principal creador y desarrollador de la versión original que sirve como punto de partida e inspiración para la evolución de **CineGest**.

---

# 🛠️ Stack tecnológico

## 🎨 Frontend y diseño de interfaces

<p>
  <img src="https://skillicons.dev/icons?i=html,css,bootstrap" alt="HTML, CSS y Bootstrap" />
</p>

- **HTML5:** estructura semántica de las vistas.
- **CSS3:** estilos y personalización visual.
- **Bootstrap 5:** componentes responsivos previstos para la modernización.
- **Django Templates:** renderizado de las interfaces del lado del servidor.

## ⚙️ Backend, framework y lógica de aplicación

<p>
  <img src="https://skillicons.dev/icons?i=python,django" alt="Python y Django" />
</p>

- **Python:** lenguaje principal del proyecto.
- **Django 5.2.15:** framework web.
- **Django Views:** procesamiento de solicitudes y respuestas.
- **Django Forms:** formularios y validaciones.
- **Django ORM:** acceso y persistencia de datos.
- **Arquitectura MVT:** separación entre modelos, vistas y plantillas.

## 🗄️ Base de datos y persistencia

<p>
  <img src="https://skillicons.dev/icons?i=sqlite" alt="SQLite" />
</p>

- **SQLite:** base de datos utilizada actualmente.
- **Microsoft SQL Server:** base de datos planificada para la evolución del sistema.
- **Migraciones de Django:** control de cambios del esquema de datos.

## 🧰 Herramientas de desarrollo

<p>
  <img src="https://skillicons.dev/icons?i=vscode,git,github" alt="Visual Studio Code, Git y GitHub" />
</p>

- **Visual Studio Code:** entorno de desarrollo.
- **Git:** control de versiones.
- **GitHub:** alojamiento y administración del repositorio.
- **pip:** gestión de dependencias de Python.
- **venv:** aislamiento del entorno de desarrollo.

---

# 🏗️ Arquitectura

```text
Navegador
    │
    ▼
Django URLs
    │
    ▼
Django Views
    │
    ▼
Django Forms
    │
    ▼
Django Models / ORM
    │
    ▼
SQLite
```

Arquitectura planificada:

```text
Navegador
    │
    ▼
Django
    │
    ▼
Django ORM
    │
    ▼
Microsoft SQL Server
```

El proyecto utiliza el patrón **MVT (Model-View-Template)** de Django.

---

# ✨ Funcionalidades Actuales

## 📊 Dashboard

- ✅ Total de clientes
- ✅ Total de artículos
- ✅ Total de empleados
- ✅ Total de rentas activas
- ✅ Visualización de las últimas rentas

## 📚 Gestión de Tipos de Artículos

- ✅ Listar, registrar, editar y eliminar tipos
- ✅ Activar o inactivar registros

## 🎭 Gestión de Géneros

- ✅ Listar, registrar, editar y eliminar géneros
- ✅ Activar o inactivar registros

## 🌎 Gestión de Idiomas

- ✅ Listar, registrar, editar y eliminar idiomas
- ✅ Activar o inactivar registros

## 🎬 Gestión de Artículos

- ✅ Registrar, editar y eliminar artículos
- ✅ Asociar tipo de artículo e idioma
- ✅ Administrar monto por día, días de renta y recargo tardío
- ✅ Activar o inactivar artículos

## 👤 Gestión de Clientes

- ✅ Registrar, editar y eliminar clientes
- ✅ Administrar cédula, tarjeta y límite de crédito
- ✅ Clasificar persona física o jurídica
- ✅ Activar o inactivar clientes

## 👨‍💼 Gestión de Empleados

- ✅ Registrar, editar y eliminar empleados
- ✅ Administrar cédula, tanda laboral y comisión
- ✅ Registrar fecha de ingreso
- ✅ Activar o inactivar empleados

## 🔑 Gestión de Rentas

- ✅ Registrar, editar y eliminar rentas
- ✅ Asociar empleado, cliente y artículo
- ✅ Registrar fechas, monto por día y cantidad de días
- ✅ Registrar comentarios
- ✅ Controlar estado de renta o devolución

---

# 🚧 Funcionalidades Planificadas

- 🔄 Gestión de elenco y relación elenco-artículo
- 🔄 Consultas por cliente, fecha, artículo y empleado
- 🔄 Reportes por rango de fechas y tipo de artículo
- 🔄 Exportación a PDF y Excel
- 🔄 Migración a Microsoft SQL Server
- 🔄 Inicio de sesión, roles y permisos
- 🔄 Eliminación lógica
- 🔄 Validación de cédula dominicana
- 🔄 Validaciones de negocio
- 🔄 Paginación y filtros avanzados
- 🔄 Dashboard moderno
- 🔄 Diseño responsivo con Bootstrap 5
- 🔄 Modo oscuro
- 🔄 Mensajes de confirmación
- 🔄 Auditoría de registros
- 🔄 Preparación para producción

---

# 🔐 Seguridad Planificada

## 👑 Administrador

Tendrá acceso completo a dashboard, clientes, empleados, artículos, catálogos, rentas, devoluciones, reportes, usuarios, roles y permisos.

## 👨‍💼 Empleado

Podrá consultar clientes y artículos, registrar rentas, procesar devoluciones, consultar su historial y generar comprobantes autorizados.

---

# 📂 Estructura del Proyecto

```text
CineGest
│
├── VideoClub
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── VideoClubApp
│   ├── migrations
│   ├── templates
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Los nombres internos `VideoClub` y `VideoClubApp` se mantienen temporalmente mientras se estabiliza el proyecto. Posteriormente podrán renombrarse a `CineGest` y `CineGestApp`.

---

# 🚀 Instalación

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Jairo0811/CineGest.git
```

## 2️⃣ Entrar al proyecto

```bash
cd CineGest/VideoClub
```

## 3️⃣ Crear el entorno virtual

```bash
python -m venv venv
```

## 4️⃣ Activar el entorno virtual

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
venv\Scripts\activate
```

### Linux o macOS

```bash
source venv/bin/activate
```

## 5️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6️⃣ Aplicar migraciones

```bash
python manage.py migrate
```

## 7️⃣ Crear un superusuario

```bash
python manage.py createsuperuser
```

## 8️⃣ Ejecutar el servidor

```bash
python manage.py runserver
```

Aplicación:

```text
http://127.0.0.1:8000/
```

Panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

---

# ⚙️ Configuración Actual

Actualmente el proyecto utiliza:

```text
Python
Django 5.2.15
SQLite
```

La base de datos se encuentra configurada en `VideoClub/settings.py`. La migración a Microsoft SQL Server será realizada en una etapa posterior.

---

# 📊 Estado del Proyecto

| Módulo | Estado |
|--------|:------:|
| 📊 Dashboard básico | ✅ |
| 📚 Tipos de artículos | ✅ |
| 🎭 Géneros | ✅ |
| 🌎 Idiomas | ✅ |
| 🎬 Artículos | ✅ |
| 👤 Clientes | ✅ |
| 👨‍💼 Empleados | ✅ |
| 🔑 Rentas | ✅ |
| 🔄 Devoluciones | ✅ |
| 🎭 Elenco | 🚧 |
| 🔍 Consultas avanzadas | 🚧 |
| 📄 Reportes | 🚧 |
| 🔐 Autenticación | 🚧 |
| 👥 Roles y permisos | 🚧 |
| 🛢️ SQL Server | 🚧 |
| 🎨 Interfaz moderna | 🚧 |
| 📱 Diseño responsivo | 🚧 |

---

# 🗺️ Hoja de Ruta

| Funcionalidad | Proyecto Académico | CineGest |
|---------------|:------------------:|:--------:|
| CRUD de tipos de artículos | ✅ | ✅ |
| CRUD de géneros | ✅ | ✅ |
| CRUD de idiomas | ✅ | ✅ |
| CRUD de artículos | ✅ | ✅ |
| CRUD de clientes | ✅ | ✅ |
| CRUD de empleados | ✅ | ✅ |
| Gestión de rentas | ✅ | ✅ |
| Gestión de devoluciones | ✅ | ✅ |
| Gestión de elenco | ❌ | 🚧 |
| Consultas por criterios | ❌ | 🚧 |
| Reportes profesionales | ❌ | 🚧 |
| Dashboard moderno | ❌ | 🚧 |
| Bootstrap 5 | ❌ | 🚧 |
| Microsoft SQL Server | ❌ | 🚧 |
| Login | ❌ | 🚧 |
| Roles y permisos | ❌ | 🚧 |
| Reportes PDF | ❌ | 🚧 |
| Exportación a Excel | ❌ | 🚧 |
| Variables de entorno | ❌ | 🚧 |
| Auditoría | ❌ | 🚧 |

---

# 🔄 Evolución del Proyecto

## Fase 1 — Preparación

- Configuración de Git
- Repositorio privado
- Archivo `.gitignore`
- Archivo `requirements.txt`
- Variables de entorno
- Configuración regional

## Fase 2 — Calidad y Arquitectura

- Refactorización de vistas
- Reducción de código duplicado
- Validaciones
- Eliminación lógica
- Manejo de errores
- Pruebas automatizadas

## Fase 3 — Base de Datos

- Migración a SQL Server
- Restricciones e índices
- Integridad referencial
- Datos iniciales

## Fase 4 — Seguridad

- Login
- Roles
- Permisos
- Auditoría
- Protección de operaciones sensibles

## Fase 5 — Interfaz

- Bootstrap 5
- Dashboard moderno
- Diseño responsivo
- Modo oscuro
- Búsquedas
- Paginación
- Confirmaciones

## Fase 6 — Reportes y Producción

- PDF
- Excel
- Reportes por criterios
- Documentación
- Pruebas
- Despliegue

---

# 👨‍💻 Autor y Mantenimiento

**Francis Jairo Matías Rosario**

🎓 Universidad APEC (UNAPEC)

📚 Ingeniería de Software

🆔 Matrícula: **A00115261**

💼 Versión evolucionada con **Python, Django y Microsoft SQL Server** como parte del portafolio académico y profesional.

---

# 🙏 Créditos

- **Universidad:** Universidad APEC (UNAPEC)
- **Asignatura:** Desarrollo de Software con Tecnología Open Source I
- **Código:** ISO-610
- **Profesor de la asignatura:** Omar de la Cruz
- **Referencia académica:** listado de proyectos propuestos por el profesor Juan Pablo Valdez Reyes
- **Desarrollador principal del proyecto académico original:** Mario David Pichardo Vásquez
- **Repositorio del proyecto académico original:** [MDGreenCode/GestionVideoClub](https://github.com/MDGreenCode/GestionVideoClub)
- **Evolución y mantenimiento de CineGest:** Francis Jairo Matías Rosario

---

<p align="center">
  Desarrollado con ❤️ por <strong>Francis Jairo Matías Rosario</strong>
</p>