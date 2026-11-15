# Note « Garder le prélèvement forfaitaire unique »

Livrable : `note-pfu.tex` (PDF et docx), environ 5 pages, rapport Robert de Sorbon, partie III.

Position (après revue, `../revue/revue_pfu.md`) : garder le PFU (31,4 % en 2026) tel qu'il est, l'argument
central étant la stabilité (2013 et 2018 sont un seul épisode de report des distributions) ; écarter le PFU
à 25 % (coût net 3,2 à 3,9 Md€) et l'impôt de 25 % sur les holdings ; mettre fin à l'effacement du report de
l'apport-cession en transmettant le report aux héritiers sans l'effacer (plutôt que l'expiration à toute
transmission du PLF 2027, art. 5, qui taxe une structure sans liquidité et alourdit de 90 à 100 M€ la facture
des plus gros apporteurs) ; garder la majoration de 3 puis 4 points (CEHR) sur le capital dans l'impôt fusionné.

- `notes/pfu_recherche.md` : droit 2026, évaluations (IPP, Insee, France Stratégie, CAE, LLS), holdings,
  statut de chaque source.
- `donnees/pfu_chiffres.csv` : chiffres avec source et statut.
- `figures_pfu.py` : figure `pfu_01_taux_cumule` (lancer depuis `fiscalite/`, puis avec `FIG_NU=1`).
- Docx : `cd ../ir_csg && python3 tex2docx.py ../pfu/note-pfu`.

Points à reprendre au contrôle transversal : la note IR-CSG reporte la CEHR sur le barème fusionné (à
retirer de sa cible si la majoration est gardée) et compte 11,5 Md€ d'IR au PFU au lieu d'environ 10 Md€.
