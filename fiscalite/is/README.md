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

Chiffres clés (euros de 2027, part imposable 75 % ; corrigés le 16/11/2026, registre des hypothèses et des
corrections : `../revue/hypotheses_is.md`) : coût an 1 de la déduction totale 14 à 15,5 Md€, coût permanent dès
l'an 8 de 1,3 à 2,0 Md€ (euros de 2034) ; coût actualisé par millésime 1,7 à 2,6 Md€ à 5 % (0,6 à 0,9 point de
taux ; un point vaut 2,95 Md€ une fois le taux réduit supprimé) ; IS à 28 % : 4,6 à 8,0 Md€ ; assiette : 3,5 à
4,6 Md€ ; calendrier 50 % puis 100 % : dette (intérêts à 3,25 %) au plus 3 à 32 Md€, remboursée en 4 à 25 ans
(100 % dès 2027 : 18 à 46 Md€, 10 à 28 ans) ; baisse finale du taux de 0,6 à 1,2 point ; gain de PIB de long terme
0,04 à 0,2 % (0,1 % au centre) avec la déduction totale.

## Refonte de la note de synthèse (16/11/2026)

La partie IS de `synthese/note-reforme-fiscale.tex` (`synthese/parties/is.tex`, annexe `synthese/parties/annexe_is.tex`)
est réécrite selon `synthese/CHARTE_NOTE.md`. Proposition : déduction immédiate des équipements neufs, à 100 % sous un
plafond de 1 M€ par groupe dès 2027 (modèle britannique) et, au-delà, 50 % en 2027 puis +10 points par an jusqu'à 100 %
en 2032 (plus de marche en 2033) ; biens neufs seulement, sans cession-bail ni achat intragroupe ; déficits issus de la
déduction imputables hors plafond ; financement par l'assiette, baisse finale du taux après extinction de la dette.

- `calculs_note_is.py` -> `sorties/calculs_note_is.txt` et `.json`, et les tableaux `synthese/parties/tab_is_transition.tex`,
  `tab_is_transition_complet.tex`, `tab_is_options.tex` : situation actuelle (OCDE, qui paie, taux), réforme naïve, sept
  calendriers comparés, sensibilités, variantes de financement, contribution exceptionnelle, cas types, transition année
  par année. Importe `simulation_is.py` sans le modifier.
- `figures_note_is.py` -> `figures/is_n01` à `is_n09` (lancer depuis `fiscalite/`, puis avec `FIG_NU=1`).
- `donnees/extraire_ocde_is_pib.py` -> `donnees/ocde_is_pib.csv` (OCDE, Revenue Statistics, IS en % du PIB, 38 pays ;
  le CSV téléchargé est passé en argument et lu avec `python3 -I`).

Chiffres clés (cas central : plan actuel moitié linéaire, moitié dégressif ; ressources 4,06 Md€ ; part imposable 75 % ;
plafond couvrant 20 % de l'investissement) : coût 2027 de 8,4 à 9,3 Md€ (dont 1,3 de coût permanent) ; dette maximale
23 Md€ en 2033 (10 à 40 selon les bornes), éteinte en 2042 (2036 à 2053) ; baisse finale du taux de 0,9 point (0,6 à
1,2) ; part imposable de 90 % : 35 Md€, éteinte en 2047 (57 Md€ et 2066 au pire). Avec la fin de la contribution
exceptionnelle, l'IS rapporte en 2027 11,8 Md€ de moins qu'en 2026 (4,8 pour la réforme, 7,0 pour l'extinction).
