# Registre des hypothèses et vérification des chiffrages : partie IR-CSG

*16/11/2026. Source du tableau « Hypothèses fortes et chiffres non vérifiés » de l'annexe IR-CSG (charte,
`synthese/CHARTE_NOTE.md`). Fichiers relus : `revue/methode_v2.md`, `synthese/modele_purs.py`,
`architectures_ircsg.py`, `etapes_ircsg.py`, `controle_hauts_purs.py` et leurs sorties, `ir_csg/` (README,
`ir_csg.py`, `bareme_lisse.py`, `bareme_v3.py`, `exercices.py`, `proposition.py`), `revue/verif_ir_csg.md`,
`revue/revue_ir_csg.md`, `revue/verif_litterature_ircsg.md`, `cours/elasticites-france.tex`,
`synthese/parties/ircsg.tex`. Aucun fichier `.tex` n'a été modifié. Scripts de vérification : section 7.*

**En bref.** L'arithmétique du modèle est juste : un recodage indépendant redonne tous les chiffres à 0,01 Md€ près.
Deux erreurs de construction ont été corrigées dans `synthese/modele_purs.py` (section 5) :
- la CRDS manquait dans le taux marginal actuel. Corrigée, elle relève tous les gains d'efficacité d'environ 0,4 Md€ :
  proposition 4,9 → **5,3 Md€** ;
- la charge actuelle des couples de retraités était sous-estimée. Corrigée, elle ramène la hausse payée par les
  retraités de 15,2 à **12,6 Md€** dans la proposition.

Barèmes, déciles et cas-types ne changent pas. Une hypothèse domine toutes les autres : on suppose que la CSG
d'aujourd'hui fait réagir les salariés autant que l'IR. Si elle était perçue comme une cotisation, le gain d'efficacité
disparaîtrait (section 3, H1).

---

## 1. La méthode en clair

**Le champ.** La réforme remplace l'IR, la CSG et la CRDS payés sur les revenus imposés au barème : salaires,
pensions, bénéfices des indépendants, loyers, allocations chômage. En 2024, ces trois impôts y prélèvent 220,1 Md€ :
80,2 d'IR, 132,4 de CSG et 7,4 de CRDS. Les revenus du capital au prélèvement forfaitaire unique (PFU) restent hors
champ. Ils représentent 90 Md€, auxquels le modèle impute 11,5 Md€ d'IR à 12,8 %.

**Les données.**
- La distribution vient des 25 tranches de revenu fiscal de l'IRCOM des revenus de 2024 (DGFiP), découpées en 60 foyers
  représentatifs par tranche.
- La composition des revenus vient des totaux par case des déclarations 2042.
- La CSG est reconstituée par type de revenu et calée sur les comptes de la Sécurité sociale (CCSS).

**Les foyers purs.** Chaque foyer représentatif est scindé en un foyer d'actifs et un foyer de retraités, de même
revenu, dans la proportion des pensions de la tranche. Chaque groupe comprend des personnes seules et des couples.
Les couples partagent leurs revenus selon l'Insee, et les enfants ne sont que chez les actifs. La charge actuelle de
chaque tranche est la charge observée. Elle est répartie entre types de foyers selon des cas-types OpenFisca de 2024.

**Le nouvel impôt.** Il porte sur le revenu après cotisations, est individuel, et n'a ni niche ni taux réduit. Son taux
marginal monte en ligne droite entre quelques seuils, jusqu'à 50 %. Chaque architecture est calée pour rapporter
exactement 220,1 Md€ avant toute réaction des contribuables.

**L'efficacité.** C'est la méthode v2 (`revue/methode_v2.md`).
- Seul le revenu d'activité des actifs réagit. Il réagit au taux de l'impôt fusionné, avec une élasticité faible :
  0,05 dans la moitié du bas et 0,10 au-dessus au centre.
- Chaque euro d'activité perdu coûte à la collectivité tout ce que l'État prélevait dessus : l'impôt, les cotisations
  non contributives et la prime d'activité qui n'est plus versée.
- La décision de travailler réagit au taux de prélèvement du premier salaire (η = 0,25, sous 2 Smic).
- La réaction du revenu déclaré des hauts revenus (forme, date, déplacement vers l'IS et le PFU) est comptée à part,
  comme un effet sur la recette. Elle n'entre pas dans le gain.
- Le « gain » est la baisse de perte sèche par rapport à aujourd'hui. On le donne avec trois jeux d'élasticités : bas,
  central et haut.

**Les architectures.** Ce n'est pas l'optimiseur qui décide.
- On construit d'abord le barème « neutre », celui qui s'écarte le moins de ce que paie chaque foyer.
- On lui ajoute ensuite les dispositifs un par un, chaque fois à recette égale.
- L'optimum d'efficacité n'est qu'un étalon : il donne le « gain atteignable ».
- La proposition est le barème le plus efficace parmi ceux qui ne déplacent la charge moyenne d'aucun décile de plus de
  500 € et n'alourdissent pas celle du 1 % le plus aisé.

**Ce que ces chiffres sont, et ne sont pas.** Ce sont des ordres de grandeur, tirés de foyers représentatifs : ce n'est
pas une microsimulation. La dispersion réelle des gagnants et des perdants est plus forte que celle du modèle.

---

## 2. Chiffres clés vérifiés

Statuts :
- **OK** : recalculé à l'identique ;
- **CORRIGÉ** : la valeur a changé après les deux corrections de la section 5 ;
- **FRAGILE** : le calcul est juste, mais il dépend d'une hypothèse forte (section 3).

Recalcul indépendant : `v1_recette.py` pour la recette, `v2_independant.py` pour le reste (section 7).

| Grandeur | Valeur (après correction) | Avant | Script / source | Statut |
|---|---|---|---|---|
| Recette remplacée | 220,09 Md€ = IR 80,20 + CSG 132,44 + CRDS 7,44 | idem | `ir_csg.py` ; recalcul indépendant depuis le CSV IRCOM | OK |
| IR IRCOM des revenus 2024 | 91,72 Md€, dont 11,52 imputés au PFU (12,8 % de 90 Md€) | idem | `donnees/ircom_national_revenus2024.csv` | OK (règle de 12,8 % : convention) |
| Assiette | 1 598 Md€ brute, 1 481 nette de cotisations (pensions 406, chômage 37) | idem | `bareme_v3.py` | OK |
| Barème de l'IR par adulte sur l'assiette large (étape 1) | 197,1 Md€ ; taux proportionnel 1,55 % | idem | `etapes_ircsg.txt` ; recodage | OK |
| Décomposition 80 → 197 Md€ | sans niche, sur le RFR : 109,9 ; assiette large +45,7 ; sans quotient familial +16,9 ; sans décote +7,0 ; impôt individuel +17,6 | — | `v8_decomp_ir.py` (nouveau, approché) | NOUVEAU. L'écart de 29,7 entre 109,9 et 80,2 recouvre les niches (au moins 24 Md€) et les revenus exonérés présents dans le RFR (heures supplémentaires : 21,8 Md€ de base). Non bouclé. |
| Barème neutre | 2 % au premier euro, 14 % à 20 k€, 23,0 % à 30 k€, 50 % à 250 k€ | idem | `architectures_ircsg.txt` | OK. Choix peu identifié : plusieurs barèmes, avec un premier taux de 0 à 3 %, ont un écart moyen à 1 € près (`v3_bords.py`) ; leur gain varie de ±0,1 Md€. |
| Gain, étape 1 | 2,8 Md€ (1,1 à 6,1), dont participation 2,6 | 2,4 (0,9 à 5,2) | `etapes_ircsg.txt` | CORRIGÉ ; FRAGILE (H1) |
| Gain, barème neutre | **4,4 Md€ (2,1 à 10,1)** ; intensif 2,6, participation 1,8 | 4,0 (1,9 à 9,2) | idem | CORRIGÉ ; FRAGILE (H1, H2) |
| Gain, neutre + franchise de 4 000 € / 8 000 € | 4,9 / 5,4 Md€ | 4,6 / 5,0 | `architectures_ircsg.txt` | CORRIGÉ |
| Gain atteignable (optimum, franchise de 4 000 €) | **8,1 Md€ (4,0 à 19,1)** ; 16 % jusqu'à 60 k€, 50 % à 2 M€ | 7,8 (3,8 à 18,2) | idem | CORRIGÉ. Robuste à la grille : porter le seuil supérieur à 3, 5 ou 10 M€ ne gagne que 0,01 Md€. |
| Proposition | 14 % jusqu'à 20 k€, 30,3 % à 45 k€, 50 % à 1 M€ ; **gain 5,3 Md€ (2,5 à 12,0)**, 64 % de l'atteignable ; 29 % de perdants de plus de 500 € | 4,9 (2,3 à 11,1), 63 % | idem | CORRIGÉ ; FRAGILE (H1). Le seuil supérieur est au bord de la grille ; à 2 M€, le gain ne monte que de 0,02 Md€. |
| Proposition avec franchise de 8 000 € | 5,6 Md€ (68 %) | 5,2 (67 %) | idem | CORRIGÉ |
| Part de l'atteignable, neutre / franchise de 4 000 € / franchise de 8 000 € | 54 / 61 / 66 % | 52 / 59 / 64 % | idem | CORRIGÉ |
| Revenu déclaré (effet sur la recette, hors gain) | neutre +3,3 (1,6 à 4,9) ; proposition +4,1 (2,0 à 6,1) Md€ | +3,0 ; +3,8 | idem | CORRIGÉ ; dépend de s (H5) |
| Prix d'un milliard levé (`perte_seche_autres.py`) | 0,03 / 0,07 / 0,14 (neutre) ; 0,04 / 0,08 / 0,17 (avec franchise et dispositifs) | idem | `[PRIX]` | OK, inchangé |
| Retraités : hausse de charge | étape 1 +2,1 ; neutre **+4,4** ; franchise de 4 000 € +11,4 ; proposition **+12,6** ; proposition avec franchise de 8 000 € +20,3 Md€ | +4,7 ; +7,0 ; +14,0 ; +15,2 ; +22,8 | `etapes_ircsg.txt`, `architectures_ircsg.txt` | CORRIGÉ ; FRAGILE (H10, H11, H12) |
| Retraité seul / couple de retraités, proposition | +662 / **+1 468 €** par foyer | +603 / +2 325 | idem | CORRIGÉ |
| Couples avec deux enfants, proposition | −8,7 Md€, −1 085 € par foyer | −9,6 ; −1 195 | idem | CORRIGÉ (les foyers sont recomposés) ; FRAGILE (H13) |
| Déciles (€ par foyer), 10 % et 1 % du haut | inchangés (neutre : −34 … +578 ; proposition : −82 … +461 ; 1 % −2,7 Md€) | idem | idem | OK (la charge de chaque tranche ne bouge pas) |
| Abattement de 10 % gardé / petites pensions exonérées (variantes du neutre) | retraités −1,7 / +0,6 Md€ (au lieu de +4,4) ; +0,60 / +0,37 point de taux pour tous | +0,9 / +3,2 | `architectures_ircsg.txt` | CORRIGÉ |
| Coût du quotient familial des enfants | 13,36 Md€ (couples 11,20, parents isolés 2,16) ; chèque de 742 € par enfant | idem | `modele_purs.py` ; recodage | OK au calcul ; 13,0 si les parents isolés ont 1,4 enfant en moyenne (H13) |
| Foyers de retraités / d'actifs | 14,49 M / 27,14 M ; 3,75 M couples de retraités | idem | `controles_purs.txt` | FRAGILE. L'IRCOM compte 14,22 M de foyers qui déclarent des pensions, les foyers mixtes compris ; les cases 1AS et 1BS, 17,47 M de pensionnés. Le modèle compte 18,2 M d'adultes retraités et en loge 3,8 M dans la tranche de 0 à 10 k€, contre 2,0 M de foyers déclarant des pensions. |
| Charge actuelle des retraités | 47,6 Md€ (11,7 % des pensions) ; actifs 172,4 Md€ (16,0 %) | 45,1 / 175,0 | `controles_purs.txt` | CORRIGÉ ; non observable (aucune source publiée) |
| Cas-types, proposition (neutre ; étape 1) | retraité seul à 17 000 € : +1 260 € (+1 207 ; +869) ; Smic : +61 (−577 ; −920) ; couple avec deux enfants à 50 k€ : −1 357 (−745 ; −1 728) ; même couple à un seul revenu : −575 à 50 k€, +1 326 à 80 k€ ; partage 60/40 à 80 k€ : −2 743 | idem | `etapes_ircsg.txt` ; recodage | OK |
| Retraité seul à 17 000 € « aujourd'hui exonéré » | IR, CSG et CRDS nuls en 2024 (OpenFisca) | — | `courbes_openfisca.csv` | OK, mais cas limite : 17 000 € est le pire cas, juste sous le seuil d'exonération de CSG (section 4) |
| Très hauts revenus | 3 804 foyers au-delà de 3 M€. Taux actuel prêté au revenu du barème : 32 à 37 % (convention mixte), 44 à 49 % (convention haut). Effet de la proposition au-delà de 3 M€ : +1,9 à +15,8 points (mixte), −13,2 à +1,0 point (haut). | idem | `controle_hauts_purs.txt` | OK au calcul ; dépend de la convention (H9) |

---

## 3. Hypothèses fortes

Les hypothèses sont classées de la plus lourde à la plus légère. « Gain » désigne la baisse de perte sèche (jeu
central), donnée après correction. Sauf mention contraire, les variantes sont calculées par les scripts de la section 7,
le barème étant recalé chaque fois sur 220,1 Md€.

| # | Hypothèse | Où elle joue | Effet si elle est fausse (sens, ampleur) |
|---|---|---|---|
| H1 | **Saillance symétrique.** La CSG et la CRDS d'aujourd'hui font réagir le revenu d'activité autant que l'IR, et l'impôt fusionné autant que les deux réunis. Le modèle lit les élasticités françaises, mesurées sur le taux de l'IR, comme une réaction à IR + CSG + CRDS. Aucune étude ne mesure la réaction à la CSG ; Lehmann, Marical et Rioux (2013) ne trouvent aucune réaction aux cotisations. | Tout le gain intensif : 2,6 Md€ (neutre) et 3,8 Md€ (proposition) | **Décisif.** Si la CSG, prélevée sur la fiche de paie avec les cotisations, n'est pas perçue aujourd'hui, la fusion la rend visible, et le taux perçu par les salariés monte. Le gain intensif devient alors une perte : +4,4 Md€ au lieu de −2,6 (neutre) et +3,1 au lieu de −3,8 (proposition). Le gain total disparaît (neutre +2,6, proposition +1,6) ; la marge extensive est gardée, ce qui est favorable à la réforme. Si la CSG est à moitié perçue, le gain intensif devient une perte de 1,0 Md€ (neutre) et un gain de 0,3 Md€ (proposition), soit un gain total de 0,8 et de 1,7 Md€. (`v7_saillance.py`) |
| H2 | **Élasticités du revenu réel** : 0,05 dans la moitié du bas, 0,10 au-dessus ; marge extensive η = 0,25 sous 2 Smic. Ce sont des élasticités de court terme ; la même valeur est prise de 90 à 99 % et au 1 % du haut, faute de mesure. η vient de Chetty, Guren, Manoli et Weber (2013), une synthèse surtout américaine. | Tous les gains | Fourchettes déjà données : de 2,1 à 10,1 (neutre), de 2,5 à 12,0 (proposition). Une élasticité de long terme de l'ordre de 0,3 (Chetty et al.) pousse vers le haut de la fourchette. La participation fait l'essentiel du gain de l'étape 1 (2,6 sur 2,8) et 40 % de celui du neutre. |
| H3 | **Coin non contributif.** Les cotisations sont séparées en contributives et non contributives par convention. Le droit retenu est celui de 2025 : la réduction générale s'éteint à 1,6 Smic, avec une pente de 0,53. La prime d'activité n'est retirée qu'aux personnes seules (31,6 % par euro brut). Les indépendants n'ont pas de coin ; les aides au logement et la TVA sont ignorées. | Prix de chaque euro perdu | Avec la réduction dégressive unique de 2026, qui s'éteint à 3 Smic, le gain monte de 0,1 à 0,3 Md€ (neutre −4,6, proposition −5,3, atteignable −8,4 ; `v9_rgdu.py`). Le partage contributif / non contributif n'est pas vérifié. Un coin plus large (aides au logement, TVA) augmenterait le prix de chaque euro perdu, donc les gains comme les pertes. |
| H4 | **Les pensions et le chômage ne réagissent pas** : ni l'âge de départ, ni le cumul emploi-retraite, ni l'épargne. | Le mécanisme même du gain : taxer davantage les pensions pour alléger le travail | Non chiffré. Si l'imposition des pensions jouait sur l'âge de départ ou sur le cumul, le sens de l'effet serait ambigu. |
| H5 | **Revenu déclaré.** Élasticités de 0,20 (90 à 99 %) et 0,30 (1 % du haut). Une part s = 0,5 se déplace vers l'IS et le PFU, à 48,6 % ; c'est une convention sans estimation française. | Effet sur la recette (hors gain) | Proposition : +4,1 Md€ avec s = 0,5, +7,1 avec s = 0, +1,0 avec s = 1 (neutre : +3,3, +5,8, +0,8). Selon Chetty (2009), si l'optimisation consomme des ressources réelles, une partie de cet effet est un gain d'efficacité : le gain est alors minoré. |
| H6 | **Taux marginal actuel.** C'est la médiane de quatre profils OpenFisca d'actifs, au RFR moyen de la tranche, la même pour les personnes seules et les couples ; IR + CSG + CRDS depuis la correction. | Perte sèche actuelle et gain | Avec un taux propre à chaque type (une personne seule à 40 k€ brut : 31 % au lieu de 22 %), le gain monte de 0,1 Md€ : neutre −4,5, proposition −5,3. Avant la correction de la CRDS, l'écart était de +0,45 Md€ (section 5). |
| H7 | **Foyers purs.** Pas de foyer mixte : couples dont un seul conjoint est retraité, retraités qui ont des loyers ou des salaires, actifs qui ont une pension d'invalidité. Les loyers sont tous chez les actifs. | Franchise d'activité, « qui paie » entre actifs et retraités, nombre de retraités | En réalité, la franchise d'activité couvre aussi les loyers des retraités bailleurs. Le coût de la franchise est donc sous-estimé, et la hausse des retraités surestimée. L'ordre de grandeur va jusqu'à environ 3 Md€ ; c'est une borne grossière, qui suppose qu'une part des 38 Md€ de loyers revient à des retraités, part non vérifiée. Les retraités sont trop nombreux en bas (tranche de 0 à 10 k€), avec peu d'effet sur les montants. Le modèle d'origine, à foyers « mélangés », était l'autre borne (`revue/verif_ir_csg.md`, point 2). |
| H8 | **Composition des revenus identique dans une tranche** : même part de salaires, de gérants, de chômage, d'indépendants et de loyers pour tous les actifs. Le chômage est réparti comme les salaires ; 70 % des revenus des indépendants et des loyers réagissent comme du travail. | Franchise, base qui réagit, chômeurs | Les chômeurs n'existent pas comme foyers : on ne peut rien dire d'eux. Traiter les loyers comme du travail gonfle la base qui réagit d'environ 2,4 % (27 Md€ sur 1 118), d'où une légère surestimation des gains. |
| H9 | **Répartition des revenus au PFU entre tranches** (non publiée) : convention mixte, moyenne du prorata et du « haut ». | Très hauts revenus, 1 % du haut, gain | 1 % du haut, neutre : +0,3 (mixte), −2,8 (haut), +4,3 Md€ (prorata) ; proposition : −2,7, −4,5, −0,1. Gain : neutre 4,4 / 4,0 / 4,9 ; proposition 5,3 / 4,8 / 5,7. Le calage sur l'IR observé (`v5_pfu_calage.py`, sans niche ni enfant) met 87 à 93 % des « autres revenus » au PFU au-delà de 1 M€, ce qui est **proche de la convention haut (90 %) et loin de la mixte (68 %)**. Le calage échoue entre 100 et 200 k€, où il faudrait connaître les niches et les enfants. Si ce calage est juste, la proposition baisse l'impôt des très hauts revenus du barème, sauf au-delà de 9 M€. |
| H10 | **Part de couples par tranche** : une fonction logistique du RFR, calée sur les 13,05 M de couples des déclarations, la même chez les actifs et chez les retraités. | Charge des retraités, individualisation | Si les couples de retraités sont 4,31 M (cases 1BS) au lieu de 3,75 M : retraités +4,9 au lieu de +4,4 (neutre), +13,0 au lieu de +12,6 (proposition) ; gain −0,1 Md€. |
| H11 | **Partage des revenus dans les couples** : Insee Première 1492, ramené à quatre classes (15 % de couples à un seul revenu, part moyenne du second revenu de 29,5 %), le même pour les couples de retraités. | Coût de l'impôt individuel pour les couples ; taux de 23 % du neutre | Couples de retraités à 62/38, d'après l'écart de 38 % entre les pensions de droit direct des femmes et des hommes (DREES, 2023) : retraités +2,5 au lieu de +4,4 (neutre), +10,6 au lieu de +12,6 (proposition) ; couple de retraités −22 € au lieu de +549 € (neutre), +844 au lieu de +1 468 € (proposition). Tous les couples à 60/40 : taux du neutre 25,6 % au lieu de 23,0 % ; couples avec deux enfants +2,3 au lieu de +5,4 Md€ ; gain 4,0 au lieu de 4,4. **Plus les revenus des couples sont partagés, moins l'impôt individuel rapporte et coûte aux couples.** |
| H12 | **Charge actuelle par type de foyer.** La charge de chaque tranche est répartie selon des cas-types OpenFisca : salariés, sans niche. Les niches sont donc réparties au prorata de la charge. Les retraités sont des personnes de plus de 65 ans (abattement des personnes âgées), sans autre revenu. | « Qui paie » entre types, cas des retraités | Corrigé pour les couples de retraités (section 5). Restent les retraités de moins de 65 ans, qui n'ont pas l'abattement (leur charge actuelle est sous-estimée, leur hausse surestimée, de moins de 0,5 Md€ selon une estimation non calculée), et les niches réelles, concentrées sur certains foyers (emploi à domicile, dons). |
| H13 | **Enfants.** Un enfant par parent isolé (1,97 M de cases T). Deux enfants par couple « avec enfants » : 86 % des couples mariés ou pacsés actifs. Pas d'enfant chez les retraités ni chez les concubins. La même proportion dans toutes les tranches. | Quotient familial (13,4 Md€), familles, franchise par enfant | Les parents isolés ont en moyenne plus d'un enfant : à 1,4 enfant, le quotient vaut 13,0 Md€. Il y a en réalité 8,78 M de foyers avec des enfants mineurs, concubins et parents isolés compris : la moyenne « couple avec deux enfants » (−1 085 €) porte sur une population trop large. Les familles de trois enfants ne sont pas dans les agrégats. En cas-type, elles gagnent à la proposition (−1 900 à −2 400 € de 40 à 80 k€), mais paient +1 300 € avec le barème neutre à 80 k€. |
| H14 | **Niches supprimées** : au moins 24 Md€ (15,5 de réductions et crédits, 5,3 d'abattement de 10 %, 2,9 de demi-parts, 0,5 d'abattement des personnes âgées). | Récit ; le calcul utilise l'IR observé | Le montant n'entre pas dans le calcul. La demi-part des parents isolés (0,87) est comptée deux fois (`verif_ir_csg.md`). La suppression de l'aide à l'emploi à domicile et des dons est une hypothèse politique. |
| H15 | **Famille de barèmes** : quatre nœuds, 50 % en haut, grilles finies. | Neutre, optimum, proposition | Robuste : un optimum non borné ne gagne que 0,01 Md€ ; la proposition avec un seuil supérieur de 2 M€, 0,02 Md€. Le neutre est mal identifié (écarts d'un euro), mais son gain varie de moins de 0,1 Md€. |
| H16 | **Contrainte de répartition** : ±500 € par décile, et le 1 % du haut ne monte pas. | Choix de la proposition | C'est un choix politique, pas un résultat. Les moyennes par décile cachent 29 % de perdants de plus de 500 € (12,1 M de foyers). |
| H17 | **Recette constante avant réaction**, et ce qui reste hors champ : CASA (0,3 %), prélèvement de solidarité sur les loyers (7,5 %), CEHR. | Recette, très hauts revenus | La CEHR disparaîtrait sur les revenus du barème ; elle n'est pas comptée dans la comparaison (3 à 4 points au très haut). L'IRCOM est supposé inclure l'IR au PFU et exclure la CEHR (non vérifié). |
| H18 | **Passage du net imposable au brut** : 1,20 pour les salaires, 1,055 pour les pensions, 1,35 pour les gérants (hypothèse), 1,04 pour le chômage, 1,15 / 1,06 pour les indépendants et les loyers. | Assiette, taux | Une erreur de 5 % sur les gérants et les indépendants (environ 130 Md€) déplace l'assiette d'environ 6 Md€, soit environ 0,1 point de taux. |
| H19 | **Cas-types OpenFisca** (France 176.1, droit 2024) : salariés du privé, sans niche ; couples à 60/40 ou à un seul revenu ; enfants nés en 2015 ; retraité né en 1950 ; RFR N−2 = RFR de l'année ; Smic à 21 500 € brut. | Tous les cas-types | Le Smic de 2024 vaut environ 21 270 € et celui de 2025, 21 620 €. Pour le retraité, le RFR N−2 fixé au RFR de l'année fait alterner le taux de CSG aux seuils (section 4). |
| H20 | **Transition** : interpolation linéaire des montants dus. | Section 6 de la partie | Elle tient la recette chaque année, mécaniquement. Elle suppose de calculer deux impôts en parallèle pendant toute la transition, et ne dit rien de l'affectation de la CSG (Sécurité sociale) ni de la CRDS (CADES). |

---

## 4. Chiffres non vérifiés, ou vérifiés ici

Sources téléchargées dans `scratchpad/dl_hyp_brochure2025/` (lues avec `pdftotext`, jamais exécutées) ou consultées en
ligne.

| Chiffre | Où il sert | Source et statut |
|---|---|---|
| Barème de l'IR des revenus 2024 (11 497 / 29 315 / 83 823 / 180 294 €) | Étape 1, IR actuel | **Vérifié** : brochure pratique IR 2025, p. 361 (impots.gouv.fr) |
| Plafond du quotient familial : 1 791 € par demi-part, 4 224 € pour la part du premier enfant d'un parent isolé ; décote 889 / 1 470 € et 45,25 % | Quotient familial, variante « quotient » | **Vérifié** : brochure IR 2025 ; BOFiP BOI-IR-LIQ-20-20-20 (14/04/2025), § 40 et 70 |
| Revenus à partir desquels le plafond joue : couple avec deux enfants 70 829 € ; parent isolé avec un enfant 44 894 € (revenu imposable) | « Part des familles au plafond » | **Vérifié** : brochure IR 2025, tableau 4 |
| Part des familles au plafond du quotient familial | Récit sur les familles | **Non vérifié sur une source primaire.** Selon le modèle, 1,77 M de foyers : 20 % des couples avec deux enfants et 10 % des parents isolés. Repère de presse : 1,0 à 1,4 M de foyers touchés par l'abaissement du plafond à 1 500 € en 2014 (chiffres du gouvernement et de Bercy rapportés par la presse, non relus à la source). |
| Abattement des plus de 65 ans (2 796 € jusqu'à 17 510 €, 1 398 € jusqu'à 28 170 €) ; abattement de 10 % sur les pensions plafonné à 4 399 € par foyer | Cas-types des retraités | **Vérifié** : brochure IR 2025 |
| Coût de l'abattement de 10 % : 5,3 Md€ | Récit, « niches » | **Vérifié** (`verif_litterature_ircsg.md`, n° 11) : amendement AN I-CF1856 ; Voies et moyens lus dans le fichier du dépôt (budget.gouv.fr est inaccessible) |
| Minimum vieillesse : 12 523,14 € par an (1 043,59 € par mois, personne seule) ; 19 442,21 € pour un couple qui touche l'allocation | Exonération des pensions jusqu'à 12 500 € | **Vérifié** : service-public.fr F16871 (montants 2026, page vérifiée le 23/06/2026). L'imposition de l'ASPA n'est pas vérifiée. |
| Seuils de CSG des retraités | Marches de la CSG, cas-types | **2026** (RFR 2024) : 13 048 / 17 057 / 26 472 €, demi-part +3 484 € (exonération). **Vérifié** sur service-public.fr F2971. **2024** (droit des cas-types) : 12 230 / 15 988 / 24 813 €, demi-part +3 265 € : valeurs d'OpenFisca, non relues sur une source officielle. `ir_csg.py` utilise les seuils de 2025 (12 817 / 16 755 / 26 004), sans effet sur le total, qui est calé. La règle des deux années consécutives ne vaut que pour le passage aux taux médian et plein (service-public), pas pour la sortie de l'exonération. |
| « 1 000 € de pension en plus peuvent coûter 620 à 770 € » | Situation actuelle | **Vérifié sur OpenFisca 2024** : 617 à 774 € aux seuils de 16 500, 17 000, 19 500, 20 000, 30 000 et 30 500 € de pension. Le calcul retient la convention RFR N−2 = RFR de l'année : en régime stable, le saut existe, décalé de deux ans. |
| Retraité seul à 17 000 € « exonéré aujourd'hui » | Cas-type central | **Vérifié** (OpenFisca 2024), mais c'est un cas limite. Son RFR (12 504 €) dépasse le seuil de 2024 (12 230 €) ; il reste exonéré parce que le RFR N−2, en euros de 2022, était plus bas. Le cas-type n'y arrive que par l'alternance des passages. À 18 000 €, il paierait 774 €. C'est bien le pire cas, à dire comme tel. |
| « Près de 60 % de coin entre 1 et 1,5 Smic » | Argument contre les marches | **Partiellement exact.** Calcul de l'auteur sur les barèmes 2025 de l'OCDE : hors IR-CSG, par euro de coût du travail, 55,6 % à 1 Smic pour une personne seule (cotisations non contributives 39,0 + prime d'activité 16,6), mais 39,0 % à 1,5 Smic, la prime d'activité étant éteinte vers 1,28 Smic. IR-CSG compris : 60,6 % et 50,2 %. Pour un couple, 39 %. Depuis 2026, la réduction générale dégressive unique s'éteint à 3 Smic (Tmin 0,02, Tdelta ≈ 0,378, exposant 1,75 ; FAQ Agirc-Arrco lue partiellement et sites secondaires ; décret non lu) : le coin est plus faible à 1,5 Smic et plus fort entre 1,6 et 3 Smic. **Écrire : « environ 55 % au Smic pour une personne seule (droit 2025) ».** |
| Prime d'activité : 61 % des revenus d'activité (2025) | Coin, PTR | 59,85 % en 2026 (service-public.fr F2882, décret de mars 2026). La valeur de 2025 est cohérente avec les fichiers OCDE ; non relue. |
| Smic horaire : 11,65 € (janvier-octobre 2024), 11,88 € (novembre 2024-2025), 12,02 € (janvier 2026), 12,31 € (juin 2026) | Coin, marge extensive, cas-type | Sources secondaires (presse, résumé de service-public) ; non relu au Journal officiel |
| PASS 2025 : 47 100 € | Coin | Non relu (cohérent avec les seuils des fichiers OCDE) |
| 90 Md€ de revenus au PFU ; IR à 12,8 % | Recette, très hauts revenus | Totaux 2042 de la DGFiP (fichier du dépôt) : **vérifié dans les données**. Les 12,8 % sont une convention ; le partage au prorata du RFR donnerait 15,1 Md€ d'IR au PFU, et 76,6 Md€ d'IR au barème au lieu de 80,2. |
| L'« impôt net » de l'IRCOM inclut l'IR au PFU et exclut la CEHR | Très hauts revenus | **Non vérifié** |
| CSG des pensions : 25,4 Md€ (CCSS 2024 : 24,81 + un tiers de l'invalidité) ; CSG du chômage : 0,561 Md€ | Calage de la CSG | Recopiés de la CCSS par le dépôt ; **non relus** (la fiche CCSS n'a pas été retrouvée en ligne) |
| 18,0 M d'enfants (0CF 15,15 + 0DJ 2,01 + 0CH / 2) ; 13,05 M de couples (0AM 11,21 + 0AO 1,84) ; 1 965 339 cases 0BT ; 8,78 M de foyers avec enfants mineurs ; 13,15 M (1AS) et 4,32 M (1BS) de pensionnés | Représentation des foyers | **Vérifié** dans `donnees/ir_2042_cases_revenus2024.csv` (DGFiP) |
| Partage des revenus dans le couple : part moyenne de la femme 36 % | H11 | Insee Première 1492 : vérifié (`verif_ir_csg.md`). Le passage à quatre classes est une hypothèse. |
| Écart de pension de droit direct entre femmes et hommes : 38 % (fin 2023), 25 % avec la réversion | Variante H11 | DREES, *Les retraités et les retraites*, édition 2025 (communiqué ; fiche non relue) |
| Coefficient de 1,35 pour les gérants ; 1,15 / 1,06 pour les indépendants et les loyers ; 70 % des revenus des indépendants et des loyers qui réagissent | Assiette, perte sèche | **Hypothèses non vérifiées** |
| Charge actuelle des retraités : 47,6 Md€ | « Les retraités financent » | **Résultat du modèle, non observable.** Ni la DGFiP ni la DREES ne publient l'IR des foyers de retraités. |
| Élasticités : 0,03 (LMR, salariés à l'année) ; 0,26 / 0,09 (Sicsic, IR / RSA) ; 0,31 (Cabannes et al., décile du haut) ; 0,25 (Chetty et al., participation) | H2 | Vérifiées dans `verif_litterature_ircsg.md` et `cours/elasticites-france.tex`. Les valeurs du modèle (0,05 / 0,10) sont des **choix**, pas des estimations. |
| Taux marginal d'IR-CSG d'aujourd'hui (personne seule : 9,5 % jusqu'à 23 k€ brut, puis 21 %, 32 % vers 40 k€, 40 % au-delà de 113,6 k€) | Situation actuelle | Vérifié sur OpenFisca (`verif_ir_csg.md`) et sur l'OCDE *Taxing Wages* (écart inférieur à 0,1 point) |

---

## 5. Erreurs trouvées et corrigées

### E1. La CRDS manquait dans le taux marginal actuel

**Le défaut.** `modele_purs.TAU0` venait de `ir_csg/sorties/marges_openfisca.csv`, qui ne compte que l'IR et la CSG (à
12 000 € brut, 9,2 % et non 9,7 %). La charge actuelle, elle, comprend la CRDS, et le taux du nouvel impôt la remplace.
Le défaut était connu (`verif_ir_csg.md`, point 4) et jugé petit. Mais avec la méthode v2, où chaque euro perdu est
coûté au coin total, il vaut 0,4 Md€, soit environ 10 % du gain.

**La correction.** `TAU0 = v.bl.TAU_CUR + v.T_CRDS` : 0,5 % de la même assiette, dans `synthese/modele_purs.py`.

### E2. La charge actuelle des couples de retraités était sous-estimée

**Le défaut.** Le modèle approchait cette charge par celle d'un couple d'actifs, multipliée par le rapport retraité seul
/ actif seul à la moitié du revenu. Cela revient à supposer que les seuils de CSG d'un couple valent deux fois ceux
d'une personne seule. Or ils valent le seuil d'une part plus deux demi-parts : 18 760 € de RFR en 2024, au lieu de
24 460 €. Taux de charge d'un couple de retraités, approximation contre OpenFisca : 0,0 contre 5,7 % à 30 k€ de
pension, 4,5 contre 8,0 % à 40 k€, 9,5 contre 12,1 % à 50 k€.

**La correction.**
- Nouveau cas-type OpenFisca 176.1, droit 2024 : deux retraités nés en 1950, pensions 60/40. Script
  `synthese/openfisca_couple_retraites.py` (à lancer avec `python3.13`), sortie
  `synthese/sorties/couple_retraites_openfisca.csv`.
- `modele_purs._U["retraite_couple"]` utilise ce cas-type.
- L'ancienne approximation reste calculée pour contrôle (`_U_ANCIEN`, ligne « contrôle » de `controles_purs.txt`).

### Scripts relancés et chiffres qui changent

**Scripts relancés.** `architectures_ircsg.py`, `etapes_ircsg.py`, `controle_hauts_purs.py` et
`perte_seche_ircsg_purs.py`. Les anciennes sorties sont gardées dans `scratchpad/verif_ircsg/hyp/avant/` (avant les
deux corrections) et `.../apres_crds/` (après E1 seule).

**Ce qui ne change pas.** Le barème neutre, l'optimum, les deux propositions, les déciles, le 1 % et le 10 % du haut,
les cas-types, les tranches de `controle_hauts_purs` et le prix d'un milliard.

**Ce qui change (avant → après).**

| Chiffre (texte actuel de `ircsg.tex` ou tableaux) | Avant | Après | Cause |
|---|---|---|---|
| Gain, étape 1 | 2,4 (0,9 à 5,2), intensif −0,2 | 2,8 (1,1 à 6,1), intensif +0,2 | E1 |
| Gain, barème neutre | 4,0 (1,9 à 9,2) ; « un peu moins de la moitié (1,8) vient de la reprise d'emploi » | 4,4 (2,1 à 10,1) ; la participation (1,8) en fait 41 % | E1 |
| Gain avec une franchise de 4 000 / 8 000 € | 4,6 / 5,0 | 4,9 / 5,4 | E1 |
| Gain atteignable | 7,8 (3,8 à 18,2) | 8,1 (4,0 à 19,1) | E1 |
| Part de l'atteignable : neutre ; avec franchise ; chemin à 30 % | 52 % ; 59 à 64 % ; 69 % | 54 % ; 61 à 66 % ; 70 % | E1 |
| Proposition (franchise de 4 000 €) | 4,9 (2,3 à 11,1), 63 % | 5,3 (2,5 à 12,0), 64 % | E1 |
| Proposition (franchise de 8 000 €) | 5,2 (67 %) | 5,6 (68 %) | E1 |
| Variante « quotient » : gain | 3,9 contre 4,0 pour le neutre | 4,3 contre 4,4 | E1 |
| Revenu déclaré, neutre / proposition | +3,0 (1,5 à 4,5) / +3,8 | +3,3 (1,6 à 4,9) / +4,1 (2,0 à 6,1) | E1 |
| Perte sèche quadratique actuelle (`controles_purs`) | 18,1 | 18,8 | E1 |
| Retraités : étape 1 / neutre / franchise de 4 000 € | +4,7 / +7,0 / +14,0 Md€ | +2,1 / +4,4 / +11,4 | E2 |
| Retraités, proposition ; actifs | +15,2 ; −15,2 | +12,6 ; −12,6 | E2 |
| Retraités, proposition avec franchise de 8 000 € ; couple de retraités | +22,8 ; +3 189 € | +20,3 ; +2 333 € | E2 |
| Retraité seul / couple de retraités, proposition | +603 / +2 325 € | +662 / +1 468 € | E2 |
| Couples avec deux enfants : étape 1 / neutre / proposition | +904 / +570 / −1 195 € | +1 013 / +679 / −1 085 € | E2 |
| Parent isolé / personne seule active, proposition | −234 / −321 € | −169 / −231 € | E2 |
| Abattement de 10 % gardé : hausse des retraités | « de 7 à 1 Md€ » | de 4,4 à −1,7 Md€ : les retraités paieraient moins qu'aujourd'hui | E2 |
| Petites pensions exonérées : hausse des retraités | « 3 Md€ » | 0,6 Md€ | E2 |
| Perdants de plus de 500 € : étape 1 / neutre / franchise de 4 000 € | 19 / 25 / 30 % | 17 / 23 / 31 % (proposition : 29 %, inchangé) | E2 |
| « Les retraités paient de 7 à 23 Md€ de plus » (`methode_v2.md`) | 7 à 23 | 4 à 20 | E2 |

**Fichiers à régénérer (non faits ici, car ils écrivent des `.tex`).**
- `synthese/tables_ircsg.py` écrit `parties/tab_ircsg_arch.tex` et `tab_ircsg_dec.tex`.
- `synthese/figures_ircsg_purs.py` écrit les figures `ircsg_p01` à `p03` et leurs notes.
- `parties/ensemble.tex` : IR-CSG 4,9 (2,3 à 11,1) → 5,3 (2,5 à 12,0) ; « moindre optimisation +1,9 à +5,7 » → +2,0 à
  +6,1 ; ensemble « environ 7 (2,5 à 15,5) » → environ 7,3 (2,8 à 16,4).
- `revue/methode_v2.md`, § 3 : les chiffres y sont à mettre à jour.

**Défaut non corrigé.** Le même oubli de la CRDS subsiste dans `synthese/ps_ircsg_methode.py` (ancien modèle à foyers
mélangés) et dans `ir_csg/` (`bareme_v3.cout_actuel`, `proposition.systeme`). Ces scripts ne servent plus à la note.

### Imprécisions du texte actuel, pour la réécriture

Aucun fichier `.tex` n'a été modifié.
- **Étape 1.** « Le taux marginal d'une personne seule saute de 1,5 % » : c'est 1,4 % par euro brut (1,55 % × 0,887).
- **Étape 1.** « Il vient tout entier de la reprise d'emploi » : c'est encore vrai à 93 % (2,6 sur 2,8).
- **Pensions.** « Entre 12 500 et 25 000 € de pension, […] le taux marginal à 28 % » : c'est 28 % jusqu'à 22 500 €,
  puis jusqu'à 34 % juste sous 25 000 € (deux fois le taux marginal du barème).
- **Coin.** « Près de 60 % entre 1 et 1,5 Smic » : voir la section 4.
- **Très hauts revenus.** Le calage sur l'IR observé soutient la convention « haut », dans laquelle la proposition baisse
  leur impôt (H9). Le texte présente les deux conventions à égalité.

---

## 6. Calculs manquants pour la nouvelle architecture, et faisabilité

| Sous-partie | Calcul | État | Faisabilité |
|---|---|---|---|
| 1. Situation actuelle | Recettes des trois impôts : dans le champ (80,2 / 132,4 / 7,4) et au niveau national (comptes nationaux 2024 : IR 96,2, CSG 153,1, CRDS 9,1 ; IRCOM : 91,7) | Disponible | — |
| 1 | Passage de 80 à 197 Md€ : niches, assiette, quotient familial, décote, quotient conjugal | Essai fait (`v8_decomp_ir.py`) ; l'écart de 29,7 Md€ entre l'IR simulé sans niche et l'IR observé n'est pas bouclé | Faisable en l'intégrant à `etapes_ircsg.py`. Boucler l'écart demande les montants par niche (Voies et moyens) et les heures supplémentaires exonérées. |
| 1 | Taux moyens et marginaux par cas-type | Disponible pour 5 profils (`courbes_openfisca.csv`) et, désormais, pour le couple de retraités | Faisable avec OpenFisca 176.1 (installé pour `python3.13`, testé : `of/cas_nouveaux.py`) : couple avec 1 ou 3 enfants, couple sans enfant à un revenu, parent isolé, indépendant. |
| 1 | Actifs contre retraités au même revenu | Cas-types : un retraité seul paie 4,3 % à 20 k€ net, contre 10,7 % pour un actif seul ; 11,0 contre 15,0 % à 30 k€. Agrégats du modèle : 11,7 contre 16,0 %. | Disponible. Les agrégats sont des résultats du modèle, à signaler comme tels. |
| 1 | Couples avec et sans enfants ; comparaison internationale | Cas-types OpenFisca ; fichiers OCDE *Taxing Wages* du dépôt | Disponible |
| 2. Problème | Coin marginal par niveau de salaire (droit 2025 et 2026) | Tableau 2025 dans `revue/methode_perte_seche.md` § 6 | Pour 2026 (réduction générale dégressive unique), faisable avec la formule (`v9_rgdu.py`), à vérifier sur le décret. |
| 3. Réforme naïve | Étape 1, impôt individuel | Disponible | — |
| 3 | Réforme naïve qui **garde l'imposition commune** (quotient conjugal et familial actuels), plus proche de « harmoniser les assiettes en gardant les barèmes » | **Calculée ici** (`v6_naive_transition.py`) : barème de l'IR seul 162,2 Md€ ; taux proportionnel 3,91 % ; gain 1,8 Md€ ; déciles −13 … +2 091 € (dernier décile +8,9 Md€) ; retraités +7,5 Md€ ; 22 % de perdants | Faisable dans `etapes_ircsg.py`. |
| 4. Proposition | Système, comparaison avec aujourd'hui | Disponible | — |
| 5. Arbitrages : retraité modeste | Retraité seul à 10, 12,5, 15, 17, 20, 25, 30 et 40 k€ de pension (proposition / neutre) : 0 / +500 ; 0 / +719 ; +700 / +975 ; +1 260 / +1 207 ; +1 240 / +740 ; +1 311 / +143 ; +1 211 / +137 ; +54 / −1 033 € | **Calculé ici** | Disponible |
| 5 | Couple avec trois enfants (60/40) | Aujourd'hui 3 812 / 5 718 / 8 234 € à 40 / 60 / 80 k€ brut. Proposition : −2 385 / −1 908 / −1 884 € ; neutre : −1 137 / −33 / +1 287 €. **Cas-types calculés ici** (OpenFisca + barèmes). | Cas-types : faisable et fait. Agrégat des familles nombreuses : demande de refaire la représentation des enfants (nombre d'enfants par foyer, non publié dans les totaux 2042). |
| 5 | Couple à un seul revenu | Avec deux enfants : disponible. Sans enfant, **calculé ici** : 30 / 50 / 80 k€ → proposition +328 / +1 475 / +3 371 € ; neutre −137 / +1 360 / +2 243 € | Disponible |
| 5 | Couple de retraités (60/40) | **Calculé ici** : 25 / 35 / 50 k€ de pension → proposition −375 / +315 / +555 € ; neutre +400 / +128 / −1 019 €. La moyenne du modèle (+1 468 €) dépend du partage (H11). | Disponible |
| 5 | Parent isolé avec deux enfants au Smic | Proposition −1 619 € ; neutre −577 € | Disponible (l'agrégat suppose un enfant par parent isolé, H13) |
| 5 | Prix et financement de chaque arbitrage (points de taux pour tous, perte de gain) | Disponible (`architectures_ircsg.txt`) | — |
| 6. Transition | Hausse annuelle des principaux perdants sur 3, 5 ou 10 ans | **Calculé ici** (proposition, interpolation linéaire). Retraité à 17 k€ (+1 260) : 420 / 252 / 126 € par an. Retraités au 90e centile (+1 970) : 657 / 394 / 197 €. Couples de retraités au 90e centile (+3 819) : 1 273 / 764 / 382 €. Ensemble des foyers au 90e centile (+1 442) : 481 / 288 / 144 €. 12,1 M de foyers perdent plus de 500 €, dont 8,3 M de retraités. | Faisable. Les centiles sont ceux de foyers représentatifs : **la dispersion réelle est plus forte**, et le 99e centile (+4 600 €) en est un minorant. |
| 6 | Trésorerie, endettement transitoire | Recette mécaniquement constante chaque année avec une interpolation linéaire des montants dus | Pas de calcul nécessaire. À dire : affectation de la CSG (Sécurité sociale) et de la CRDS (CADES), double calcul pendant la transition. |
| Très hauts revenus | Part des revenus au PFU par tranche calée sur l'IR observé | **Essai** (`v5_pfu_calage.py`) : au-delà de 1 M€, 87 à 93 % des « autres revenus » sont au PFU ; le calage échoue entre 100 et 200 k€ | Partiellement faisable. Un calage complet demande les réductions d'impôt et les enfants par tranche (données DGFiP non publiées) ou une microsimulation. |
| Annexe | Sensibilités de la section 3 (saillance, partage, couples, coin 2026) | Calculées ici | À intégrer dans un script du dépôt pour l'annexe. |
| Hors de portée | Foyers mixtes (loyers des retraités, couples dont un seul conjoint est retraité) ; dispersion réelle des perdants ; chômeurs | — | **Non faisable** avec l'IRCOM ; il faut une microsimulation sur fichiers individuels (Ines, ERFS ou données DGFiP). |

---

## 7. Scripts de vérification (scratchpad, non versionnés)

Tous les scripts sont dans
`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/hyp/`. Ils se
lancent depuis `fiscalite/` avec `python3 -B`, sauf `of/*.py`, qui se lancent avec `/usr/bin/python3.13`.

| Script | Rôle | Sortie |
|---|---|---|
| `v1_recette.py` | Recette de 220 Md€ refaite depuis le CSV IRCOM, sans importer le modèle | — |
| `v2_independant.py` | Barèmes, types de foyers, répartition, cas-types et perte sèche v2 recodés à partir des seules entrées du modèle | `final/v2_independant.txt` |
| `v3_bords.py` | Bords des grilles (fait avant les corrections : seuls les écarts comptent) | — |
| `v4_sensib.py` | Quotient familial recodé, part des familles au plafond, sensibilités H6, H10, H11 | `final/v4_sensib.txt` |
| `v5_pfu_calage.py` | Calage du PFU sur l'IR observé | — |
| `v6_naive_transition.py` | Réforme naïve avec imposition commune, centiles des hausses, retraités modestes | `final/v6_naive_transition.txt` |
| `v7_saillance.py` | Hypothèse H1 | `final/v7_saillance.txt` |
| `v8_decomp_ir.py` | Décomposition de 80 à 197 Md€ | — |
| `v9_rgdu.py` | Coin 2026 | `final/v9_rgdu.txt` |
| `v10_couple_retraites.py` | Diagnostic de E2 | — |
| `of/cas_nouveaux.py`, `of/couple_retraites.py` | Cas-types OpenFisca | — |
