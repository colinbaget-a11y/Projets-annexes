# Vérification des chiffres « foncier », « IS » et « capital » de la note (bilan 2032 et texte hors IR)

17/11/2026. Lecture seule : aucun fichier existant modifié. Montants en Md€ de 2026 sauf mention. Le « calcul » signale un
recalcul de ma part à partir de la source citée ; « non relu » signale un chiffre que je n'ai pas pu rouvrir moi-même.
Fichiers téléchargés dans le scratchpad de session (`verif_dl/`, `d41/`, `n51x/`, `i8212/`, `x8200/`).

## 1. Lignes du bilan 2032 (`bilan_lignes.txt`) : reproduction

| Ligne | Valeur | Reproduction | Verdict |
|---|---|---|---|
| Taxe nationale sur le sol | 13,63 | foncier3.json B_E15, 2032 : (15,0 − 0,511 report − 1,26 déductibilité) × 1,03 = 13,63 | CONFIRMÉ (calcul) ; libellé trompeur : 15,45 brut, 13,63 net |
| Droits de mutation ÷ 2 | −8,32 | −8,075 × 1,03 | CONFIRMÉ (calcul) |
| Total foncier | 5,31 | 5,155 × 1,03 | CONFIRMÉ (calcul) |
| Fin du taux réduit | 2,03 | is4 `annuel_caisse` 2032 : 2,42 / 1,03⁶ (1,194) | CONFIRMÉ (calcul) |
| Fin du CIR | 5,61 | 6,70 / 1,194 | CONFIRMÉ (calcul) |
| Autres niches | 1,80 | 2,15 / 1,194 | CONFIRMÉ (calcul) |
| Déduction immédiate | −7,20 | (−5,71 − 2,89 − 0) / 1,194 | CONFIRMÉ (calcul) |
| Revalorisation des déficits | −1,17 | pal.json, central 1,133 × 1,03 (non déflaté) | CONFIRMÉ (calcul) |
| Total IS ; foncier + IS | 1,07 ; 6,38 | id. ; 2033 : −0,88 ; 2040 : 12,6 | CONFIRMÉ (calcul) |

## 2. Tableau de vérification

| Chiffre | Valeur note / modèle | Source lue et valeur | Écart | Verdict |
|---|---|---|---|---|
| DMTO au taux permanent | 16,15 Md€ (€ 2025) | OFGL-DGCL, Rapport 2026, annexe 8 : DMTO toutes collectivités **16 703 M€ en 2025** (+18,5 %, donc ≈ 14,1 en 2024) ; note REI 2025 : 13,5 Md€ part départementale 2025 (11,1 en 2024), 16 Md€ dép. + communes (note 7) ; 80 départements à 5 % | −3 % ; le perçu 2025 inclut la majoration à 5 % dès avril 2025 | COHÉRENT |
| Division par deux | « 8 » Md€ (8,07 € 2025 ; 8,32 € 2026) | moitié de 16,15 | — | CONFIRMÉ (calcul) |
| TFPB actuelle | 43-45 Md€ | REI 2025 : **43 131 M€** (41 964 en 2024) ; OFGL 2026 : 43 113 M€ + 769 de coefficients correcteurs | dans la fourchette basse | CONFIRMÉ (43,1) |
| Valeur du sol privé (assiette) | 6 655,9 Md€ fin 2025 | Insee, tableau 8.200 (2025) : N2111 + N2119 de S11 (1 700,671 + 113,036), S12 (200,287), S14 (4 136,126 + 451,854), S15 (53,9) = 6 655,874 | 0 | CONFIRMÉ |
| Taux national | ≈ 0,24 % pour 15 Md€ | 15 / 6 655,9 = 0,225 % statique ; 0,2437 % après capitalisation (sol − 500 Md€, r = 3 % [H]) | — | CONFIRMÉ (calcul, sous hypothèse) |
| 300 €/logement ; 490 € sur 200 000 € | note, § foncier | foncier3.md B_E15 : +290 € ; 0,2437 % × 200 000 = 487 € | — | COHÉRENT ; mais l'annexe C citée est en B_E10 (10 Md€, 0,158 %, 193 €) | 
| Orléans → Essonne | 21 190 € au taux de 5,81 % | DGFiP, taux au 1/6/2026 : Essonne **5,00 %** (art. 116 LF 2025, hors primo-accédant) ; 4,50 % (art. 1594 D). Taux global 2026 hors primo-accédant : 5 + 1,2 + 2,37 % × 5 = 6,32 % → **23 063 €** ; taux permanent 5,807 % → 21 194 € | 5,81 % est le taux permanent (de nouveau en vigueur au 1/4/2028), pas celui de 2026 ; un vendeur d'Orléans n'est pas primo-accédant | À CORRIGER (préciser) |
| 300 €/mois pendant 6 ans | 294 € | 21 194 / 72 | — | CONFIRMÉ (calcul) |
| Taux réduit PME : n° de dépense VM | (consigne) | VM PLF 2026, t. II, p. 8 : le taux de 15 % « fait partie intégrante de la norme » : **pas de dépense fiscale ni de coût** ; le code 320117 n'apparaît que dans la table des articles (219-I-b), sans fiche ; « aucun déclassement » cette année | — | NON VÉRIFIABLE dans les VM (pas de chiffre officiel) |
| Taux réduit : base et coût | 2,0 Md€ (prudent), 3,18 statique 2027 | DGFiP *Statistiques* n° 51 (sept. 2026), graphique 2 : **BI à 15 % = 30,6 Md€** en 2025 → 10 points = 3,06 Md€ ; série prudente bâtie sur CPO 2023 (2,2 Md€ en 2019 pour 13 points), non relu | prudent = 68 % du statique | COHÉRENT |
| CIR, VM PLF 2026 | 8,0 Md€ | VM t. II, **200302** : 7 800 (2024 réalisé), 8 068 (2025), **8 041 (2026)** | 0 | CONFIRMÉ |
| CIR, Sénat PLF 2027 | 7,4 Md€ en 2027 | note de présentation « Remboursements et dégrèvements » PLF 2027 non retrouvée ; repères : DGFiP n° 51, CIR + CII + collaboratif utilisés en 2025 : 7,69 Md€ ; jaune « Recherche » PLF 2027 : créance CIR-recherche 2024 7,4 Md€ | — | NON VÉRIFIABLE (par moi) |
| CIR, recette retenue | 5,6 (2032), « ≈ 5,5 à terme » | 0,8 × statique [H], profil de restitution [H] | — | COHÉRENT (hypothèse) |
| Autres niches : coûts officiels | 2,60 statique ; 2,1 prudent | VM t. II, 2026 : mécénat **210309 : 1 730** (compté 1 730 × 35/60 = 1 010) ; culture **706** (320121 : 156, 320128 : 31, 320129 : 263, 320135 : 78, 320140 : 125, 320142 : 47, 320145 : 4, 320148 : 2) ; zonages **657** (220104 : 376, 220109 : 60, 220102 : 89, 230602 : 42, 210305 : 83 ; 230606/608/605 : 7, d'après is3.json) ; crédit famille **210308 : 223** | 0 | CONFIRMÉ (coûts) ; « 2,1 après réaction » = 2,05 en 2040 : COHÉRENT ; la note omet le crédit famille dans sa parenthèse |
| Recettes IS 2025 | « recettes d'IS 2025 » (note de bas de page) | DGFiP n° 51 : BI à 25 % **256,8 Md€**, à 15 % 30,6, assiette CEBGE 20,4 ; IS brut des sociétés 70,5 Md€ ; Sénat, rapport général PLF 2027, t. I (provisoire) : IS net 60,3 Md€ en 2026 révisé, +0,4 sur 2025 → ≈ 59,9 en 2025 (calcul) | le calcul part des bénéfices imposables, pas des recettes | À CORRIGER (source) |
| Baisse du taux 25 → 22,5 % | 7,3 Md€ | modèle : 2,5 × (267,2 + 31,8)/100 = 7,48 (€ 2027) : le point est appliqué aussi à la base taxée à 15 %. Sur la seule base à 25 % : 2,5 % × 256,8 = **6,42 Md€ (2025)**, ≈ 6,5-6,6 en 2026 | +0,7 à +0,8 Md€ | À CORRIGER (≈ 6,5) |
| Investissement éligible (transition) | 84,1 Md€ en 2025 | Insee 8.212 (S11), flux d'actifs 2025 : autres machines (N1139) **75,524** + TIC (N1132) **8,534** = 84,06 | 0 | CONFIRMÉ |
| Coût de transition | 7 Md€ en 2032, 1,5 ensuite | is4 : −7,20 (2032) ; 2040 : −0,64 − 0,25 − 0,64 = −1,53 ; ordre de grandeur cohérent avec 89 Md€ × 75 % [H] × 25 % × ≈ 0,45 | — | COHÉRENT |
| Revalorisation des déficits | « 1 Md€ » ; 1,2 (0,4-2,3), source « déficits imputés, DGFiP n° 21 » | pal.json : τ × 32 Md€ imputés [H] × ((1,0337)⁴ − 1) = 1,13 (0,43-2,20) ; ×1,03 = 1,17 (0,44-2,26). DGFiP n° 21 donne les **déficits nouveaux** (113 Md€ en 2022) ; le volume imputé vient du CGE 2010 (25 Md€/an, rapport Carrez n° 3718) porté à 32 [H] | montants : 0 ; source : erronée | COHÉRENT (montant) / À CORRIGER (source) |
| 27,3 k€ pour 100 k€ de perte à 3 ans | 25 × 1,03³ = 27,32 | — | — | CONFIRMÉ (calcul) |
| Pilier 2 | 0,5 Md€ en 2026 ; 1,5 prévus ; Sénat n° 780, juin 2026 | Sénat, rapport **n° 780 (2025-2026), déposé le 24 juin 2026** (Capus) : « 500 millions d'euros de recettes fiscales en 2026, contre 1,5 milliard d'euros selon les prévisions initiales » (données transmises en 2023) | 0 | CONFIRMÉ (chiffre de l'administration fiscale, repris par le Sénat) |
| PS + 1,4 point → 1,5 Md€ | 1,5 (statique du PFU à 30 %) | Sénat, rapport **n° 205 (2025-2026)**, nouvelle lecture PLFSS 2026 : l'art. 6 bis « majore la CSG sur les revenus du capital de 1,5 milliard d'euros » (2,8 en 1re lecture). Constaté : 1,2 Md€ (Sénat, rapport PLFSS 2027, exposé général), 1,3 (CR commission des finances, semaine du 2/11/2026) | prévision exacte ; réalisé −0,2 à −0,3 ; assiette plus large que celle du PFU (1,4 pt × 84,4 = 1,18) | CONFIRMÉ (prévision) ; préciser 1,2-1,5 |
| Assiette PFU (revenus 2024) | 50,1 / 10,4 / 18,8 Md€ | Totaux DGFiP de la 2042 (`donnees/ir_2042_cases_revenus2024.csv`) : 2DC 50 135,5 M€ ; 2TR 10 427,8 ; 3VG 18 777,5 | 0 | CONFIRMÉ (extrait local, non retéléchargé) ; 2DC inclut les optants au barème : majorant |
| Élasticité | 0,77 (0,22-0,96) | Lefebvre, Lehmann et Sicsic, IZA DP 16112 : lu selon `pfu/notes/pfu_recherche.md` [TEXTE LU] ; non relu ici | — | COHÉRENT (non relu) |
| PFU à 30 % / 25 % | ≈ 1 ; ≈ 4 (5,4 ; 3,5-5,0) | pfu_options.json : 1,10 ; 5,40 / 3,89 (3,51-4,97) | — | CONFIRMÉ (calcul) |
| CPO 2026 : 12,8 M de foyers, 1 520 € | attribué au CPO | CPO, sept. 2026 : **12,5 M** de foyers bénéficiaires effectifs, 14,26 M déclarants ; pas de « 1 520 € ». Les deux chiffres sont ceux de **DGFiP *Statistiques* n° 41** (nov. 2025), tableau 3 : 12 829 186 foyers, 19,53 Md€, **1 522 €** (dont 3,83 Md€ de réduction pour revenus de source étrangère) | attribution | À CORRIGER (source) |
| Entrepreneuse | 411 k€ / 213 k€ | Barème ligne directe (service-public F14198, vérifié le 9/2/2026), abattement 100 000 € : vente = 282,6 (PFU 31,4 % sur 900 k€) + 128,2 = **410,8** ; transmission = **213,0** | 0 | CONFIRMÉ (calcul) ; hors CEHR (≈ +23,5 k€ sur 900 k€ de plus-value) |
| Antoine / Béatrice | 46 900 € / 58 200 € | recalcul indépendant (aire sous le taux marginal interpolé, barème `ircsg4.json`) : 46 868 / 58 239 | 0 | CONFIRMÉ (calcul) |
| Zwick et Mahon (2017) | +10 à +17 % | *AER* 107(1) : +10,4 % (2001-2004), +16,9 % (2008-2010), investissement éligible par rapport au non éligible | 0 | CONFIRMÉ |
| Maffini, Xing et Devereux (2019) | ≈ +11 % | *AEJ: Policy* 11(3) : +2,1 à 2,5 points de taux d'investissement ; version de travail 2016 : « 11 percent at the mean » | 0 | CONFIRMÉ |
| France Stratégie 2023 sur le PFU | dividendes ↑, pas d'effet mesurable sur l'investissement | Comité d'évaluation : 3e rapport (2021) et rapport final (oct. 2023) : fort effet sur les dividendes, aucun effet identifié sur l'investissement (résumés lus ; texte intégral 2023 non relu ici) | — | COHÉRENT |

## 3. Corrections recommandées

1. Baisse du taux à 22,5 % : écrire « environ 6,5 milliards » (2,5 points sur 256,8 Md€ de bénéfices imposés à 25 % en 2025, DGFiP n° 51) et sourcer « bénéfices imposables », non « recettes » ; corriger en annexe D « un point de taux normal : 2,99 » (2,67 en 2027) et la barre de g7.
2. Note 1 (12,8 M, 1 520 €) : citer DGFiP *Statistiques* n° 41 (nov. 2025), ou garder le CPO avec 12,5 millions.
3. Orléans : « 21 190 € au taux permanent de 5,81 % ; 23 060 € (6,32 %) jusqu'au 31 mars 2028 en Essonne hors primo-accédants ».
4. Déficits : source = volume imputé supposé (32 Md€/an, d'après le CGE 2010) ; DGFiP n° 21 ne publie que les déficits nouveaux.
5. Foncier : annexe C et commentaire d'en-tête de `note.tex` en B_E10, note et bilan en B_E15 (0,24 %, 300 €) : aligner.
6. Bilan : la ligne « Taxe nationale sur la valeur du sol » (13,6) est nette du report et de la déductibilité (15,45 brut) : le dire.
7. Taux réduit : ne pas citer de numéro des Voies et moyens (le taux de 15 % est dans la norme) ; sources : DGFiP n° 51 et CPO 2023.
8. PFU à 30 % : « 1,5 milliard prévu (Sénat, n° 205), 1,2 à 1,3 constaté ».
9. Pilier 2 : « selon l'administration fiscale, citée par le Sénat (rapport n° 780) ».
10. CIR 7,4 Md€ en 2027 : donner le lien de la note du Sénat, ou s'en tenir à 8,0 (VM 2026) et 7,7 utilisés en 2025 (DGFiP n° 51).

## Sources lues

- Évaluation des voies et moyens, tome II, PLF 2026 (copie locale `scratchpad/vm/vm.pdf`), p. 8-9 et fiches 200302, 210305, 210308, 210309, 220102, 220104, 220109, 230602, 3201xx.
- DGFiP, taux des DMTO au 1/6/2026 : https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/notaires/dmto/dmto_2026-06.pdf
- OFGL-DGCL, Rapport 2026, annexes 6 à 8 : https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/Annexes%206%20%C3%A0%208.pdf
- DGCL-DGFiP, note REI 2025 : https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/Taux%20de%20fiscalit%C3%A9%20directe%20locale%20vot%C3%A9s%20par%20les%20collectivit%C3%A9s/2025/Note%20analyse%20REI_2025.pdf
- Insee, tableau 8.200 (2025) : https://www.insee.fr/fr/statistiques/fichier/8988859/T_8200_2025_fr.xlsx ; tableau 8.212 : https://www.insee.fr/fr/statistiques/fichier/8988859/T_8212_fr.xlsx
- DGFiP *Statistiques* n° 51 (sept. 2026), xlsx : https://www.impots.gouv.fr/sites/default/files/media/9_statistiques/0_etudes_et_stats/0_publications/dgfip_statistiques/2026/num51_09/dgfip_stat_51_is-2025.xlsx
- DGFiP *Statistiques* n° 41 (nov. 2025), xlsx : https://www.impots.gouv.fr/sites/default/files/media/9_statistiques/0_etudes_et_stats/0_publications/dgfip_statistiques/2025/num41_11/dgfip_stat_41.xlsx
- CPO, *L'impôt sur le revenu, ses réductions et crédits d'impôt depuis 2017* (sept. 2026) : https://www.vie-publique.fr/files/rapport/pdf/304837.pdf
- Sénat, rapport n° 780 (2025-2026) : https://www.senat.fr/rap/l25-780/l25-7800.html et https://www.senat.fr/rap/l25-780/l25-7801.html
- Sénat, rapport n° 205 (2025-2026), PLFSS 2026 nouvelle lecture : https://www.senat.fr/rap/l25-205/l25-205_mono.html
- Sénat, PLFSS 2027, exposé général : https://www.senat.fr/rap/l26-144-1/l26-144-132.html ; commission des finances, CR semaine du 2/11/2026 : https://www.senat.fr/compte-rendu-commissions/20261102/fin.html
- Sénat, rapport général PLF 2027, tome I (provisoire) : https://www.senat.fr/fileadmin/Commissions/Finances/2026-2027/PLF_2027/Divers_PLF_2027/Rapport_provisoire_Tome_I.pdf
- Jaune « Politiques nationales de recherche » PLF 2027 : https://www2.assemblee-nationale.fr/static/17/Annexes-DL/PLF_2027/11-Jaune-2027-Politiques-nationales-recherche-formations-superieures.pdf
- service-public, droits de succession (F14198) : https://www.service-public.gouv.fr/particuliers/vosdroits/F14198
- Zwick et Mahon : https://www.nber.org/papers/w21876 ; Maffini, Xing et Devereux : https://www.aeaweb.org/doi/10.1257/pol.20170254 et https://oxfordtax.sbs.ox.ac.uk/files/wp16-01pdf
- France Stratégie, rapport 2023 : https://www.strategie.gouv.fr/sites/strategie.gouv.fr/files/atoms/files/fs-2023-rapport-isf-quatrieme_rapport_complet_17octobre.pdf (résumé) ; 3e rapport : https://www.vie-publique.fr/rapport/281944-comite-devaluation-des-reformes-de-la-fiscalite-du-capital-3e-rapport
