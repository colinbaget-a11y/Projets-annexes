# Revue de littérature : taux du haut, élasticités, heures, barèmes lisses, taux uniques

*Novembre 2026. Les textes ont été ouverts (PDF ou page de l'éditeur) sauf mention « non vérifié ». Téléchargements : `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/litA/`. Formule de référence : taux qui maximise les recettes sur la tranche du haut τ\* = 1/(1+a·e), avec a le paramètre de Pareto et e l'élasticité du revenu imposable (ETI), sans effet revenu (Saez 2001 ; Saez, Slemrod et Giertz 2012, éq. 5).*

## 1. Taux marginal supérieur « à ne pas dépasser » en France

**Les « estimations de Jaravel ».** Je n'ai trouvé **aucune estimation de Xavier Jaravel (LSE, président délégué du CAE depuis mars 2025) d'un taux maximal d'impôt sur le revenu**. Ce qui circule sous son nom :
- **Taxe Zucman (patrimoine, pas revenu).** Tribune dans *Le Monde* (début septembre 2025), cosignée notamment avec Ph. Aghion, qui ramène le rendement d'environ 20 à environ 5 Md€. Je n'ai pas pu lire la tribune (payante) ; le chiffre est rapporté par le rapport du Sénat r25-760 et par l'entretien aux *Échos* du 23/09/2025 (« grave erreur »), lu sur cae-eco.fr. Le calcul détaillé figure dans le **Focus CAE n° 124** (oct. 2025 ; Auclert, Barbara, Jaravel, Lasterra, Laveissière, Lopes, Ragot, Renaud), encadré 4 : on part d'un rendement mécanique de 18,26 Md€ (simulateur WID) et on applique le ratio de Jakobsen et al. (Danemark, Suède), soit 0,74 € perdu par euro mécanique à long terme, dont 0,54 sur la marge intensive et 0,20 sur l'exil. On obtient **≈ 4,75 Md€**. Les auteurs jugent eux-mêmes la transposition « incertaine ».
- **Chiffrages d'IR du CAE** (Focus 124, puis Focus 147 d'octobre 2026, Auclert-Jaravel-Philippon-Ragot-Taugourdeau, base de plus de 150 mesures). La formule ΔR/M = 1 − ε·t/(1−t) est appliquée avec **ε = 0,40** pour +1 point d'IR sur toutes les tranches : 6,8 Md€ au lieu de 7,6 Md€ en mécanique, sur une assiette de 760 Md€. Elle est appliquée avec **ε = 0,65** pour le PFU porté de 30 à 33 % : 1,2 Md€ au lieu de 1,7 Md€. Cette formule, qui revient à un taux unique sur toute l'assiette, n'utilise pas le paramètre de Pareto. Elle ne donne pas de taux maximal : avec ε = 0,4, le taux unique qui maximise les recettes serait 1/(1+ε) ≈ 71 %. Ce chiffre est **mon calcul**, et les auteurs ne l'écrivent pas. La Note CAE n° 95 (oct. 2026, « stratégie de ruptures ») ne contient pas de taux maximal d'IR.
- **Conclusion.** Il s'agit vraisemblablement de ces chiffrages : effets de comportement de la taxe Zucman, et ε = 0,4 et 0,65 du CAE. Si l'utilisateur pense à un autre texte, il faut demander la source exacte.

**Estimations françaises.** Le tableau donne pour chacune l'élasticité e, le paramètre de Pareto a, le taux qui maximise les recettes τ\* et son champ.

| Étude (ouverte) | Question, données, identification | e | a | τ\* et champ |
|---|---|---|---|---|
| **Cabannes, Houdré, Landais 2014**, *Économie et Statistique* 467-468 | ETI au taux de rétention sur 1997-2004, échantillon « 500 000 déclarations » DGFiP, réformes du barème et du QF, méthode Gruber-Saez (2SLS) | 0,02 tous foyers ; **0,31** pour le top 10 % (IC95 du taux : 57-64 %) ; variantes 0,15 et 0,45 | 2,1 (2 à 2,25) | **61 %** sur l'assiette 2004 (avec abattement de 20 %), 76 % si e = 0,15, 51 % si e = 0,45. Converti sur l'assiette 2013 : **≈ 49-50 %**. **IR seul** : les effets sur les cotisations, la CSG et la TVA sont explicitement exclus |
| **Lefebvre, Lehmann, Sicsic** (IZA DP 16112, 2023 ; *Scand. J. Econ.* 2025) | Taux de Laffer sur les **revenus du capital**, POTE 2008-2017, réformes de 2008-2017 (instrument : changement mécanique de taux) | directe 0,76-0,77 ; croisée sur les revenus du travail faible mais positive | n.d. | **56-57 %** sans réponse croisée, **43-44 %** avec, en comptant l'IR sur le travail. Ce taux inclut les prélèvements sociaux, puisque les taux étudiés comprennent la CSG et la CRDS. Les auteurs notent que prendre en compte les cotisations **abaisserait** encore τ\* |
| **Sicsic** (WP TEPP 2020 ; *Fiscal Studies* 43(3) 2022) | ERFS 2006-2015 (panels de deux ans, enquête Emploi plafonnée en haut), 2SLS, réformes d'IR et de prestations | IR : **0,26** pour tous ; **0,22** bas 50 % ; **0,33** 40 % du milieu ; **0,51** top 10 % (tableau 6, version WP). Prestations : 0,1 (RSA activité) ; 0 (prestations familiales) | — | non calculé. Pas de très hauts revenus dans les données |
| **Lehmann, Marical, Rioux 2013**, *JPubE* 99 | Revenus d'activité < 2 SMIC, 2003-2006 | **≈ 0,2** au taux net d'IR ; **0** au taux net de cotisations | — | — |
| **IPP, note n° 46** (Bach, Bozio, Fabre, Guillouzouic, Leroy, Malgouyres 2019) | Dividendes : passage au barème en 2013, puis PFU en 2018 | Dividendes −40 % en 2013 | — | La réforme de 2013 a **coûté 0,9 Md€** au lieu de rapporter 0,4 Md€. Le PFU a fait **+15 %** de dividendes et coûte 0,4 Md€ au lieu de 0,9 Md€ |
| Aghion, Ciornohuz, Gravoueille, Stantcheva 2019 (WP, Collège de France) | Panel exhaustif 2011-2015 : taxe à 75 %, mise au barème | Études d'événements seulement : **aucune élasticité chiffrée** dans la version ouverte | — | — |

Non ouverts ou non vérifiés : Guillot (taxe à 75 % ; d'après un résumé de conférence, e ≈ 0,3 et incidence en partie sur l'employeur) ; les rapports du comité d'évaluation de la fiscalité du capital de France Stratégie ; un « Bozio et al. sur 2013-2018 » distinct de la note IPP 46 ; « Garbinti-Goupille-Lebrault-Pressel », introuvable. Le plus proche est Garbinti, Goupille-Lebret, Muñoz, Stantcheva, Zucman (NBER w31333) sur l'**ISF** : effet de l'information plutôt que du taux. Le Focus CAE n° 118 (Bach, Bozio et al. 2025) montre que l'exil est faible : **0,2 %** du top 1 % part chaque année. Repère étranger : Brewer, Saez et Shephard, cités par *Tax by Design*, trouvent e = 0,46 pour le top 1 % britannique, soit τ\* = **56 % tous prélèvements**, ce qui correspond à **40 % d'impôt sur le revenu** une fois les NICs et les impôts indirects déduits.

**À retenir pour la fusion.** Les τ\* d'IR seul (≈ 50 % aujourd'hui selon CHL) ne se comparent pas directement au taux du nouveau barème. Pour un impôt fusionné IR, CSG et CRDS, le τ\* pertinent porte sur le **coin total** : impôt fusionné, cotisations non contributives et TVA. Avec a ≈ 2, on obtient 67 % pour e = 0,25, 56 % pour e = 0,4 et 50 % pour e = 0,5 (mon calcul). Je n'ai pas vérifié de valeur de a pour le top 1 % français récent.

## 2. Élasticité « moyenne » pour le triangle de Harberger

**Formule.** Feldstein (1999, *REStat* 81(4), 674-680) montre que l'ETI résume toutes les marges de réponse (heures, effort, forme de la rémunération, évasion) : SSG 2012 le citent pour cette idée. J'ai vérifié la référence, mais le PDF NBER w5055 est un scan illisible, donc **je n'ai pas vérifié l'équation dans le texte original**. La perte sèche approchée ½·e·z·τ²/(1−τ) est la forme usuelle. SSG (2012, note 11) précisent que **l'approximation par le triangle de Harberger n'est valide que pour de petits taux**. La forme exacte de la perte marginale par euro levé est e·a·τ/(1−τ−e·a·τ). SSG estiment qu'avec e = 0,25, la perte marginale vaut 0,195 $ par dollar pour une hausse proportionnelle aux États-Unis, et 0,339 $ si elle est ciblée sur le top 1 %.

**Limites connues** (SSG 2012, section 2) :
- **Externalités fiscales** : un revenu déplacé vers une autre assiette, ou dans le temps, n'est pas une perte sèche. Si l'assiette fusionnée intègre les revenus du capital, une partie de l'élasticité du haut disparaît (cf. Lefebvre et al., Gorodnichenko et al.).
- **τ est le coin marginal total**, pas l'IR seul.
- L'ETI n'est **pas un paramètre structurel** : elle dépend de l'assiette et des niches (Neisser 2021).
- Les réponses observées en haut de la distribution relèvent surtout du **calendrier et de l'optimisation**. SSG notent qu'il n'existe « no compelling evidence » de réponses réelles en haut.

**Méta-analyse.** Neisser (version ECONtribute 2021, publiée dans *EJ* 131(640), 3365-3391) recense 61 études et 1 720 estimations.

| Concept | Moyenne | Médiane |
|---|---|---|
| Avant déductions | 0,287 | 0,185 |
| — dont revenu d'activité | 0,125 | 0,062 |
| — dont indépendants | 0,675 | 0,858 |
| Après déductions | 0,403 | 0,353 |

On observe un **biais de publication**. Le résultat principal est qualitatif : les estimations dépendent de la spécification et du contexte, et l'article ne propose pas de valeur unique corrigée. SSG 2012 jugent que les meilleures estimations de long terme vont de **0,12 à 0,40** aux États-Unis.

**Jeu proposé.** Élasticité du revenu d'activité au taux net marginal, sur le **coin total** :

| Groupe | Bas | Central | Haut | Fondement |
|---|---|---|---|---|
| 50 % du bas | 0,05 | 0,15 | 0,25 | CHL 0,02 (tous) ; Chetty et al. < 0,02 (salariés danois) ; LMR ≈ 0,2 et Sicsic 0,22 (comprend la participation) ; médiane Neisser du revenu d'activité 0,06 |
| 50-90 % | 0,05 | 0,20 | 0,35 | Sicsic 0,33 (40 % du milieu) ; Hicksienne intensive structurelle 0,33 (Chetty 2012, cité par CGMW) |
| 10 % du haut | 0,15 | 0,30 | 0,50 | CHL 0,31 (IC du taux 57-64 %) ; Sicsic 0,51 ; Hongrie 0,3 pour le top 20 % (Bakos et al. 2008, résumé seulement) |
| 1 % du haut | 0,20 | 0,40 | 0,70 | SSG 0,12-0,40 ; Royaume-Uni 0,46 ; moyenne Neisser après déductions 0,40 ; le haut de fourchette couvre le déplacement d'assiette, qui est en partie une externalité fiscale |

Ce jeu est **mon jugement**, sans moyenne publiée par niveau de revenu. Le scénario central de la note, 0,22-0,51, correspond au haut de cette fourchette pour les salariés ordinaires.

## 3. Gethin et Saez, « Global Working Hours » (NBER w34217, sept. 2025, révisé mai 2026), lu en v4

- **Données.** Enquêtes emploi de 160 pays (97 % de la population mondiale) et séries de plus de 20 ans pour 86 pays.
- **Mesure des impôts.** Le taux d'imposition est un **taux moyen macro** sur les revenus du travail, cohérent avec la comptabilité nationale (Bachas et al. 2026). Ce n'est **pas un taux marginal**.
- **Régressions en coupe** (138 pays, pondérées par la population, avec contrôle du log du PIB par adulte et de la part musulmane ou hindoue). L'élasticité des heures des 20-59 ans à (1−τL) vaut **0,9** : 0,6 pour les heures par emploi et 0,2 pour le taux d'emploi. Elle est de 0,8 pour les hommes et 1,2 pour les femmes. En panel avec effets fixes pays, elle tombe à **0,3-0,4**.
- **Contrôle des dépenses sociales.** Avec les transferts monétaires hors pensions, l'élasticité est **divisée par deux, à 0,3-0,7**. Un point de PIB de transferts va avec 2-3 % d'heures en moins.
- **Contrôle de la réglementation.** Les auteurs ajoutent un indice de réglementation du temps de travail (12 variables *Employing Workers* de la Banque mondiale, multipliées par la part d'emploi formel). L'élasticité **tombe de 0,5 à 0,1, non significative**. Passer de l'absence de réglementation au niveau le plus strict, celui de la France, va avec **−0,3 log** d'heures (≈ 35 %).
- **Lecture des auteurs** (« exploratory »). Les impôts sur le travail sont associés à moins d'heures parce qu'ils financent des transferts (effet revenu : élasticité non compensée faible, élasticité compensée positive) et parce qu'ils vont de pair avec l'État social et la réglementation des horaires.
- **Ce qu'ils ne peuvent pas conclure.** Ce sont des corrélations entre pays, avec des taux moyens. La réglementation est mesurée de façon « highly imperfect ». Les variables sont colinéaires. L'article ne dit rien de l'effet d'un taux marginal à recettes et transferts donnés, qui est exactement la question d'une refonte du barème.

**Comment concilier avec les autres travaux ?**
- **Bick, Brüggemann, Fuchs-Schündeln** (IZA DP 10179, version de travail ; *SJE* 2019). Dans un modèle à la Prescott, les écarts de taux moyens d'imposition **et** du ratio consommation/production expliquent **52 %** de l'écart d'heures Europe-États-Unis mesuré dans les enquêtes emploi, contre plus de 100 % avec les heures de la comptabilité nationale. Le reste vient des **semaines travaillées** (congés) et de la composition par diplôme. Les chiffres de la version publiée n'ont pas été vérifiés : l'écart y est de 14 % contre 19 % dans la version de travail.
- **Bick et Fuchs-Schündeln 2018** (*REStud* 85(3)). Résumé seulement : texte payant. Sur 17 pays européens et les États-Unis, avec un modèle de décision du couple, la prise en compte complète des non-linéarités et du traitement fiscal du couple est « cruciale » pour reproduire les heures des femmes mariées. Ce sont des **modèles calibrés**.
- **Micro, intensif, chocs petits ou temporaires.**
  - Danemark : élasticité observée par regroupement aux ressauts < 0,02 pour les salariés. Avec frictions, la borne inférieure de l'élasticité macro intensive est de **0,34** (Chetty, Friedman, Olsen, Pistaferri, *QJE* 2011, w15617).
  - Suisse : années sans impôt, élasticité intertemporelle de **0,025**, environ 0,1 pour les hauts salaires et 0,25 pour les indépendants (évitement), **aucun** effet sur la participation (Martínez, Saez, Siegenthaler, *AER* 2021).
  - Islande : année 1987 sans impôt, Frisch de **0,4** sur les heures et de 0,09 sur la participation, concentré sur les emplois flexibles, les jeunes et les seniors (Sigurdsson, *AEJ: Policy* 17(4) 2025, résumé AEA).
- **Synthèse Chetty, Guren, Manoli, Weber** (NBER 2011, *Macro Annual*). Élasticités hicksiennes de **0,3 intensive et 0,25 extensive**, cohérentes avec les écarts permanents entre pays. C'est la Frisch, et non la Hicksienne, qui est trop faible en micro pour les modèles de cycle.

**Réponse à « le taux marginal compte-t-il beaucoup pour les heures ? »** Pour la plupart des salariés, à court terme, l'effet est **faible**. Les horaires sont fixés par l'employeur et la convention, le taux est mal connu et les petits changements de barème ne valent pas l'ajustement. À long terme et à grande échelle, une élasticité hicksienne de **0,2-0,35** reste plausible, mais elle passe par les normes d'horaires, la participation, les seconds apporteurs et les seniors. Les écarts de taux moyens entre pays reflètent surtout des taxes **qui financent des transferts** et vont de pair avec la réglementation : on ne peut pas en tirer une élasticité des heures au taux marginal de 0,9.

## 4. Barème « formule » (§32a EStG) contre tranches

- **Aucun article n'isole l'effet d'un barème à zones linéaires-progressives par rapport à des tranches.** La recherche n'en a trouvé aucun ; l'argument se construit à partir de travaux généraux.
- **Rees-Jones et Taubinsky** (*REStud* 2020, w22884). **43 %** des Américains « repassent » le barème avec leur taux moyen (*ironing*), y compris dans un barème à tranches. Les auteurs montrent que cela **augmente le bénéfice de la progressivité**, puisque les distorsions perçues sont moindres.
- **Feldman, Katuščák, Kawano** (*AER* 2016, résumé). La perte forfaitaire du crédit pour enfant à 17 ans fait baisser le revenu déclaré : les ménages la prennent pour une hausse du taux marginal.
- **Abeler et Jäger** (*AEJ: Policy* 2015, IZA 7373). En laboratoire, dans un système complexe, les sujets réagissent moins aux nouvelles taxes, voire les ignorent, quelle que soit leur taille.
- **Allemagne : Blaufus et al.** (*EJLE* 2015). Les taux perçus s'écartent des taux réels pour la majorité, avec une sous-estimation aux hauts revenus. Les auteurs n'établissent pas de lien avec la formule du barème.
- **Bilan.** La littérature ne dit pas qu'un barème lisse est contre-productif. Elle dit que les gens comprennent mal **tout** barème non linéaire, et que la complexité **atténue** les réponses. C'est une perte de lisibilité, mais pas forcément une perte d'efficacité.
- ***Tax by Design*** (ch. 4). Deux ou trois taux et un abattement suffisent à approcher presque exactement tout barème optimal ; ajouter des tranches « n'apporte rien ». Ce texte défend la simplicité **affichée**, pas la formule.
- **Kostøl et Myhre** (*AER* 2021, IZA 13900, pensionnés d'invalidité norvégiens). Sans tenir compte des frictions, les élasticités sont **atténuées d'au moins 70 %**. Une lettre d'information porte l'élasticité à **0,15**, contre 0,06 sans lettre, et les erreurs de perception expliquent environ **deux tiers** de la hausse de l'atténuation.
- **Conséquence pour la communication des taux.** Faire connaître les taux marginaux est utile quand on **veut** une réponse, par exemple aux faibles taux du bas. Cela rend aussi les taux élevés plus distorsifs. Pour une réforme qui *abaisse* les taux marginaux, il faut les communiquer, sinon le gain d'incitation n'arrive pas.

## 5. Recommandations des think tanks et institutions

- **Tax Foundation, ITCI 2025.**
  - Critères pour l'impôt sur le revenu, mieux noté quand il est plus bas : taux supérieur, y compris les cotisations salariales ; seuil du taux supérieur en multiple du revenu moyen ; rapport entre coin marginal et coin moyen (moyenne OCDE 1,27, Hongrie 1). La complexité est mesurée par les surtaxes et les cotisations non standard. S'y ajoutent les taux sur les plus-values et les dividendes.
  - Position de la France : **38e sur 38** au classement général, 31e pour l'impôt sur le revenu (36e pour l'impôt sur le revenu ordinaire, 1re pour la complexité).
  - Ces critères favorisent mécaniquement un impôt proportionnel. Il s'agit d'un indice de « compétitivité », pas d'efficacité au sens du bien-être.
- **IFS, *Tax by Design*** (2011, ch. 4-5 et 20).
  - **Fusionner l'impôt sur le revenu et les NICs salariales, voire patronales.** Raisons : transparence (débattre des taux combinés de 31/41/51 % et non de 20/40/50 %), baisse des coûts administratifs, fin des promesses « pas de hausse d'IR » contournées par les NICs.
  - Deux ou trois taux au-dessus d'un abattement. Supprimer les abattements dégressifs, qui créent des taux marginaux « absurdes ».
  - Un barème des prestations intégré mais **distinct** de l'impôt, avec un calcul séquentiel.
  - Des taux plus faibles pour les groupes réactifs : mères d'enfants scolarisés, 55-70 ans.
  - Unité d'imposition : l'IFS ne tranche pas et prend comme données l'imposition individuelle et la conjugalisation des prestations.
  - Taux du haut : 50 % est « à l'extrémité haute » du taux qui maximise les recettes si l'assiette n'est pas élargie.
- **OCDE**, *Fundamental Reform of Personal Income Tax* (Tax Policy Studies n° 13, 2006). Seul le résumé a été lu : il compare impôt global, impôt dual et taux unique selon la simplicité, l'efficacité, l'équité, le civisme fiscal et les recettes. **Conclusions non vérifiées.**
- **FMI.**
  - Keen, Kim, Varsano (voir § 6).
  - *Fiscal Monitor*, octobre 2017 : selon le résumé, la théorie suggère des taux du haut « nettement » plus élevés. Le chiffre de **44 % souvent cité n'a pas été vérifié** : le site du FMI a bloqué le téléchargement.

## 6. « En Europe de l'Est, les taux uniques n'ont pas produit d'effet Laffer »

- **Ivanova, Keen, Klemm** (IMF WP 05/16 ; *Economic Policy* 2005, Russie 2001, 13 %). Les recettes réelles de l'impôt sur le revenu progressent de ≈ 26 %, mais il n'y a « **no evidence of a strong supply side effect** ». Le civisme fiscal s'améliore « d'environ un tiers », sans qu'on sache si cela vient du taux ou du renforcement des contrôles.
- **Gorodnichenko, Martinez-Vazquez, Sabirianova Peter** (*JPE* 2009, w13719, panel RLMS 1998-2004, écart consommation-revenu). Le revenu déclaré **augmente de 10-11 %** par rapport à la consommation chez ceux dont le taux baisse, ce qui traduit un **effet sur la fraude volontaire**. L'effet sur la productivité est faible. La perte sèche est **au moins 30 %** plus faible que dans l'approche conventionnelle.
- **Keen, Kim, Varsano** (IMF WP 06/218 ; *ITAX* 2008). La Russie est la seule exception. Sinon, la « seconde vague » (Ukraine, Slovaquie, Géorgie, Roumanie…) s'accompagne d'une **baisse des recettes de l'impôt sur le revenu**, par exemple −0,7 point de PIB en Slovaquie et environ −1 point pour l'impôt sur le revenu et l'IS en Roumanie. Pour les auteurs, « in no case does there appear to have been a Laffer effect ». La Lituanie (1994, taux unique fixé au taux *le plus élevé*) a vu ses recettes augmenter, ce qui n'est pas un effet Laffer.
- **Travaux postérieurs.** Je n'ai trouvé aucune estimation de Laffer contraire. En Hongrie, Bakos, Benczúr et Benedek (MNB WP 2008/7, résumé) trouvent une ETI de 0,06 et prévoient un gain de recettes modeste (+2 %) pour un taux unique hypothétique. Il s'agit d'une simulation antérieure à la réforme de 2011.
- **Phrase corrigée** : « Dans les pays d'Europe centrale et orientale qui ont adopté un taux unique bas au début des années 2000, les recettes de l'impôt sur le revenu ont en général baissé et aucune réforme ne s'est autofinancée (Keen, Kim et Varsano, 2008) ; en Russie, où elles ont augmenté de 26 % en termes réels après le passage à 13 % en 2001, la hausse tient à la reprise économique et à un meilleur civisme fiscal, non à un surcroît de travail (Ivanova, Keen et Klemm, 2005 ; Gorodnichenko, Martinez-Vazquez et Sabirianova Peter, 2009). »

## Non vérifié ou à vérifier

- Le texte des tribunes de Jaravel et d'Aghion (presse payante).
- L'équation dans Feldstein (1999).
- Le texte intégral de Bick et Fuchs-Schündeln (2018) et de la version *SJE* de Bick et al. (2019).
- Le chiffre de 44 % du FMI (2017).
- Les conclusions de l'OCDE (2006).
- Guillot sur la taxe à 75 %.
- Les rapports de France Stratégie.
- La valeur de a pour le top 1 % français.
- Le taux combiné de 58-66 % du coût du travail cité par l'OCDE.
- Points de la note actuelle à corriger :
  - « Bick et Fuchs-Schündeln… 18 pays… plus qu'au niveau moyen des impôts » : le résumé ne dit pas « plus que le niveau moyen ».
  - « Bick, Brüggemann et Fuchs-Schündeln : prélèvements ≈ moitié » : il s'agit des taxes **et** du ratio C/Y, dans le modèle de Prescott avec les heures des enquêtes emploi, chiffre de la version de travail.
  - Sigurdsson : écrire 0,4 (heures) et 0,09 (participation) plutôt que « 0,1 à 0,4 ».

## Ce qu'on peut écrire dans la note

1. « En France, l'élasticité du revenu imposable estimée sur 1997-2004 est de 0,02 pour l'ensemble des foyers et de 0,31 pour les 10 % les plus aisés ; avec un paramètre de Pareto de 2,1, le taux d'IR seul qui maximise les recettes serait d'environ 50 % sur l'assiette actuelle, hors CSG, cotisations et TVA (Cabannes, Houdré et Landais, 2014). »
2. « Sur 2006-2015, l'élasticité des revenus d'activité au taux net d'IR est d'environ 0,2 pour la moitié la moins aisée, 0,3 pour les 40 % suivants et 0,5 pour les 10 % du haut, mais elle est deux à trois fois plus faible pour les réformes de prestations, moins visibles (Sicsic, 2022). »
3. « Pour les revenus du capital, le taux qui maximise les recettes, prélèvements sociaux compris, tombe de 57 % à 43 % quand on tient compte de la baisse induite des revenus du travail (Lefebvre, Lehmann et Sicsic, 2025) ; la mise au barème des dividendes en 2013 a fait perdre 0,9 Md€ au lieu d'en rapporter 0,4 (IPP, 2019). »
4. « Le Conseil d'analyse économique retient une élasticité de 0,4 pour chiffrer une hausse d'un point de l'IR (6,8 Md€ au lieu de 7,6 Md€ à comportements inchangés) et de 0,65 pour le PFU (CAE, Focus n° 124, 2025). »
5. « La formule ½·e·τ²/(1−τ) de Feldstein n'est qu'une approximation, valable pour de petits taux ; elle surestime la perte quand une partie de la réponse consiste à déplacer du revenu vers une autre assiette taxée (Saez, Slemrod et Giertz, 2012). »
6. « Une méta-analyse de 1 720 estimations donne une élasticité médiane de 0,19 avant déductions et de 0,35 après, avec un biais de publication marqué (Neisser, 2021). »
7. « Entre pays, les heures sont nettement plus faibles là où le travail est plus taxé, mais ce lien disparaît une fois prises en compte les dépenses sociales et la réglementation du temps de travail (Gethin et Saez, 2026) : il mesure l'effet de l'État social dans son ensemble, pas celui du taux marginal. »
8. « Les expériences d'années sans impôt donnent des réponses d'heures faibles en Suisse (0,025) et modérées en Islande (0,4 sur les heures, 0,09 sur l'emploi), concentrées sur les emplois aux horaires flexibles (Martínez, Saez et Siegenthaler, 2021 ; Sigurdsson, 2025). »
9. « Le Royaume-Uni de *Tax by Design* recommande de fusionner impôt sur le revenu et cotisations salariales, afin que le débat porte sur les taux réellement payés, et juge que deux ou trois taux au-dessus d'un abattement suffisent à reproduire presque n'importe quel barème (Mirrlees et al., 2011). »
10. Phrase corrigée sur les taux uniques : voir § 6.
