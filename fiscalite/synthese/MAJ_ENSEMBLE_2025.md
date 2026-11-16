# Mises à jour à reporter dans ensemble.tex, essentiel.tex, introduction.tex, annexe_methode.tex, synthese_ensemble.py
(base PO 2025, rapports des agents du 17/11/2026)

## Immobilier
- ensemble.tex l. 33-35 : 14,3 / 11,6 → 15,2 / 12,4 ; 1,9 (0,2 à 4,3) → 2,1 (0,2 à 4,6) ; +1,3 → +1,4 ; +96 % → +99 % ;
  +1,2 net → +1,4 ; −7,1 → −7,6 ; l. 54 : « 2023-2024 pour l'immobilier » → ventes et fiscalité locale de 2025 ;
  l. 108 trajectoire −5,7/−4,3/−2,9/−1,4 → −6,1/−4,5/−3,0/−1,5 ; l. 162 : 1,2 → 1,4 ; l. 277 Guéret 26 → 27 € ; l. 329 0,4 → 0,5 Md€
- essentiel.tex : « 1,9 pour l'immobilier » → 2,1 ; annexe_methode.tex l. 101 : dates de l'immobilier
- synthese_ensemble.py : l. 492 Limoges taxe 1 209 → 1 232 € ; l. 494 Guéret +26/+248 → +27/+253 ; l. 497 Paris taxe
  518 → 527 € ; l. 570 [DATES] ; puis relancer
- Droits chiffrés au taux permanent de 5,81 % (le relèvement temporaire à 6,32 % non compté, ~0,4 Md€ en 2025, non vérifié)
- references.tex : « REI 2017, 2024 et 2025 ; DVF 2023 à 2025 » ; Insee, Comptes de la Nation 2025 (8.200 ; 1.101), juin 2026 ;
  Bonomo, Makhzoum et Lattaud (2026), Insee Première n° 2135 ; indices Notaires-Insee ; note REI 2025 (DGCL-DGFiP, mai 2026) ;
  DGFiP Statistiques n° 43 (2026)

## IS et PFU
- ensemble.tex l. 36 : baisse finale 0,9 → 1,0 point ; dette 22,9 → 21,5 Md€ ; extinction 2042 → 2041 ; relancer synthese_ensemble.py
  (trajectoire, bilan du haut)
- synthese_ensemble.py : recettes.cehr = 1,39 (revenus 2025) ; 1,94 si impôt encaissé en 2025 (champ cehr_2024) ;
  ir_pfu reste 10,24 (revenus 2024), ir_pfu_2025 = 8,43 ajouté ; ps_tot = 36,19 encaissés en 2025 ; assiette.total_2025 ajouté
- PFU : assiette des revenus 2025 = 67,0 Md€ (DGFiP n° 53) ; PFU à 25 % : 4,3 mécanique, 2,8-3,3 ; perte sèche 0,3 ;
  impôt du 1 % sur ses revenus du capital 22 → 16 Md€ : la fin de l'effacement pèse ~20 % de cet impôt au lieu de 15 %
- IS : un point = 2,99 Md€ ; ressources 3,5/4,22/4,9 ; dette 21,5 Md€ en 2033, éteinte en 2041 (8 à 40)
- perte_seche_autres.py : B_PFU 79,6 → 67,0 ; IS 251×1,061 → 256,8×1,0404
- note-reforme-fiscale.tex page de titre : « IS 2022 » → « IS 2025 » ; DECISIONS.md « 2,95 » → 2,99
- references.tex : DGFiP Statistiques n° 39, 41 (2025), 43, 51, 53 (2026) ; AN rapport n° 2847 (2026, Ph. Juvin) ;
  Insee comptes nationaux 2026, tableaux 3.217 et 8.212

## IR-CSG
- 220,1 → 229,9 Md€ (IR 86,6 / CSG 135,8 / CRDS 7,6) ; gain 4,9 (2,3 à 10,9) → 4,7 (2,1 à 10,3) ; long terme 7,3 → 6,7 ;
  revenu déclaré +3,0 (1,5 à 4,5) → +2,6 (1,3 à 3,9) ; retraités/actifs 20,8 → 21,5 ; franchise 4 000 € : 13,5 → 14,3 ;
  valeur actualisée 245 → 250 ; 50 % à 265 000 → 231 000 € ; « garde 95 % du gain » → 89 % ; 9,1 → 9,4 M de retraités perdants ;
  premier salaire au Smic 7,4 → 7,8 % (aujourd'hui 9,5 %) ; CSG non perçue −2,1 → −2,5 ; gain permanent 3,0 à 3,8
- IR encaissé en 2025 : surtout la retenue à la source sur les revenus 2025 + solde 2024 (ne pas écrire « en grande partie sur
  les revenus 2024 ») ; fragilité : si la hausse de l'IR 2025 est passagère, recette surestimée d'environ 4,5 Md€
- synthese_ensemble.py importe modele_purs : relancer ; note-reforme-fiscale-plat.tex cite ircsg_n06 (supprimée) : réaplatir
- references.tex : Insee (2026) « Impôts. Données annuelles de 1995 à 2025 » (28/08/2026) ; Insee Informations rapides n° 78
  (27/03/2026) ; Insee, Comptes de la Nation 2025, tableau 1.101 ; Sénat (2026), J.-F. Husson, rapport n° 736 (2025-2026), t. I ;
  annexe 1 « Financement » du PLACSS 2025 (2026) ; OpenFisca-France 176.1, législation des revenus 2025
