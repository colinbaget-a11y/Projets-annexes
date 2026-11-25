# Qui paie une réforme des retraites ?

Valeur actualisée, par âge, de trois réformes de même effet sur le solde public (calage sur les simulations DG Trésor,
OFCE et I-MIP présentées au COR le 26 mars 2026) : baisse des pensions, hausse des cotisations (salariales ou
employeurs), recul d'un an de l'âge de départ.

- `note.md` / `note.pdf` : note de 4 pages (résultats, méthode, sensibilités, sources).
- `params.json` : paramètres avec leur statut (OBS, DED, CAL, HYP) et leur source ; `data/` : séries par âge (Insee,
  Eurostat, DREES) et `calage.json` ; `data/SOURCES.csv` : adresses des fichiers d'origine.
- `prepare_data.py` : construit `data/` à partir des extractions ; `model.py` : modèle (`python3 model.py` imprime
  l'audit) ; `check.py` : identité de comptabilité générationnelle et calage ; `sensibilites.py` ; `figures.py`.

Chaîne : `python3 model.py && python3 check.py && python3 sensibilites.py && python3 figures.py`, puis
`pandoc note.md -o note.pdf --pdf-engine=pdflatex -V lang=fr --resource-path=. -H entete_note.tex`.
