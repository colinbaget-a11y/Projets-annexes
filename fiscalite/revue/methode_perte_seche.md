# Perte sèche des quatre réformes : une méthode commune

*16/11/2026. Point de départ : assiette large, même taux pour tous ; chaque écart est une variante chiffrée (perte sèche, recette, qui paie), sans trancher. [calc.] : calcul de cette note (programmes du dépôt lus sans modification, script hors dépôt) ; [conv.] : convention posée ici, sans estimation publiée.*

## 1. La formule commune

**ΔPS = − Σ_j (T̄_j − s_j·τ_k) · ΔQ_j**, avec **ΔQ_j = ε_j · Q_j · Δln(1 − T_j)**.

- *j* parcourt toutes les marges : heures et effort par niveau de revenu, participation, capital, transactions, bénéfices déclarés.
- *T_j* est le coin **total** sur la marge : tous les prélèvements et retraits de prestations, pas seulement l'impôt réformé. T̄_j est sa moyenne avant et après (trapèze). Pour une élasticité constante, l'intégrale exacte s'écrit ΔPS_j = ε_j Q_j [(1+c_er)·ln(a₀/a₁) − (τ₁ − τ₀)], avec a = 1 − τ − c_ee − c_pa.
- *s_j·τ_k* : part *s_j* de la réponse qui passe vers une autre assiette taxée au taux τ_k (Chetty, 2009). Une réponse de calendrier se compense d'une année sur l'autre et pèse presque zéro.

**Intuition.** Un euro d'activité perdu sur une marge coûte à la collectivité le coin qui la frappe. Le triangle ½·ε·τ²/(1−τ) est le cas d'une seule marge partant d'un taux nul. Si la marge est déjà taxée, un point de plus coûte au premier ordre T_existant × ΔQ, et non au second ordre. À l'inverse, un revenu qui se déplace vers l'IS ne coûte que l'écart des taux.

**Recette** : ΔR = ΔR_mécanique + Σ_j T_j,1·ΔQ_j, avec les mêmes ΔQ. **Qui paie** : par le théorème de l'enveloppe, la perte de chaque groupe est, au premier ordre, la variation *mécanique* de son impôt. L'incidence (capitalisation, salaires) fait exception.

**Comparer des variantes.** Chaque variante garde la même recette mécanique, en recalant l'instrument de bouclage. Quand ce n'est pas possible, on utilise le *prix d'un milliard*, μ − 1 = ΔPS par Md€ levé par l'instrument de bouclage (Dahlby, 2008 ; Kleven et Kreiner, 2006). Pour le barème fusionné, il vaut 0,16 (coin IR-CSG seul), 0,38 (coin non contributif) et 0,60 (toutes cotisations) [calc. : +1 Md€ de recette cible]. Pour une taxe sur le terrain, il est proche de 0.

**Statistiques suffisantes.** Il en faut cinq :
- les assiettes Q_j par groupe ;
- les coins T_j avant et après (§ 6) ;
- les élasticités ε_j ;
- les parts déplacées s_j et les taux τ_k des assiettes d'accueil ;
- le prix μ de l'instrument de bouclage.

## 2. Fusion IR-CSG-CRDS

**Formule.** Par adulte *a* :

ΔPS = Σ_a e_a z_a [(1+c_er)·ln(a₀/a₁) − (τ₁−τ₀)] + Σ_haut s·τ_k·ΔQ_a + Σ_a η·g_a [ln((1−PTR₀)/(1−PTR₁)) − (PTR₁−PTR₀)].

- τ : taux marginal IR-CSG du modèle (`proposition.py`, `systeme`).
- c_er, c_ee, c_pa : cotisations patronales et salariales non contributives, retrait de la prime d'activité (§ 6). Ils sont appliqués à la part salariale du revenu du travail de la tranche (indépendants : 0) [conv.].
- Les deux derniers termes répondent aux problèmes 2 et 5 de la revue.

**Paramètres.**
- e par rang : 0,15 / 0,20 / 0,30 / 0,40 (jeu central du modèle ; Sicsic 2022 : 0,22 / 0,33 / 0,51).
- s = 0,5 pour le décile supérieur, avec τ_k = 48,6 % (IS 25 % puis PFU) ou 25 % (bénéfice conservé) [conv.].
- η = 0,25 (élasticité extensive hicksienne ; Chetty, Guren, Manoli et Weber 2011, d'après `lit_haut_elasticites.md`). Elle est appliquée aux adultes sous 2 Smic.
- Les PTR viennent de TaxBEN (§ 6).

**Calcul central (proposition : franchise d'activité de 8 000 €, franchise par enfant)**

| Étape | ΔPS (Md€/an) |
|---|---|
| Modèle actuel, ½eτ²/(1−τ) : 18,1 → 9,3 | −8,9 |
| Même coin, intégrale exacte | −7,1 |
| + cotisations non contributives et prime d'activité | −11,2 (décile 10 : −11,9 ; déciles 1-9 : **+0,7**) |
| Variante toutes cotisations | −17,1 |
| + déplacement s = 0,5 vers une assiette à 48,6 % | −4,8 (−7,9 si 25 % ; **+1,7** si s = 1) |
| + marge extensive (couples, seuls sous 0,5 Smic) | −2,1 |
| **Central** | **≈ −7 Md€ (+2 à −19)** |

Recette : 220,1 Md€ par construction. L'externalité fiscale vaut +2,7 Md€ (coin non contributif, s = 0,5), contre +5 Md€ de recette induite selon la revue (coin IR-CSG seul, sans déplacement).

**Arbitrages (même recette ; barème recalé ou grille optimisée du dépôt)**

| Variante | ΔPS modèle | ΔPS central | Qui paie |
|---|---|---|---|
| Franchise 0 € (étape 3) | −12,9 | −12,6 | pensions +16,7 Md€ ; déciles 3-4 +1 230/+1 310 € ; 1 % du haut −10,3 Md€ ; 57 % de perdants > 500 € |
| Franchise 4 000 € | −10,5 | −9,5 | pensions +14,1 ; 43 % de perdants |
| Franchise 6 000 € | −9,8 | −7,7 | pensions +13,6 ; 37 % |
| **Franchise 8 000 €** | **−8,9** | **−6,9** | pensions +13,0 ; déciles 2-4 +208/+355/+450 € ; 1 % du haut −4,4 Md€ ; 33 % |
| Franchise 10 000 € | −8,0 | −6,1 | pensions +12,6 ; 32 % |
| Franchise 8 000 € sur salaires seuls (borne de « hors loyers ») | −8,9 | −7,1 | indépendants et bailleurs paient davantage (le modèle ne sépare pas loyers et bénéfices) |
| Franchise 8 000 € sur tous revenus, pensions comprises | −8,0 | −4,4 | pensions +12,0 ; déciles 1-2 −87/−229 € ; 31 % |
| Famille : rien | −10,4 | −9,8 | parents isolés +1 030 €, couples avec deux enfants +530 € |
| Famille : chèque de 772 € | −9,9 | −7,8 | 36 % de perdants |
| Imposition commune (quotient conjugal et familial) | −10,1 | −9,3 | couples sans enfant −450 € ; 31 % |
| Taux supérieur 45 % | −9,2 | −6,9 | 1 % du haut −5,2 Md€ |
| Taux supérieur 55 % | −8,5 | −6,9 | 1 % du haut −3,7 Md€ |
| Petites pensions (garantie au niveau de l'ASPA) | coût L Md€ | +0,16 à +0,60 × L | non chiffrable : le modèle n'a que des foyers mixtes |

**Ce que montre le tableau.**
- Chaque millier d'euros de franchise réduit le gain de 0,4 à 0,9 Md€. C'est moins qu'annoncé, car la marge extensive en récupère 1,4 Md€ entre 0 et 8 000 €.
- Avec un barème presque proportionnel, l'unité d'imposition change peu le PTR des seconds apporteurs (0,19 → 0,08 dans les deux cas) : la franchise par adulte fait l'essentiel.
- Le taux supérieur, qui ne joue qu'au-delà de 600 000 €, déplace 1,5 Md€ dans le 1 % du haut sans changer la perte sèche.

**Limites qui changent le signe ou l'ordre de grandeur.**
1. *Déplacement d'assiette.* Le gain s'annule vers s ≈ 0,9. Aucune estimation française de s n'existe.
2. *Coin total.* Le gain est multiplié par 1,6 (cotisations non contributives) à 2,4 (toutes cotisations). Sous le décile 10, le signe s'inverse : la proposition relève le taux de 9,5 à environ 20 % là où le coin dépasse déjà 60 % (sortie de la réduction générale, prime d'activité). L'ordre des barèmes peut donc changer en bas.
3. *Élasticités.* Avec le coin non contributif, ΔPS va de −5,8 (jeu bas) à −19,1 Md€ (jeu haut).
4. *Taux supérieur et coin total.* Le taux qui maximise la recette, τ* = 1/(1 + a·e), porte sur le coin total. Avec a = 2 (2,1 chez Cabannes et al., 2014 ; non vérifié pour le 1 % récent) et e = 0,4, τ* = 56 %, soit environ 42 % d'IR-CSG une fois ajoutés 27 % de cotisations patronales non contributives ; avec e = 0,25, environ 56 % [calc.]. Un taux de 50 % est donc du mauvais côté si e ≈ 0,4.
5. *Marge extensive.*
   - Avec η = 1 pour les seconds apporteurs, le gain des couples passe de −1,4 à −5,6 Md€.
   - Le modèle donne aussi −3,9 Md€ pour les personnes seules de 0,5 à 2 Smic. C'est un artefact des foyers représentatifs, qui mêlent pensions et salaires : sur les cas-types, un salarié seul à 21 500 € gagne 14 €, à 30 000 € 75 €, ce qui laisse son PTR inchangé. Ce terme n'est pas retenu.
6. Non modélisé :
   - la TVA dans le coin ;
   - la réduction générale unique de 2026 (données OCDE 2025) ;
   - la différence entre marge des heures (réduction au Smic horaire constante) et marge du salaire horaire (sortie de la réduction).

## 3. Droits de mutation divisés par deux, taxe foncière à deux taux

**Formule.** ΔPS = −∫ τ dV_ventes − ∫ t_b dK_bâti + 0 × Δ(terrain), avec dV/V = −σ·dτ et dK/K = −ε_K·dt_b/u. En intégrant :
- droits : ΔPS ≈ σ·V̄·(τ₁² − τ₀²)/2 ;
- bâti : ΔPS ≈ ε_K·(K/u)·(t₁² − t₀²)/2.

**Intuition.** Chaque vente découragée est un appariement manqué, qui valait au plus le droit payé. L'impôt sur le sol ne change aucune quantité. L'impôt sur le bâti renchérit le coût d'usage du logement.

**Paramètres.**
- V = 11,4/0,0581 = 196 Md€ de ventes de logements anciens par an.
- σ = 6 % de ventes par point (valeur centrale de la note ; 0 à 15 %, `notes/droits_mutation.md`).
- Bâti : K = 6 762 − 3 068 = 3 694 Md€ ; t₀ = 14,1/K = 0,38 % ; t₁ = 7,3/K = 0,20 % (`sorties/simulation.txt`).
- u = 4 à 5 % [conv.] ; ε_K = 1 [conv. ; aucune estimation française lue].

**Calcul.**

| Variante | ΔPS (Md€/an) | Recette | Qui paie |
|---|---|---|---|
| Droits −50 % (σ = 6 ; 3 à 15) | **−1,6** (−0,8 à −4,6) | −5,7 (σ = 0) / −4,6 | acheteurs gagnent, ou vendeurs si capitalisation |
| Droits −30 % | −1,1 (−0,5 à −2,9) | −3,4 / −2,6 | taxe foncière +14 % au lieu de +24 % |
| Bâti, terrain = 4 × bâti par commune (proposition) | **−0,4 ε_K** | 0 | taxe foncière de +3 % à +69 % selon le décile ; 23 % des logements > +300 € |
| Bâti, deux taux nationaux 2× / 4× / ∞ | −0,2 / −0,4 / −0,5 ε_K | 0 | dernier décile +184 / +215 / +266 % ; appartements +51 / +62 / +80 % ; maisons +10 / +4 / −6 % |
| Taux national 0,19 % (sans reprise des ventes) ou 0,15 % (avec) | 0 | écart 1,1 Md€ = τ₁·ΔV | à 0,19 % les propriétaires portent le risque, à 0,15 % le budget |

**Central** (−50 %, 4×, 0,19 %) : **≈ −2,0 Md€** (de +0,9 à −5).

**Limites.**
1. *Le triangle ignore le coût d'appariement.* Määttänen et Terviö chiffrent le gain à remplacer un droit de 2 % à environ 30 € par ménage, et un droit de 6 % à environ 180 € (euros 2004). Interpolé à 5,81 → 2,9 %, cela donne 116 € × 30,5 M de logements, de l'ordre de −3,5 Md€ [calc. ; modèle d'Helsinki, non calibré sur la France].
2. *Réponse de calendrier.* L'effet durable est nul au-delà de trois mois selon Bérard et Trannoy, et Dolls et al. ne trouvent pas d'effet sur les volumes en Allemagne : σ → 0.
3. *Signe du terme bâti.* Le loyer imputé des propriétaires occupants n'est pas taxé. Si l'on compare au PFU sur un rendement de 3 %, le logement occupé est déjà subventionné d'environ 0,9 % de sa valeur. Baisser l'impôt sur le bâti accroît alors la perte (+0,9 ε_K Md€) [calc., hypothèses explicites].
4. *Capitalisation.* Elle change qui paie, pas la perte sèche.

## 4. IS : déduction immédiate, fin du taux réduit, ou 28 %

**Formule.** ΔPS = (r+δ)·K·ε·(m₁² − m₀²)/2 − κ·τ̄·ΔB_déclaré + (μ−1)·(−ΔR).
- m = c/(r+δ) − 1 est le coin sur le coût d'usage c = (r+δ)(1−τz)/(1−τ) (Hall-Jorgenson).
- ΔB_déclaré est la base perdue par transfert de bénéfices (semi-élasticité) ; κ ∈ [0 ; 1] est la part de son coût qui est une ressource réelle (Chetty, 2009) [conv.].

**Intuition.** La perte sèche est le triangle sur le capital supplémentaire, pas le surcroît de PIB : ce surcroît rémunère d'abord le capital qui le produit. La hausse des salaires (L·dw = K·|dc|) est un transfert. Elle n'a de valeur d'efficacité que par l'écart de taux entre salaires et bénéfices, (μ−1)(τ_L − τ_IS)·ΔwL : environ 0,2 Md€ avec μ−1 = 0,38, τ_L − τ_IS = 0,15 et ΔwL = 3,9 Md€ [calc.].

**Paramètres.**
- K = 0,75 × 541 Md€ d'équipements imposables ; r+δ = 19 %.
- m₀ = 5,1 % (amortissement linéaire) ou 3,5 % (dégressif) ; m₁ = 0 (100 %) ou 2,5 % (50 %) ; 6,0 % à 28 % (`sorties/simulation_is.txt`).
- ε = 0,5 à 1,6.
- Semi-élasticité des bénéfices déclarés : 1 à 1,5 par point (Beer, de Mooij et Liu, 2020, d'après le cours).

**Calcul.**

| Variante | ΔPS (Md€/an) | Recette (Md€/an) | Qui paie |
|---|---|---|---|
| Déduction 100 % | −0,10 ε (−0,05 ε dégressif) | coût actualisé 1,8 à 2,6 | salaires +3,9 à long terme si le capital est mobile [calc.] |
| Déduction 50 % | −0,075 ε | 0,9 à 1,3 | salaires +2,0 |
| Fin du taux réduit | 0 au-dessus du plafond (forfait) ; jusqu'à +0,8 sous le plafond (29 % de coût marginal au seuil britannique, Devereux, Liu et Loretz, résumé) | +2,2 à 2,7 | TPE : au plus 4 250 €, +2/3 d'IS sous le plafond |
| Taux réduit maintenu | 0 | il faut 2,2 à 2,7 ailleurs (× μ−1) | — |
| Taux à 28 % | +0,04 ε + de 0 à +3,0 (base transférée : 7,5 à 11 Md€) | +4,3 à 5,4 (7,5 statique) | toutes les sociétés, surtout les profits mobiles |

**Central** (50 % puis 100 %, financé par l'assiette) : **≈ −0,1 Md€** (−0,2 à +0,7). La hausse à 28 % donnerait **0 à +3 Md€**.

**Limites.**
1. *Coût réel du transfert de bénéfices.* κ fixe tout l'écart : de 0 (frais qui sont des transferts) à τ̄·ΔB (κ = 1). Du point de vue national, la recette partie à l'étranger est perdue pour la France si les actionnaires sont étrangers.
2. *Trésorerie contre coût d'usage.* Si la déduction agit par la trésorerie (Zwick et Mahon), ε dépend de la taille de l'entreprise, et supprimer le taux réduit l'affaiblit.
3. *Excédent de financement.* L'assiette dégage 1 à 2,6 Md€ de plus que le coût actualisé : c'est une hausse d'IS.

## 5. PFU : 31,4 % ou 25 %, report d'apport-cession

**Formule.** ΔPS = −(τ̄ − τ_alt)·ΔQ + (μ−1)·(−ΔR), avec ΔQ = e·B·Δln(1−τ).
- τ_alt est la valeur actuelle de l'impôt sur le bénéfice conservé : τ si la distribution n'est que différée au même taux ; 0 pour la part π effacée au décès.
- Donc τ̄ − τ_alt ≈ π·τ̄.

**Intuition.** Selon la « new view », l'impôt sur le dividende ne touche pas l'investissement financé par les bénéfices conservés. Une réponse de calendrier n'est pas une perte sèche. Seule compte la part qui échappe définitivement à l'impôt, ou qui modifie l'activité.

**Paramètres.**
- B = 79,6 Md€.
- e = 0,65 à 1 (0,77 : Lefebvre, Lehmann et Sicsic).
- π ∈ [0 ; 1] [conv.]. Aucun effet sur l'investissement n'a été trouvé en 2013 ni en 2018 (IPP), ni aux États-Unis en 2003 (Yagan).

**Calcul.**

| Variante | ΔPS (Md€/an) | Recette | Qui paie |
|---|---|---|---|
| 31,4 % maintenu | 0 | 0 | — |
| 25 % | 0 (π = 0) à −2,0 (π = 1, e = 1), plus le bouclage +0,5 à +2,3 → **central +1,4** (−1,5 à +2,3) | −3,2 à −3,9 (note) | gain : 1 % du haut (96 % des dividendes) |
| Report expirant à toute transmission (PLF 2027, art. 5) | non chiffrable | +0,5 en 2027 (seconde main), ≈ 2 en croisière [calc. : 153 Md€ en 25 ans] | 84 foyers ≈ 90 M€ chacun ; impôt sans liquidité |
| Report expirant à la cession par la holding | non chiffrable : verrou déplacé vers la holding | moindre | idem, plus tard |
| Report transmis sans effacement (retenu) | non chiffrable ; supprime l'incitation à garder jusqu'au décès | moindre, plus tard | idem, à la sortie du capital |

**Central** (taux maintenu, report transmis) : **≈ 0 Md€** ; le PFU à 25 % coûterait **+1,4 Md€**.

**Limites.**
1. *Part effacée π.* Si la réponse est surtout définitive (purge au décès), la baisse à 25 % devient un gain d'efficacité.
2. *Réponse croisée.* Les revenus du travail des mêmes foyers montent quand le taux sur le capital baisse (élasticité croisée 0,04 à 0,08, LLS). C'est une externalité favorable à la baisse, non chiffrée faute d'assiette.
3. *Report d'apport-cession.* Aucune élasticité des réalisations n'existe pour ce régime.

## 6. Coins marginaux et taux de participation, France, personne seule sans enfant

*Points de coût du travail. 0,5 Smic : hausse des heures au Smic horaire (TaxBEN 50 → 100 %, réduction générale constante, employeur 4,3 % en 2024). 1 à 5 Smic : hausse du salaire (OCDE Taxing Wages, données 2025, fichier `ir_csg/sorties/ocde_taxing_wages_2025_seul.csv` ; 1 Smic lu à 1,06 Smic). Non contributives : toutes cotisations sauf vieillesse plafonnée, Agirc-Arrco hors CEG/CET et chômage [conv.].*

| Smic | IR+CSG+CRDS | Cotis. non contrib. | Prime d'activité | Coin non contrib. | Coin OCDE (toutes cotis.) | + aides logement | PTR OCDE (sans / avec AL) |
|---|---|---|---|---|---|---|---|
| 0,5 | 9,1 | −11,3 | 10,7 | 8,6 | 34,8 | +15,3 | 54 / 64 [calc.] |
| 1 | 5,0 | 39,0 | 16,6 | 60,6 | 75,0 | n.d. | 43 / 56 |
| 1,5 | 11,2 | 39,0 | 0 | 50,2 | 64,6 | +3 (heures) | 49 / 58 (1,42 Smic) |
| 2 | 23,2 | 14,9 | 0 | 38,1 | 58,2 | 0 | 45 / 51 (2,13 Smic) |
| 3 | 22,4 | 19,1 | 0 | 41,5 | 59,5 | ≈ 0 | 44 [calc.] |
| 5 | 22,1 | 20,1 | 0 | 42,2 | 60,0 | ≈ 0 | 43 [calc.] |

**Lecture.**
- À 1 et 1,5 Smic, la sortie de la réduction générale fait payer à l'employeur 0,90 € de cotisations par euro de salaire en plus. C'est le cœur du coin.
- À 0,5 Smic, la réduction finance les cotisations contributives : la part non contributive est négative.
- Les PTR sont personnels : ils excluent les cotisations patronales et sont calculés depuis le RSA (OCDE TaxBEN 2025). Ceux à 0,5, 3 et 5 Smic sont déduits des fichiers, avec 7 822 € de minima perdus.

**Non vérifié.**
- Le Smic horaire de 2025 (11,88 €) et le PASS (47 100 €) sont cohérents avec les seuils des fichiers OCDE, mais n'ont pas été relus en ligne.
- Le partage patronal entre cotisations contributives et non contributives (8,55 / 4,72 / 4,05 %) n'est pas vérifié ; le partage salarial retrouve exactement le total de l'OCDE.
- La réduction générale unique de 2026 n'est pas couverte.
- Les aides au logement à chaque niveau de salaire et la TVA ne sont pas couvertes.
- Les simulateurs IPP et OpenFisca n'ont pas été relancés.

## 7. Sources et statut de lecture

**Notices lues dans cette session.**
- Chetty (2009), *AEJ: Economic Policy* 1(2), 31-52, résumé : la perte dépend d'une moyenne de l'élasticité du revenu imposable et de celle du revenu gagné, pondérée par le coût en ressources de l'évitement.
- Hines (1999), « Three Sides of Harberger Triangles », *JEP* 13(2), 167-188, résumé.
- Kleven et Kreiner (2006), *JPubE* 90(10-11), 1955-1973, notice : coût marginal des fonds publics autour de 2 dans les pays à fort PTR (version CEPR).
- Kleven (2021), « Sufficient Statistics Revisited », *Annual Review of Economics* 13, 515-538, notice.
- Hendren et Sprung-Keyser (2020), *QJE* 135(3) : titre seulement.

**Lus par les notes du dépôt.**
- Sicsic (2022) ; Lehmann, Marical et Rioux (2013) ; Cabannes, Houdré et Landais (2014) ; Lefebvre, Lehmann et Sicsic (2025) ; Neisser (2021) ; Chetty, Guren, Manoli et Weber (2011) ; Saez, Slemrod et Giertz (2012).
- Määttänen et Terviö (2022) ; Eerola et al. (2021) ; Buettner (2017) ; Bérard et Trannoy (2018) ; Kopczuk et Munroe (2015, version NBER) ; Hilber et Lyytikäinen (2017).
- Best et Kleven (2018) : résumé seulement.
- Chodorow-Reich et al. (2026) ; IPP note 46.
- Devereux, Liu et Loretz (2014) : résumé seulement.

**Non lus, cités de mémoire ou par le cours.**
- Feldstein (1999) : équation non vérifiée.
- Harberger (1964) ; Goulder et Williams (2003) ; Saez (2002) ; Immervoll, Kleven, Kreiner et Saez (2007) ; Dahlby (2008).
- Beer, de Mooij et Liu (2020) ; Chetty et Saez (2005, 2010) ; Yagan (2015) ; Lutz (2015) ; Zwick et Mahon (2017).

**Données.**
- OCDE Taxing Wages et TaxBEN 2025 : fichiers du dépôt, non retéléchargés.
- Sorties `proposition.txt`, `simulation.txt`, `simulation_is.txt`, `pfu_chiffres.csv`.
- Cour des comptes 2025 (4,3 % au Smic), via le cours.
