from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8")

anchor = '''Vistos en conjunto, ambos proyectos documentan una experiencia paralela con el mismo docente en dos líneas complementarias del plan de estudios: **tecnología propietaria** y **tecnología open source**. Cada repositorio conserva su identidad, equipo y alcance académico original, y su relación se documenta exclusivamente como continuidad docente.

**Mario David Pichardo Vásquez** fue el principal creador y desarrollador de la versión original que sirve como punto de partida e inspiración para la evolución de **CineGest**.
'''

replacement = '''Vistos en conjunto, ambos proyectos documentan una experiencia paralela con el mismo docente en dos líneas complementarias del plan de estudios: **tecnología propietaria** y **tecnología open source**. Cada repositorio conserva su identidad, equipo y alcance académico original, y su relación se documenta exclusivamente como continuidad docente.

### 🏫 Cruce institucional ITLA → UNAPEC

CineGest también documenta un cruce institucional particular entre **ITLA** y **UNAPEC**. Además de Francis Jairo Matías Rosario, tres integrantes del equipo académico original de CineGest también cursaron estudios en el **Instituto Tecnológico de Las Américas (ITLA)** antes de coincidir posteriormente en UNAPEC.

Esta relación **no representa continuidad por materias compartidas en ITLA**. Francis Jairo Matías Rosario **no coincidió con Mario David Pichardo Vásquez, Pieranyela José Carrasco Rodríguez ni Jenrry Monegro Rosario en ninguna asignatura durante su etapa en ITLA**. El vínculo documentado es exclusivamente una **trayectoria institucional compartida**: estudiantes provenientes del ITLA que posteriormente coincidieron como integrantes del mismo proyecto en UNAPEC.

| Integrante | Matrícula UNAPEC | Matrícula ITLA | Relación documentada |
|---|---|---|---|
| **Mario David Pichardo Vásquez** | A00114273 | **2015-2935** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Francis Jairo Matías Rosario** | A00115261 | **2015-2984** | ITLA → UNAPEC |
| **Pieranyela José Carrasco Rodríguez** | A00116415 | **2019-8767** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Jenrry Monegro Rosario** | A00116621 | **2019-8690** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |

Este cruce permite documentar una dimensión distinta de la continuidad académica del portafolio: no la repetición de un profesor o compañero dentro de una misma institución, sino la convergencia posterior en UNAPEC de varios estudiantes con formación previa en ITLA. La coincidencia relevante ocurre en **CineGest (ISO-610, Enero - Abril 2026)**, no durante la etapa de Francis Jairo Matías Rosario en ITLA.

**Mario David Pichardo Vásquez** fue el principal creador y desarrollador de la versión original que sirve como punto de partida e inspiración para la evolución de **CineGest**.
'''

if anchor not in text:
    raise SystemExit("Continuity anchor not found")

text = text.replace(anchor, replacement, 1)
path.write_text(text, encoding="utf-8")
