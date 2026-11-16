# Vérification chiffre par chiffre : « Moins taxer les ventes, mieux taxer le sol »

*16/11/2026. Note vérifiée : `foncier/note-foncier.tex` (version du 15/11/2026, 22 h 38), avec ses quatre notes de
figures `figures/nu/fon_0*_note.tex`, `foncier/sorties/simulation.txt`, `primo.csv` et `foncier/README.md`.*

**Méthode.** `simulation.py` a été relancé sur une copie (scratchpad `verif_foncier/`) : `simulation.txt` et
`primo.csv` sont reproduits **à l'octet près**. Les figures sont postérieures à la dernière exécution du modèle
(22 h 35 contre 22 h 34). Chaque nombre a été retrouvé dans une sortie, recalculé, ou rapproché de la note de lecture
qui le source (`notes/inventaire.md`, `droits_mutation.md`, `taxe_fonciere_split_rate.md`). Les chiffres de la
littérature sont donc vérifiés **contre les notes de lecture, pas contre les textes primaires**. Repères externes
consultés le 16/11/2026 : Insee Première n° 2081 (comptes de patrimoine, fin 2024), page DGFiP Statistiques n° 46
(taxe foncière 2025), notes Insee-Notaires (nombre de ventes). Scripts de contrôle :
`v2_verif.py` et `v3_verif.py` dans le dossier de travail, non versionnés.

Statuts : **OK** ; **ERREUR** (avec la bonne valeur) ; **ARRONDI DOUTEUX** ; **NON VÉRIFIABLE** ; **SUSPECT** (calcul
juste, ordre de grandeur discutable).

---

## A. Erreurs et absurdités, par gravité

### A1. Erreurs qui changent une conclusion ou un chiffre mis en avant

**1. Gain d'efficacité mal multiplié (l. 240-242).** Texte : « déplacer 5,7 Md€ rapporte de l'ordre de 1,5 à 4 Md€
par an, 0,05 à 0,15 % du PIB », avec un coût de 0,3 à 0,9 € par euro.
- Calcul : 5,7 × 0,3 = **1,7 Md€** et 5,7 × 0,9 = **5,1 Md€**, soit **0,06 à 0,17 % du PIB** (PIB 2024 : 2 935 Md€,
  `inventaire.md`).
- « 1,5 à 4 » correspond à 4,6 Md€ × 0,3 à 0,9 = 1,4 à 4,1 Md€, c'est-à-dire à la perte **avec** reprise des ventes.
  La revue précédente (`revue_foncier.md`, point 4) avait proposé « 1,5 à 4 Md€ » ; le texte a gardé ce chiffre en
  changeant la base.
- *Correction* : « déplacer 5,7 Md€ rapporte de l'ordre de 1,7 à 5 Md€ par an, 0,06 à 0,17 % du PIB », ou garder
  « 1,4 à 4 Md€ » en écrivant « 4,6 Md€ ».
- Remarque : on supprime la moitié haute du taux (de 2,9 à 5,8 %), là où le coût marginal est le plus élevé. Selon le
  texte lui-même (l. 126-129), il va de 0,7-0,9 € vers 4-5 % à 1-2 € au taux français. Une moyenne de 0,3 à 0,9 € sur
  les euros supprimés est donc plutôt basse.

**2. Les « années d'amortissement » ne sont pas actualisées, et la fourchette omet Nantes (l. 250-251).** Texte :
« ne rattrape cette économie qu'au bout de 17 à 23 ans dans les grandes villes, davantage ailleurs ».
- Ces durées viennent de `cas_types` (`simulation.py`, l. 216) : économie ÷ hausse annuelle, **sans actualisation**.
  Or la note actualise à 3 % deux lignes plus bas (« 22 000 € en valeur actuelle » = 660 / 0,03).
- Recalcul au même taux de 3 % (durée n telle que la valeur actuelle de la hausse égale l'économie) :

  | Cas-type (proposition N4) | Économie | Hausse TF/an | Durée simple | Durée actualisée à 3 % |
  |---|---:|---:|---:|---:|
  | Paris, appartement | 12 083 € | +660 € | 18,3 ans | **27 ans** |
  | Lyon, appartement | 8 105 € | +358 € | 22,7 ans | **39 ans** |
  | Bordeaux, appartement | 6 469 € | +377 € | 17,1 ans | **24 ans** |
  | Nantes, maison | 13 051 € | +252 € | 51,9 ans | **jamais** (perpétuité 8 385 €) |
  | Limoges, maison | 4 988 € | +264 € | 18,9 ans | **28 ans** |
  | Arcachon, maison | 22 700 € | +253 € | 89,7 ans | **jamais** (8 435 €) |
  | Ussel, maison | 2 982 € | +19 € | 157 ans | **jamais** (635 €) |
  | Guéret, maison | 3 193 € | +31 € | 104 ans | **jamais** (1 022 €) |
  | Annecy, maison ; Saint-Étienne, appartement | 20 125 € ; 2 266 € | −102 € ; −39 € | sans objet (la TF baisse) | sans objet |

- « 17 à 23 ans dans les grandes villes » exclut Nantes, sixième ville de France (52 ans sans actualisation). « Davantage
  ailleurs » est faux pour Limoges (19 ans), Annecy et Saint-Étienne (la taxe y baisse).
- *Correction* : « au taux de 3 % retenu plus loin, la hausse de taxe foncière ne rattrape l'économie qu'au bout de 24
  à 39 ans à Paris, Bordeaux, Limoges et Lyon, et jamais à Nantes, Arcachon ou dans les villes moyennes ; elle baisse à
  Annecy et Saint-Étienne ». La conclusion pour l'acheteur est **plus favorable** que ce qu'écrit la note.

**3. Les logements dont la taxe double ne sont pas « surtout sur le littoral » (l. 233-234).** Texte : « un sur vingt
(5 %, surtout à Paris et dans les communes littorales les plus chères) la voit plus que doubler ».
- Recalcul (scénario N4) : 1,65 million de logements, 5,4 % du champ.
  - **Paris : 70 %** ;
  - **Hauts-de-Seine : 14 %** (Boulogne-Billancourt, Courbevoie, Neuilly, Levallois, Issy, Montrouge, Puteaux, Rueil) ;
  - reste : 16 %, dont Haute-Savoie 3,5 % (Chamonix, Morzine), Pyrénées-Atlantiques 2,9 % (Biarritz, Saint-Jean-de-Luz),
    Alpes-Maritimes 2,4 %, Var, Morbihan, Savoie, Corse.
- *Correction* : « surtout à Paris (sept sur dix) et dans les Hauts-de-Seine ; le reste dans les stations littorales et
  de montagne ». Le texte ne dit pas non plus que **toute la ville de Paris** voit sa taxe plus que doubler en moyenne :
  +122 %, +648 € par logement, sur 1,16 million de logements.

**4. La compensation aux départements couvre aussi la part communale (l. 219-220 et 300-303).** Texte : « un taux
national unique de 0,19 % sur la valeur des terrains, reversé aux départements selon leurs pertes » ; « Paris
environ 270 M€, les Hauts-de-Seine 130 M€ ».
- La perte de 5,69 Md€ comprend **1,18 Md€ de taxe communale** (1,20 / 5,81) et 0,10 Md€ de frais d'assiette de
  l'État. Les départements ne perdent que 4,41 Md€. Calcul : `PART_DEP_DMTO`, défini mais jamais utilisé dans
  `simulation.py`.
- Si tout le produit va aux départements, ils sont surcompensés de 1,2 Md€ et les communes ne le sont pas.
- Les montants de Paris et des Hauts-de-Seine sont justes dans l'hypothèse du code : contribution nette de 268 et
  133 M€. Si l'on ne compense que la part départementale, elle tombe à **213 et 106 M€** ; avec reprise des ventes, à
  219 et 109 M€.
- *Correction* : dire qui reçoit la part communale (fonds départemental de péréquation ou communes), ou écrire
  « reversé aux départements et aux communes ».

**5. Les 16,7 Md€ ne viennent pas surtout des locaux professionnels (l. 190-191).** Texte : « les locaux
professionnels, qui portent le total des droits à 16,7 Md€ en 2025, ne sont pas traités ici ».
- Sur les seuls logements, les DMTO valent déjà 13,6 Md€ en 2025 (Compte du logement, `inventaire.md` § 3.1). Les
  autres biens (locaux, terrains) ne pèsent qu'environ **3,1 Md€** (calcul de la note de lecture).
- L'écart avec les 11,4 Md€ du modèle tient surtout :
  - à l'année : 2025 en reprise et majoration à 6,32 %, contre une moyenne 2023-2024 ;
  - au champ : outre-mer et Alsace-Moselle sont exclus.
- *Correction* : « la mesure porte sur les logements anciens (11,4 Md€ en moyenne en 2023-2024 dans le champ, 13,6 Md€
  sur tous les logements en 2025) ; les autres biens (environ 3 Md€) ne sont pas traités ».

### A2. Ordres de grandeur suspects (calcul juste, base discutable)

**6. La valeur du parc est inférieure d'environ 17 à 19 % aux comptes de patrimoine, et tous les taux « en % de la
valeur » sont gonflés d'autant.**
- Insee Première n° 2081, figure 2, fin 2024, ménages y compris entrepreneurs individuels et ISBLSM :
  - logements 4 807 Md€ ;
  - terrains bâtis 4 043 Md€ ;
  - total **8 850 Md€**.
- Rapporté au champ du modèle (30,46 M logements sur 32,19 M logements de particuliers en métropole selon
  `croissance_tf.json`), cela donne 8 370 Md€, ou environ 8 120 Md€ si l'on ajoute environ 1 M de logements outre-mer
  (hypothèse non vérifiée). Le modèle trouve **6 762 Md€, soit 81 à 83 %**.
- Indice concordant : la valeur moyenne d'un logement du modèle (222 000 €) est inférieure de 11 % au prix moyen des
  ventes DVF des mêmes communes (249 350 €, `v2_verif.py`). Le produit d'un prix médian par une surface médiane sous-estime
  la moyenne.
- Les **recettes** restent justes : taux × assiette modélisée. En revanche, les **taux affichés** sont surestimés
  d'environ 15 à 20 % par rapport à des valeurs vénales moyennes :
  - 0,19 % sur le terrain correspondrait à environ **0,15 %** sur les terrains au niveau des comptes de patrimoine
    (5,69 Md€ / 3 710 Md€) ;
  - 0,73 / 0,18 % correspondraient à environ 0,61 / 0,15 % ;
  - la taxe moyenne rapportée à la valeur serait de 0,29 % au lieu de 0,35 %.
- Appliqué tel quel à des valeurs administratives réalistes, le taux national de 0,19 % rapporterait environ 1 Md€ de
  plus que prévu.
- *À dire dans l'encadré* : « valeurs médianes, inférieures d'environ 18 % aux comptes de patrimoine ; les taux sont
  exprimés sur cette assiette ».

**7. Le coût de la baisse est mesuré au creux du cycle.** La base (moyenne 2023-2024) est la plus basse de la série du
Compte du logement :
- 13,0 Md€ en 2023 et 11,2 Md€ en 2024 ;
- contre 16,4 Md€ en 2021 et 16,8 Md€ en 2022 ;
- et 13,6 Md€ en 2025.

Aux volumes de 2021-2022, diviser les droits par deux coûterait de l'ordre de 7,5 à 8 Md€ (France entière, calcul
indicatif) au lieu de 5,7 Md€. Un taux national calé sur 2023-2024 serait donc trop bas en haut de cycle. Ce n'est pas
une erreur, mais il faut le dire.

**8. Le dernier décile, c'est d'abord Paris.** Les déciles sont formés de cellules commune × type, et Paris
(1,16 M d'appartements) forme à lui seul **38 %** du dixième le plus cher.
- « +69 % dans le plus cher » (l. 228) vaut **+51 % hors Paris** et +122 % à Paris.
- Même remarque pour « +215 % » (K4, l. 211) et pour « 560 € dans le dixième le plus cher » (l. 270).

**Repères vérifiés et cohérents** (aucune absurdité) :
- **Taxe foncière moyenne de 773 € par logement.**
  - Comptabilité nationale : la TFPB payée par les ménages en 2024 vaut 26,1 Md€ (`inventaire.md` § 2.1). Pour
    32-33 M logements de particuliers, cela fait environ 800 €. Le modèle se situe 3 à 5 % plus bas, ce qui est
    cohérent, car les ménages paient aussi la TFPB de biens non résidentiels.
  - DGFiP Statistiques n° 46 : le montant moyen de 1 117 € s'entend **par propriétaire particulier**, en 2025, sur un
    total qui comprend les taxes annexes (TEOM) et les frais de gestion. Il n'est pas comparable tel quel.
- **Recette totale (23,6 Md€).** Le calcul 19,2 × 1,296 × 0,946 = 23,55 Md€ est cohérent avec la TFPB des ménages au
  prorata du champ (environ 24 Md€) et avec la clé « ménages » du REI (60 % de 42 Md€).
  - Réserve : la croissance de 1,296 est celle de toute la TFPB. Or celle-ci a été diminuée en 2021 par la division par
    deux des valeurs locatives industrielles, compensée par l'État à hauteur de 2,4 Md€ en 2025. La croissance propre
    aux logements est donc probablement un peu plus forte. L'effet joue à la hausse, de quelques pour cent.
- **Part du terrain de 45 %.** Insee : 4 043 / 8 850 = 45,7 %. Le code utilise 3 993 Md€, chiffre que l'on ne retrouve
  pas dans la publication, ce qui donne 45,4 %. L'écart de 0,3 point est négligeable. Avec les autres bâtiments des
  ménages (233 Md€), on obtient 44,5 %, le « 44 % » des notes LVT.
- **Taux de 0,73 / 0,18 % et de 0,19 %.**
  - Ils sont compatibles avec les recettes : 0,733 % × 3 068 + 0,183 % × 3 694 = 22,5 + 6,8 = 29,2 Md€, soit la TF
    actuelle plus 5,7 Md€.
  - De même, 0,185 % × 3 068 = 5,69 Md€ et 0,151 % × 3 068 = 4,64 Md€.
  - Seule réserve : le niveau des valeurs (point 6).
- **DMTO de 11,4 Md€.** Le Compte du logement donne 12,1 Md€ en moyenne pour 2023-2024 sur tous les logements de
  France ; le champ du modèle (environ 94 %) en fait 11,4 Md€. C'est cohérent.
- **Nombre de ventes : 785 600 par an dans le champ (DVF).**
  - Les notes Insee-Notaires donnent 872 000 ventes en 2023 et 778 000 sur les douze mois à fin novembre 2024, outre-mer
    hors Mayotte compris. Une fois l'Alsace-Moselle et l'outre-mer retirés, c'est cohérent.
  - Le taux de rotation qui en résulte est de 2,6 % du parc par an, 3,4 % à Paris.
- **Prix au m².**
  - Médianes des déciles : de 1 035 à 6 261 €/m².
  - Appartements à Paris : 9 909 €/m² ; à Lyon : 4 653 €/m².
  - Ces valeurs sont plausibles, mais aucun repère externe n'a été téléchargé.
- **Montants de Paris (270 M€) et des Hauts-de-Seine (130 M€).** L'arithmétique est juste (268 et 133 M€). Voir le
  point 4 pour leur périmètre.

### A3. Erreurs mineures et arrondis douteux

| # | Passage | Écrit | Juste | Provenance |
|---|---|---|---|---|
| 9 | l. 230 « la charge totale varie de −63 à +133 € […] selon le décile » | −63 à +133 | **−75 à +133** (minimum au 3e décile ; −63 est le 1er) | `simulation.txt` l. 56 |
| 10 | l. 194-195 « 6 %, valeur centrale de la littérature » | 6 % | incohérent avec l. 108 « chaque point […] supprime environ 8 % des ventes » ; la note de lecture propose « +5 à +8 % » | `droits_mutation.md`, synthèse |
| 11 | l. 195-196 « Une baisse de 30 % coûterait 2,6 à 3,4 Md€ » | 2,6 à 3,4 | **2,3 à 3,4** avec les mêmes hypothèses (0 à 8 %) que la fourchette « 4,3 à 5,7 » de la baisse de 50 % | `simulation.txt` l. 47-50 |
| 12 | l. 64 titre « dont un quart sur les ventes » | un quart | 25 / 116 = **22 %**, un cinquième | `inventaire.md` § 1 |
| 13 | l. 249 « 13 000 € pour une maison à Nantes » | 13 000 | **13 100** (13 051, les autres montants sont arrondis à la centaine) | `simulation.txt` l. 76 |
| 14 | l. 260-261 « un septième à un tiers » | 1/7 à 1/3 | 2,9/20 = 14,5 % (1/7) ; 2,9/10 = **29 %** (trois dixièmes) | calcul |
| 15 | l. 75 « taxe d'aménagement (1,5 Md€) » | TA 1,5 | TA encaissée 1,37 + redevance d'archéologie 0,10 ; TA liquidée 1,6 | `inventaire.md` § 6 |
| 16 | fig. 3, étiquettes de barres | « 12 » (transmissions), « 2 » (construction) | 12,5 et 1,5 : `f"{g:.0f}"` arrondit au pair ; afficher une décimale | `figures_foncier.py` l. 105, `pdftotext` |
| 17 | l. 285-286 « le Bade-Wurtemberg a mis cinq ans à les établir (loi de 2020, premier impôt en 2025) » | cinq ans | loi du 4/11/2020, premier impôt 2025 : un peu plus de quatre ans. Les Bodenrichtwerte existaient avant la loi (§ 196 BauGB) ; ce qui a pris ce temps, c'est l'évaluation de toutes les parcelles | `taxe_fonciere_split_rate.md` § 2.2 |
| 18 | l. 258 « l'appartement médian parisien perdrait environ 8 000 € » | 8 000 | 8 252 € (le README écrit 8 250) ; arrondi acceptable, 2 % juste | `simulation.txt` l. 66 |
| 19 | l. 128-129 « l'extrapolation du modèle finlandais donne de l'ordre de 1 à 2 € par euro » | 1 à 2 € | la note de lecture écrit « vraisemblablement supérieur à 2 € par € » ; la revue a proposé « 1 à 2 € ». Extrapolation non établie : NON VÉRIFIABLE | `droits_mutation.md`, synthèse et § 3.7 |

### A4. Cohérence entre le texte, les figures, `simulation.txt` et le README

- **Texte, notes de figures et `simulation.txt`** : cohérents, sauf les points 1, 2, 3 et 9. Les notes de figures
  (5,7 Md€ ; 0,19 % ; quatre fois ; 10 ans à 3 %) correspondent au code de `figures_foncier.py`.
- **Le README n'a pas été mis à jour** après la révision. Ses chiffres ne correspondent plus aux sorties :

  | README | Écrit | Sortie actuelle | Le texte écrit |
  |---|---|---|---|
  | TF / valeur aujourd'hui | 0,55 % et 0,16 % | 0,52 % et 0,18 % | 0,52 et 0,18 (juste) |
  | Report simple, hausse par logement | +110 à +230 € | +106 à +237 € | 110 à 240 (juste) |
  | Deux taux nationaux, dernier décile | +238 % | +215 % | 215 % (juste) |
  | Deux taux nationaux, TF en hausse de plus de moitié | 25 % | 24 % | « un sur quatre » |
  | Deux taux par commune, taux départemental | +9 à +55 % | +10 à +51 % | non cité |
  | Proposition retenue : TF | « +2 % à +60 % » | N4 : +3 à +69 % ; N4v : +2 à +56 % | +3 % et +69 % (N4) |
  | Proposition retenue : total TF + DMTO | « −86 à +26 € » | N4v : −85 à +26 € (biaisé, voir A5) ; N4 : −75 à +133 € | −63 à +133 (point 9) |
  | Proposition retenue : hausses de plus de 300 € | 18 % | N4v : 18 % ; N4 : 23 % | 23 % (N4) |

  La section « Proposition retenue » du README mélange le scénario avec reprise des ventes (N4v) et un « +60 % » que
  plus aucune sortie ne donne, alors que la section « Révision » et le texte retiennent le calage sans reprise (N4).
- Le reste du README est juste : 30,5 M ; 6 760 Md€ ; 1 560 €/m² ; 45,4 % ; 23,6 Md€ ; 11,4 Md€ ; Paris +36 % ;
  0,11-0,85 % ; 14,1 → 7,3 Md€ ; +660 € ; −22 000 € ; −8 250 €.
- **Docstring de `simulation.py`** (l. 11-13) : elle décrit encore la part du terrain par résidu pour tous les logements.
  Pour les maisons, le code utilise en réalité le prix des terrains à bâtir.

### A5. Revue du code des scénarios (`simulation.py`)

- **`report_tf`** : correct. La hausse uniforme vaut s × D0/TF0 (24,1 %) ; les droits passent à (1 − s) × d0.
- **`deux_taux` et `deux_taux_local`** : corrects. Les taux recalculés redonnent exactement la recette cible
  (29,24 Md€).
- **`deux_taux_local_national`** : l'arithmétique est correcte (tc par commune, tn = perte / TERRE). Deux défauts :
  1. **Scénario N4v (avec reprise des ventes)** : on passe `cout = 4,64 Md€`, mais la fonction renvoie toujours
     `d1 = (1 − s) × d0`. Les droits encaissés sur les ventes supplémentaires sont donc oubliés : les droits restants
     valent 0,592 × D0 et non 0,5 × D0. Conséquences :
     - la ligne « recette TF + DMTO 33.9 Md€ (avant 34.9) » de `simulation.txt` est fausse : la recette est neutre
       par construction ;
     - les « totaux » par décile, par type et par taille sous-estiment la charge de 1,05 Md€, soit 34 € par logement
       en moyenne.

     Le texte n'utilise pas ces totaux, mais le README si (« −86 à +26 € »). *Correction* : multiplier `d1` par
     1,06^2,9 quand on passe `cout`. La revue précédente (point 5) le signalait déjà.
  2. Le docstring et le texte disent « reversé aux départements », alors que la perte compensée inclut la part
     communale (point 4). `PART_DEP_DMTO` est calculé mais jamais utilisé.
- **`cout_baisse`** : correct. On a dpts = 100 × s × 5,81 % = 2,90 points, une reprise multiplicative de (1 + v)^dpts,
  et une perte = D0 × (1 − (1 − s)(1 + v)^dpts). Les huit valeurs (2,3 à 5,7 Md€) sont reproduites.
- **`resume`** :
  - Les pourcentages par décile sont des rapports d'agrégats (Σ ΔTF / Σ TF0). Ce ne sont pas des moyennes de
    variations individuelles : « en moyenne » (l. 211) est donc un abus léger.
  - Les parts de logements (« 23 % au-delà de 300 € », « 5 % qui doublent ») sont calculées sur des cellules
    commune × type, où tous les logements reçoivent la valeur médiane. La dispersion à l'intérieur d'une commune est
    ignorée : ce sont des ordres de grandeur.
- **`cas_types`** : « amorti en {eco/dtf} ans » n'est pas actualisé (point 2). À remplacer par
  −ln(1 − r × eco/dtf) / ln(1 + r), et « jamais » si r × eco ≥ dtf.
- **`primo`** : correct. La valeur actuelle sur H ans est dt × (1 − 1,03^−H) / 0,03 et celle du propriétaire installé
  −dt / 0,03 ; les vingt lignes de `primo.csv` sont reproduites.
- **Bloc [CONTROLE]** : correct.
  - Impôt sur le bâti : Σ n × tf0 × (1 − λ) = 14,07 Md€ avant, Σ n × tc × v × (1 − λ) = 7,3 Md€ après ; la taxe
    nationale porte sur le seul terrain.
  - Paris : 518 → 1 178 € ; 660 / 0,03 = 21 997 € ; (660 − 0,5 × 825) / 0,03 = 8 252 €, soit 1,98 % de la valeur.
- **VARIANTE** : correcte. Le coût recalé de 2 016 €/m² donne un coût maison de 2 016 / 1,25 ; λ et TERRE sont rétablis
  après usage.
- **Autres points du code** :
  - `c["dmto"]` et `PART_DEP_DMTO` ne servent pas.
  - Le premier `qcut` des déciles est écrasé par les déciles pondérés : sans effet.
  - La cible de part du terrain (3 993 Md€) ne correspond pas à la publication Insee (4 043 Md€) ; effet de 0,3 point.

### A6. Non vérifiable

- **Insee Analyses n° 91** : 19,2 Md€ de TFPB des ménages en 2017 et ratios communaux. La publication n'a pas été
  relue ; on ne sait pas si le chiffre couvre l'outre-mer. S'il le couvre, `part_champ` (calculée sur la métropole)
  surestime la cible de quelques pour cent.
- **Amendement I-CF1872** : ni « adopté en commission le 9 octobre 2026 » ni « tombé avec le rejet de la première
  partie » ne sont établis. La note de lecture date l'amendement du 7/10 et marque son sort comme non vérifié ; la
  revue précédente cite LCP.
- **« Finlande 2023, rétroactive »** : la baisse s'applique au 1/1/2024, rétroactivement au 12/10/2023, source
  secondaire dans la note.
- **Élasticité de 1,54 sur 3 307 communes** : vérifiée seulement comme sortie du modèle, la régression étant interne.
- **Chiffres de littérature** (Bérard-Trannoy, Bachelet-Poulhès, Dolls et al., HMRC, Banzhaf-Lavery, Karlsruhe,
  Pittsburgh, BFH) : conformes aux notes de lecture, mais les textes primaires n'ont pas été relus ici.
- **Nombre de logements de particuliers outre-mer** (environ 1 M) : hypothèse utilisée pour le prorata des comptes de
  patrimoine (point 6). Sans elle, l'écart est de 19 % au lieu de 17 %.

---

## B. Tableau de tous les nombres vérifiés

Lignes : `note-foncier.tex`. Sources : « sim » = `sorties/simulation.txt` (ligne) ; « inv » = `notes/inventaire.md` ;
« dm » = `notes/droits_mutation.md` ; « sr » = `notes/taxe_fonciere_split_rate.md`.

| # | Ligne | Nombre du texte | Source | Recalcul / valeur source | Statut |
|---|---|---|---|---|---|
| 1 | 45 | 5,8 à 6,3 % de droits | dm § 1 | 4,5 + 1,2 + 2,37 % × 4,5 = 5,807 ; 5 + 1,2 + 2,37 % × 5 = 6,319 | OK |
| 2 | 64 | 116 milliards | inv § 1 | 69 + 25 + 12,5 + 8,4 + 1,5 = 116,4 | OK |
| 3 | 64 | « dont un quart sur les ventes » | inv | 25 / 116 = 21,6 % | ARRONDI DOUTEUX |
| 4 | 66 | 4 % du PIB | inv (PIB 2 935) | 3,97 % | OK |
| 5 | 67 | détention 69 Md€ | inv, fig. 3 | 42 + 9 + 8 + 10,0 | OK |
| 6 | 68 | TFPB 42 Md€ (2024) | inv § 2.1 | 41 964 M€ | OK |
| 7 | 68 | 43,1 en 2025 | inv | 43 131 M€ | OK |
| 8 | 68 | dont 31,6 Md€ sur les logements | inv (CSL 2025) | 31 590 M€ (2025, comptabilité nationale ; 30,5 en 2024) | OK |
| 9 | 69 | TEOM 9 Md€ | inv § 2.5 | 8 996 M€ (2024) | OK |
| 10 | 69 | CFE 8 Md€ | inv § 2.9 | 8 031 M€ (2024) | OK |
| 11 | 70 | IFI 2,7 Md€ | inv § 2.7 | 2,74 Md€ encaissés 2024 | OK |
| 12 | 71 | transactions 25 Md€ | inv | 14,1 + 7,1 + 2,8 + 0,7 + 0,3 = 25,0 | OK |
| 13 | 71 | DMTO 14,1 Md€ (2024) | inv § 3.1 (OFGL) | 14 093 M€ | OK |
| 14 | 72 | 16,7 en 2025 | inv (OFGL) | 16 703 M€ | OK |
| 15 | 72 | TVA neuf et terrains 7,1 Md€ | inv § 3.4 | 6 163 + 965 = 7 128 M€ | OK |
| 16 | 73 | plus-values 2,8 Md€ | inv § 3.5 (Cour) | 2,8 Md€ (2024) | OK |
| 17 | 73 | CSI 0,7 Md€ | inv § 3.3 | 692 M€ | OK |
| 18 | 74 | successions immobilières 12,5 Md€ | inv § 4 | 60 % × 20,9 = 12,5 (clé conventionnelle) | OK (estimation) |
| 19 | 75 | revenus locatifs 8,4 Md€ | inv § 5 | 8 391 M€ | OK |
| 20 | 75 | taxe d'aménagement 1,5 Md€ | inv § 6 | TA 1,37 + RAP 0,10 | ARRONDI DOUTEUX |
| 21 | 79-80 | OCDE 2023 : 1,90 / 0,95 / 0,72 / 0,37 % du PIB ; « le double » | inv § 8 | identiques ; 1,90 = 2 × 0,95 | OK |
| 22 | 86-87 | 4,50 / 1,20 / 2,37 % ; 5,81 % | dm § 1 | 5,8066 % | OK |
| 23 | 87-88 | 5 % ; 1/4/2025-31/3/2028 | inv § 3.1 (BOFiP) | idem | OK |
| 24 | 88-89 | 88 collectivités ; 6,32 % | inv § 3.1 | 88 sur 100 au 1/6/2026 ; 6,3185 % | OK |
| 25 | 90-91 | Savoie seule | inv § 3.1 | idem (4,00 %) | OK |
| 26 | 95 | révision reportée à 2031 | sr § 3.2 | intégration au 1/1/2031 | OK |
| 27 | 96-97 | 0,52 % et 0,18 % | sim l. 45 | 0,52 … 0,18 | OK |
| 28 | 97 | Paris 0,12 % | calcul | TF0 / valeur Paris = 0,124 % | OK |
| 29 | 97 | taux parisien 13,5 → 20,5 % en 2023 | sr § 1a | idem | OK (note) |
| 30 | 106 | +26 % (France 2014) ; 41 % (Allemagne) | dm | idem | OK (note) |
| 31 | 108-109 | 8 % par point ; 0 à 18 % ; quelques mois à quatre ans | dm, synthèse | idem | OK (note) |
| 32 | 110 | mobilité −8 à −14 % par point | dm | idem | OK (note) |
| 33 | 116-117 | 0,7 point ; −6 % sur trois mois | dm § 2.1 | 0,72 ; −6 % | OK |
| 34 | 118 | −10 à −12 % ; −20 % ; nul | dm § 2.2 | idem | OK |
| 35 | 121 | Allemagne −3 % de prix par point | dm § 3.6 | idem | OK |
| 36 | 123-124 | +11 % d'achats, +1 % de prix | dm § 4 | +10,7 % ; +1,04 % | OK |
| 37 | 127-128 | 1 à 2 % → 5 à 30 % ; 4-5 % → 0,7 à 0,9 € | dm, synthèse | idem | OK |
| 38 | 129 | « 1 à 2 € par euro » au taux français | dm | la note écrit « > 2 € » | NON VÉRIFIABLE (écart avec la note) |
| 39 | 131 | +0,2 % de consommation | dm § 2.3 | idem | OK |
| 40 | 143 | Høj 2018 complète ; Nielsson 2024 nulle | sr § 1a | idem | OK |
| 41 | 148-149 | Philadelphie : trente ans de gel, 2014 | sr § 1d | 1980-2012, effet 2014 | OK |
| 42 | 151 | Pittsburgh 2001 ; sol +81 % | sr § 2.1 | idem | OK |
| 43 | 156-157 | 4:1 → environ +3 points | sr § 2.1 | 2:1 ≈ +1 ; 4:1 ≈ +3 | OK |
| 44 | 159-160 | BW depuis 2025 ; −30 % pour le logement ; BFH mai 2026 | sr § 2.2 | § 40 al. 3 ; 20/05/2026 | OK |
| 45 | 161-162 | Karlsruhe : maisons +76 %, copropriétés −20 % | sr § 2.2 | idem | OK |
| 46 | 168 | 30,5 millions de logements | sim l. 1 | 30,46 M | OK |
| 47 | 169 | valeur 6 760 Md€ | sim l. 1 | 6 762 Md€ ; Insee au prorata ≈ 8 100-8 400 Md€ | OK (calcul) / SUSPECT (niveau) |
| 48 | 175 | élasticité 1,54 sur 3 300 communes | sim l. 3 | 1,54 ; 3 307 | OK |
| 49 | 177 | 45 % (comptes de patrimoine) | sim l. 1 ; Insee IP 2081 | 45,4 % ; Insee 45,7 % | OK |
| 50 | 177-178 | 16 % à 67 % | sim l. 4 | 16 … 67 | OK |
| 51 | 182 | 23,6 Md€ | sim l. 2 | 19,2 × 1,2964 × 0,9463 = 23,55 | OK |
| 52 | 182-183 | 5,81 % ; 11,4 Md€ | sim l. 2 | 11,37 Md€ ; CSL ≈ 12,1 France | OK |
| 53 | 191 | « locaux professionnels […] portent le total à 16,7 Md€ » | inv § 3.1 | non-logements ≈ 3,1 Md€ ; logements 13,6 Md€ en 2025 | ERREUR (interprétation) |
| 54 | 192 | 5,81 % → 2,9 % | calcul | 2,903 % | OK |
| 55 | 192-193 | 6,32 % jusqu'en mars 2028 | inv | idem | OK |
| 56 | 194 | perte 5,7 Md€ | sim l. 51 | 5,69 | OK |
| 57 | 194-195 | 4,6 Md€ si +6 % par point | sim l. 53 | 4,64 | OK |
| 58 | 195 | 6 % « valeur centrale de la littérature » | dm | 8 % au l. 108 ; « +5 à +8 % » dans la note | ARRONDI DOUTEUX (incohérent) |
| 59 | 195 | 4,3 à 5,7 Md€ | sim l. 51-54 | 4,26 … 5,69 | OK |
| 60 | 195-196 | baisse de 30 % : 2,6 à 3,4 Md€ | sim l. 47-50 | 2,27 … 3,41 | ARRONDI DOUTEUX (→ 2,3 à 3,4) |
| 61 | 197 | Finlande 2023, rétroactive | dm § 4 | 1/1/2024, rétroactive au 12/10/2023 (secondaire) | NON VÉRIFIABLE |
| 62 | 204 | +24 % (+20 % avec reprise) | sim l. 51, 53 | 24,1 % ; 19,7 % | OK |
| 63 | 204-205 | 110 à 240 € | sim l. 11 | +106 … +237 | OK |
| 64 | 206-207 | 0,65 % et 0,22 % | sim l. 42 | idem | OK |
| 65 | 210 | 0,73 % terrain ; 0,18 % bâti | sim l. 39 | 0,733 / 0,183 ; recette 22,5 + 6,8 = 29,2 Md€ | OK (SUSPECT en niveau, point 6) |
| 66 | 211 | +215 % dans le dixième le plus cher | sim l. 23 | +215 % (Paris = 38 % du décile) | OK |
| 67 | 212 | un logement sur quatre au-delà de +50 % | sim l. 22 | 24 % | OK |
| 68 | 217-218 | terrain = 4 × bâti | code | k = 4 | OK |
| 69 | 219 | taux national 0,19 % | sim l. 63 | 0,185 % = 5,69 / 3 068 | OK (SUSPECT en niveau : ≈ 0,15 % sur les valeurs Insee) |
| 70 | 220 | vers 0,15 % si reprise | sim l. 63 | 0,151 % | OK |
| 71 | 222 | bâti 14 → 7 Md€ | sim l. 65 | 14,07 → 7,3 | OK |
| 72 | 223-224 | 0,12 % à Paris, 0,85 % dans la Creuse | sim l. 41 | 0,119 % ; 0,845 % | OK |
| 73 | 228 | +3 % et +69 % | sim l. 56 | idem (+51 % hors Paris) | OK |
| 74 | 230 | total de −63 à +133 € | sim l. 56 | **−75** (3e décile) à +133 | ERREUR |
| 75 | 231 | 0,54 % et 0,30 % | sim l. 64 | idem | OK |
| 76 | 232-233 | un sur quatre (23 %) au-delà de +300 € | sim l. 55 | 23 % (dont Paris 17 %) | OK |
| 77 | 233-234 | un sur vingt (5 %) qui double, « surtout Paris et littoral » | `v3_verif.py` | 5,4 % ; Paris 70 %, Hauts-de-Seine 14 %, autres 16 % | 5 % OK ; localisation ERREUR |
| 78 | 235-236 | appartements +240 €, maisons +150 € | sim l. 57 | +237 / +149 | OK |
| 79 | 237 | variante : +130 / +230 € | sim l. 69 | +131 / +228 | OK |
| 80 | 240 | 0,3 à 0,9 € par euro | dm | hypothèse de l'auteur | NON VÉRIFIABLE (hypothèse) |
| 81 | 241 | 5,7 Md€ déplacés | sim | 5,69 | OK |
| 82 | 241-242 | 1,5 à 4 Md€ par an | calcul | 5,7 × 0,3-0,9 = **1,7 à 5,1** | ERREUR |
| 83 | 242 | 0,05 à 0,15 % du PIB | calcul | **0,06 à 0,17 %** | ERREUR |
| 84 | 248 | 2 300 € (Saint-Étienne) | primo.csv | 2 266 | OK |
| 85 | 248 | 22 700 € (Arcachon) | primo.csv | 22 700 | OK |
| 86 | 249 | 8 100 € (Lyon) | primo.csv | 8 105 | OK |
| 87 | 249 | 13 000 € (Nantes) | primo.csv | 13 051 → 13 100 | ARRONDI DOUTEUX |
| 88 | 250 | 12 100 € (Paris) | primo.csv | 12 083 | OK |
| 89 | 250 | −100 à +660 € par an | primo.csv (N4) | −102 … +660 | OK |
| 90 | 251 | 17 à 23 ans dans les grandes villes, « davantage ailleurs » | sim l. 72-81 | non actualisé ; à 3 % : 24-39 ans, jamais à Nantes, Arcachon, Ussel et Guéret ; Limoges 19 ans (28 à 3 %) | ERREUR |
| 91 | 253 | 660 € par an ; 22 000 € en valeur actuelle | sim l. 66 | 660 / 0,03 = 21 997 | OK |
| 92 | 258 | environ 8 000 €, 2 % | sim l. 66 | 8 252 € ; 1,98 % | OK (arrondi large) |
| 93 | 260 | apport 10 à 20 % ; 2,9 points | calcul | 2,905 | OK |
| 94 | 260-261 | un septième à un tiers | calcul | 14,5 % à 29 % | ARRONDI DOUTEUX |
| 95 | 265 | « la moitié moins en impôt » | calcul | s = 0,5 | OK |
| 96 | 270 | 560 € dans le dixième le plus cher | sim l. 56 | +561 € | OK |
| 97 | 281 | contestation au-delà de 30 % (BW) | sr § 2.2 | § 38 al. 4 | OK |
| 98 | 282 | amendement I-CF1872, adopté en commission le 9/10/2026, puis tombé | sr § 3.2 | dépôt le 7/10, adoption en commission ; sort non vérifié | NON VÉRIFIABLE |
| 99 | 285-286 | BW : cinq ans (2020 → 2025) | sr § 2.2 | loi du 4/11/2020 → 2025 : environ 4 ans | ARRONDI DOUTEUX |
| 100 | 289 | hausse temporaire de 20 à 24 % | sim l. 51, 53 | 19,7 et 24,1 % | OK |
| 101 | 291 | 0,19 % | sim l. 63 | 0,185 % | OK |
| 102 | 293 | exonération au-delà de 75 ans | sr § 1c | art. 1390-1391 (secondaire) | OK (note) |
| 103 | 300 | décision 2019-796 DC | sr § 3.3 | idem | OK |
| 104 | 303 | Paris environ 270 M€ | `v2_verif.py` | +268 M€ (+213 si seule la part départementale est compensée) | OK (périmètre à préciser) |
| 105 | 303 | Hauts-de-Seine 130 M€ | `v2_verif.py` | +133 M€ (+106) | OK (périmètre à préciser) |
| F1 | fig. 1, note | 5,7 Md€ ; 0,19 % ; « quatre fois » | sim ; code | 5,69 ; 0,185 % ; k = 4 | OK |
| F2 | fig. 2, note | aucun nombre | — | axe −500 à 1 900 contient K4 = +1 752 | OK |
| F3a | fig. 3, note | part immobilière des successions 60 % | inv § 4 | clé du CPO | OK |
| F3b | fig. 3, note | 4100 avec TEOM, sans CFE | inv § 8 | idem | OK |
| F3c | fig. 3, barres | 69 / 25 / 12 / 8 / 2 ; 1,90 / 0,95 / 0,72 / 0,37 | `figures_foncier.py` | 12,5 affiché « 12 », 1,5 affiché « 2 » | ARRONDI DOUTEUX |
| F4 | fig. 4, note | 0,19 % ; 4 × bâti ; 10 ans à 3 % | code | identiques | OK |

---

## C. Repères externes consultés

- Insee, *Le patrimoine économique national en 2024* (Insee Première n° 2081), figure 2 : ménages (y compris EI et
  ISBLSM), logements 4 807 Md€, terrains bâtis 4 043 Md€, autres bâtiments et génie civil 233 Md€ ; terrains −3,2 % en
  2024. https://www.insee.fr/fr/statistiques/8661938
- DGFiP Statistiques n° 46, « En 2025, la taxe foncière progresse de 2,4 % » : 55,1 Md€ de TFPB dus, « y compris taxes
  annexes et frais de gestion » ; 1 117 € de TFPB moyenne par particulier.
  https://www.impots.gouv.fr/dgfip-statistiques-en-2025-la-taxe-fonciere-progresse-de-24
- Ventes de logements anciens (cumul sur douze mois) : 872 000 fin 2023 et 778 000 fin novembre 2024 (outre-mer hors
  Mayotte compris), selon les notes Insee-Notaires et la note de conjoncture des Notaires de France de janvier 2025,
  lues à travers les résultats de recherche.
  https://www.notaires.fr/fr/article/marche-de-limmobilier-tendances-et-evolutions-des-prix-de-limmobilier-janvier-2025
- Repères internes, lus dans les notes de lecture vérifiées et non retéléchargés :
  - Compte du logement 2025 : TFPB sur les logements, 30,5 Md€ (2024) et 31,6 Md€ (2025) ; DMTO sur les logements,
    13,0 Md€ (2023), 11,2 Md€ (2024) et 13,6 Md€ (2025) ;
  - OCDE : TFPB payée par les ménages, 26,1 Md€ en 2024 ;
  - REI : clé ménages/entreprises.
