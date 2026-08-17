from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8")
old = '''| **Mario David Pichardo Vásquez** | A00114273 | **2015-2935** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Francis Jairo Matías Rosario** | A00115261 | **2015-2984** | ITLA → UNAPEC |
| **Pieranyela José Carrasco Rodríguez** | A00116415 | **2019-8767** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Jenrry Monegro Rosario** | A00116621 | **2019-8690** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |'''
new = '''| **Mario David Pichardo Vásquez** | A00114273 | **2015-2935** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Francis Jairo Matías Rosario** | A00115261 | **2015-2984** | ITLA → UNAPEC |
| **Jenrry Monegro Rosario** | A00116621 | **2019-8690** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |
| **Pieranyela José Carrasco Rodríguez** | A00116415 | **2019-8767** | ITLA → UNAPEC; sin materias compartidas con Francis Jairo en ITLA |'''
if old not in text:
    raise SystemExit("ITLA cross table not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
