from pathlib import Path

p = Path('README.md')
s = p.read_text(encoding='utf-8')

anchor = '### 🏫 Cruce institucional ITLA → UNAPEC'
lineage = '''### 📚 Línea académica de Juan P. Valdez

CineGest también pertenece a una **línea académica común de enunciados de Proyecto Final elaborados por el profesor Juan P. Valdez en 2020**. El documento original de Video Club identifica explícitamente a **Juan P. Valdez** como profesor y define el problema de negocio que posteriormente sirvió de base para la versión académica y la evolución actual de CineGest.

Dentro de esta colección se han identificado tres enunciados relacionados:

| Orden | Enunciado académico de 2020 | Evolución en el portafolio | Relación con Juan P. Valdez |
|---:|---|---|---|
| 1 | Dispensario Médico de UNAPEC | [**MediCore**](https://github.com/Jairo0811/MediCore) | Enunciado de Proyecto Final elaborado por **Juan P. Valdez** |
| 2 | Sistema de Video Club | **CineGest** | Enunciado de Proyecto Final elaborado por **Juan P. Valdez** |
| 3 | Sistema de Rentcar | [**RentCarRD**](https://github.com/Jairo0811/RentCarRD) | Enunciado de Proyecto Final elaborado por **Juan P. Valdez** |

Esta relación se documenta como **continuidad por origen del enunciado académico** y es independiente de la continuidad docente de 2026. En CineGest, el profesor efectivo de **ISO-610** fue **Ing. Omar Antonio De Jesus De La Cruz Gonzalez**; Juan P. Valdez corresponde al origen documentado del enunciado académico que inspiró el proyecto.

'''

if anchor not in s:
    raise SystemExit('ITLA anchor not found')
s = s.replace(anchor, lineage + anchor, 1)

p.write_text(s, encoding='utf-8')
