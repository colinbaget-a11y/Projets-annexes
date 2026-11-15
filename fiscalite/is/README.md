# Note « Ne pas toucher au taux, mieux déduire l'investissement »

Livrable : `note-is.tex` (PDF et docx), 6 pages, rapport Robert de Sorbon, partie III.

Position : garder le taux normal à 25 % et laisser la contribution exceptionnelle s'éteindre ; déduction
immédiate de 50 % des équipements (machines, équipements, informatique), permanente, puis 100 % quand les
finances le permettent ; financement par l'assiette (fin du taux réduit de 15 %, CIR au niveau du groupe,
fin des exonérations zonées, boîte à brevets) ; pas d'IS à 28 %, pas de barème progressif, pas de minimum.

- `notes/is_recherche.md` : Tax Foundation, OCDE, CPO, littérature sur l'amortissement accéléré, taux
  réduit, statut de chaque source ; `donnees/is_chiffres.csv` : chiffres sourcés.
- `simulation_is.py` -> `sorties/simulation_is.txt` : coût annuel de la déduction immédiate (variantes 100 %,
  50 %, paliers), coût actualisé par millésime, recette d'une hausse de taux, élargissement de l'assiette,
  solde cumulé, cas de petites sociétés.
- `figures_is.py` : figure `is_01_cout_deduction` (lancer depuis `fiscalite/`, puis avec `FIG_NU=1`).
- Docx : `cd ../ir_csg && python3 tex2docx.py ../is/note-is`.

Chiffres clés (part imposable 75 %) : coût an 1 de la déduction totale 14 à 15,5 Md€ ; coût actualisé par
millésime 1,8 à 2,6 Md€ (0,7 à 1 point de taux) ; IS à 28 % : 4,4 à 7,5 Md€ ; assiette : 3,5 à 4,4 Md€ ;
déduction de 50 % : 7 à 7,8 Md€ l'an 1, solde cumulé au plus −3 à −10,5 Md€, regagné en 4 à 9 ans.
