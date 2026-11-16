# Partie Immobilier : méthodes de chiffrage revérifiées et registre des hypothèses

*16/11/2026. Préparé pour la réécriture de `synthese/parties/foncier.tex` selon `synthese/CHARTE_NOTE.md`. Ce registre
est la source du tableau d'annexe « Hypothèses fortes et chiffres non vérifiés ». Fichiers relus : `foncier/README.md`,
`foncier/simulation.py` et ses sorties, `foncier/figures_foncier.py`, `foncier/notes/`, `synthese/perte_seche_autres.py`
et sa sortie, `revue/methode_v2.md`, `revue/methode_perte_seche.md`, `revue/verif_foncier.md`, `revue/revue_foncier.md`,
`revue/verif_litterature_foncier.md`. Les chiffres attribués à la littérature ont déjà été contrôlés sur les textes
(`verif_litterature_foncier.md`) ; ils ne sont pas repris ici.*

**Comment les chiffres ont été refaits.** Un script indépendant (il n'importe pas `simulation.py`) relit
`foncier/donnees/` et réimplante la méthode : `verif_foncier/verif.py` dans le scratchpad de la session (non versionné ;
sortie `verif.txt`). Avant toute modification, `simulation.py` relancé sur une copie redonne `simulation.txt` et
`primo.csv` à l'octet près. Mentions : **[recalc.]** recalculé et identique ; **[calc.]** calcul nouveau de ce
registre ; **[conv.]** convention de l'auteur, sans estimation publiée ; **[NV]** non vérifié sur une source primaire.

## En bref

- **Les chiffres clés sont justes** : 6 762 Md€, 23,6 et 11,4 Md€, coût de 5,7 / 4,6 Md€, taux national de 0,185 %,
  variations par décile, Paris +122 %, 70 % des taxes qui doublent situées à Paris, délais de 24 à 39 ans, perte sèche
  de −1,9 Md€. Aucun ordre de grandeur n'est absurde.
- **Quatre chiffres du texte actuel sont faux ou incohérents** (§ 5.2) :
  - la perte sèche « sol seul » vaut −0,6 Md€, non −0,5 ;
  - les 213 et 106 M€ de Paris et des Hauts-de-Seine supposent un taux national plus bas que le taux de référence ;
  - les 31,6 Md€ de taxe foncière sur les logements sont de 2025, à côté des 42 Md€ de 2024 ;
  - « jusqu'à 660 € par an » : 5 % des logements dépassent ce montant.
- **Un défaut de conception de la transition** : 88 % du montant des hausses de plus de 300 € vient du taux national
  sur le terrain, que la note applique en totalité dès la première année. L'étalement sur dix ans ne porte que sur la
  redistribution communale. À Paris, il couvre 10 € sur 660 € (§ 6, point 10).
- **Hypothèse la plus forte, absente de l'encadré actuel.** Le modèle suppose qu'à l'intérieur d'une commune la taxe
  foncière actuelle est proportionnelle à la valeur. Il ne voit donc pas la principale redistribution individuelle du
  passage des valeurs de 1970 à la valeur de marché : entre quartiers d'une même ville, le rapport taxe/valeur varie du
  simple à 1,6 à Paris. Les parts de logements perdants (23 %, 5,4 %) sont des ordres de grandeur, probablement
  sous-estimés.
- **Un biais de vieillissement** (ratio de 2017 appliqué aux valeurs de 2024, en plus de la croissance communale de la
  taxe) compte deux fois la hausse des prix. Ordre de grandeur : Paris +109 % au lieu de +122 %. Les déciles sont peu
  touchés (§ 3, H6).
- **Script corrigé** : `foncier/simulation.py` affiche désormais les délais de rattrapage actualisés à 3 %, ceux que le
  texte utilise déjà, et l'impôt sur le bâti de chaque variante. Aucun chiffre du texte ni aucune figure ne change (§ 5.1).

---

## 1. La méthode en clair

**Le champ.** Les 30,5 millions de logements des particuliers de France métropolitaine hors Alsace-Moselle (où DVF
n'existe pas), soit environ 94 % de la métropole. Ils sont obtenus en retirant du parc du recensement de 2022 les HLM
loués. Le champ comprend donc les résidences secondaires, les logements vacants et environ un million de logements
détenus par d'autres personnes morales. L'unité de calcul est la *cellule* « commune × maisons » ou « commune ×
appartements ». Tous les logements d'une cellule y sont identiques.

**La valeur.** Prix médian au m² des ventes 2023-2024 de la commune (repli sur l'intercommunalité, puis sur le
département, sous 10 ventes), multiplié par la surface médiane des logements vendus. Total : 6 762 Md€.

**La part du terrain.**
- *Maisons* : prix au m² des terrains à bâtir de la commune (sinon celui du département, ajusté par une régression sur
  l'écart de prix des maisons), multiplié par la parcelle médiane plafonnée à 1 500 m².
- *Appartements* : 1 − coût de reconstruction / prix au m². Ce coût (1 560 €/m², le même partout) est calé pour que le
  terrain fasse 45,4 % de la valeur totale, comme dans les comptes de patrimoine.
- Bornes de 10 et 90 %.

**La taxe foncière actuelle.** Le rapport taxe/valeur de chaque commune en 2017 (Insee Analyses n° 91), multiplié par
la valeur de 2024 et par la croissance propre de la taxe de la commune entre 2017 et 2024 (REI). Le tout est calé sur
19,2 Md€ (2017) × 1,296 × part du champ, soit 23,6 Md€ ou 773 € par logement.

**Les droits de mutation.** 5,81 % (4,50 % départemental, 1,20 % communal, frais d'assiette de l'État) de la valeur
annuelle moyenne des ventes de logements anciens en 2023-2024 dans DVF : 196 Md€ de ventes, 11,4 Md€ de droits.

**Les scénarios.** Tous remplacent la moitié des droits (5,7 Md€) par de la taxe foncière, à recette constante :
- *R50, réforme naïve* : taxe actuelle relevée de 24 % partout ;
- *K4* : deux taux nationaux sur la valeur de marché, le terrain taxé quatre fois plus que le bâti ;
- *N4, proposition* : chaque commune garde sa recette, répartie selon deux taux (terrain = 4 × bâti), et un taux
  national sur la valeur des terrains remplace les droits perdus.

**La perte sèche.** Elle se calcule sur deux marges.
- *Ventes* : un triangle de Harberger, σ·V·(τ₁² − τ₀²)/2, où σ est la baisse des ventes par point de droits.
- *Capital bâti* : un triangle ε_K·(K/u)·(t₁² − t₀²)/2, où t est l'impôt sur le bâti rapporté à la valeur du bâti et
  u le coût d'usage.
- Le terrain ne réagit pas à l'impôt et n'entre donc dans aucun des deux triangles.

**Le primo-accédant.** Il achète le logement médian de la commune. On compare l'économie de droits à l'achat à la valeur
actuelle (taux de 3 %) de la hausse de taxe foncière, sans effet sur les prix, ou avec capitalisation complète des deux
mouvements.

---

## 2. Chiffres clés vérifiés

| Chiffre (texte actuel) | Recalcul | Statut |
|---|---|---|
| Prélèvements sur l'immobilier : 116 Md€, 4 % du PIB | 69 + 25 + 12,5 + 8,4 + 1,5 = 116,4 Md€ ; 3,97 % de 2 935 Md€ | OK. Mais 12,5 Md€ de successions est une estimation (clé de 60 % du CPO) et le PIB n'a pas été relu [NV] |
| « TFPB 42 Md€, dont environ 31,6 sur les logements » | 42,0 est le chiffre de 2024, 31,6 celui de 2025 ; en 2024, 30,5 (Compte du logement) | **années mélangées** : écrire 30,5 |
| Droits : 14,1 Md€ (2024), 16,7 (2025), dont 13,6 sur les logements | Compte du logement 2025 : 13,568 Md€ (2025), 11,239 (2024), 13,002 (2023) | OK (lu sur la source par `notes/inventaire.md`) |
| Taux de 5,81 % | 4,5 + 1,2 + 2,37 % × 4,5 = 5,807 % | OK. En 2024, l'Indre et le Morbihan étaient à 3,80 % (§ 4) : taux moyen pondéré de 5,795 %, droits surestimés de 22 M€, effet négligeable |
| Valeur du parc : 6 760 Md€, 17 à 19 % sous l'Insee | 6 762 Md€ ; Insee (4 807 + 4 043) au prorata du champ : 8 375 Md€ ; rapport 0,81 [recalc.] | OK. Écart **non uniforme** : le prix moyen des ventes dépasse la valeur modélisée de 24 % dans le décile de communes le moins cher, de 6 à 10 % au milieu, de 21 % dans le plus cher [calc.] |
| Taxe foncière actuelle : 23,6 Md€ ; 773 € par logement | 19,2 × 1,2964 × 0,9463 = 23,55 Md€ [recalc.] | OK. Le champ des 19,2 Md€ est plus étroit que celui du calage (§ 3, H7) |
| Droits : 11,4 Md€ par an | 11,37 Md€ ; 786 000 ventes par an ; rotation de 2,6 % du parc [recalc.] | OK |
| Coût de la baisse de 50 % : 5,7 Md€, ou 4,6 si +6 % de ventes par point | 5,69 / 5,18 / 4,64 / 4,26 Md€ pour 0 / 3 / 6 / 8 % ; baisse de 30 % : 3,41 / 2,99 / 2,56 / 2,27 [recalc.] | OK |
| Hausse de taxe foncière nécessaire : 20 à 24 % | 24,1 % ; 19,7 % avec reprise des ventes | OK |
| Taux national sur le terrain : 0,19 %, 0,15 % avec reprise | 0,1854 % et 0,1512 % ; sur des valeurs au niveau de l'Insee, 0,150 % et 0,122 % [recalc.] | OK |
| Deux taux nationaux : 0,73 % sur le terrain, 0,18 % sur le bâti | 0,733 % et 0,183 % | OK |
| TF / valeur aujourd'hui : 0,52 % → 0,18 % selon le décile ; Paris 0,12 % | 0,52 … 0,18 ; Paris 0,124 % [recalc.] | OK. Paris : 0,140 % si l'on corrige le vieillissement (H6) |
| Proposition : TF +3 % à +69 % selon le décile ; charge totale de −75 à +133 € | +3 … +69 % ; −63, −66, −75 … +133 € [recalc.] | OK |
| TF / valeur après réforme : 0,54 % → 0,30 % | 0,54 … 0,30 | OK |
| Un logement sur quatre au-delà de +300 € ; un sur vingt dont la taxe double | 23,0 % ; 5,4 % [recalc.] | OK, en cellules et non en avis d'imposition (H1) |
| Parmi les taxes qui doublent : 70 % à Paris, 14 % dans les Hauts-de-Seine | 70 % et 14 % [recalc.] | OK, sous la même réserve. Avec deux taux nationaux (K4) : 28 % à Paris |
| Paris : +122 % ; dernier décile hors Paris : +51 % | +122 % (+648 € par logement) ; +51 % [recalc.] | OK. +109 % avec la correction de vieillissement |
| Maisons +150 € / appartements +240 € ; variante +230 / +130 € | +149 / +237 ; variante +228 / +131 | OK (résultat non robuste : H5) |
| Impôt sur le bâti : de 14 à 7 Md€ | 14,07 → 7,31 Md€ [recalc.] | OK |
| Rattrapage du primo-accédant : 24 à 39 ans à Paris, Lyon, Bordeaux et Limoges ; jamais à Nantes, Arcachon, Ussel, Guéret | Paris 27, Lyon 39, Bordeaux 24, Limoges 28 ans ; jamais pour les quatre autres ; taxe en baisse à Annecy et Saint-Étienne [recalc.] | OK. `simulation.py` affichait des durées non actualisées : corrigé (§ 5.1) |
| Économie à l'achat : 2 300 € à 22 700 € ; Paris 12 100 € ; Lyon 8 100 € ; Nantes 13 000 € | 2 266 / 22 700 / 12 083 / 8 105 / 13 051 € | OK (Nantes : 13 100 € à la centaine près) |
| Appartement parisien : +660 €/an ; 22 000 € en valeur actuelle ; 8 000 € (2 %) si tout se capitalise | 660 € ; 21 997 € ; 8 252 € (1,98 %) | OK, mais « jusqu'à 660 € » est faux (§ 5.2) |
| Compensation : la taxe communale de 1,2 Md€ reste à compenser | Perte de 5,69 Md€ = 4,41 (départements) + 1,18 (communes) + 0,10 (frais de l'État) [recalc.] | OK |
| Paris paie 213 M€ et les Hauts-de-Seine 106 M€ de plus qu'ils ne perdent | Reproduits seulement pour un taux national limité à la part départementale (≈ 0,147 %). Au taux de référence de 0,185 % : +268 et +133 M€ nets de leur perte totale [recalc.] | **incohérent** avec le taux de référence (§ 5.2) |
| Perte sèche sur les ventes : −1,5 Md€ (0,8 à 3,7 pour σ de 3 à 15) ; −1,0 pour une baisse de 30 % | −1,49 (−0,74 à −3,72) ; −1,01 [recalc.] | OK |
| Perte sèche sur le bâti : −0,4 Md€ | −0,43 (ε_K = 1, u = 4,5 %) [recalc.] | OK |
| Gain central d'environ 2 Md€ par an, 0,07 % du PIB | −1,92 Md€ ; 0,066 % | OK |
| Rapport terrain/bâti 2, 4 ou sol seul : −0,2, −0,4, −0,5 Md€ | Par commune : −0,26 / −0,43 / **−0,60** ; deux taux nationaux : −0,23 / −0,46 / −0,60 [calc.] | **−0,5 est faux** à u = 4,5 % : il suppose u = 5 % |
| Coût d'appariement : de l'ordre de 3,5 Md€ (Määttänen et Terviö) | Interpolation linéaire entre 30 € (droit de 2 %) et 180 € (6 %) : 173 − 64 = 109 € par ménage, soit 3,3 Md€ en euros de 2004 et environ 4,5 Md€ en euros de 2024 si l'on revalorise [calc.] | Ordre de grandeur juste ; les 116 € de `methode_perte_seche.md` ne se retrouvent pas |

---

## 3. Hypothèses fortes

Classées selon leur capacité à changer une conclusion. Colonne « Effet si fausse » : sens et ordre de grandeur, quand on
a pu le mesurer.

| # | Hypothèse | Où elle joue | Effet si elle est fausse |
|---|---|---|---|
| H1 | **Dans une commune, la taxe foncière actuelle est proportionnelle à la valeur de marché** : même rapport taxe/valeur pour tous les logements, maisons comme appartements | Toutes les variations individuelles ; parts de perdants (23 % au-delà de +300 €, 5,4 % qui doublent, 70 % à Paris) | Le modèle ne voit pas la redistribution *à l'intérieur* des communes, que produit le passage des valeurs de 1970 à la valeur de marché. Or elle est grande : à Paris, le rapport taxe/valeur des quartiers (IRIS) va de 0,074 % (1er décile) à 0,121 % (9e) ; dans l'agglomération lyonnaise, de 0,25 à 0,52 % (IA 91, fig. 3a et 3b) [calc.]. Les gagnants et les perdants sont donc plus nombreux et plus extrêmes que simulé. Non chiffrable sans les fichiers fonciers (Majic). À dire dans le texte |
| H2 | **Tous les logements d'une cellule sont identiques** (valeur médiane, taxe moyenne) | Mêmes indicateurs ; cas-types | Les pourcentages de logements sont des pourcentages de cellules. « Un logement sur vingt voit sa taxe doubler » se lit comme un ordre de grandeur, pas comme un nombre d'avis d'imposition |
| H3 | **Valeur = prix médian au m² × surface médiane** | Tous les taux exprimés en part de la valeur (0,52/0,18 % ; 0,19 % ; 0,73/0,18 %) | Niveau sous-estimé de 19 %, donc taux surestimés d'autant ; les recettes restent justes. Biais en U : sous-estimation de 24 % dans les communes les moins chères, de 6 à 10 % au milieu, de 21 % dans les plus chères [calc.]. Corrigé de ce biais, le rapport taxe/valeur actuel irait d'environ 0,42 à 0,15 % : la régressivité tient. Présenter le taux national comme une **cible de recette** (5,7 Md€), pas comme « 0,19 % » |
| H4 | **Terrain des appartements = valeur − coût de reconstruction**, coût uniforme de 1 560 €/m², calé sur l'agrégat des comptes de patrimoine (lui-même un résidu) ; bornes de 10 et 90 % | Répartition du taux national entre communes (Paris : 84 % de terrain) ; impôt sur le bâti ; perte sèche sur le bâti | Aucune variation régionale ni d'âge du coût. 2,8 M logements (9 %) sont à la borne de 10 % : la valeur y est inférieure au coût de reconstruction, et le chiffre est arbitraire [calc.]. Si le coût était de 2 500 €/m² à Paris, la part du terrain y tomberait à 75 % et la hausse parisienne d'environ 11 % [calc. indicatif]. Le coût calé n'a été comparé à aucune source publiée [NV] |
| H5 | **Terrain des maisons = prix des terrains à bâtir × parcelle médiane** (plafond 1 500 m² ; imputation par une élasticité de 1,54 estimée sur 3 307 communes) | Partage de la charge entre maisons et appartements | Les terrains à bâtir sont des lots viabilisés, pas le sol sous une maison existante. Avec un résidu pour les maisons aussi, le classement s'inverse : maisons +228 €, appartements +131 € (`simulation.txt`, VARIANTE). **Ne rien conclure sur qui, des maisons ou des appartements, paie davantage** |
| H6 | **Vieillissement 2017 → 2024.** Le modèle applique le ratio de 2017 aux valeurs de 2024, *puis* la croissance relative de la taxe de chaque commune | Taxe actuelle par commune, donc tous les pourcentages de hausse | La croissance des prix est comptée deux fois : le bon calcul serait ratio 2017 × valeur 2017 × croissance de la taxe. Les prix ont crû de 11 % à Paris (appartements), 13 % en Île-de-France hors Paris, 28 % en province et 24 % en métropole entre 2017 et 2023-2024 (indices Notaires-Insee, § 4). Correction grossière à trois zones [calc.] : Paris 0,124 → 0,140 % de la valeur ; hausse de **+122 → +109 %** ; déciles +3…+69 → +4…+65 % ; parts de perdants inchangées (5,4 % et 22,8 %). Incohérence de méthode, à corriger proprement avec DVF 2017-2019 ou des indices départementaux (§ 5.3) |
| H7 | **Calage sur 19,2 Md€ (2017)** | Niveau de la taxe actuelle, donc pourcentages de hausse | IA 91 : 19,2 Md€ pour les logements **et dépendances** de **28,4 M** logements de propriétaires résidents retrouvés dans Fidéli, en métropole, et non pour les 30,3 M logements des particuliers. Le calage rapporte ce montant à un champ plus large (logements moins HLM). La taxe actuelle est donc peut-être sous-estimée, jusqu'à 7 % ; le recoupement avec le Compte du logement (≈ 24 Md€ dans le champ) la situe à moins de 5 %. Effet : hausses en pourcentage un peu surestimées |
| H8 | **Assiette des droits de 2023-2024, taux de départ de 5,81 %** | Coût de la baisse, taux national, perte sèche | 2023-2024 est le creux du cycle : 11,2 à 13,0 Md€ sur les logements, contre 16,4 à 16,8 en 2021-2022. Au milieu du cycle, la baisse coûterait 7 à 8 Md€ (France entière, calcul indicatif de `verif_foncier.md`). Le droit en vigueur jusqu'au 31/3/2028 est de 6,32 % dans 88 départements : diviser par deux ce taux coûte 9 % de plus. Le champ exclut les autres biens (≈ 3,1 Md€ de droits), l'outre-mer et l'Alsace-Moselle |
| H9 | **Les ventes augmentent durablement de 6 % par point de baisse** (σ ; fourchette de 0 à 8 %, ou de 3 à 15 % pour la perte sèche) | Coût (5,7 contre 4,6 Md€) ; taux national (0,19 contre 0,15 %) ; perte sèche sur les ventes (−1,5 Md€) | Aucune étude ne donne 6 % : c'est une médiane construite par la note de lecture [conv.]. En France, rien de durable selon Bérard et Trannoy ; −10 % dans les seuls marchés détendus selon Bachelet et Poulhès ; aucun effet sur les volumes en Allemagne selon Dolls et al. **Si σ ≈ 0, le gain sur les ventes disparaît** et il ne reste que le bâti (−0,4 Md€). La perte sèche est linéaire en σ |
| H10 | **Incidence** : deux cas polaires (prix inchangés / capitalisation complète des deux mouvements) | Gain du primo-accédant, perte du propriétaire installé, « transfert entre générations » | Les études se contredisent : l'acheteur paie la hausse de 2014 (Bachelet et Poulhès) ; le vendeur paie en Allemagne (Dolls et al.) ; capitalisation complète (Høj et al.) ou nulle (Nielsson et al., non publié) de l'impôt danois sur le sol. Garder les deux cas, et l'argument de liquidité |
| H11 | **Perte sèche sur le bâti** : ε_K = 1, u = 4,5 %, offre de logements non contrainte [conv.] | −0,4 Md€ ; écart entre réforme naïve et proposition | ε_K = 0,5 : −0,22 ; u = 3,5 % : −0,56 ; u = 6 % : −0,33 [calc.]. Là où le zonage bloque la construction (les zones chères, où le terrain pèse le plus), ε_K est plus faible. **Omission** : les droits sont aussi un impôt annuel implicite sur le capital (2,6 % de rotation × 5,81 % ≈ 0,17 % de la valeur par an). Compté sur le bâti, ce coin porte le terme bâti de la proposition à −0,9 Md€ et celui de la réforme naïve à +0,04 [calc., variante]. À l'inverse, le loyer imputé non taxé peut inverser le signe du terme bâti (+0,9 ε_K, `methode_perte_seche.md`) |
| H12 | **Chaque commune garde sa recette ; la réforme ne porte que sur les logements des particuliers** | Proposition N4 | Les HLM, les locaux professionnels (révisés en 2017) et la taxe d'enlèvement des ordures ménagères (9 Md€, assise sur la même base [NV]) restent hors du modèle. Si la nouvelle assiette s'étendait à eux, il y aurait des transferts non simulés |
| H13 | **Le taux national est reversé aux départements (et aux communes) selon leurs pertes** | Finances locales | Péréquation implicite de 809 M€ entre départements. Paris et les Hauts-de-Seine paient 20 % du produit national pour 7 % des logements (Paris seul : 13 % du produit pour 3,8 % des logements) [calc.]. Les départements échangent un impôt à taux voté contre une dotation |
| H14 | **Actualisation de 3 % réels**, hausse constante en euros réels, logement médian | Délais de rattrapage, valeur actuelle de la perte (22 000 €) | Koster et Pinchbeck mesurent 3 à 4 % en Angleterre. À 4 %, la perte en valeur actuelle passe de 22 000 à 16 500 € et les délais s'allongent |
| H15 | **Le taux calé sur le champ s'applique à toute la France** | Taux national ; recettes par département | Champ = 94 % de la métropole. L'Alsace-Moselle et l'outre-mer paient aussi des droits ; leurs valeurs de terrain sont inconnues |
| H16 | **Âge des données** : recensement 2022, REI 2024, DVF 2023-2024, ratios de 2017 | Tout | Les prix ont baissé en 2023-2024, puis remonté (indice de mars 2026 : −1 % sur le trimestre, selon l'Insee). À actualiser si la réforme vise 2028-2030 |
| H17 | **Exonérations non modélisées** (plus de 75 ans sous condition de revenu, logements neufs) | Cas-type « retraité modeste » ; taux national | La taxe actuelle est nette des exonérations à l'échelle de la commune. On ne sait pas si elles s'appliqueraient au taux national : il faut le décider |
| H18 | **Coût d'appariement (Määttänen et Terviö) transposé** à 30,5 M logements | « Le gain pourrait doubler » | Modèle d'Helsinki, euros de 2004, gain par ménage et non par logement. Ce coût mesure les mêmes échanges manqués que le triangle sur les ventes : il le **remplace**, il ne s'y ajoute pas. Total ≈ −3,3 − 0,4 ≈ −3,7 Md€ |
| H19 | **Valeurs de zone établies en quatre ans environ**, comme dans le Bade-Wurtemberg | Calendrier ; durée de la surtaxe transitoire | Le Bade-Wurtemberg disposait déjà de valeurs du sol par zone (*Bodenrichtwerte*) ; la France part de DVF et DV3F. Délai probablement plus long, financement transitoire plus lourd |

---

## 4. Chiffres vérifiés ici, déjà vérifiés, ou non vérifiés

**Vérifiés ici sur source primaire** (fichiers dans le scratchpad, `telech_foncier/`, lus avec `python3 -I` ou
`pdftotext`) :

| Chiffre | Source | Ce qu'elle dit |
|---|---|---|
| 19,2 Md€ de taxe foncière des ménages en 2017 | Insee Analyses n° 91, p. 1 et encadré 2 (https://www.insee.fr/fr/statistiques/fichier/7735076/IA91.pdf) | « Le total de la taxe foncière sur les logements et dépendances possédés par les ménages atteint 19,2 milliards d'euros en 2017 » ; 660 € par logement. Champ : 28,4 M logements de particuliers résidents appariés à Fidéli ; valeurs estimées en métropole ; 30,3 M logements détenus par les particuliers ; HLM 5,6 M ; autres personnes morales 1,1 M (H7) |
| Dispersion du rapport taxe/valeur à l'intérieur des villes | IA 91, fichier de données (IA91.xlsx), fig. 3a, 3b, 3d, 3e | Rapport du 9e au 1er décile des IRIS : Paris 1,64 ; agglomérations de Lyon 2,09, de Toulouse 1,76, de Lille 1,52 (H1) |
| Taxe foncière en % du revenu disponible des propriétaires | IA 91, fig. 2 | 2,4 % au centile médian de niveau de vie ; 3,7 % au 10e centile ; 2,8 % au 20e ; 1,6 % au dernier |
| Prix 2017 → moyenne 2023-2024 | Insee, indices Notaires-Insee, séries brutes en base 2015 (API SDMX de la BDM : 010567058 métropole, 010567012 Paris appartements, 010567072 province, 010567088 Île-de-France hors Paris) | Métropole ×1,239 ; Paris ×1,113 ; province ×1,281 ; Île-de-France hors Paris ×1,134 (H6) |
| Taux départemental en 2024 | Weblex, « Taux des droits d'enregistrement en matière de vente immobilière 2024 » (source secondaire) ; tableau officiel des impôts lu à travers le résumé du moteur de recherche (PDF en 404) | Indre, Morbihan et Mayotte à 3,80 %, les autres à 4,50 %. Le Morbihan passe à 4,50 % au 1/6/2025 [SECONDAIRE] |
| Régression du prix des terrains (élasticité 1,54 sur 3 307 communes), coût calé de 1 560 €/m² | Recalcul indépendant sur `foncier/donnees/` | 1,543 ; 3 307 ; 1 560 €/m² (1 525 €/m² avec la cible publiée de 45,7 %) |

**Déjà vérifiés sur source primaire par d'autres revues** (renvoyer à ces fichiers) :
- OCDE 2023 : 1,90 / 0,95 / 0,72 / 0,37 % du PIB (API SDMX) : `verif_litterature_foncier.md` n° 1.
- Insee Première n° 2081 (logements 4 807 Md€, terrains bâtis 4 043 Md€) : `verif_foncier.md` § C.
- Compte du logement 2025 (droits et taxe foncière sur les logements), note REI 2025 (taxe foncière 42,0 et 43,1 Md€),
  OFGL (droits 14,1 et 16,7 Md€), DGFiP Statistiques n° 43 (IFI, successions), BOFiP (5 % de 2025 à 2028, exclusion
  des primo-accédants), tableaux DGFiP (88 départements à 5 %) : `notes/inventaire.md` [TEXTE LU].
- Taux parisien passé de 13,5 à 20,5 % en 2023 : IA 91, p. 2.
- Toute la littérature citée : `verif_litterature_foncier.md`.

**Non vérifiés : à signaler dans le texte, ou en annexe** :

| Chiffre | Où il sert | État |
|---|---|---|
| Part immobilière des successions : 60 % (12,5 Md€) | Inventaire (116 Md€) | Clé conventionnelle du CPO ; aucune ventilation de la DGFiP |
| PIB 2024 de 2 935 Md€ | « 4 % du PIB », « 0,07 % du PIB » | Repris de `inventaire.md`, non relu ici |
| 3 993 Md€ de terrains (code) contre 4 043 (publication) | Calage de la part du terrain | Origine introuvable ; effet de 0,3 point, coût calé de 1 525 au lieu de 1 560 €/m² |
| Frais d'assiette de 2,37 % ; 0,26 à 0,32 Md€ | Taux de 5,81 % | Taux lu dans le CPO et le BOFiP, article 1647 non relu sur Légifrance ; montant calculé |
| Taxe foncière hors logements : 11,5 Md€ | Inventaire | Différence entre deux périmètres (REI et Compte du logement) |
| Taxe d'enlèvement des ordures ménagères assise sur la base de la taxe foncière | Transition | Article 1522 non relu |
| Plafond de revenu de l'exonération des plus de 75 ans : 12 793 € pour une part (2026) | Cas-type du retraité | LégiFiscal [SECONDAIRE] |
| σ = 6 % par point | Coût, taux national, perte sèche | Convention (H9) |
| ε_K = 1 ; u = 4,5 % | Perte sèche sur le bâti | Conventions (H11) |
| Coût de reconstruction de 1 560 €/m² | Part du terrain | Calé, jamais comparé à une source publiée (H4) |
| Environ 1 M logements de particuliers outre-mer | Écart de 17 % (au lieu de 19 %) à l'Insee | Hypothèse de `verif_foncier.md` |
| Apport de 10 à 20 % du prix | « La baisse représente un septième à un tiers de l'apport » | Loan-to-value moyenne de 84,7 % (CCSF 2026, d'après `droits_mutation.md`) : apport moyen d'environ 15 %. Fourchette non sourcée |
| Taxe foncière non récupérable sur le locataire, déductible des revenus fonciers au régime réel | Cas-type du bailleur | Non vérifié : à lire dans le décret n° 87-713 et à l'article 31 du CGI |

---

## 5. Erreurs

### 5.1 Corrigées dans les scripts

`foncier/simulation.py` (relancé ; seules ces lignes de `sorties/simulation.txt` changent ; `primo.csv` et les figures
sont identiques) :
1. **Délais de rattrapage non actualisés.** `cas_types` affichait « amorti en économie / hausse ans », sans
   actualisation, alors que tout le reste du modèle actualise à 3 % et que le texte cite les durées actualisées.
   - Ligne affichée désormais : « rattrapé en N ans à 3 % (M ans sans actualisation) », ou « jamais rattrapé » quand la
     rente perpétuelle de la hausse reste inférieure à l'économie.
   - Proposition : Paris 27 ans (18 sans actualisation), Lyon 39 (23), Bordeaux 24 (17), Limoges 28 (19) ; jamais à
     Nantes, Ussel, Guéret et Arcachon.
   - Réforme naïve : jamais à Paris, Lyon, Bordeaux, Annecy et Arcachon ; 84 ans à Nantes ; 14 à 24 ans dans les
     villes moyennes.
   - Le texte actuel (24 à 39 ans) est déjà juste.
2. **Ligne [CONTROLE] ajoutée** : l'impôt sur le bâti après chaque variante. Taxe actuelle relevée de 24 % : 17,5 Md€ ;
   par commune, 2 × : 10,6 ; national, 2 × : 11,0 ; par commune, 4 × : 7,3 ; national, 4 × : 6,8 ; sol seul : 0. Elle
   permet de calculer la perte sèche des arbitrages (§ 2) et de la réforme naïve (§ 6).
3. **Docstring** : elle décrivait encore la part du terrain par résidu pour tous les logements.

`synthese/perte_seche_autres.py` n'a **pas** été modifié : un autre agent le modifiait pendant ce travail (partie PFU,
modifications non validées). La partie Immobilier de sa sortie est inchangée (−1,93 Md€). À y ajouter quand le fichier
sera libre :
- bâti avec un rapport de 2, 4 ou sol seul : −0,26 / −0,43 / −0,60 par commune ; −0,23 / −0,46 / −0,60 avec deux taux
  nationaux ;
- réforme naïve : +0,32 sur le bâti, −1,16 Md€ au total pour σ = 6 ;
- variante avec le coin des droits sur le capital (H11).

### 5.2 Erreurs ou imprécisions du texte actuel (`foncier.tex` non modifié) : à corriger dans la réécriture

1. « TFPB (42 Md€, dont environ 31,6 Md€ sur les logements) » : 42 est le chiffre de 2024 et 31,6 celui de 2025.
   Écrire **30,5 Md€** (2024).
2. Tableau des arbitrages, « −0,2, −0,4, −0,5 Md€ » : le sol seul vaut **−0,6** avec u = 4,5 %, la convention de tout
   le reste du calcul.
3. Tableau, « Paris paie 213 M€ de plus qu'elle ne perd, les Hauts-de-Seine 106 M€ (part départementale seule) ».
   - Ces montants supposent un taux national qui ne remplace que la part départementale (≈ 0,147 %). Or la référence
     retient 0,19 %, qui lève aussi la part communale.
   - Au taux de référence, Paris paie 755 M€ et perd 486 M€ (377 départementaux, 101 communaux, le reste en frais de
     l'État) : **+268 M€**. Les Hauts-de-Seine : **+133 M€**.
   - Pour Paris, une seule collectivité perçoit les deux parts : comparer à la seule part départementale n'a pas de sens.
4. Tableau, « 0,65 % de la valeur dans les communes pauvres, 0,22 % dans les riches » : les déciles portent sur le
   **prix au m²**, pas sur le revenu. Écrire « les moins chères » et « les plus chères ».
5. « Jusqu'à 660 € par an pour l'appartement médian parisien » : « jusqu'à » est faux.
   - 5 % des logements dépassent +660 €/an et 1 % dépassent +760 € ; 9,5 % dépassent +500 € ; 0,4 % dépassent
     +1 000 €.
   - Plus fortes hausses (cellules d'au moins 1 000 logements) : maisons de Saint-Tropez +3 200 €/an (+92 %), Megève
     +2 470 €, Ramatuelle +2 220 €, La Clusaz +2 170 €, Cassis +2 050 € (+136 %) [calc.].
6. Transition : « Le taux national sur le terrain s'applique en totalité dès la première année. Seule la nouvelle
   répartition de la taxe communale est étalée sur dix ans. »
   - Le calcul est juste, mais le texte laisse croire à une transition douce. Or le taux national porte 88 % du montant
     des hausses de plus de 300 € et 94 % de celui des taxes qui doublent ; pour l'appartement parisien médian, 650 €
     sur 660 € [calc.].
   - Après la surtaxe transitoire de 24 % (+125 € à Paris), la première année de la nouvelle assiette ajoute **+526 €
     d'un coup** à Paris. 7 % des logements prennent plus de +300 € cette année-là, quel que soit l'étalement communal.
7. « Un septième à un tiers » de l'apport : 2,9 points rapportés à 20 % ou 10 % du prix font 14,5 % et 29 %. Écrire
   « un septième à trois dixièmes ».
8. « Il pourrait doubler si l'on compte le coût des logements mal adaptés (3,5 Md€) » : préciser que ce chiffrage
   **remplace** le triangle sur les ventes (H18). Total ≈ −3,7 Md€.
9. L'encadré « Non modélisé » doit ajouter les hypothèses H1, H6, H12 et H17.

### 5.3 Incohérence de méthode non corrigée dans le script

Le vieillissement de la taxe actuelle (H6) compte deux fois la hausse des prix. La correction propre demande les
valeurs de 2017 par commune, qui ne sont pas dans le dépôt (DVF 2017-2019, ou indices départementaux). La correction à
trois zones de ce registre est trop grossière pour remplacer le calcul central : elle sert d'ordre de grandeur (Paris
+109 % au lieu de +122 %). À l'auteur de décider. En attendant, le texte peut écrire « environ +110 à +120 % » pour
Paris.

### 5.4 Défauts mineurs relevés, non corrigés

- `foncier/README.md`, section « Proposition retenue » : elle mélange encore le scénario avec reprise des ventes et des
  chiffres périmés (« +2 % à +60 % », « −86 à +26 € », « 18 % »). Les sorties actuelles donnent +3 à +69 %, −75 à
  +133 € et 23 % (sans reprise).
- `figures_foncier.py`, figure de l'inventaire : `f"{g:.0f}"` affiche 12,5 comme « 12 » et 1,5 comme « 2 ». À régler
  quand les figures seront refaites sous les nouveaux noms (`foncier_nNN_…`).

---

## 6. Calculs qui manquent pour la nouvelle architecture : lesquels sont faisables

Les premiers chiffres ci-dessous viennent de `verif.py` [calc.]. Ils ne sont pas encore dans le dépôt, sauf mention.

| # | Calcul | Faisable ? | Premiers chiffres, données à ajouter |
|---|---|---|---|
| 1 | **Qui paie la taxe foncière aujourd'hui, par statut d'occupation** | Oui, avec les données du dépôt (recensement 2022 et modèle ; taxe moyenne de la commune appliquée à chaque statut) | Propriétaires occupants 12,7 Md€ (54 %) ; logements loués par des particuliers 5,8 Md€ (24 %) ; résidences secondaires 2,6 Md€ (11 %) ; vacants 2,0 Md€ (8 %) ; logés gratuitement 0,5 Md€ (2 %) |
| 2 | **Par revenu** | Oui, sur données publiées (IA 91, fig. 1 et 2, données de 2017, fichier téléchargé). Croiser les variations par commune avec le revenu médian communal (Filosofi) est faisable après un téléchargement | Parmi les propriétaires : 3,7 % du revenu disponible au 10e centile de niveau de vie, 2,4 % au centile médian, 1,6 % au dernier. Rapportée au patrimoine immobilier : 0,67 % au 40e centile, 0,22 % au dernier |
| 3 | **Par âge** | Non avec les données du dépôt ; aucune publication ne ventile la taxe foncière par âge (IA 91 ne le fait pas). Approximation possible : taux de propriétaires par âge (tableaux détaillés du recensement) × taxe moyenne | À télécharger |
| 4 | **Droits de mutation par âge ou revenu des acheteurs** | Non : DVF ne décrit pas l'acheteur. Possible seulement à partir de tableaux publiés (Notaires, enquête Logement 2020) | Au mieux : âge moyen des primo-accédants, à vérifier |
| 5 | **Par type de commune** | Oui (fait) ; la grille de densité de l'Insee peut s'ajouter par un téléchargement | Taxe par logement : 594 € (moins de 1 000 habitants), 740 €, 839 €, 876 € (20 000-100 000), 791 € (plus de 100 000) ; taxe/valeur de 0,38 à 0,30 % ; droits annuels par logement de 225 à 501 € |
| 6 | **Comparaison internationale** | Oui : déjà extraite (`notes/inventaire.md` § 8, API de l'OCDE) | Impôts périodiques sur l'immobilier, 2024 : France 1,95 % du PIB ; Royaume-Uni 2,80 ; États-Unis 2,67 ; Belgique 1,26 ; Italie 1,05 ; Allemagne 0,37. Transactions (titres compris) : France 0,62 ; Italie 1,05 ; Belgique 0,89 ; Espagne 0,81 ; Allemagne 0,29. Moyenne de l'OCDE (2023) : 0,95 et 0,37 |
| 7 | **Réforme naïve** (droits divisés par deux, taxe actuelle +24 % partout) | Oui, **déjà simulée** (scénario R50) | Taxe +106 à +237 € par logement et par an selon le décile ; taxe/valeur de 0,65 % (communes les moins chères) à 0,22 % (les plus chères) ; charge totale de +28 à −231 €. Perdants relatifs : les zones détendues (Guéret +233 €/an, Ussel +260 €, contre +31 et +19 € avec la proposition). Perte sèche −1,16 Md€ contre −1,92 pour la proposition : l'écart de 0,76 Md€ vient tout entier du bâti (conventions ε_K = 1, u = 4,5 %). Avec le coin des droits sur le capital : −1,45 contre −2,40 |
| 8 | **Proposition comparée à aujourd'hui** | Oui (figures fon_01 et fon_02) ; ajouter la distribution | Variation de taxe, du 10e au 99e centile des logements : −8, +45 (25e), +129 (médiane), +279 (75e), +495 (90e), +660 (95e), +760 € (99e) |
| 9 | **Cas-types** | Oui avec le modèle actuel ; les revenus sont illustratifs | **Jeune ménage primo-accédant** : déjà calculé (`primo.csv`, figure fon_04). **Retraité modeste dans une zone chère** : appartement parisien médian, +660 €/an (proposition) ou +125 € (réforme naïve). Exonéré s'il a plus de 75 ans et un revenu fiscal de référence d'au plus 12 793 € pour une part [SECONDAIRE], si l'exonération vaut aussi pour le taux national (H17). Nombre de bénéficiaires : non disponible. **Propriétaire en zone détendue** : Guéret et Ussel, voir la ligne 7. **Bailleur** : même variation de taxe ; déductible au régime réel, pas au micro-foncier [NV] ; répercussion sur les loyers des nouveaux locataires de 50 à 89 % à Berkeley (Baker, 2025, d'après les notes LVT). **Famille qui s'agrandit** : droits divisés par deux sur l'achat (maison nantaise : −13 050 €) |
| 10 | **Transition sur 3, 5 ou 10 ans** | Oui (fait) ; il faut choisir un calendrier | Si toutes les composantes montent linéairement, hausse annuelle : 9e décile de 165 / 99 / 49 € ; 99e centile de 253 / 152 / 76 € ; appartement parisien de 220 / 132 / 66 €. Avec le calendrier actuel de la note (taux national plein dès la première année), Paris prend +526 € la première année, quel que soit l'étalement communal (§ 5.2, point 6) |
| 11 | **Financement transitoire** ; coût de transition et coût permanent | Oui | Coût permanent : nul (recette constante). Si les droits baissent dès l'annonce et que le taux national monte linéairement, déficit cumulé de 5,7 / 11,4 / 25,6 Md€ (sur 3, 5 ou 10 ans ; ×0,81 avec la reprise des ventes). Avant que les valeurs existent (environ 4 ans), sans surtaxe : environ 23 Md€ (18,6 avec la reprise). La surtaxe uniforme (20 à 24 %) supprime le déficit, mais elle reprend la réforme naïve pendant la transition, au détriment des zones détendues |
| 12 | **Distribution à l'intérieur des communes** (gagnants et perdants individuels) | Non avec les données du dépôt : il faut les fichiers fonciers (Majic) et des valeurs individuelles. Ordre de grandeur possible par IRIS à partir d'IA 91 (fig. 3a à 3e) | Voir H1 |
| 13 | **Effets sur les prix, la natalité, la mobilité professionnelle** | Non : seuls les cas polaires d'incidence sont calculables | — |
