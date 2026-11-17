# Vérification des lignes « Nouvel impôt sur le revenu » du bilan (17/11/2026)

Périmètre : lignes « Nouvel impôt sur le revenu » de `bilan_lignes.txt` (Md€ de 2026 = niveau 2025 × 1,03, année 2032,
réforme installée). Chiffres du modèle : `sorties/ircsg4.json`, `sorties/ircsg4_calculs.txt`, `annexes/annexe_ircsg.tex`.
Chaque ligne du bilan est la valeur du JSON × 1,03. Je l'ai vérifié ligne par ligne, par exemple 7,029 × 1,03 = 7,24 ;
« autres » = 3,136 × 1,03 = 3,23 ; « forfait » = `technique_frais` 25,73 × 1,03 = 26,5 ; dernière ligne = (CEHR −0,580
+ ASPA −0,249) × 1,03 = −0,85. Les lignes du bloc s'additionnent à 0 (8,5e-15).

Le facteur 1,03 convertit des prix ; ce n'est pas une projection à 2032. Les montants restent ceux de la statique 2025.

## Tableau

Pour les niches, la colonne « Écart » compare la valeur du modèle avant × 1,03 au coût Voies et moyens (VM) de 2025.

| Ligne | Note (€ 2026) | Modèle (niveau 2025) | Source officielle et valeur | Écart | Verdict |
|---|---|---|---|---|---|
| Crédit emploi à domicile | 7,24 | 7,029 | VM PLF 2026, n° 110246 : 6 420 M€ (réalisé 2024), **7 029 (2025)**, 7 208 (2026). CPO 2026, fiche 1 : 6,507 Md€ en 2024. | 0 % (+8 % sur le CPO 2024) | CONFIRMÉ |
| Intéressement et participation | 2,53 | 2,457 = 0,85 × 2,890 | VM n° 120108 : **2 890 M€** en 2024, 2025 et 2026 (fiabilité « ordre de grandeur », reconstitution de base). | −15 % | COHÉRENT : l'écart vient de la part supprimable de 85 %, une hypothèse [H] (report de 15 % vers l'épargne retraite déductible), pas d'une erreur. |
| Heures supplémentaires | 2,28 | 2,212 | VM n° 120146 : 2 144 (2024), **2 212 (2025)**, 2 250 (2026) ; fiabilité « ordre de grandeur ». | 0 % | CONFIRMÉ |
| Dons | 2,27 | 2,204 | VM n° 110201 : 1 990 (2024), **2 204 (2025)**. CPO : 2,212 Md€ (2024). LFI 2026, art. 28 : plafond « Coluche » porté à 2 000 € (coût 0,1 Md€, VM t. I). | 0 % (environ −4 % après la LFI 2026) | CONFIRMÉ, léger minorant |
| Crédit garde des jeunes enfants | 1,85 | 1,799 | VM n° 110203 : 1 737 (2024), **1 799 (2025)**. CPO : 1,796 Md€ (2024). | 0 % | CONFIRMÉ |
| Demi-parts dérogatoires | 1,31 | 1,274 | VM 2025 : n° 110102, 684 (vivant seul ayant élevé un enfant) + n° 110103, 475 (anciens combattants) + n° 110107, 115 (veufs avec enfants) = 1 274. La demi-part des parents isolés (n° 110110, 865) n'est pas dans cette ligne ; elle est comptée dans « fin du QF ». | 0 % | CONFIRMÉ |
| Autres niches (Girardin, DOM, scolarité…) | 3,23 | 3,136 | VM 2025 : Girardin productif n° 110224, 825 ; DOM n° 110302, 426 ; scolarité n° 110215 + n° 110242, 229 + 225 ; syndicales n° 110202, 156 ; prestation compensatoire n° 110223, 56 ; IJ ALD n° 120204, 621 ; impatriés 394 ; détachés n° 120124, 369 (valeur 2024, 2025 « nc »), etc. Montants repris correctement. **Mais** n° 110224 : « fin du fait générateur 2029, fin d'incidence budgétaire 2030 », et la LFI 2026 ne le proroge pas. De même, n° 110259 (Scellier outre-mer, 37) est un stock et n° 110256 (logement social outre-mer, 12) prend fin en 2029. | En 2032, par rapport au droit actuel : environ −0,87 Md€ (2,26 au lieu de 3,14, soit **2,33** en € 2026) | À CORRIGER |
| Retraités : fin de l'abattement de 10 % sur les pensions | 7,49 | 7,273 | Dépense fiscale VM n° 120401 : 4 803 (2024), **5 322 (2025)**, 4 665 (2026, chiffrage qui inclut le forfait de 2 000 € du PLF, non adopté). IPP, note n° 129 (sept. 2026) : suppression = +5,0 Md€ d'IR (2027), +5,4 avec les aides au logement. Plafond des revenus 2025 : **4 439 € par foyer**, minimum 454 € par pensionné (brochure IR 2026). Le modèle utilise 4 439 / 454. | +37 % sur le VM. Ma décomposition du modèle : IR +5,95 (+12 % sur le VM, +19 % sur l'IPP) et **CSG +1,33** (la hausse du RFR fait passer des pensionnés à un taux de CSG supérieur). | À CORRIGER (ventilation) |
| Retraités : CSG alignée sur celle des actifs | 8,17 | 7,929 (CSG +8,89 ; IR −0,96) | Taux vérifiés : pensions 0 / 3,8 / 6,6 / 8,3 %, dont 0 / 3,8 / 4,2 / 5,9 points déductibles, CRDS 0,5 %, CASA 0,3 % (service-public F2971 ; brochure IR 2026) ; actifs 9,2 %, dont 6,8 déductibles. Seul rendement publié : **IPP n° 129, 4,2 Md€ nets** (0,6 Md€ de moindre IR), pour l'alignement des seuls taux médian et plein. Rien trouvé du COR, de la Cour des comptes ni du PLFSS. | Pas comparable : le modèle aligne aussi les taux 0 et 3,8 % et ajoute la CRDS des exonérés. Mesure isolée dans le modèle : 9,36. | COHÉRENT |
| Retraités : fin de l'abattement des personnes âgées | 0,59 | 0,570 | VM n° 100201 : 390 (2024), **419 (2025)**, 11 (2026, chiffrage du PLF, mesure non adoptée). Montants de l'abattement des revenus 2025 : 2 822 € jusqu'à 17 670 €, 1 411 € jusqu'à 28 430 € (brochure IR 2026). | **+36 %**. Le modèle suppose que tous les retraités ont 65 ans ou plus et vivent dans des foyers « purs », alors que le VM couvre aussi les invalides : il surestime. | À CORRIGER |
| Salariés : forfait de 500 € au lieu de l'abattement de 10 % (et des frais réels) | 26,5 | 25,73 = 22,98 (étape de la cascade) + 2,75 (frais réels au-delà du forfait, pris dans le résidu) | Le VM classe la déduction de 10 % dans la norme (art. 83-3° CGI) : ce n'est pas une dépense fiscale, et je n'ai trouvé aucun coût publié. Frais réels déclarés en 2024 : 35,3 Md€ et 5,865 M de déclarants (cases 1AK à 1DK, `donnees/ir_2042_cases_revenus2024.csv`). Le modèle cible 36,1 Md€ (+2,3 %) et 5,87 M de déclarants. Bornes de la déduction des revenus 2025 : 509 € / 14 555 € (brochure IR 2026). | Pas de chiffre officiel direct. Le forfait simulé (72,8 Md€) est plausible face à 794,6 Md€ de salaires déclarés. Sans le passage aux 500 €, la mesure isolée vaut 12,0. | COHÉRENT, libellé à préciser |
| Fin de la CSG déductible | 24,81 | 24,08 | Aucun rendement officiel publié trouvé. Le VM ne la classe pas en dépense fiscale. Contrôle de l'assiette : CSG sur les revenus d'activité de 2025 = 110,67 Md€ (CCSS mai 2026, tableau 1), soit 81,8 Md€ de part déductible (6,8/9,2). Modèle : 81,5. | Mesure isolée dans le modèle (droit actuel, QC et QF maintenus) : **15,2**. Les 24,1 viennent de l'ordre de la cascade : l'étape est calculée après la fin du QC et du QF, qui relève les taux marginaux. | NON VÉRIFIABLE (ordre de grandeur cohérent) |
| Impôt individuel : fin du quotient conjugal | 12,48 | 12,12 | Cour des comptes, ROD « La prise en compte de la famille dans la fiscalité », 19/10/2023 : **11,06 Md€ (2021, IR + CEHR)**. Source secondaire (IFRAP), le site de la Cour est inaccessible. Insee, Économie et statistique n° 526-527 (2021) : environ 10 Md€. | +10 % en € 2025 (base 2021) ; mesure isolée : 11,42 (+3 %) | COHÉRENT |
| Fin du quotient familial | 16,72 | 16,23 | Même source : **16,54 Md€ (2021)**. QC + QF de la Cour : 27,6 ; QC + QF isolés dans le modèle : 27,66. Le QF du modèle inclut la demi-part des parents isolés (VM n° 110110 : 865 M€). Il est calculé après individualisation, avec les enfants rattachés au parent qui gagne le plus. | −2 % ; mesure isolée : 13,33 | COHÉRENT |
| Franchise de 4 700 € par enfant | −15,57 | −15,12 | Résultat du modèle. | — | COHÉRENT (somme nulle) |
| Baisse des taux (nouveau barème) | −101,05 | −98,10 | Résultat du modèle, solde de la cascade par catégories (`cascade_categories.solde` = 0). | — | COHÉRENT |
| Minimum vieillesse ; contribution sur les hauts revenus | −0,85 | −0,580 (CEHR) − 0,249 (ASPA) | L'ASPA est une dépense sociale (annexe) et non de l'IR : libellé correct, mais rattachement à vérifier. | — | COHÉRENT |
| Recette de référence IR + CSG + CRDS | (229,9) | 86,55 IR barème + 108,50 CSG activité + 26,68 CSG pensions + 0,58 CSG chômage + 7,61 CRDS (`synthese/modele_purs.RECETTES["2025"]`) | IR net 2025 (État, PFU compris) : 94,9 Md€ (VM t. I PLF 2026, prévision révisée) ; le modèle compte 98,99 PFU compris (calage sur l'IR des comptes nationaux avant crédits). CSG 2025, tous affectataires : activité **110,67**, remplacement **28,26** (dont environ 2 Md€ sur les IJ et l'invalidité), capital 17,59 (CCSS mai 2026). CRDS totale 2025 : 9,4 Md€ toutes assiettes (CADES, même rapport ; ventilation non publiée). Recomposition : 94,9 − PFU (≈ 12,4, estimation du modèle) + 110,67 + 28,26 + CRDS hors capital (≈ 8,5, estimation) ≈ 230. | ≈ 0 % au total ; IR +4 %, CSG −2 à −4 % | COHÉRENT |

Les écarts propres au modèle (IR et CSG de chaque étape, mesures isolées) ont été recalculés avec
`calculs/ircsg3_cascade.py` et `ircsg3_droit.py`, sans modification. Script de contrôle :
`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ir/split.py`.
Il reproduit la cascade du JSON : 7,27 / 0,57 / 7,93 / 12,12 / 16,23 / 24,08.

### Points de droit vérifiés (droit actuel = LFI 2026, loi n° 2026-103 du 19/02/2026, texte définitif AN TA n° 227)

- Les suppressions proposées par le PLF 2026 n'ont pas été reprises : TA 227 ne touche ni l'art. 80 quinquies (IJ ALD,
  n° 120204), ni les frais de scolarité (n° 110215, n° 110242), ni l'art. 158-5-a (forfait de 2 000 € sur les pensions),
  ni l'art. 157 bis. Les chiffrages 2026 du VM (4 665 ; 11 ; « - ») intègrent ces mesures non adoptées : la référence
  2025 retenue par le modèle est donc la bonne.
- La réduction pour frais de comptabilité (n° 110211) a été supprimée par la LFI 2025 : le modèle ne la compte pas, à juste titre.
- Le Girardin productif (art. 199 undecies B) s'éteint en 2029 en droit actuel. La LFI 2026 (art. 21) modifie ses
  dérogations mais pas sa date de fin.
- Le PLF 2027 propose de ramener le plafond de l'abattement sur les pensions à 3 000 € (sources de presse, non lues sur
  le texte). Ce n'est pas du droit actuel.

## Corrections recommandées

1. « Autres niches » : le Girardin (0,83 Md€), le Scellier outre-mer et le logement social outre-mer prennent fin avant 2032 en droit actuel. Ligne à ramener à **2,33** (−0,90), ou garder 3,23 en disant que le modèle suppose leur prorogation. C'est incohérent avec le Pinel, compté sans recette.
2. Abattement de 10 % sur les pensions : 7,49 contient 1,37 Md€ de CSG (effet du RFR sur les taux). Écrire « 6,1 d'IR + 1,4 de CSG » ou déplacer ces 1,4 vers la ligne CSG (9,5). Coût officiel : 5,3 Md€ (VM 2025), 5,0 selon l'IPP.
3. Abattement des personnes âgées : caler sur le VM (0,419 → **0,43** en € 2026, au lieu de 0,59), ou dire que le modèle traite tous les retraités comme âgés de 65 ans ou plus.
4. Ligne « forfait » : la libeller « forfait de 500 € au lieu de l'abattement de 10 % et des frais réels ». Dans `ircsg4.json`, l'étape `forfait` s'appelle encore « Forfait de 10 % (frais réels gardés) » alors qu'elle chiffre l'option `forfait_seul_500`.
5. CSG déductible (24,8) : préciser que le montant dépend de l'ordre de la cascade (15,7 en mesure isolée), et qu'aucun rendement officiel n'est publié.
6. QC / QF : citer la Cour des comptes (2023, chiffres 2021 : 11,1 et 16,5 Md€) comme repère, en signalant que le QF du modèle inclut la demi-part des parents isolés.
7. Hors bilan : `annexe_ircsg.tex` n'est plus synchrone avec le JSON (franchise de 6 000 € contre 4 700 € ; financement de 5,87 Md€ contre 0 ; barème −100,6 contre −98,1).
8. Les écarts des points 1 à 3 (environ −1,0 Md€ de recette en 2032) se reportent sur le barème : à recalculer par le modèle, pas à la main.

## Sources lues

- Voies et moyens, t. II, PLF 2026, copie texte :
  `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/vm/vm.txt`. Fiches lues :
  110246, 120108, 120146, 110201, 110203, 110102, 110103, 110107, 110110, 110224, 110259, 110256, 110302, 110202,
  110223, 110211, 110215, 110242, 120204, 120401, 100201 ; norme de l'IR p. 7 ; sous-partie IV.
- Voies et moyens, t. I, PLF 2026 (IR net 2025 : 94,9 Md€), copie :
  `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/inv_vmt1_2026/vmt1.txt`.
- LFI 2026, texte définitif : https://www.assemblee-nationale.fr/dyn/17/textes/l17t0227_texte-adopte-provisoire.pdf ; dossier : https://www.senat.fr/dossier-legislatif/pjlf2026.html
- Brochure IR 2026 : https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2026/pdf_som/07-pensions_115a120.pdf et https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2026/pdf_som/aide_memoire.pdf
- Service-public, CSG sur les pensions : https://www.service-public.gouv.fr/particuliers/vosdroits/F2971
- IPP, Notes n° 129 (sept. 2026) : https://www.ipp.eu/wp-content/uploads/2026/09/Note_contribution_retraites_129.pdf
- CCSS, mai 2026 (CSG par assiette, CRDS) : https://www.securite-sociale.fr/files/live/sites/SSFR/files/medias/CCSS/2026/CCSS%20mai%202026_assembl%C3%A9_V2.pdf
- CPO, *L'impôt sur le revenu, ses réductions et crédits d'impôt depuis 2017*, sept. 2026 (fiches 1 à 3, 5), copie :
  `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/cpo/cpo.txt`.
- QC / QF, source secondaire (IFRAP, 25/03/2024, citant la Cour des comptes, ROD du 19/10/2023) : https://www.ifrap.org/budget-et-fiscalite/non-les-quotients-conjugaux-et-fiscaux-ne-sont-pas-des-niches-fiscales-cachees
- CSG non déductible, ordre de grandeur (IFRAP 2023, données 2021 : environ 2 Md€ pour rendre déductibles les 2,4 points) : https://www.ifrap.org/budget-et-fiscalite/pourquoi-il-faut-rendre-la-csg-totalement-deductible-de-lir-sur-les-revenus-dactivite
- Statut de l'abattement sur les pensions, des IJ ALD et des frais de scolarité dans la LFI 2026, confirmé aussi par la presse (secondaire) : https://www.previssima.fr/actualite/loi-finance-2026-changements-entreprises-particuliers.html ; https://www.lafinancepourtous.com/2026/02/23/fiscalite-nouveautes-2026-pour-les-particuliers/

Non vérifié : le rapport de la Cour des comptes de 2023 lui-même (ccomptes.fr inaccessible) ; le coût de la déduction
forfaitaire de 10 % (non publié) ; la ventilation de la CRDS par assiette ; les composantes à 0,015 (« IJ AT-MP ») et
0,020 (« Girardin ») de `ircsg4_donnees.py`, que je n'ai pas identifiées dans le VM.
