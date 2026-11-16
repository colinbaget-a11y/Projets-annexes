# Revenus du capital : PFU, holdings, apport-cession, effacement à la transmission

## Livrable actuel (refonte du 16/11/2026)

Partie « Revenus du capital : garder le taux, fermer la sortie sans impôt » de la note fusionnée :
`../synthese/parties/pfu.tex` (corps, six temps de `../synthese/CHARTE_NOTE.md`) et
`../synthese/parties/annexe_pfu.tex` (calibrage, variantes, hypothèses fortes et chiffres non vérifiés).

Position : garder le PFU à 31,4 % (stabilité ; une baisse à 25 % coûte 3,3 à 5,1 Md€, une hausse à 33 %
rapporte 0,7 à 1,3 Md€) ; majoration de 3-4 points à la place de la CEHR sur le capital ; fermer l'effacement de la
plus-value à la donation et au décès (le bénéficiaire reprend le prix d'acquisition ; report d'apport-cession
transmis sans effacement ; décision 3 de `../synthese/DECISIONS.md`). Arbitrages : taux, majoration, alignement des
prélèvements sociaux, trois traitements du report, intérêt sur l'impôt différé.

- `calculs_pfu.py` → `sorties/calculs_pfu.txt` et `.json` : tous les chiffres de la partie (lancer depuis
  `fiscalite/`). Recalcule les chiffres vérifiés de `../revue/hypotheses_pfu.md` et ajoute la série des dividendes,
  la comparaison européenne avec un IS à 25,8 %, la capitalisation en holding, le chiffrage de l'effacement (jeux
  bas / central / haut), la valeur actualisée des reports, les cas types, la charge du haut.
- `figures_pfu_n.py` → figures `pfu_n01` à `pfu_n10` (`python3 pfu/figures_pfu_n.py && FIG_NU=1 python3
  pfu/figures_pfu_n.py`, après `calculs_pfu.py`).
- `donnees/` : `insee_dividendes_menages.csv` (Insee, comptes nationaux base 2020, tableaux 7.401 et 7.101, mai
  2026), `patrimoine_actions_menages.csv` (Insee 8.210 ; Banque de France, Stat Info épargne des ménages 2025T4),
  `tf_taux_integres_2025.csv` (Tax Foundation, taux intégrés 2025), `pfu_chiffres.csv` (recherche de novembre 2026).
- `notes/pfu_recherche.md` : droit 2026, évaluations, holdings, statut de chaque source.

Chiffres clés (centre, fourchette) : impôt effacé à la transmission 7,5 Md€ par an (3,7 à 14,7), dont 1,7 pour les
reports ; recette de la reprise du prix d'acquisition 1,9 Md€ l'an 1, 3,6 l'an 10 (1,0 à 9,4), 5,8 l'an 30 ; valeur
actualisée d'une année de transmissions 4,7 Md€ (7,5 avec intérêt) ; stock de reports en valeur actualisée 4,5
aujourd'hui, 15,5 transmis, 25,1 avec l'art. 5 du PLF 2027 ; charge du 1 % : +2,5 Md€ par an en moyenne sur dix ans
(0,7 avec clause de droits acquis). Ces chiffres reposent sur des hypothèses sans mesure publiée (annexe).

## Ancien livrable

`note-pfu.tex` (PDF, docx) et `figures_pfu.py` (figure `pfu_01_taux_cumule`) : note de novembre 2026 « Garder le
prélèvement forfaitaire unique », antérieure à la refonte ; plusieurs chiffres y sont périmés (registre
`../revue/hypotheses_pfu.md`). Docx : `cd ../ir_csg && python3 tex2docx.py ../pfu/note-pfu`.
