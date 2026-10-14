# PISA 2000-2025 : indicateurs UE-27, notes de méthode

Fichiers : `pisa.py` (code), `pisa.csv` (résultat, format long : `pays, indicateur, annee, valeur, source, note`).
Pays : codes Eurostat (EL = Grèce). Pays entier dans tous les cycles (variable `CNT`, qui couvre toutes les régions
d'un pays, par exemple les communautés belges, les régions espagnoles et italiennes).
Données traitées le 14 octobre 2026.

## 1. Couverture

| Cycle | Origine | Indicateurs |
|---|---|---|
| 2025 | microdonnées `CY09_MS_STU_PUF` (26 pays) + Chypre publiée | tous sauf pensée créative |
| 2022 | microdonnées `CY08MSP_STU_QQQ` + `CY08MSP_CRT_COG` (25 pays) + Chypre publiée ; Luxembourg absent du cycle | tous |
| 2018 | microdonnées `CY07_MSU_STU_QQQ` (26 pays) + Chypre via EdStats | tous sauf sécurité et pensée créative |
| 2015 | microdonnées `CY6_MS_CMB_STU_QQQ` + `QQ2` (26 pays) + Chypre via EdStats | idem 2018, sans indice de harcèlement |
| 2000-2012 | **repli** : valeurs publiées (Banque mondiale EdStats `LO.PISA.*`, reprises des tableaux OCDE) | scores moyens, % faibles, % forts, D9-D1 |

Pays présents : 2000 = 19 (sans CY, EE, HR, LT, MT, SI, SK, et sans NL car l'OCDE n'a pas publié ses résultats) ;
2003 = 19 (sans BG, CY, EE, HR, LT, MT, RO, SI) ; 2006 = 25 (sans CY, MT) ; 2009 = 26 (sans CY) ;
2012 = 26 (sans MT) ; 2015, 2018, 2025 = 27 ; 2022 = 26 (le Luxembourg n'a pas participé).

**Chypre** ne figure pas dans les fichiers publics de microdonnées de 2015, 2018, 2022 et 2025 (aucun code
`CYP` ni `QCY`). Pour 2015 et 2018, on reprend les valeurs EdStats (moyennes, niveaux, D9-D1). Pour 2022 et 2025,
on reprend les scores moyens publiés par l'OCDE (Vol. I, tableau I.1), plus l'indice d'appartenance de 2025
(tableau I.5). Pour 2012, on reprend le score en maths publié (440), qui manque dans EdStats.

**Pourquoi un repli pour 2000-2012.** Les fichiers texte 2000-2012 ne sont accessibles que par l'Internet
Archive (le site `www.oecd.org` bloque les .zip). Le 14 octobre 2026, `web.archive.org` refusait toutes les
connexions (réinitialisation TLS ; `archive.org` répondait 429). Le proxy de session n'était pas en cause. Tous les
essais ont échoué (sept tentatives de 09 h 00 à 09 h 32 UTC). Le code de lecture des fichiers texte est en place
(`_cycle_txt` : positions lues dans les syntaxes SPSS officielles, téléchargées) et testé sur des fichiers
synthétiques au format 2000, 2006 et 2012. Il n'a pas encore tourné sur les vraies données. Il suffit de relancer
`telecharger` puis `extraire` quand l'Internet Archive répond : les valeurs calculées sur microdonnées remplacent
alors automatiquement le repli. On obtient en plus ESCS, résilients, BELONG (2000, 2003, 2012) et l'effectif.

## 2. Méthode commune (microdonnées)

- **Poids** : `W_FSTUWT` (poids élève final), même nom dans tous les cycles. En 2000, chaque fichier par domaine
  (maths et sciences sur sous-échantillon) a son propre `W_FSTUWT`. Le fichier lecture sert pour l'effectif et
  BELONG.
- **Valeurs plausibles** : chaque statistique (moyenne, %, déciles, écarts, résilients) est calculée sur chaque
  valeur plausible, puis on fait la moyenne. 10 valeurs (`PV1MATH`…`PV10MATH`, `READ`, `SCIE`) depuis 2015,
  5 avant. Pas de BRR : point estimé uniquement.
- **Déciles** : quantile pondéré, première valeur dont le poids cumulé atteint q × poids total. On retrouve
  exactement les P10 et P90 publiés par l'OCDE (écart 0,00 sur 2015 et 2018, cf. § 6).
- **Quarts nationaux d'ESCS** : élèves d'ESCS non manquant, triés par ESCS, puis quart attribué selon le poids
  cumulé (point milieu du poids de l'élève).
- **Lecture** : `pyreadstat` avec `usecols`, par blocs de 150 000 lignes, filtrage UE-27 immédiat. Les valeurs
  manquantes déclarées (95-99 ou 5-9 selon le cycle) deviennent NaN. Un cache `cache_<année>_*_ue27.csv.gz` est
  écrit dans le dossier brut, et le zip peut être supprimé (`extraire(..., nettoyer=True)`).
- Le zip 2025 utilise la compression Deflate64 (méthode 9), non gérée par `zipfile`. Le code passe alors par
  `unzip`.

## 3. Seuils des niveaux (bornes inférieures, identiques dans tous les cycles)

| Domaine | Niveau 2 | Niveau 5 | Niveaux définis depuis |
|---|---|---|---|
| Maths | 420,07 | 606,99 | 2003 |
| Lecture | 407,47 | 625,61 | 2000 |
| Sciences | 409,54 | 633,33 | 2006 |

Ces seuils sont vérifiés pour 2025 dans les notes techniques PISA 2025 (NCES, tableau 3, qui reproduit l'OCDE) :
maths 1c 233,17 → 6 669,30 ; lecture 1c 189,33 → 6 698,32 ; sciences 1b 260,54 → 6 707,93 (pas de niveau 1c en
sciences). Les subdivisions sous le niveau 1 changent selon les cycles (1a, 1b en lecture en 2009, 1c en 2018 ;
1a, 1b, 1c en maths en 2022), mais les bornes des niveaux 2 et 5 ne changent pas.
`pisa_faibles_*` = score < niveau 2 ; `pisa_forts_*` = score ≥ niveau 5.
Ces deux indicateurs ne sont pas produits avant que l'échelle existe : maths 2000, sciences 2000 et 2003.

## 4. Indicateurs et variables par cycle

| Indicateur | Définition | Variables |
|---|---|---|
| `pisa_maths`, `pisa_lecture`, `pisa_sciences` | score moyen | `PVnMATH`, `PVnREAD`, `PVnSCIE` |
| `pisa_faibles_*`, `pisa_forts_*` | % < niveau 2, % ≥ niveau 5 | idem + seuils § 3 |
| `pisa_d9d1_*` | P90 − P10 du score | idem |
| `pisa_ecart_escs_maths` | moyenne maths du quart national ESCS supérieur − quart inférieur | `ESCS` |
| `pisa_resilients` | % des élèves du quart national ESCS inférieur dont le score en maths est dans le quart supérieur national (tous élèves du pays) | `ESCS`, PV maths |
| `pisa_appartenance` | moyenne de l'indice | `BELONG` (2015, 2018, 2022, 2025) |
| `pisa_securite` | moyenne de l'indice | `FEELSAFE` (2022, 2025) |
| `pisa_harcelement` | moyenne de l'indice | `BEINGBULLIED` (2018), `BULLIED` (2022, 2025) |
| `pisa_harcelement_freq` | % victimes d'au moins un acte « quelques fois par mois » ou plus (codes 3-4), parmi les élèves ayant répondu à au moins un item | `ST038` (cf. ci-dessous) |
| `pisa_pensee_creative` | score moyen, 0-60 points (« number correct ») | `PV1CRTH_NC`…`PV10CRTH_NC` du fichier CRT, apparié par `CNT`+`CNTSTUID` au fichier élève pour `W_FSTUWT` |
| `pisa_effectif_15ans` | somme des `W_FSTUWT` | – |

**Résilients : définition OCDE et ses changements.** Le cahier des charges impose les maths et le quart national,
et on applique cette définition à tous les cycles. Elle correspond à la définition OCDE de 2022 (Vol. I,
tableau I.2). L'OCDE l'a fait varier :
- 2006-2012 : défavorisés selon le quart inférieur national de l'ESCS, résilients dans le quart supérieur de
  performance **de l'ensemble des pays**, après prise en compte de l'ESCS (domaine majeur du cycle).
- 2015 (Vol. I) : « core-skills resilience », c'est-à-dire quart inférieur national d'ESCS et au moins le niveau 3
  dans les trois domaines.
- 2018 (Vol. II) : quart national, domaine **lecture**.
- 2022 : quart national, **maths**. La note du tableau I.2 du Vol. I dit « reading », mais les valeurs publiées
  sont celles des maths, et on les reproduit à 0,1 point près.
- 2025 (Vol. I) : quart national, domaine **sciences** en titre (OCDE 12 %), avec maths (12 %) et lecture (13 %) en
  annexe.

`pisa_resilients` 2025 est donc en maths (série homogène). Le chiffre OCDE mis en avant en 2025 est celui des
sciences.

**Sécurité, équivalent 2025.** `FEELSAFE` existe aussi en 2025 (« Student reports on feeling safe (WLE) ») mais
n'est pas renseigné pour DE et DK. En 2022, il manque pour DE, DK et ES. L'indice n'existe pas avant 2022.

**Harcèlement.** Les indices WLE sont réétalonnés à chaque cycle (moyenne OCDE ≈ 0) : comparer les pays dans un
cycle, pas les niveaux d'un cycle à l'autre. Il n'existe dans la base aucune variable OCDE « fréquemment harcelé »
(en 2018, l'OCDE l'avait définie comme les 10 % supérieurs de l'indice dans l'OCDE, sans la publier comme variable).
On retient donc la mesure absolue que l'OCDE publie en 2018 et 2025 : au moins un acte au moins quelques fois par
mois. Les items varient selon le cycle :
- 2015, 2018 et 2022 : 6 actes `ST038Q03NA` à `Q08NA` (tenu à l'écart, moqué, menacé, affaires prises ou
  détruites, frappé ou bousculé, rumeurs). En 2015, ils viennent du fichier complémentaire `CY6_MS_CMB_STU_QQ2` ;
  Q01 et Q02 sont exclus par l'OCDE ; l'item n'a pas été posé en IT, MT et RO.
- 2025 : 5 actes `ST038Q04NA`, `Q05NA`, `Q07NA`, `Q08NA` et `Q12DA` (cyberharcèlement : informations publiées en
  ligne sans consentement). C'est une **rupture** : Q03 et Q06 sont retirés et la cyberintimidation est ajoutée.

## 5. Ruptures de série

- **Lecture** : échelle créée en 2000 (domaine majeur). Nouveau cadre en 2009 (lecture électronique ; niveaux 1a
  et 1b), échelle maintenue. Nouveau cadre en 2018, avec test adaptatif et niveau 1c. L'OCDE compare la lecture
  depuis 2000.
- **Maths** : échelle et niveaux établis en 2003. La valeur 2000 (domaine mineur, sous-échantillon, autre
  échelle) n'est **pas comparable** (colonne `note`). Nouveau cadre en 2022 (domaine majeur).
- **Sciences** : échelle et niveaux établis en 2006. Les valeurs 2000 et 2003 ne sont pas comparables. Nouveau
  cadre en 2015 et en 2025 (domaine majeur, test adaptatif multi-étapes).
- **2015** : passage à l'évaluation sur ordinateur (CBA) et nouveau modèle d'échelonnement (modèle hybride
  2PL/Rasch, 10 valeurs plausibles). L'OCDE maintient les tendances, avec des erreurs de lien plus grandes.
- **2022** : cycle décalé d'un an par la pandémie. **2025** : PISA devient quadriennal ; test adaptatif
  multi-étapes dans les 3 domaines. Le lien 2022-2025 est estimé directement (erreur de lien : sciences 3,1 ;
  lecture 1,1 ; maths 1,2).
- **Cas particuliers** (colonne `note`) :
  - Espagne 2018 : lecture **non publiée par l'OCDE** (réponses invraisemblables). Valeur calculée mais à exclure.
  - Autriche 2009 : comparabilité limitée.
  - Pays-Bas 2000 : non publié (absent du repli).
  - Luxembourg 2000 : comparabilité limitée.

## 6. Contrôles contre les chiffres OCDE

`pisa.controles(df)` compare le résultat aux valeurs publiées intégrées au module.
- **Scores moyens, microdonnées** : 2022 et 2025, tous les pays de l'UE du tableau I.1 (25 et 26 pays, 3
  domaines) ; 2015 et 2018 (FR, DE, EE, FI/PL). **Écart maximal 0,50 point**, c'est-à-dire l'arrondi. France 2022 :
  473,9 / 473,9 / 487,2 (publié 474 / 474 / 487). France 2025 : 457,7 / 456,3 / 483,4 (publié 458 / 456 / 483).
  France 2018 : 495 / 493 / 493. France 2015 : 493 / 499 / 495.
- **Résilients et écart ESCS 2022** (Vol. I, tableau I.2, 25 pays) : résilients à 0,11 point au plus ; écart de
  score à 0,7 point au plus (FR 112,5 contre 113 ; DE 111,6 contre 111). L'écart résiduel vient de la répartition
  en quarts.
- **2025, contrôle de la méthode sur les indicateurs publiés** (Vol. I, tableaux I.2 et I.5, 26 pays). Mêmes
  fonctions, appliquées aux sciences :
  - % de résilients en sciences : écart ≤ 0,16 (FR 11,04 contre 11,0) ;
  - écart ESCS en sciences : ≤ 0,8 (FR 99,98 contre 100) ;
  - indice `BELONG` moyen : ≤ 0,005 (FR 0,06) ;
  - % jamais ou presque jamais harcelé sur les 5 actes : ≤ 0,05 (FR 55,97 contre 56,0), ce qui valide le codage
    des items `ST038`.
- **% faibles 2022 et 2025** : France maths 28,8 % (OCDE 29 %) et 35,7 % (36 %) ; lecture 2025 32,7 % (33 %) ;
  sciences 2025 25,8 % (26 %) ; % forts en maths 2025 5,2 % (5 %).
- **Pensée créative 2022** (Vol. III) : EE 35,9 (36), LV 35,1 (35), BE 34,9 (35), PL 34,4 (34), DE 32,5 (33),
  FR 32,4 (32), DK 35,5 (35).
- **Repli EdStats contre microdonnées** (2015 et 2018, 26 pays) : moyennes, D9-D1, % faibles et % forts en maths
  et sciences **identiques** (écart 0,00). En lecture, EdStats arrondit les parts par niveau à l'unité, d'où des
  écarts ≤ 1,1 point sur les % faibles et ≤ 1,0 sur les % forts. Pour 2000-2012, les moyennes EdStats de FR et DE
  correspondent aux rapports OCDE (≤ 0,5). Les % faibles en lecture correspondent aussi aux valeurs connues
  (FR 2000 : 15 contre 15,2 ; DE 2000 : 23 contre 22,6).

## 7. Lacunes

- **2000-2012** : pas d'écart ESCS, de résilients, de BELONG ni d'effectif tant que les microdonnées ne sont pas
  téléchargées (cf. § 1). Les % faibles et forts en lecture sont arrondis à environ ± 1 point.
- **Chypre** : seulement des valeurs publiées. Il n'y a ni indicateurs de distribution ni ESCS pour 2022 et 2025,
  et rien d'autre que les moyennes et les niveaux pour 2012-2018.
- **Pensée créative** : 2022 seulement ; non passée par AT, IE, SE (et CY, LU absents).
- **Sécurité** : 2022 et 2025 seulement, sans DE et DK (ni ES en 2022). **Harcèlement** : indice à partir de
  2018 ; fréquence à partir de 2015 (sans IT, MT, RO en 2015).
- Les indices WLE (appartenance, sécurité, harcèlement) ne se comparent pas d'un cycle à l'autre.

## 8. Fichiers sources et retéléchargement

Microdonnées, fichiers élèves au format SPSS, supprimés après extraction du sous-ensemble UE-27 :
- 2025 : https://webfs.oecd.org/pisa2022/2025/CY09_MS_STU_PUF.zip
- 2022 : https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip et https://webfs.oecd.org/pisa2022/CRT_SPSS.zip
- 2018 : https://webfs.oecd.org/pisa2018/SPSS_STU_QQQ.zip
- 2015 : https://webfs.oecd.org/pisa/PUF_SPSS_COMBINED_CMB_STU_QQQ.zip (contient aussi `STU_QQ2`)
- 2000-2012 : copies Internet Archive et syntaxes SPSS OCDE, liste complète dans `pisa.FICHIERS` et dans
  `../../manifest_acces_pisa.csv`. Par exemple
  https://web.archive.org/web/2023id_/https://www.oecd.org/pisa/pisaproducts/INT_STU12_DEC03.zip
- EdStats : `https://api.worldbank.org/v2/country/<ISO3;…>/indicator/LO.PISA.MAT;…?source=12&format=json`
- Rapports de contrôle : PISA 2022 Results Vol. I
  (https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/12/pisa-2022-results-volume-i_76772a36/53f23881-en.pdf),
  PISA 2025 Results Vol. I
  (https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/09/pisa-2025-results-volume-i_5265bfb1/73451bc5-en.pdf),
  notes techniques NCES PISA 2025 (https://nces.ed.gov/surveys/pisa/pisa2025/technical-notes/index.asp).

Reproduction (environ 2,7 Go à télécharger pour 2015-2025, puis 5 minutes de calcul) :

```bash
python3 -I pisa.py --telecharger /chemin/pisa_raw   # zips élèves + syntaxes + EdStats
python3 -I pisa.py /chemin/pisa_raw                 # écrit pisa.csv à côté de pisa.py
```
