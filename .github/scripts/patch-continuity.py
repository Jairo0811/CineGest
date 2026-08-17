from pathlib import Path
import re

path = Path("README.md")
text = path.read_text(encoding="utf-8")

section = """## 🧭 Continuidad académica

**CineGest** forma parte de una continuidad docente compartida con [**MediCore**](https://github.com/Jairo0811/MediCore) dentro de la formación de Ingeniería de Software en la Universidad APEC (UNAPEC). La relación entre ambos proyectos es **académica y formativa**: no existe una dependencia técnica entre las aplicaciones, sino la coincidencia del mismo profesor en dos asignaturas diferentes cursadas durante el mismo período.

Durante **Enero - Abril de 2026**, el profesor **Ing. Omar Antonio De Jesus De La Cruz Gonzalez** impartió tanto **Desarrollo de Software con Tecnología Propietaria 1 (ISO-605)** como **Desarrollo de Software con Tecnología Open Source 1 (ISO-610)**, asignaturas en las que Francis Jairo Matías Rosario participó en los proyectos finales MediCore y CineGest respectivamente.

| Orden | Código | Asignatura | Proyecto | Período | Vínculo de continuidad |
|---:|---|---|---|---|---|
| 1 | ISO-605 | Desarrollo de Software con Tecnología Propietaria 1 | [**MediCore**](https://github.com/Jairo0811/MediCore) | Enero - Abril 2026 | Mismo profesor |
| 2 | ISO-610 | Desarrollo de Software con Tecnología Open Source 1 | **CineGest** | Enero - Abril 2026 | Mismo profesor |

Vistos en conjunto, ambos proyectos documentan una experiencia paralela con el mismo docente en dos líneas complementarias del plan de estudios: **tecnología propietaria** y **tecnología open source**. Cada repositorio conserva su identidad, equipo y alcance académico original, y su relación se documenta exclusivamente como continuidad docente."""

updated = re.sub(
    r"## 🔗 Continuidad académica.*?(?=\n\n\*\*Mario David Pichardo Vásquez\*\*)",
    section,
    text,
    flags=re.S,
)
if updated == text:
    raise SystemExit("Continuity block not found")
path.write_text(updated, encoding="utf-8")
