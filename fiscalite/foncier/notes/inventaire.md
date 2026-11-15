# Inventaire des prélèvements assis sur l'immobilier en France (état des lieux chiffré)

Collecte du 15/11/2026, pour la partie « état des lieux » de la note sur la réforme de la fiscalité immobilière.
Ce document complète `../../lvt/notes/france_institutions_chiffres.md` (TFPB, valeurs locatives, révisions, DMTO),
dont les constats ne sont pas repris ici, et respecte les règles de `../../CLAUDE.md`.

**Statuts.** [TEXTE LU] : chiffre ou règle lu dans le document primaire téléchargé (PDF, xlsx, page officielle).
[RÉSUMÉ] : page officielle lue seulement à travers le résumé d'un moteur de recherche. [SECONDAIRE] : presse ou
site spécialisé, non recoupé avec le texte. [NON VÉRIFIÉ] : non confirmé, ou calcul de l'auteur (signalé « calcul »).

**Légifrance est inaccessible depuis l'environnement (erreur 403).** Les articles du CGI ont donc été vérifiés à
travers le BOFiP, les pages de la DGCL, les réponses ministérielles et les documents budgétaires, jamais sur le texte
consolidé. Tout article cité sans autre source est à relire sur Légifrance.

**Quatre familles de sources, quatre périmètres.** On ne compare pas sans précaution :
- le **REI** (DGFiP-DGCL) : rôles généraux primitifs, avant dégrèvements et rôles supplémentaires (note REI 2025,
  note 2) ;
- les **comptes de gestion** (OFGL-DGCL) : recettes encaissées par les collectivités, y compris la fiscalité
  indirecte (DMTO, taxe d'aménagement) ;
- les **données budgétaires DGFiP** (*DGFiP Statistiques* n° 43) : encaissements de l'année, nets de remboursements,
  « et non ceux dus au titre de cette période » (encadré 1) ;
- la **comptabilité nationale** (liste nationale des impôts transmise à Eurostat, OCDE, Compte du logement) : le
  Compte du logement ne retient que les logements.

---

## 1. Tableau récapitulatif

Rendements en millions d'euros courants, année la plus récente disponible (2025 si publiée). Le même tableau est dans
`../donnees/inventaire.csv`.

| Famille | Prélèvement | Assiette | Taux | Redevable | Bénéficiaire | Rendement (M€) | Année | Source | Statut |
|---|---|---|---|---|---|---:|---|---|---|
| Détention | Taxe foncière sur les propriétés bâties (TFPB), total | Revenu cadastral = 50 % de la VLC (tarifs 1970 ; locaux pro révisés en 2017) | Voté ; moyen communal 37,18 % | Propriétaire au 1er janvier | Communes, EPCI, syndicats | 43 131 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 1 | TEXTE LU |
| Détention | TFPB, part « ménages » (clé 61 %) | id. | id. | Ménages | id. | 26 310 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 4 | TEXTE LU (clé conventionnelle) |
| Détention | TFPB, part « entreprises » (clé 39 %) | id. | id. | Entreprises et autres | id. | 16 821 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 11 | TEXTE LU (clé conventionnelle) |
| Détention | TFPB sur les seuls logements | id., logements | id. | Propriétaires de logements (ménages, HLM, sociétés) | id. | 31 590 | 2025 | SDES, Rapport du compte du logement 2025 (14/09/2026), fig. 6.1 | TEXTE LU |
| Détention | TFPB hors logements (par différence) | id., locaux non résidentiels | id. | Surtout entreprises | id. | 11 541 | 2025 | Calcul : REI 2025 − CSL 2025 | NON VÉRIFIÉ (calcul, périmètres différents) |
| Détention | Taxe foncière sur les propriétés non bâties (TFNB), y.c. taxe additionnelle | VLC des terrains (bases 1961) ; terres agricoles exonérées à 30 % depuis 2025 | Voté | Propriétaire au 1er janvier | Communes (≈77 %), EPCI | 1 196 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 1 | TEXTE LU |
| Détention | Taxe d'habitation sur les résidences secondaires (THRS) | VLC des locaux meublés non affectés à l'habitation principale | Voté ; moyen bloc communal 24,14 % | Personne disposant du local au 1er janvier | Communes, EPCI | 2 610 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), p. 3 | TEXTE LU |
| Détention | Majoration de THRS (zones tendues) | Cotisation de THRS | +5 % à +60 % ; 1 629 communes sur 3 690 éligibles | id. | Communes | 391 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), p. 3-4 | TEXTE LU |
| Détention | TH sur les logements vacants (THLV) | VLC des logements vacants (hors zone TLV) | Taux de TH, sur délibération | Propriétaire | Communes, EPCI | 127 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), p. 3 | TEXTE LU |
| Détention | Taxe sur les logements vacants (TLV) | VLC des logements vacants depuis 1 an (zone tendue) | 17 % puis 34 % (depuis 2023) | Propriétaire | État ; TVLH communale à partir de 2027 | 80 | 2022 | CPO, Pour une fiscalité du logement plus cohérente (déc. 2023), p. 23 | TEXTE LU (rendement 2024-2025 NON VÉRIFIÉ) |
| Détention | Taxe d'enlèvement des ordures ménagères (TEOM) | Base de la TFPB (non relu sur le texte) | Voté ; moyen 9,54 % | Redevables de la TFPB | EPCI (93 %), communes, syndicats | 9 234 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 1 | TEXTE LU (assiette NON VÉRIFIÉE) |
| Détention | Taxe GEMAPI | Produit voté, réparti sur TF, THRS et CFE (non relu) | Plafond 40 €/habitant | id. | EPCI | 588 | 2025 | OFGL-DGCL, Rapport 2026, annexe 8, tableau 2 | TEXTE LU (plafond : RÉSUMÉ) |
| Détention | Taxe additionnelle spéciale annuelle (TASA) | Additionnelle (non relu) | — | — | Région Île-de-France | 77 | 2025 | OFGL-DGCL, Rapport 2026, annexe 8, tableau 2 | TEXTE LU |
| Détention | Taxes spéciales d'équipement (TSE), opérateurs de l'État et SGP | Additionnelles aux TF, THRS et CFE | Montant voté (plafond 20 €/hab. : non relu) | Redevables de ces taxes | EPF d'État, SGP, agences | 390 | 2027 (prévision) | PLF 2027 (n° 3210), art. 42, colonne E (somme) | TEXTE LU (périmètre partiel : hors EPF locaux) |
| Détention | Impôt sur la fortune immobilière (IFI) | Patrimoine immobilier net > 1,3 M€ (abattement 30 % sur la résidence principale) | 0,5 % à 1,5 % | Foyers (193 600 en 2025) | État | 2 770 | 2025 | DGFiP Statistiques n° 43 (mars 2026), tableau 1 (encaissements) | TEXTE LU |
| Détention | Taxe sur les bureaux, commerces, stockage et stationnement en Île-de-France (TSBCS) | Surfaces taxables au 1er janvier | Tarif au m² par circonscription | Propriétaire (non relu) | SGP, Région Île-de-France | 1 055 | 2024 | Eurostat, National Tax List France (21/07/2026), D29A-C16 | TEXTE LU (contenu de la ligne NON VÉRIFIÉ) |
| Détention | Cotisation foncière des entreprises (CFE) | VL des biens passibles de TF utilisés pour l'activité en N-2 | Voté ; moyen EPCI 26,96 % ; base minimum | Entreprises | Bloc communal (EPCI 93 %) | 8 381 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 1 | TEXTE LU |
| Détention (connexe) | Taxe sur les surfaces commerciales (Tascom) | Surface de vente (non relu) | Tarif au m² | Exploitants | EPCI | 976 | 2025 | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), annexe 1 | TEXTE LU |
| Détention (connexe) | Taxe pour frais de chambres d'agriculture | Additionnelle à la TFNB (non relu) | — | Propriétaires de terrains | Chambres d'agriculture | 303 | 2024 | OCDE, DF_REVFRA (4110 + 4120) | TEXTE LU |
| Détention (connexe) | Taxes additionnelles à la CFE (CCI, chambres de métiers) | Base de CFE (non relu) | — | Entreprises | CCI, CMA | 739 | 2024 | Eurostat, National Tax List France (21/07/2026), D29A-C13 et C14 | TEXTE LU (rattachement NON VÉRIFIÉ) |
| Transactions | Droits de mutation à titre onéreux (DMTO), total collectivités | Prix ou valeur vénale de l'immeuble | Part dép. 3,80 % (1,20-4,50 % ; ≤ 5 % du 1/4/2025 au 31/3/2028) + 1,20 % communal | Acquéreur | Départements, communes, Région Île-de-France | 16 703 | 2025 | OFGL-DGCL, Rapport 2026, annexe 8, tableau 1 | TEXTE LU |
| Transactions | DMTO, part départementale (y.c. Paris, Lyon, CTU) | id. | 4,50 % à 5 % (88 collectivités sur 100 à 5 % au 1/6/2026) | Acquéreur | Départements | 13 500 | 2025 (provisoire) | DGCL-DGFiP, Note d'analyse REI 2025 (mai 2026), encadré DMTO p. 8 | TEXTE LU |
| Transactions | DMTO, taxe additionnelle communale (hors péréquation) | id. | 1,20 % | Acquéreur | Communes ; fonds départemental de péréquation | 2 700 | 2023 | Réponse à la QE AN n° 4482 (JO 3/06/2025) | TEXTE LU |
| Transactions | Frais d'assiette et de recouvrement sur les DMTO | Droit départemental | 2,37 % | Acquéreur | État | 320 | 2025 | Calcul : 2,37 % × 13,5 Md€ (taux : CPO 2023) | NON VÉRIFIÉ (calcul) |
| Transactions | Contribution de sécurité immobilière (CSI) | Prix ou valeur des actes publiés | 0,10 % | Acquéreur | État | 692 | 2024 | Eurostat, National Tax List France (21/07/2026), D214B-C01 | TEXTE LU |
| Transactions | TVA sur les logements neufs | Prix de vente des logements neufs | 20 % ; 10 % et 5,5 % (logement social et assimilé) | Vendeur assujetti (charge : acquéreur) | État (fractions aux collectivités et à la Sécurité sociale) | 5 369 | 2025 | SDES, Rapport du compte du logement 2025 (14/09/2026), fig. 6.1 | TEXTE LU |
| Transactions | TVA sur les terrains à bâtir (non récupérée) | Prix des terrains à bâtir | Taux normal (régime de la marge non relu) | Vendeur assujetti | id. | 789 | 2025 | SDES, Rapport du compte du logement 2025 (14/09/2026), fig. 6.1 | TEXTE LU |
| Transactions | Imposition des plus-values immobilières des particuliers (IR, PS, surtaxe) | Plus-value après abattements pour durée (résidence principale exonérée) | IR 19 % + PS 17,2 % ; exonération après 22 ans (IR) et 30 ans (PS) | Vendeur particulier | Sécurité sociale (≈ 2/3), État (≈ 1/3) | 2 800 | 2024 | Cour des comptes, audition AN commission des finances, CR n° 43 (25/11/2025) | TEXTE LU |
| Transactions | dont surtaxe sur les plus-values élevées (art. 1609 nonies G) | Plus-values > 50 000 € (hors terrains à bâtir) | 2 % à 6 % | Vendeur | État | 106 | 2023 | Cour des comptes, audition AN commission des finances, CR n° 43 (25/11/2025) | TEXTE LU |
| Transactions | Taxes sur la cession de terrains devenus constructibles (art. 1529 et 1605 nonies) | Plus-value de première cession | 1529 : 10 % (communal) ; 1605 nonies : 5 % ou 10 % | Vendeur | Communes ; ASP (1605 nonies) | 20 | 2022 | CPO, Pour une fiscalité du logement plus cohérente (déc. 2023), p. 19 | TEXTE LU (1605 nonies seule : 17 M€ prévus en 2027) |
| Transmissions | Droits de mutation à titre gratuit (successions et donations) | Part nette de chaque ayant droit après abattements | Ligne directe : 5 % à 45 %, abattement 100 000 € par enfant | Héritiers et donataires | État | 21 180 | 2025 | DGFiP Statistiques n° 43 (mars 2026), tableau 1 | TEXTE LU (barème : RÉSUMÉ) |
| Transmissions | DMTG, part due à l'immobilier (estimation) | id. | id. | id. | État | 12 700 | 2025 | Calcul : 60 % (approximation CPO 2023, note 7) × 21,18 Md€ | NON VÉRIFIÉ (aucune ventilation DGFiP) |
| Revenus | Impositions des revenus locatifs des logements (IR, IS, CSG-CRDS-PS, CRL) | Revenus fonciers et loyers nets des avantages fiscaux | IR au barème + PS 17,2 % ; IS | Bailleurs | État, Sécurité sociale | 8 678 | 2025 | SDES, Rapport du compte du logement 2025 (14/09/2026), fig. 6.1 | TEXTE LU (logements seuls) |
| Revenus | Contribution sur les revenus locatifs (CRL) | Loyers perçus par certaines personnes morales (non relu) | Non relu | Personnes morales bailleresses | État | 511 | 2024 | Eurostat, National Tax List France (21/07/2026), D214H-C04 | TEXTE LU (montant seul) |
| Construction | Taxe d'aménagement (TA) | Surface de plancher × valeur forfaitaire (914 €/m², 1 036 € en Île-de-France) | Communal 1-5 % (jusqu'à 20 %) ; dép. ≤ 2,5 % ; IdF ≤ 1 % | Bénéficiaire de l'autorisation d'urbanisme | Bloc communal (≈61 %), départements (≈36 %), Région IdF (≈3 %) | 1 600 | 2024 (liquidé) | AN, rapport d'information n° 1594 (18/06/2025), p. 92-96 | TEXTE LU (encaissé : 1 366 en 2024, 782 en 2025) |
| Construction | Redevance d'archéologie préventive (RAP) | Part logement : base de la TA ; part culture : m² de terrain | 0,40 % ; 0,71 €/m² (2025) | Aménageur | État | 96,5 | 2024 | AN, rapport d'information n° 1594 (18/06/2025), p. 98 | TEXTE LU |
| Total de référence | Prélèvements fiscaux relatifs au logement (Compte du logement) | — | — | — | — | 103 429 | 2025 | SDES, Rapport du compte du logement 2025 (14/09/2026), fig. 6.1 | TEXTE LU |
| Total de référence | Fiscalité du logement, périmètre « cycle de vie » | — | — | — | — | 91 500 | 2022 | CPO, Pour une fiscalité du logement plus cohérente (déc. 2023), p. 18 | TEXTE LU |
| Total de référence | OCDE 4100, impôts périodiques sur la propriété immobilière (1,95 % du PIB) | — | — | — | — | 56 841 | 2024 | OCDE, Revenue Statistics, DF_REVFRA | TEXTE LU |
| Total de référence | OCDE 4400, impôts sur les transactions mobilières et immobilières (0,62 % du PIB) | — | — | — | — | 18 222 | 2024 | OCDE, Revenue Statistics, DF_REVFRA | TEXTE LU |

**Ordre de grandeur agrégé, 2024 (calcul de l'auteur, périmètres hétérogènes)** : détention ≈ 69 Md€ (dont CFE
8,0 et TEOM 9,0) ; transactions ≈ 25 Md€ (DMTO 14,1, TVA sur le neuf et les terrains 7,1, plus-values 2,8, CSI 0,7,
frais d'assiette 0,3) ; transmissions ≈ 12,5 Md€ pour la part immobilière estimée des DMTG (20,9 Md€ au total) ;
revenus ≈ 8,4 Md€ (logements seuls) ; construction ≈ 1,5 Md€ (TA encaissée 1,37 et RAP 0,1). Total ≈ 116 Md€,
soit environ 4,0 % du PIB 2024 (2 935 Md€). Sans la CFE ni la TEOM, ≈ 99 Md€. [NON VÉRIFIÉ (calcul)]

---

## 2. Détention

### 2.1 Taxe foncière sur les propriétés bâties

**Rendement.** REI 2025, annexe 1 : 41 964 M€ en 2024 et **43 131 M€ en 2025** (+2,8 %) [TEXTE LU]. Les comptes de
l'OFGL donnent le même ordre : foncier bâti du secteur communal 41 946 M€ (2024) et 43 113 M€ (2025), plus un effet net
des coefficients correcteurs de 763 et 769 M€ (Rapport OFGL 2025 et 2026, annexe 8, tableau 1) [TEXTE LU]. En
comptabilité nationale, la ligne « Foncier bâti » vaut 42 059 M€ en 2024 (liste nationale des impôts, D29A-C03), et
l'OCDE la répartit en 26 118 M€ payés par les ménages et 15 941 M€ par les autres agents (DF_REVFRA, code L_3516)
[TEXTE LU]. Les données budgétaires de la DGFiP regroupent « taxes foncières et taxes annexes » : 53,27 Md€ en 2024 et
54,85 Md€ en 2025, soit TFPB, TFNB, TEOM, GEMAPI, TSE et taxes additionnelles confondues (*DGFiP Statistiques* n° 43,
tableau 1) [TEXTE LU].

**Bénéficiaires.** Depuis 2021, les départements ne perçoivent plus de TFPB (14 314 M€ en 2020, zéro ensuite : Rapport
OFGL 2026, annexe 8, tableau 2) ; leur part a été transférée aux communes, avec un coefficient correcteur. En 2025, les
communes perçoivent 40 275 M€, les EPCI 2 654 M€ et les syndicats 184 M€ [TEXTE LU].

**Assiette et taux.** Voir la note `france_institutions_chiffres.md` (§ 2) : revenu cadastral égal à la moitié de la
VLC, tarifs de 1970 pour l'habitation, révision des locaux professionnels en 2017, revalorisation forfaitaire de 1,7 %
en 2025 et 0,8 % en 2026. Taux moyen communal : 37,16 % (2024) et 37,18 % (2025), rapporté à la base communale
(REI 2025, p. 2) [TEXTE LU].

**Habitation contre locaux professionnels.** Aucune source ne ventile directement le produit selon la nature du local.
Deux approches indirectes :
- le Compte du logement isole la TFPB sur les logements : 30 489 M€ en 2024 et **31 590 M€ en 2025**, nette des
  exonérations des logements neufs et sociaux, champ France entière [TEXTE LU]. Par différence avec le REI, la TFPB
  hors logements vaudrait environ 11,5 Md€, soit 27 % du total, en 2024 comme en 2025 [NON VÉRIFIÉ (calcul) : le REI
  porte sur les rôles primitifs, le Compte du logement sur la comptabilité nationale] ;
- la ventilation « ménages/entreprises » du REI applique une clé **conventionnelle** : 60/40 pour 2024, 61/39 pour
  2025, « calcul INSEE » (REI 2025, notes 11 et 57) [TEXTE LU]. Elle ne mesure pas l'usage du local : une HLM ou une
  société foncière qui possède des logements est comptée hors ménages. La comptabilité nationale donne 62/38 en 2024
  (26 118/15 941) [calcul sur TEXTE LU].

### 2.2 Taxe foncière sur les propriétés non bâties

1 305 M€ en 2024 et **1 196 M€ en 2025** (−8,4 %), taxe additionnelle comprise (OFGL 2026, annexe 8, tableau 1 ;
REI 2025, annexe 1) [TEXTE LU]. La baisse vient de l'art. 66 de la LF 2025, qui porte l'exonération des terres
agricoles de 20 à 30 %. L'exonération est compensée à hauteur de 101,7 M€ en 2025 (REI 2025, p. 3). Part « ménages »
729 M€, part « entreprises » 466 M€ (clé conventionnelle). L'OCDE retient 1 181 M€ pour 2024 ; la liste nationale des
impôts ne porte que 883 M€ en D29A, sous l'intitulé « Foncier non-bâti (partie) », le reste étant classé ailleurs
[TEXTE LU ; écart de classement non élucidé]. S'y ajoute la taxe pour frais de chambres d'agriculture : 303 M€ en 2024
(OCDE, L_3520) [TEXTE LU]. L'abattement légal sur la VLC des terrains n'a pas été relu [NON VÉRIFIÉ].

### 2.3 Taxe d'habitation : résidences secondaires, majoration, logements vacants

| M€ | 2024 | 2025 | Source |
|---|---:|---:|---|
| THRS, communes | 2 226 | 1 749 | REI 2025, tableau p. 3 |
| THRS, EPCI | 1 046 | 861 | id. |
| Majoration de THRS (communes) | 436 | 391 | id. |
| THLV (communes et EPCI) | 177 | 127 | id. |
| Total TH, syndicats compris | 3 901 | 3 141 | REI 2025, annexes 1 et 4 |

[TEXTE LU]. La baisse de 19,5 % en 2025 tient à la fiabilisation des déclarations d'occupation dans « Gérer mes biens
immobiliers » et à l'art. 110 de la LF 2025, qui recentre la THRS sur les seuls locaux meublés à usage d'habitation
(REI 2025, p. 3). Taux moyen de THRS du bloc communal : 24,41 % en 2024 et 24,14 % en 2025 (p. 4). La majoration en
zone tendue, de 5 % à 60 %, est ouverte aux 3 690 communes du champ de la TLV depuis le décret n° 2023-822 du 25 août
2023 ; 1 629 l'appliquent en 2025, dont 657 au taux de 60 % [TEXTE LU].

**Pièges.** Le Compte du logement retient une THRS de 2 971 M€ (2024) et 2 798 M€ (2025), et la comptabilité
nationale une taxe d'habitation de 3 317 M€ en 2024 (OCDE, « Council tax » ; liste nationale, D59A-C04 et C05),
contre 3 901 M€ au REI [TEXTE LU]. Une partie de l'écart tient sans doute aux dégrèvements, que le REI ne déduit pas
[NON VÉRIFIÉ]. La DGFiP publie « taxe d'habitation et taxes annexes » : 4,53 Md€ encaissés en 2024 et 3,84 Md€ en 2025,
dont 1 % pour l'État en 2025 (*DGFiP Statistiques* n° 43) [TEXTE LU].

### 2.4 Taxe sur les logements vacants (TLV) et future taxe sur la vacance (TVLH)

- **TLV** (art. 232 CGI) : due de plein droit dans les communes de la zone tendue, sur les logements vacants depuis au
  moins un an. Taux de 17 % la première année et 34 % ensuite depuis 2023 (impots.gouv.fr et service-public.fr)
  [RÉSUMÉ]. Le produit va au budget de l'État (REI 2025, note 29) [TEXTE LU].
- **Rendement, non établi au-delà de 2022.** Le CPO l'évalue à environ 80 M€ en 2022 (p. 23) [TEXTE LU]. Le Compte du
  logement publie la somme TLV + THLV : 160 M€ en 2022, 367 M€ en 2023, 426 M€ en 2024 et 202 M€ en 2025 (série T321)
  [TEXTE LU]. Une fois la THLV retranchée (OFGL : 83, 139, 178 et 128 M€), il resterait 77, 228, 248 et 74 M€ de TLV
  [NON VÉRIFIÉ (calcul, deux sources)]. La part de l'État dans la « TH et taxes annexes » de la DGFiP suggérerait plutôt
  une quarantaine de millions en 2025 (1 % de 3,84 Md€) [NON VÉRIFIÉ (calcul)].
- **TVLH à partir du 1er janvier 2027.** Le PLF 2027 (exposé de l'article sur les prélèvements sur recettes) supprime
  deux compensations de 36,7 M€ « en cohérence avec l'entrée en vigueur de la taxe sur la vacance des locaux
  d'habitation (TVLH) au 1er janvier 2027, dont le rendement revient entièrement aux communes » [TEXTE LU]. Selon
  Légifiscal [SECONDAIRE], elle est créée par l'art. 108 de la LF 2026 et codifiée à l'art. 1406 bis du CGI. Elle
  remplace la TLV et la THLV, sur la VLC. En zone tendue, elle s'applique de plein droit aux logements vacants depuis
  un an, aux taux de 17 % puis 34 %, que la commune peut porter à 30 % puis 60 %. Hors zone tendue, elle est
  facultative, au taux de 50 % au plus, sur les logements vacants depuis deux ans. **Droit 2027, à relire sur le
  texte.**

### 2.5 Taxe d'enlèvement des ordures ménagères

8 996 M€ en 2024 et **9 234 M€ en 2025**, dont 5 633 M€ de part « ménages » et 3 601 M€ de part « entreprises » (clé
conventionnelle) ; taux moyen national 9,57 % puis 9,54 %. La taxe est facultative ; les EPCI en perçoivent 93 %
(REI 2025, p. 2-5 et annexe 1) [TEXTE LU]. **Piège de classement** : la comptabilité nationale traite la TEOM comme une
vente de service et non comme un impôt depuis la base 95 (Compte du logement 2025, « Concepts et méthodes », p. 82).
Elle est donc absente de la liste nationale des impôts et du Compte du logement, et le CPO l'exclut de la fiscalité du
logement (p. 23). L'OCDE la compte au contraire dans la catégorie 4100 : 9 428 M€ en 2024 (« Waste collection tax »)
[TEXTE LU]. Le fait qu'elle soit assise sur la base de la TFPB n'a pas été relu sur le texte [NON VÉRIFIÉ].

### 2.6 Taxe GEMAPI, TASA, taxes spéciales d'équipement

- **GEMAPI** (gestion des milieux aquatiques et prévention des inondations) : 458 M€ en 2023, 546 M€ en 2024,
  **588 M€ en 2025** (OFGL 2026, annexe 8, tableau 2) [TEXTE LU] ; 532 M€ en 2024 selon la comptabilité nationale
  (D29A-C18). Le produit, facultatif, est voté par l'EPCI dans la limite de 40 € par habitant (art. 1530 bis CGI,
  DGCL) [RÉSUMÉ].
- **TASA** (Région Île-de-France) : 77 M€ par an depuis 2021 (même tableau) [TEXTE LU]. Le REI ne retient ni la GEMAPI
  ni la TASA (661 M€ à elles deux en 2025, REI note 4).
- **TSE.** Aucun total national trouvé. Le PLF 2027 (art. 42, colonne E « rendement prévisionnel en 2027 ») liste les
  TSE affectées aux opérateurs de l'État [TEXTE LU] : EPF d'Île-de-France 139,1 M€, Provence-Alpes-Côte d'Azur 45,5,
  Occitanie 32,1, Nouvelle-Aquitaine 23,7, Ouest Rhône-Alpes 19,8, Hauts-de-France 14,6, Grand-Est 12,0,
  Normandie 10,7, Bretagne 8,3, Vendée 7,9, Guyane 3,9, Mayotte 2,8, agences des 50 pas géométriques 2,7, Société des
  grands projets (art. 1609 G) 67,1. Total ≈ **390 M€** [calcul]. **Il manque les TSE des établissements publics
  fonciers locaux**, non plafonnées, que ce tableau n'inclut pas [NON TROUVÉ]. Une question écrite mentionne un
  plafond de 20 € par habitant [SECONDAIRE, non relu].

### 2.7 Impôt sur la fortune immobilière

| | 2024 | 2025 | Source |
|---|---:|---:|---|
| IFI payé (avis émis au 1er janvier), M€ | 2 159 | 2 332 | *DGFiP Statistiques* n° 45 (avril 2026), tableau 1 |
| Foyers imposables | 186 100 | 193 600 | id. |
| Patrimoine net imposable, Md€ | 466,8 | 492,8 | id. |
| Encaissements budgétaires, Md€ | 2,74 | 2,77 | *DGFiP Statistiques* n° 43, tableau 1 |

[TEXTE LU]. Les Voies et moyens (PLF 2026, tome I, p. 24) donnent 2 739 M€ de recettes en 2024, 2 965 M€ prévus en 2025
et 3 095 M€ en 2026 ; le PLF 2027 (état A, ligne 1406) en prévoit 3 081 M€ pour 2027 [TEXTE LU]. Comptabilité
nationale : 2 678 M€ (2024) ; Compte du logement : 2 644 M€ (2024) et 2 675 M€ (2025). L'écart d'environ 0,5 Md€ entre
l'impôt émis (2,3 Md€) et les encaissements (2,8 Md€) n'est expliqué par aucune source lue ; la DGFiP précise
seulement que la n° 43 porte sur des encaissements et non sur l'impôt dû au titre de l'année [NON VÉRIFIÉ].
**Règles** : seuil de 1,3 M€ de patrimoine immobilier net ; taux de 0 % jusqu'à 0,8 M€, 0,5 % jusqu'à 1,3 M€, puis
progressif jusqu'à 1,5 % au-delà de 10 M€ (CPO, encadré 22, p. 80) ; abattement de 30 % sur la résidence principale ;
barème inchangé depuis 2018 (n° 45) [TEXTE LU]. L'IFI payé représente 0,47 % du patrimoine net imposable ; le
patrimoine brut soumis à l'IFI s'élève à 573 Md€ (n° 45).

### 2.8 Taxe annuelle sur les bureaux en Île-de-France (art. 231 ter CGI)

Rendement total : la comptabilité nationale porte une ligne « Taxe sur construction de bureaux et sur les locaux à
usage de bureaux » de 942 M€ (2022), 1 003 M€ (2023) et **1 055 M€ (2024)** (D29A-C16) [TEXTE LU]. Il n'a pas été
vérifié si cette ligne englobe aussi la taxe sur la création de bureaux (TCBCS) [NON VÉRIFIÉ]. **Répartition** : la
fraction de la Société des grands projets a un rendement prévu de 824,3 M€ en 2027, pour un plafond de 861,4 M€ (PLF
2027, art. 42) ; la Région Île-de-France perçoit 217 M€ en 2024 et 213 M€ en 2025 (« Locaux à usage de bureaux », OFGL
2025 et 2026, annexe 8) [TEXTE LU]. L'assiette porte sur les locaux de bureaux, les locaux commerciaux, les locaux de
stockage et les surfaces de stationnement annexées (intitulé du PLF 2027). Les tarifs au m² et l'extension annoncée
à Provence-Alpes-Côte d'Azur au 1er mars 2026 n'ont pas été relus [NON VÉRIFIÉ ; SECONDAIRE pour la PACA]. S'y ajoute
la taxe sur les surfaces de stationnement (art. 1599 quater C) : 20,4 M€ prévus en 2027, au profit de la SGP (PLF
2027, art. 42) [TEXTE LU].

### 2.9 Cotisation foncière des entreprises

8 031 M€ en 2024 et **8 381 M€ en 2025** (+4,4 %), dont 93 % pour les EPCI (REI 2025, p. 4-5) [TEXTE LU]. **La CFE est
un impôt sur la valeur locative de l'immobilier d'entreprise** : sa base « est calculée par rapport à la valeur
locative des biens immobiliers soumis à la taxe foncière que l'entreprise a utilisés pour son activité professionnelle
lors de l'avant-dernière année (année N-2) » (REI 2025, note 39) [TEXTE LU]. Elle est due par l'utilisateur, qu'il
soit propriétaire ou locataire. La valeur locative des établissements industriels est réduite de moitié depuis la
LF 2021 (art. 29), avec des compensations de 2,1 Md€ pour la CFE et 2,4 Md€ pour la TFPB en 2025. Une base minimum
s'applique (art. 1647 D) ; le taux moyen des EPCI est de 26,96 % [TEXTE LU].
**Pièges** : la comptabilité nationale retient 7 708 M€ en 2024 ; **l'OCDE classe la CFE en 6100 (autres impôts payés
par les entreprises), et non en 4100** (« Property contributions of the corporations », DF_REVFRA) [TEXTE LU]. La DGFiP
publie « CFE et IFER » ensemble : 11,29 Md€ (2024) et 11,53 Md€ (2025) encaissés.

### 2.10 Prélèvements connexes, non comptés dans les totaux

- Tascom (surfaces commerciales) : 1 039 M€ (2024) et 976 M€ (2025) (REI) [TEXTE LU]. Son assiette est la surface de
  vente, non la valeur locative [assiette exacte NON VÉRIFIÉE].
- Taxes additionnelles à la CFE pour les chambres de commerce et de métiers : 525 + 214 = 739 M€ en 2024 (liste
  nationale, D29A-C13 et C14) [TEXTE LU ; rattachement à la CFE NON VÉRIFIÉ].
- IFER : impôt sur les réseaux, non immobilier, exclu (1 988 M€ en 2025).

---

## 3. Transactions

### 3.1 Droits de mutation à titre onéreux

**Structure du droit (en vigueur au 15/11/2026)** :
- part départementale (taxe de publicité foncière ou droit d'enregistrement, art. 1594 D) : 3,80 % par défaut,
  modulable par le conseil départemental entre 1,20 % et 4,50 % (DGCL, page « Droits de mutation ») [TEXTE LU] ;
- taxe additionnelle communale (art. 1584) de 1,20 %, versée directement aux communes de plus de 5 000 habitants ou
  classées stations de tourisme, sinon à un fonds départemental de péréquation (art. 1595 bis) (DGCL ; taux : CPO,
  encadré 4) [TEXTE LU] ;
- prélèvement de l'État pour frais d'assiette et de recouvrement (art. 1647, V-b) : 2,37 % du droit départemental
  (CPO, encadré 4 ; BOFiP BOI-ENR-DMTOI-10-20 § 130 pour le principe) [TEXTE LU] ;
- en Île-de-France, taxe additionnelle de 0,6 % sur les mutations de bureaux, commerces et locaux de stockage, au
  profit de la Région (art. 1599 sexies ; BOFiP § 125) [TEXTE LU] ;
- les logements neufs soumis à la TVA paient un droit réduit de 0,715 % (art. 1594 F quinquies, CPO p. 20)
  [TEXTE LU]. Le taux global dans l'ancien était de 5,81 % avec une part départementale de 4,50 % (CPO) ; il passe à
  6,32 % avec 5 % [calcul : 5 + 1,2 + 2,37 % × 5].

**Le relèvement à 5 % (LF 2025, art. 116)**, d'après le BOFiP BOI-ENR-DMTOI-10-20 du 17/06/2026, § 106-152 [TEXTE LU] :
- les conseils départementaux et la métropole de Lyon peuvent porter le taux au-delà de 4,50 %, dans la limite de 5 %,
  « pour les actes passés et les conventions conclues entre le 1er avril 2025 et le 31 mars 2028 » (A du II) ;
- calendrier modifié par l'art. 121 de la LF 2026 (loi n° 2026-103 du 19 février 2026). Les délibérations notifiées
  au plus tard le 15 avril 2025, entre le 1er décembre 2025 et le 15 avril 2026, puis entre le 1er décembre 2026 et le
  15 avril 2027, s'appliquent le premier jour du deuxième mois suivant la notification. Celles notifiées entre le
  16 avril et le 30 novembre 2027 s'appliquent au 1er janvier 2028. À compter du 1er avril 2028, le taux redevient
  celui en vigueur le 31 janvier 2025 ;
- **primo-accédants : l'exclusion est de droit, pas une option départementale.** Selon le B du II, la hausse « ne
  s'applique pas lorsque le bien immobilier acquis constitue pour l'acquéreur une première propriété au sens du I de
  l'article L. 31-10-3 » du CCH, s'il est destiné à sa résidence principale. Est primo-accédant l'acquéreur qui n'a
  pas été propriétaire de sa résidence principale au cours des deux années précédant l'acte (réponse à la QE AN
  n° 5129, JO du 16/09/2025, p. 8098) [TEXTE LU]. En indivision, l'exclusion vaut pour chaque indivisaire
  primo-accédant à hauteur de sa quote-part ; en communauté, les deux époux doivent remplir la condition (même
  réponse). Deux sources secondaires officielles divergent : le Compte du logement 2025 écrit que les départements
  « peuvent également exonérer les primo-accédants » (p. 81), ce qui laisse croire à une option alors que l'exclusion
  est de droit ; service-public.fr (actualité du 2 avril 2025) donne le 30 avril 2028 comme terme, contre le 31 mars
  2028 dans le BOFiP et la réponse ministérielle, qu'on retient ;
- **option distincte (art. 1594 F septies)** : le tableau des taux de la DGFiP comporte une colonne « biens
  constituant une première propriété pour l'acquéreur, taux après réduction ». Au 1er juin 2026, seule la Savoie
  l'utilise, à 4,00 % [TEXTE LU]. Ni la date de création de cet article ni son régime exact n'ont été vérifiés ;
  doctrine.fr indique une modification par la LF 2026 [SECONDAIRE].

**Combien de départements l'appliquent** :
- note REI 2025 (mai 2026, p. 8) : « 80 départements y compris la métropole de Lyon, soit 83 % » ont voté la hausse
  [TEXTE LU, date d'arrêté du décompte non précisée] ;
- tableaux officiels de la DGFiP (impots.gouv.fr, « Taux, abattements et exonérations ») : **86 collectivités sur 100
  au 1er janvier 2026, 88 sur 100 au 1er juin 2026** [TEXTE LU, comptage de l'auteur]. Les 100 lignes regroupent les
  départements, la métropole de Lyon, la Collectivité européenne d'Alsace, la Corse, Paris et les cinq DROM. Restent
  hors hausse au 1er juin 2026 : Hautes-Alpes, Alpes-Maritimes, Ardèche, Charente, Drôme, Lozère, Oise,
  Hautes-Pyrénées, Saône-et-Loire, Guadeloupe et Mayotte (4,50 %), ainsi que l'Indre (3,80 %). Entre le 1er janvier et
  le 1er juin 2026, l'Eure et la Martinique sont passées à 5 %, et Mayotte de 3,80 % à 4,50 %.

**Rendements** (M€) :

| Source et périmètre | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|
| OFGL, total des collectivités (comptes de gestion) | | | 16 311 (calcul) | 14 093 | **16 703** |
| dont départements hors Paris, CTU et métropole de Lyon | | | | 9 857 | 11 868 |
| dont communes (Ville de Paris comprise, part départementale incluse) | | | | 3 803 | 4 325 |
| Départements avec Paris, Lyon et CTU (REI 2025, p. 8 ; QE 4482) | | | 13 000 | 11 100 | 13 500 (prov.) |
| Communes, hors péréquation (QE 4482) | 3 400 | 3 500 | 2 700 | | |
| Compte du logement, DMTO sur les logements | 16 418 | 16 818 | 13 002 | 11 239 | 13 568 |
| Comptabilité nationale, « droits d'enregistrement (y compris taxe additionnelle) » | 21 007 | 21 605 | 16 843 | 14 663 | |
| DGFiP, « DMTO et droits d'enregistrement » (encaissements, part État 11 %) | | | | 16 260 | 19 180 |

[TEXTE LU, sauf la ligne 2023 de l'OFGL, déduite de l'évolution de −13,6 % ; sources : Rapport OFGL 2025 et 2026,
annexe 8, tableau 1 ; réponse à la QE n° 4482 ; Compte du logement 2025, série T321 ; liste nationale des impôts ;
*DGFiP Statistiques* n° 43]. La note REI 2025 donne aussi 16 Md€ pour les DMTO communaux et départementaux de 2025,
arrêtés au 28 février 2026 (note 7).
**Pièges** : dans les tableaux de l'OFGL, la colonne « communes » inclut la Ville de Paris, y compris sa part
départementale, et la colonne « GFP » la métropole de Lyon ; la colonne « régions et CTU » mêle les CTU (Corse,
Martinique, Guyane) et la taxe additionnelle de la Région Île-de-France. Le Compte du logement ne retient que les
logements : par différence, les DMTO sur les autres biens (locaux, terrains) représenteraient environ 3,1 Md€ en 2025
[NON VÉRIFIÉ (calcul)]. La série « droits d'enregistrement » de la comptabilité nationale inclut des droits sans lien
avec l'immobilier (fonds de commerce, actes civils).

### 3.2 Frais d'assiette de l'État sur les DMTO

Aucune source ne les isole : la ligne 2303 des Voies et moyens (950 M€ en 2024) regroupe tous les frais d'assiette sur
des impositions affectées à des tiers (PLF 2026, tome I, p. 55-56) [TEXTE LU]. À 2,37 % de la part départementale, ils
vaudraient environ 263 M€ en 2024 et 320 M€ en 2025 [NON VÉRIFIÉ (calcul)].

### 3.3 Contribution de sécurité immobilière

Taux de 0,10 % du prix (CPO, encadré 4) [TEXTE LU] ; due depuis le 1er janvier 2013, en remplacement du salaire du
conservateur des hypothèques (Compte du logement 2025, p. 81) ; recette de l'État. Rendement en comptabilité nationale
(D214B-C01) : 898 M€ (2021), 922 (2022), 783 (2023), **692 M€ (2024)** ; le PLF 2027 en prévoit 790 M€ pour 2027 (état
A, ligne 1707) [TEXTE LU]. Sur les seuls logements : 239 M€ (2024) et 289 M€ (2025) au Compte du logement, 360 M€
(2022) au CPO. L'état A comporte aussi deux lignes de l'État : 1713 « Taxe de publicité foncière » (626 M€ prévus en
2027) et 1704 « Mutations à titre onéreux d'immeubles » (97 M€). Leur contenu n'a pas été vérifié.

### 3.4 TVA sur le neuf, les terrains et les services liés

Compte du logement 2025 (série T321, M€) [TEXTE LU] :

| | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|
| TVA sur les logements neufs | 7 749 | 7 511 | 6 163 | 5 369 |
| TVA sur les terrains à bâtir (non récupérée) | 1 260 | 1 205 | 965 | 789 |
| TVA sur les gros travaux d'entretien et d'amélioration | 5 231 | 5 546 | 5 664 | 5 674 |
| TVA sur les frais d'agence et de notaire | 2 087 | 1 639 | 1 394 | 1 625 |

Taux de 20 % sur la livraison d'immeubles neufs (CPO, p. 21 et 29) ; taux réduits de 10 % et 5,5 % pour le logement social et
assimilé, qui représentaient en 2022 un coût de 2,0 et 1,0 Md€, pour un rendement de ces taux d'environ 5,3 Md€ (CPO,
p. 22, note 10) [TEXTE LU]. Le régime de TVA des terrains à bâtir (prix total ou marge) n'a pas été relu. **Champ** :
logements seulement. La TVA sur les bâtiments neufs non résidentiels n'a été trouvée dans aucune source.

### 3.5 Plus-values immobilières des particuliers

Cour des comptes, enquête demandée en application du 2° de l'art. 58 de la LOLF, présentée à la commission des
finances de l'Assemblée le 25 novembre 2025 (compte rendu n° 043) [TEXTE LU du compte rendu ; rapport lui-même non
lu, ccomptes.fr étant inaccessible] :
- produit de 4,1 Md€ en 2021, **3,6 Md€ en 2023 et 2,8 Md€ en 2024** ; « les deux tiers de l'imposition des PVI
  financent non le budget de l'État, mais la sécurité sociale » ;
- taux de 36,2 %, soit 19 % d'IR et 17,2 % de prélèvements sociaux. L'exonération est acquise après 22 ans au titre
  de l'IR et 30 ans au titre des PS. Taux effectif : 36,2 % les cinq premières années, 30 % après dix ans, 20 % après
  dix-sept ans, 10 % après vingt-deux ans ;
- **surtaxe sur les plus-values de plus de 50 000 €** (art. 1609 nonies G), de 2 % à 6 % : 106 M€ en 2023 ;
- assiette de 17,7 Md€ en 2022, dont 71 % pour les 20 % de redevables les plus aisés ; environ 300 000 transactions
  imposées en 2024, soit un cinquième ; exonérations ciblées d'environ 100 M€.

Recoupements : la part IR (État) vaut 0,9 Md€ en 2024 et 1,0 Md€ prévu en 2025 et 2026 (PLF 2026, Voies et moyens
tome I, tableau p. 17) [TEXTE LU], ce qui cadre avec le tiers indiqué par la Cour. Le Compte du logement ne retient
que les logements : 2,80 Md€ (2022), 2,17 (2023), 1,53 (2024), 1,59 (2025). Le CPO donne 2,8 Md€ pour 2022. **Les
deux séries divergent en 2024 (1,5 contre 2,8 Md€)** : la Cour couvre toutes les plus-values immobilières des
particuliers (logements, terrains, autres biens), le Compte du logement les seuls logements. L'écart n'est pas
décomposé dans les sources lues.

### 3.6 Taxes sur la cession de terrains devenus constructibles

- Art. 1529 : taxe communale de 10 %, instituée sur délibération, sur la première cession de terrains nus rendus
  constructibles ;
- art. 1605 nonies : taxe nationale au profit de l'ASP, de 5 % ou 10 % selon le rapport entre prix de cession et prix
  d'acquisition (voir `france_institutions_chiffres.md`, § 4). Rendement prévisionnel et plafond : 17 M€ en 2027 (PLF
  2027, art. 42, ligne 37) [TEXTE LU] ;
- les deux taxes ensemble : « env. 20 M€ » en 2022 (CPO, p. 19) [TEXTE LU]. Rendement de la seule taxe communale :
  non trouvé.

---

## 4. Transmissions

**Total des DMTG.** 20,9 Md€ en 2024 : 4,9 Md€ de donations (ligne 1705) et 16,0 Md€ de successions (ligne 1706)
(PLF 2026, Voies et moyens tome I, p. 34). Prévisions : 20,8 Md€ en 2025 et 21,4 Md€ en 2026. *DGFiP Statistiques*
n° 43 : 20,91 Md€ (2024) et **21,18 Md€ (2025)** encaissés. Le PLF 2027 prévoit 22,0 Md€ pour 2027 (5,0 + 17,0)
[TEXTE LU]. L'OCDE classe en 4300 21 474 M€ en 2024 : successions 15 907, donations 4 912, prélèvement sur les capitaux
décès d'assurance-vie 458, recettes diverses 197 [TEXTE LU]. **Barème** en ligne directe : de 5 % à 45 % après un
abattement de 100 000 € par enfant et par parent (service-public.fr, impots.gouv.fr) [RÉSUMÉ].

**Part due à l'immobilier : il n'existe pas de ventilation officielle.**
- La DGFiP « contrôle uniquement la liquidation des droits lors du dépôt des déclarations de succession. Il n'y a donc
  pas de remontées statistiques » sur la composition des successions ; le projet « e-Enregistrement » doit y remédier
  (réponse à la QE AN n° 32562, JO du 5/01/2021, p. 84) [TEXTE LU].
- Le CPO retient « l'approximation communément admise » de 60 % du produit, parce que 62 % du patrimoine des ménages
  est immobilier, dont 97 % à usage d'habitation. Il obtient 11,2 Md€ sur 18,6 Md€ en 2022 (p. 20, note 7)
  [TEXTE LU]. Appliquée à 2025, cette clé donne environ **12,7 Md€** [NON VÉRIFIÉ (calcul sur une clé
  conventionnelle)]. La clé porte sur le patrimoine des ménages, pas sur l'assiette taxée. Or le CAE (note n° 69,
  décembre 2021) estime qu'environ 40 % du patrimoine transmis échappe au flux successoral vu par le fisc
  (assurance-vie notamment) [TEXTE LU]. Rien ne dit donc dans quel sens la clé se trompe.
- Le Compte du logement exclut les DMTG « compte tenu de difficultés d'estimation » (p. 82). France Stratégie
  (document de travail de janvier 2018) et le CAE (note n° 69) ne publient pas de décomposition par actif [TEXTE LU,
  recherche dans le texte].
- Repère en volume : 702 000 logements sont transmis chaque année entre 2018 et 2023, dont 519 000 par héritage et
  183 000 par donation, soit 40 % des changements de propriétaire (Insee Analyses n° 125, octobre 2026) [TEXTE LU].

---

## 5. Revenus

**Chiffrage disponible, logements seulement.** Le Compte du logement regroupe les « impositions sur les revenus
immobiliers » : CRL, IR, IS, CSG, CRDS, prélèvements sociaux et prélèvements sur les profits immobiliers des
non-résidents. Montants : 8 132 M€ (2022), 8 231 M€ (2023), 8 391 M€ (2024) et **8 678 M€ (2025)**, nets des avantages
fiscaux à l'investissement locatif (Pinel, etc.) (fig. 6.1, série T321, p. 81-82) [TEXTE LU]. Le CPO détaille 2022 :
4,2 Md€ d'IR « lié aux revenus immobiliers », 2,4 Md€ de prélèvements sociaux sur les revenus fonciers, 1,1 Md€ de CSG
sur les revenus immobiliers et 100 M€ de CRL, pour un total de 8,3 Md€ (p. 23) [TEXTE LU]. Les composantes citées ne
font que 7,8 Md€ ; l'écart, sans doute l'IS, n'est pas expliqué.

**Bases déclarées** (déclarations 2042, revenus 2024, data.economie.gouv.fr « ir-declarations-2042-nat », fichier
`fiscalite/donnees/ir_2042_cases_revenus2024.csv` du projet) [TEXTE LU des données] :
- revenus fonciers nets au régime réel (case 4BA) : 34,95 Md€ pour 2,86 millions de foyers ;
- recettes brutes au micro-foncier (4BE) : 8,48 Md€ pour 1,43 million de foyers ;
- déficits imputables : 1,53 Md€ sur les revenus fonciers (4BB) et 1,82 Md€ sur le revenu global (4BC) ; déficits
  antérieurs en stock : 8,52 Md€ (4BD).

**Fragilité.** À 17,2 %, une base de 35 à 40 Md€ donnerait mécaniquement 6 à 7 Md€ de prélèvements sociaux, presque
deux fois le chiffre du CPO pour les seuls logements (3,5 Md€ en 2022) [NON VÉRIFIÉ (calcul)]. L'écart peut tenir au
champ (les revenus fonciers incluent les locaux professionnels et les fermages), aux déficits ou à l'année ; il n'est
pas réconcilié. Aucun chiffrage officiel de l'IR et des PS sur l'ensemble des revenus fonciers n'a été trouvé. Les
loueurs en meublé (BIC) ne sont pas dans ces cases.
**CRL** : 541 M€ (2021), 539 (2022), 559 (2023), 511 M€ (2024) (liste nationale, D214H-C04, « contributions sur les
loyers immobiliers ») [TEXTE LU] ; assiette et taux non relus.

---

## 6. Construction

### 6.1 Taxe d'aménagement (art. 1635 quater A et suivants)

Rapport d'information de l'AN n° 1594, mission sur les dysfonctionnements de la gestion des impôts locaux, 18 juin
2025 (p. 89-96) [TEXTE LU] :
- **assiette** : surface de plancher multipliée par une valeur forfaitaire de 914 €/m², 1 036 €/m² en Île-de-France,
  indexée sur l'indice du coût de la construction. Abattement de 50 % notamment sur les 100 premiers m² de résidence
  principale. Forfaits pour les piscines (258 €/m²), les emplacements de tentes et caravanes, les éoliennes. Depuis
  l'art. 111 de la LF 2025, la transformation de locaux en logements est taxée, même sans création de surface ;
- **taux** : part communale ou intercommunale de 1 % à 5 %, jusqu'à 20 % dans certains secteurs ; part départementale
  de 2,5 % au plus ; part régionale de 1 % au plus, en Île-de-France seulement ;
- **rendement** : « en 2024, un montant total de 1,6 milliard d'euros a été liquidé », réparti à 61 % pour le bloc
  communal, 36 % pour les départements et 3 % pour la Région Île-de-France (p. 96).

**Encaissements (comptes de gestion)** : 1 366 M€ en 2024 (415 en section de fonctionnement et 951 en
investissement) ; 2023 implicite ≈ 1 890 M€ (calcul à partir des évolutions de −32,3 % et −25,5 %) ; **782 M€ en 2025**
(232 + 550 ; −44 % et −42 %) (OFGL 2025 et 2026, annexe 8, tableau 1) [TEXTE LU]. QE 4482 : part communale 0,98 Md€
et part départementale 0,59 Md€ en 2023. Comptabilité nationale, « taxes sur la construction » : 1 692 M€ (2022), 1 671
(2023), 1 194 (2024) ; OCDE, « Building permit tax » : 1 202 M€ (2024) ; Compte du logement (logements) : 1 139, 667
et 423 M€ de 2023 à 2025.
**Rupture de série** : pour les autorisations déposées après le 1er septembre 2022, la liquidation est passée des DDTM
à la DGFiP, et la taxe n'est plus exigible qu'à l'achèvement des travaux (AN n° 1594, p. 89 ; ordonnance n° 2022-883
du 14 juin 2022) [TEXTE LU]. La chute des encaissements en 2024-2025 reflète ce décalage et le recul de la
construction, sans que les sources lues mesurent la part de chacun.

### 6.2 Redevance d'archéologie préventive

Part « logement », aussi appelée taxe d'archéologie préventive : 0,40 % de la valeur forfaitaire de la TA, liquidée
par la DGFiP. Part « culture » : 0,71 €/m² de terrain en 2025. **96,5 M€ en 2024**, dont 69,3 M€ pour la part
logement et 27,2 M€ pour la part culture (AN n° 1594, p. 96-98) [TEXTE LU]. Le produit est versé au budget général de
l'État depuis la LF 2016 [RÉSUMÉ].

### 6.3 Hors champ ou non chiffré

- Taxe sur la création de bureaux en Île-de-France (TCBCS) : taxe d'urbanisme non liquidée par la DGFiP (AN n° 1594,
  p. 89, note) ; rendement non trouvé.
- Participation des employeurs à l'effort de construction : 1 497 M€ en 2024 (liste nationale) et 2 025 M€ prévus en
  2027 pour Action Logement (PLF 2027, art. 42). Elle est assise sur la masse salariale : exclue, bien que le CPO la
  rattache à la fiscalité du logement (1,6 Md€ en 2022).

---

## 7. Totaux de référence

### 7.1 Compte du logement du SDES, édition 2025 (publiée le 14/09/2026)

*Rapport du compte du logement 2025*, partie 6, et fichiers « Données 2025 – Les prélèvements » et « Séries longues
Prélèvements » [TEXTE LU] :

| M€ | 2024 | 2025 |
|---|---:|---:|
| Prélèvements sur la consommation associée au service de logement | 26 004 | 28 035 |
| dont TVA sur l'énergie et les charges | 15 106 | 15 338 |
| dont autres taxes sur les produits (énergie, contrats d'assurance) | 7 927 | 9 899 |
| dont THRS | 2 971 | 2 798 |
| Prélèvements sur les producteurs de service de logement | 44 770 | 46 066 |
| dont impositions sur les revenus immobiliers | 8 391 | 8 678 |
| dont IFI | 2 644 | 2 675 |
| dont TFPB | 30 489 | 31 590 |
| dont taxes sur les charges | 2 819 | 2 921 |
| dont TLV et THLV | 426 | 202 |
| Prélèvements sur l'investissement en logement | 14 854 | 13 881 |
| dont taxes d'urbanisme | 667 | 423 |
| dont TVA sur les terrains, le neuf, les travaux et les frais | 14 187 | 13 457 |
| Prélèvements sur les mutations | 13 004 | 15 447 |
| dont DMTO bruts | 11 239 | 13 568 |
| dont CSI | 239 | 289 |
| dont impôts et prélèvements sur les plus-values immobilières | 1 526 | 1 590 |
| **Ensemble** | **98 631** | **103 429** |

En 2025, ces prélèvements représentent 7,9 % des prélèvements obligatoires (p. 77). Les lignes 2024 sont recalculées
à partir de la série T321, qui donne les totaux hors IFI et hors THRS (93 016 et 97 956 M€). **Pièges** :
- les données 2024 ont été révisées de −582 M€ entre les éditions 2024 et 2025 (fig. 6.5). La presse citait 99,2 Md€
  pour 2024 d'après l'édition précédente [SECONDAIRE] ;
- dans le fichier xlsx de la fig. 6.1, la ligne de 202 M€ est intitulée par erreur « Taxes d'urbanisme » ; le PDF et
  la série T321 disent « taxes sur les logements vacants et d'habitation sur les logements vacants » ;
- le champ couvre les seuls logements, sans DMTG, sans TEOM (traitée comme un service), sans CFE ni foncier
  professionnel, mais avec la TVA et les taxes sur l'énergie consommée dans les logements.

### 7.2 Autres totaux

- **CPO (décembre 2023)** : fiscalité du logement de 91,5 Md€ en 2022, soit 3,5 % du PIB et 7,6 % des PO, selon les
  étapes du « cycle de vie » du logement. L'édition 2023 du Compte du logement donnait 96,7 Md€ pour la même année
  (p. 17-18) [TEXTE LU].
- **DGFiP, impôts sur le patrimoine encaissés** : 93,18 Md€ (2024) et 98,00 Md€ (2025), dont taxes foncières et taxes
  annexes 54,85, DMTG 21,18, DMTO et droits d'enregistrement 19,18 et IFI 2,77 en 2025 ; part de l'État 27 %
  (*DGFiP Statistiques* n° 43) [TEXTE LU].
- **Liste nationale des impôts** (comptabilité nationale) : « impôts sur les bâtiments, terrains et autres
  constructions » (D29A) de 61 440 M€ en 2024, CFE et taxes non immobilières comprises [TEXTE LU].

---

## 8. Comparaison internationale (OCDE, *Revenue Statistics*)

Données extraites le 15/11/2026 de l'API SDMX de l'OCDE (flux `DSD_REV_COMP_OECD@DF_RSOECD`, en % du PIB, et
`DSD_REV_OECD@DF_REVFRA`, détail français en M€) [TEXTE LU]. Dernière année disponible : **2024 pour les pays, 2023
pour la moyenne de l'OCDE** (code `OECD_REP`). Ces valeurs sont identiques à celles du fichier
`fiscalite/donnees/recettes_ocde_pct_pib.csv` du projet.

| % du PIB | 4100, 2024 | 4400, 2024 | 4100, 2023 | 4400, 2023 | 4300, 2024 |
|---|---:|---:|---:|---:|---:|
| **France** | **1,95** | **0,62** | 1,90 | 0,72 | 0,73 |
| Moyenne OCDE | n.d. | n.d. | 0,95 | 0,37 | 0,15 (2023) |
| Allemagne | 0,37 | 0,29 | 0,37 | 0,29 | 0,23 |
| Royaume-Uni | 2,80 | 0,65 | 2,78 | 0,60 | 0,29 |
| Danemark | 0,91 | 0,22 | 1,20 | 0,22 | 0,28 |
| Pays-Bas | 0,57 | 0,34 | 0,69 | 0,29 | 0,30 |
| Italie | 1,05 | 1,05 | 1,09 | 0,94 | 0,05 |
| Espagne | 0,89 | 0,81 | 0,93 | 0,75 | 0,22 |
| Belgique | 1,26 | 0,89 | 1,28 | 0,84 | 0,62 |
| États-Unis | 2,67 | 0,08 | 2,63 | 0,08 | 0,13 |

4100 : impôts périodiques sur la propriété immobilière ; 4400 : impôts sur les transactions mobilières et
immobilières ; 4300 : droits de succession et de donation. Ménages (4110) et autres agents (4120) en France, 2024 :
1,39 % et 0,56 % du PIB (OCDE en moyenne, 2023 : 0,32 % et 0,45 %).

**Ce que contient le chiffre français** (DF_REVFRA, 2024, M€) [TEXTE LU] :
- **4100 = 56 841** : TFPB 42 059 (ménages 26 118, autres 15 941), **TEOM 9 428**, taxe d'habitation 3 317, TFNB 1 181,
  taxes pour frais de chambres d'agriculture 303, taxe de balayage 113, autres 440. **La CFE n'y figure pas**
  (classée en 6100). Sans la TEOM, la France serait à 1,62 % du PIB ; avec la CFE, à 2,20 % [calcul].
- **4400 = 18 222** : DMTO perçus par les collectivités (« Additional registration taxes ») 14 669, « Land registration
  tax » de l'État 957, taxe sur les transactions financières 1 323, autres droits 1 273. La part immobilière
  représente environ 86 % [calcul]. La catégorie mêle partout immobilier et titres : le droit de timbre britannique
  sur les actions, par exemple, y figure aussi [NON VÉRIFIÉ pour le détail des autres pays].
- La baisse du Danemark en 2024 (de 1,20 à 0,91 point) et celle des Pays-Bas ne sont pas expliquées ici. Pour la
  réforme danoise de 2024, voir `../../lvt/notes/transitions_et_saillance.md`.

---

## 9. Non trouvé, à vérifier

1. **Textes du CGI sur Légifrance** (inaccessible) : art. 1388 (abattement de 50 %), 1396 (abattement sur la TFNB),
   1522 (assiette de la TEOM), 1530 bis (GEMAPI), 1607 bis (TSE des EPF locaux), 231 ter (tarifs de la TSBCS), 232
   (TLV), 234 nonies (CRL), 879 (CSI), 1594 F septies (réduction pour une première propriété : date de création et
   régime), 1406 bis (TVLH, art. 108 de la LF 2026). Les articles 116 de la LF 2025 et 121 de la LF 2026 ont été lus à
   travers le BOFiP, pas sur le JORF.
2. **Part immobilière des DMTG** : seule existe la clé conventionnelle de 60 % du CPO. À rechercher : une étude
   notariale (Conseil supérieur du notariat), l'enquête « Patrimoine » de l'Insee, les remontées d'« e-Enregistrement ».
3. **TFPB sur les locaux d'habitation et sur les locaux professionnels** : pas de ventilation observée ; le calcul par
   différence mêle deux périmètres. À rechercher : le rapport de la Cour des comptes « Les taxes foncières » (2023),
   les fichiers REI ou Majic par catégorie de local.
4. **Imposition de l'ensemble des revenus fonciers** (IR et PS) : seul existe le chiffre du Compte du logement, limité
   aux logements et net des avantages fiscaux ; il ne se raccorde pas aux bases déclarées (§ 5).
5. **TSE totales** : il manque les EPF locaux. **TSBCS** : contenu exact de la ligne à 1 055 M€, part de l'État,
   extension à la région PACA.
6. **TLV en 2023-2025** : estimations divergentes (40 à 250 M€).
7. **Écart sur l'IFI** entre l'impôt émis (2,33 Md€) et les encaissements (2,77 Md€) en 2025.
8. **Écart sur les plus-values** entre la Cour (2,8 Md€) et le Compte du logement (1,5 Md€) en 2024 : ventilation par
   type de bien non trouvée. Le rapport de la Cour lui-même n'a pas été lu (ccomptes.fr inaccessible), seul le compte
   rendu de l'audition à l'AN.
9. **Taxe d'aménagement** : séries liquidée et encaissée non raccordées ; la part de 2025 tenant au décalage
   d'exigibilité n'est pas mesurée.
10. **Taxe additionnelle de la Région Île-de-France aux DMTO (0,6 %)**, **taxe communale sur les terrains devenus
    constructibles (art. 1529)**, **TCBCS** : rendements non trouvés.
11. **TVA sur la construction neuve non résidentielle** : non trouvée.
12. **Frais d'assiette sur les DMTO** : seulement calculés (2,37 %) ; aucune ligne budgétaire dédiée n'a été trouvée.
13. **Moyenne OCDE pour 2024** : pas encore publiée dans la base au 15/11/2026.

---

## Sources (consultées le 15/11/2026)

- DGCL-DGFiP, *Analyse de l'évolution des produits 2025 de la fiscalité directe locale* (note REI 2025, mai 2026) :
  https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/Taux%20de%20fiscalit%C3%A9%20directe%20locale%20vot%C3%A9s%20par%20les%20collectivit%C3%A9s/2025/Note%20analyse%20REI_2025.pdf
- OFGL-DGCL, Rapport 2026, annexes 6 à 8 (fiscalité locale 2025) :
  https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/Annexes%206%20%C3%A0%208.pdf
- OFGL-DGCL, Rapport 2025, annexes 6 à 8 (fiscalité locale 2024) :
  https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202025/Rapport%20OFGL%202025%208%20Annexe%206%20%C3%A0%208.pdf
- SDES, *Rapport du compte du logement 2025* (14/09/2026), PDF et xlsx « Les prélèvements » et « Séries longues
  Prélèvements » : https://www.statistiques.developpement-durable.gouv.fr/rapport-du-compte-du-logement-2025
- DGFiP, *DGFiP Statistiques* n° 43 (mars 2026), « Les recettes fiscales collectées par la DGFiP progressent plus vite
  que le PIB en 2025 » : https://www.impots.gouv.fr/node/28174
- DGFiP, *DGFiP Statistiques* n° 45 (avril 2026), « L'impôt sur la fortune immobilière en 2025 » :
  https://www.impots.gouv.fr/dgfip-statistiques-limpot-sur-la-fortune-immobiliere-en-2025
- DGFiP, tableaux des taux de DMTO au 1er janvier et au 1er juin 2026 :
  https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/notaires/dmto/dmto_2026-06.pdf (et
  `dmto_2026-01.pdf`)
- BOFiP, BOI-ENR-DMTOI-10-20 du 17/06/2026, et actualité du même jour sur l'art. 116 de la LF 2025 et l'art. 121 de
  la LF 2026 : https://bofip.impots.gouv.fr/doctrine/pgp/3311-PGP ; https://bofip.impots.gouv.fr/doctrine/pgp/14771-PGP
- DGCL, page « Droits de mutation » :
  https://www.collectivites-locales.gouv.fr/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-indirecte-locale/droits-de-mutation
- Annexe au PLF 2026, *Évaluation des voies et moyens*, tome I :
  https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1087930/file/PLF%202026%20-%20V%26M%20TI%20-%20Evaluations%20des%20recettes.pdf
- Projet de loi de finances pour 2027 (n° 3210), état A et art. 42 :
  https://www.assemblee-nationale.fr/dyn/opendata/PRJLANR5L17B3210.html
- CPO, *Pour une fiscalité du logement plus cohérente*, 18/12/2023 : https://www.vie-publique.fr/files/rapport/pdf/292676.pdf
- AN, commission des finances, compte rendu n° 043 du 25/11/2025, audition de la Cour des comptes sur les plus-values
  immobilières :
  https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/cion_fin/l17cion_fin2526043_compte-rendu.pdf
- AN, rapport d'information n° 1594 (Pirès Beaune et Amiel), 18/06/2025 :
  https://www.assemblee-nationale.fr/dyn/17/rapports/cion_fin/l17b1594_rapport-information.pdf
- Réponses ministérielles aux QE AN n° 4482 (JO 3/06/2025), n° 5129 (JO 16/09/2025) et n° 32562 (JO 5/01/2021) :
  https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE4482.pdf ;
  https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE5129.pdf ;
  https://www.assemblee-nationale.fr/dyn/15/questions/QANR5L15QE32562.pdf
- CAE, note n° 69, « Repenser l'héritage » (décembre 2021) : https://cae-eco.fr/static/pdf/cae-note069.pdf
- Insee Analyses n° 125 (octobre 2026), transmissions de logements :
  https://www.insee.fr/fr/statistiques/fichier/version-html/9061645/IA125.pdf
- OCDE, API SDMX : flux `OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD` et `OECD.CTP.TPS,DSD_REV_OECD@DF_REVFRA`
  (https://sdmx.oecd.org/public/rest/data/…)
- Eurostat, *National Tax Lists*, fichier `National_tax_lists_2024_2026-07-21.xlsx`, onglet FR, extrait dans
  `fiscalite/donnees/ntl_france.csv` par `extract_donnees.py`
- Secondaires : Légifiscal, fiche TVLH ; doctrine.fr, art. 1594 F septies ; service-public.fr (actualité A18183 du
  2/04/2025)

Les fichiers téléchargés ont été lus dans des dossiers isolés du scratchpad de la session (`inv_*`) et ne sont pas
conservés dans le dépôt.
