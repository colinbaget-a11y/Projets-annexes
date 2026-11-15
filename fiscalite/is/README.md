# Note « Ne pas toucher au taux, mieux déduire l'investissement »

Livrable : `note-is.tex` (PDF et docx), 6 pages, rapport Robert de Sorbon, partie III.

Position (après revue) : garder le taux normal à 25 % ; déduction immédiate des équipements votée en une fois,
50 % de 2027 à 2032 puis 100 % ; financement par l'assiette (fin du taux réduit de 15 %, CIR au niveau du
groupe, fin des exonérations zonées, boîte à brevets), dont l'excédent rembourse la transition puis permet de
baisser le taux d'environ un point ; pas d'IS à 28 %, pas de barème progressif, pas de minimum. La fin du taux
réduit est la pièce discutable (Bernini et Treibich, 2016). Revue : `../revue/revue_is.md`.

- `notes/is_recherche.md` : Tax Foundation, OCDE, CPO, littérature sur l'amortissement accéléré, taux
  réduit, statut de chaque source ; `donnees/is_chiffres.csv` : chiffres sourcés.
- `simulation_is.py` -> `sorties/simulation_is.txt` : coût annuel de la déduction immédiate (variantes 100 %,
  50 %, paliers), coût actualisé par millésime, recette d'une hausse de taux, élargissement de l'assiette,
  solde cumulé, cas de petites sociétés.
- `figures_is.py` : figure `is_01_cout_deduction` (lancer depuis `fiscalite/`, puis avec `FIG_NU=1`).
- Docx : `cd ../ir_csg && python3 tex2docx.py ../is/note-is`.

Chiffres clés (part imposable 75 %) : coût an 1 de la déduction totale 14 à 15,5 Md€ ; coût actualisé par
millésime 1,8 à 2,6 Md€ (0,7 à 1 point de taux) ; IS à 28 % : 4,4 à 7,5 Md€ ; assiette : 3,5 à 4,4 Md€ ;
calendrier 50 % puis 100 % : dette (intérêts à 3,25 %) au plus 3 à 33 Md€, remboursée en 5 à 25 ans ; gain de PIB
de long terme 0,04 à 0,2 % (0,1 % au centre) avec la déduction totale.
