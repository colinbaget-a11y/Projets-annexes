# Baisse des scores PISA de la France : deux chiffrages à grand trait

## Données (moyennes publiées, échelle PISA : moyenne OCDE 500 / écart-type élève 100 à l'année de base)

Les comparaisons ne sont valides qu'à partir du cycle où le domaine a été « majeur » : lecture depuis 2000,
maths depuis 2003, sciences depuis 2006.

| France | 2000 | 2003 | 2006 | 2009 | 2012 | 2015 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| Maths | – | 511 | 496 | 497 | 495 | 493 | 495 | 474 | 458 |
| Lecture | 505 | 496 | 488 | 496 | 505 | 499 | 493 | 474 | 456 |
| Sciences | – | – | 495 | 498 | 499 | 495 | 493 | 487 | 483 |

Sources : 2022 et 2025 — notes DEPP n° 26.40 (sept. 2026) et notes pays OCDE (PISA 2022 et 2025) ;
2003 maths (511) — DEPP 26.40 ; cycles intermédiaires — tableaux OCDE repris par l'IFRAP (les tableaux
de tendance de l'OCDE eux-mêmes sont sur des pages inaccessibles depuis cet environnement).
Moyenne OCDE : maths 485 (2015) → 463 (2025), sciences 489 → 482 (PISA 2025 Vol. I).

Écarts retenus : maths −53 pts depuis 2003 (−37 depuis 2018, −16 depuis 2022) ; lecture −49 depuis 2000
(−37 depuis 2018) ; sciences −12 depuis 2006. En écart-type élève : 0,53 / 0,37 / 0,16 / 0,49 / 0,12.

## 1. Équivalent en années de scolarité

Paramètre : le rythme auquel une cohorte progresse en un an autour de 15 ans, maturation comprise (détail et sources dans `note_litterature.md`, section 1).

* Avvisati & Givord (2021, WP 257 et 249) : discontinuité de date de naissance à âge d'entrée constant, PISA 2015-2018 : **≈ 20 points en moyenne (18 pays)** ; Autriche 26, Écosse 30, Luxembourg 31, Allemagne 34, Suisse 36. PISA 2025 Vol. I (Table I.2.7, 10 pays, 2015-2025) : ≈ 20, Angleterre 27, Écosse 29. L'OCDE a adopté 20 points comme référence dans PISA 2022.
* Ancienne règle OCDE (PISA 2009/2012, Table A1.2) : 39-41 points, classe non instrumentée ; France 47-49, artefact du redoublement. Écartée.
* Hors PISA : Carlsson et al. (2015), 180 jours d'école = 0,14-0,21 SD ; Hill et al. (2008), 0,19-0,25 SD par « année de vie » autour de la 3e-2de.
* France : pas d'estimation causale possible (cohorte PISA = cohorte d'entrée au CP) ; Givord (2024) mesure l'effet de l'âge d'entrée, 14-18 points.

Résultat (2025 vs référence) :

| | −53 pts (maths, 2003) | −37 pts (maths ou lecture, 2018) | −16 pts (maths, 2022) |
|---|---|---|---|
| 20 pts/an (référence OCDE) | 2,65 ans | 1,85 an | 0,8 an |
| **25 pts/an (retenu)** | **2,1 ans** | **1,5 an** | 0,6 an |
| 35 pts/an (Allemagne, Suisse) | 1,5 an | 1,05 an | 0,45 an |

Lecture : un élève de 15 ans de 2025 est, en maths, au niveau qu'avait un élève de 13-13,5 ans en 2003. L'OCDE et Avvisati-Givord refusent la conversion mécanique en années de scolarité ; « l'équivalent de 1,5 à 2,5 années d'apprentissage au rythme observé autour de 15 ans » est la formulation défendable.

## 2. Équivalent en PIB de long terme

Deux cadres coexistent dans la littérature et donnent des résultats sans commune mesure.

### 2a. Effet de niveau (rendement des compétences) — le chiffrage défendable

Mécanisme : des élèves moins compétents à 15 ans deviennent des travailleurs moins productifs ; à l'équilibre
le salaire mesure la productivité ; quand toute la population active est composée de ces cohortes, le PIB par
tête est plus bas dans la proportion du rendement des compétences × la perte de compétences.

Paramètre : Hanushek, Schwerdt, Wiederhold & Woessmann (2015, EER), PIAAC, salaire horaire des 35-54 ans à
temps plein : **+17,4 % de salaire par écart-type de numératie en France** (17,8 % pour les 23 pays).

* −0,53 SD (maths depuis 2003) → **−9 %** de PIB par tête à terme ; −0,37 SD (depuis 2018) → **−6,5 %** ;
  −0,16 SD (depuis 2022) → −3 %.
* Calendrier : la cohorte de 2025 entre sur le marché du travail vers 2030 ; le remplacement complet des
  actifs prend ~45 ans. Vers 2050, un peu plus de la moitié de l'effet est réalisé (≈ −3,5 % à −5 %).
* Fourchette (détail dans `note_litterature.md`, section 2) : à diplôme donné 0,094 (−3,4 % / −4,9 %) ; emploi inclus 0,275
  (−9,7 % / −13,6 %) ; passage PISA → PIAAC de 0,55 plutôt que 1 (−3,5 % / −4,9 %) ; l'OLS est plutôt une borne basse
  (Hampf et al. 2017). Cadre macro OCDE (Égert et al. 2022, moyenne des trois domaines) : −3,8 à −4,5 % de PGF pour la
  baisse depuis 2018 avec l'élasticité PISA→PIAAC de 0,278, −8 à −9,5 % avec 0,603 ; depuis 2003-2006 : −4,6 à −5,5 % / −9,7 à −11,6 %.
  **Retenu : ≈ −5 % (−3,5 à −10) pour la baisse depuis 2018, ≈ −8 % (−4 à −14) pour la baisse depuis 2003.**
* Hypothèses fortes : 1 SD PISA à 15 ans ≈ 1 SD PIAAC adulte (correspondance d'échelles, pas de
  rattrapage ultérieur) ; pass-through complet à l'emploi et au PIB (capital qui s'ajuste) ; baisse permanente
  des cohortes futures.

### 2b. Effet de croissance (Hanushek & Woessmann 2012, 2020) — à manier avec précaution

Régression de croissance 1960-2000 sur 50 pays : **+1,98 point de croissance annuelle par SD** de
compétences de la main-d'œuvre (1,74 sur les seuls pays de l'OCDE ; 0,6 à 1,3 quand la croissance est mesurée après les tests). Appliqué mécaniquement à une baisse permanente de −0,37 SD (maths depuis
2018) : la croissance française serait durablement inférieure de 0,7 pt/an une fois les cohortes
remplacées, soit un PIB inférieur de ~5 % en 2050, ~20 % en 2075, ~38 % en 2100 (−55 % en 2100 pour
−0,53 SD). Ce n'est pas un « niveau de long terme » : l'écart croît sans borne.

Pourquoi ne pas retenir ces chiffres comme chiffrage central : (i) la spécification impose qu'un niveau de
compétences change durablement le taux de croissance, alors que 40 ans de données ne distinguent pas un
effet de croissance d'un long effet de niveau ; (ii) appliqué à la baisse de la moyenne OCDE (−37 pts en maths
depuis 2003), il impliquerait que l'OCDE entière ait perdu ~0,7 pt de croissance tendancielle — proche de
toute sa croissance par tête ; (iii) Hanushek & Woessmann eux-mêmes ne l'utilisent que pour une seule
cohorte touchée (COVID : −0,11 SD → −1,5 % de PIB en moyenne sur le siècle, −2,6 % en 2100).

Calcul officiel OCDE (2010, coef. 1,736) inversé pour la France (`simulation_ocde2010.py`) : −37 pts → PIB −5 % en 2050,
−25 % en 2090, croissance −0,64 pt à terme ; variante néoclassique (H&W 2011) : −17,5 % en 2090, état stationnaire −29 %.

### Ce qu'on peut dire

« Les 15 ans de 2025 ont en maths environ deux ans de scolarité de retard sur ceux de 2003 (1,5 an sur ceux
de 2018) ; si ce niveau se maintient et se traduit un pour un en compétences adultes, le PIB par tête de long
terme est inférieur d'environ 5 à 8 % à ce qu'il aurait été (fourchette 3,5 à 14 %), effet atteint vers 2075 et à moitié
réalisé vers 2050. » Les scénarios « effet de croissance » donnent des pertes plusieurs fois supérieures mais reposent sur
une identification que la littérature ne juge pas établie.

Le script `chiffrage_pisa_pib.py` reproduit tous les chiffres ; chaque paramètre est modifiable en tête de fichier.
