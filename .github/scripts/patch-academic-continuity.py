from pathlib import Path
import re

path = Path('README.md')
text = path.read_text(encoding='utf-8')
section = '''## 🧭 Continuidad académica

**CineGest** documenta su continuidad académica mediante relaciones verificables entre estudiantes y profesores. En la colección actual de proyectos de UNAPEC se ha verificado una **continuidad por profesor** con MediCore; no se ha identificado un compañero recurrente de UNAPEC que coincida de forma inequívoca por nombre y matrícula en otro proyecto de la colección.

### 👥 Continuidad por estudiante

No se ha verificado, dentro de los proyectos de UNAPEC actualmente documentados en este portafolio, un integrante de CineGest que vuelva a coincidir con Francis Jairo Matías Rosario en otro equipo académico de UNAPEC por **mismo nombre completo y misma matrícula**.

La ausencia de una coincidencia recurrente no elimina el valor del equipo original; simplemente evita presentar como continuidad directa relaciones que no están verificadas.

### 👨‍🏫 Continuidad por profesor

El profesor **Ing. Omar Antonio De Jesus De La Cruz Gonzalez** impartió durante **Enero - Abril de 2026** dos asignaturas en las que Francis Jairo Matías Rosario participó en proyectos finales distintos: [**MediCore**](https://github.com/Jairo0811/MediCore), correspondiente a **Desarrollo de Software con Tecnología Propietaria 1 (ISO-605)**, y **CineGest**, correspondiente a **Desarrollo de Software con Tecnología Open Source 1 (ISO-610)**.

| Orden | Asignatura | Proyecto | Período | Profesor recurrente |
|---:|---|---|---|---|
| 1 | Desarrollo de Software con Tecnología Propietaria 1 (ISO-605) | [**MediCore**](https://github.com/Jairo0811/MediCore) | Enero - Abril 2026 | **Ing. Omar Antonio De Jesus De La Cruz Gonzalez** |
| 2 | Desarrollo de Software con Tecnología Open Source 1 (ISO-610) | **CineGest** | Enero - Abril 2026 | **Ing. Omar Antonio De Jesus De La Cruz Gonzalez** |

La relación es **académica y formativa**: los proyectos son independientes y la continuidad se fundamenta exclusivamente en el mismo profesor.

### 🏫 Cruce institucional ITLA → UNAPEC

CineGest también documenta un cruce institucional entre **ITLA** y **UNAPEC**. Además de Francis Jairo Matías Rosario, tres integrantes del equipo académico original cursaron estudios en el **Instituto Tecnológico de Las Américas (ITLA)** antes de coincidir posteriormente en UNAPEC.

Esta relación **no representa continuidad por materias compartidas en ITLA**. Francis Jairo Matías Rosario no coincidió con Mario David Pichardo Vásquez, Jenrry Monegro Rosario ni Pieranyela José Carrasco Rodríguez en ninguna asignatura durante su etapa en ITLA. El vínculo documentado es una **trayectoria institucional compartida**.

| Integrante | Matrícula UNAPEC | Matrícula ITLA | Relación documentada |
|---|---|---|---|
| **Mario David Pichardo Vásquez** | A00114273 | **2015-2935** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Francis Jairo Matías Rosario** | A00115261 | **2015-2984** | ITLA → UNAPEC |
| **Jenrry Monegro Rosario** | A00116621 | **2019-8690** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Pieranyela José Carrasco Rodríguez** | A00116415 | **2019-8767** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |

**Mario David Pichardo Vásquez** fue el principal creador y desarrollador de la versión original que sirve como punto de partida e inspiración para la evolución de **CineGest**.
'''
pattern = r'## 🧭 Continuidad académica.*?(?=\n---\n\n# 🛠️ Stack tecnológico)'
new = re.sub(pattern, section.rstrip(), text, flags=re.S)
if new == text:
    raise SystemExit('Continuity section not found')
path.write_text(new, encoding='utf-8')
