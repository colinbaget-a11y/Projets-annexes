# Données réelles pour la carte des électeurs

Objectif : remplacer la simulation par des répondants réels. Il faut, pour chaque personne, trois
choses — une position économique, une position culturelle, un vote déclaré — et, pour la dimension
temporelle, plusieurs dates avec des items comparables. Ce document recense ce qui existe, ce que
j'ai pu vérifier, et dans quel ordre s'en servir.

Convention : **vérifié** = lu sur la page de la source ou dans un document primaire pendant ce
recensement ; **de mémoire** = connaissance antérieure, à confirmer avant usage.

---

## 1. Le graphique existe déjà dans la littérature française

Deux précédents directs, qu'il faut lire avant de commencer.

**Chiche, Le Roux, Perrineau & Rouanet (2000)**, « L'espace politique des électeurs français à la
fin des années 1990. Nouveaux et anciens clivages, hétérogénéité des électorats », *Revue française
de science politique* 50(3), 463-488. Analyse géométrique des données (ACM) sur la post-électorale
CEVIPOF du 26-31 mai 1997, avec explicitement un **nuage des individus** et non seulement un nuage
des modalités — c'est le principe des figures 10-11 du prototype. Résultats vérifiés : le premier
axe oppose attitudes « ouvertes » et « fermées » (étrangers, Europe, mondialisation) et n'est pas
l'axe gauche-droite ; les axes 2 et 3 portent sur les attitudes sociales et le libéralisme de marché,
où le clivage gauche-droite réapparaît ; et la **variance intra-électorat dépasse toujours la
variance inter-électorats**. Autrement dit, ce que montre la figure 11 simulée était déjà le résultat
empirique de 1997.

**Grunberg & Schweisguth**, « Libéralisme économique et libéralisme culturel » (1990) et « Vers une
tripartition de l'espace politique » (1997). Ils ont construit, sur les post-électorales CEVIPOF, deux
échelles — libéralisme économique, libéralisme culturel — qui sont exactement les deux axes du
projet, et montré qu'elles sont corrélées négativement. La notion de « libéralisme culturel » vient
de leur analyse de la post-électorale de 1978. Le projet est donc une reprise de cette tradition
avec trois ajouts : la longue durée (1988-2024), la couche « marché / captation », et l'estimation
d'un modèle de choix.

## 2. Le cœur : les enquêtes électorales du CEVIPOF, archivées au CDSP

Le Centre de données socio-politiques (Sciences Po / CNRS) archive et diffuse la série. Portail :
data.sciencespo.fr. Accès : téléchargement direct pour les fichiers ouverts, inscription ou demande
motivée pour les fichiers restreints.

| Enquête | Année(s) | Dispositif | N | Accès | Statut |
|---|---|---|---|---|---|
| Post-électorales | 1958, 1962, 1967-69, 1978 | face-à-face | — | CDSP ; 1958, 1967-69 aussi à l'ICPSR | vérifié (existence) |
| Post-électorale CEVIPOF-SOFRES | 1988 | face-à-face, échantillon aléatoire | ≈ 4 000 | CDSP (fiche CESSDA) | vérifié |
| Post-électorale CEVIPOF | 1995 | face-à-face | 4 078 | CDSP ; ICPSR 6806 | vérifié |
| Post-électorale CEVIPOF-CIDSP-CRAPS | 1997 | téléphone, aléatoire, entre les deux tours | 3 010 | CDSP ; ICPSR 3138 | vérifié |
| Panel électoral français | 2002 | 3 vagues | — | CDSP | vérifié (existence) |
| Baromètre politique français (BPF) | 2006-2007 | 4 vagues, CATI, IFOP, Ministère de l'Intérieur | ≈ 5 000 par vague | CDSP | vérifié |
| Panel électoral français | 2007 | 2 vagues | — | CDSP | vérifié (existence) |
| French Election Study | 2012 | post-électorale, échantillon aléatoire, composante CSES module 4 | — | CDSP | vérifié |
| French Election Study (FES 2017) | 2017 | post-électorale face-à-face, quotas, CSES module 5 | 1 830 | CDSP ; Gougou et al., *French Politics* 2017 | vérifié |
| **ENEF 2017** | 2015-2017 | panel en ligne Ipsos, **20 vagues** | ≈ 10 000 panélistes, 13 000-23 000 répondants par vague selon les vagues | **licence Etalab 2.0, ouvert**, DOI 10.21410/7E4/N7HZLA | vérifié |
| ENEF 2019 | 2019 | panel, européennes | — | CDSP, fichiers restreints, publié avril 2025 | vérifié |
| **ENEF 2022** | avr. 2021 - juin 2022 | panel Ipsos, **12 vagues**, dir. M. Foucault | 16 000 panélistes, 10 928-16 228 par vague | diffusion CDSP annoncée pour 2026 | vérifié |
| **ENEF 2024** | mars-août 2024 | panel Ipsos CAWI, 7 vagues, européennes + législatives | > 10 000 | **CC BY-SA 4.0**, publié février 2026, DOI par vague (ex. 10.21410/7E4/7HRNPP) | vérifié |
| ELIPSS | 2012 → | panel probabiliste en ligne, mensuel, modules politiques (Dynamob) | ≈ 2 600 | ouvert à la communauté scientifique | vérifié |

**La post-harmonisation du CDSP.** Jan, Marie & Sauger (2023), *65 ans d'enquêtes électorales en
France : une post-harmonisation* (HAL hal-04032972) : 25 enquêtes pré- et post-électorales
1958-2022, plus de 2 500 variables tirées de 11 enquêtes de référence, harmonisées au format DDI-L
sur la classification du projet True European Voter, dans une banque de questions et de variables
publique : https://explore.cdsp.sciences-po.fr/ (le portail refuse les robots, il faut un navigateur).
C'est l'outil qui permet de répondre à la question qui conditionne tout — *quels items ont été posés
à l'identique en 1988, 1995, 1997, 2002, 2007, 2012, 2017, 2022 ?* — avant de construire un axe
comparable dans le temps. La France ne figure pas, à ma lecture du codebook, dans le fichier True
European Voter lui-même (GESIS ZA5054).

Ce que ces enquêtes contiennent (vérifié pour 2017, de mémoire pour les autres) : auto-positionnement
gauche-droite, vote déclaré aux deux tours, batteries d'attitudes sur l'économie (réduction des
inégalités, rôle de l'État, entreprises) et sur la dimension culturelle (immigration, peine de mort,
ordre, mœurs), et dans les panels récents le placement perçu des candidats — ce qui permet de mettre
l'offre dans l'espace des électeurs.

## 3. Séries internationales comparables dans le temps

Ces enquêtes ne sont pas électorales mais posent les **mêmes items à chaque vague**, ce qui règle
d'emblée le problème de comparabilité que les enquêtes du CEVIPOF n'ont pas résolu par construction.

**European Social Survey — la meilleure série continue.** France présente aux 11 rounds, 2002/03 à
2023/24 (vérifié), environ 1 500 à 2 000 répondants par round, échantillon probabiliste, face-à-face.
Téléchargement libre après inscription sur ess.sikt.no. Items du questionnaire commun utiles
(noms de variables de mémoire, à confirmer sur le portail) :

| Dimension | Items |
|---|---|
| économie | `gincdif` (l'État doit réduire les écarts de revenus) ; modules bien-être social des rounds 4 (2008) et 8 (2016) pour des batteries plus riches |
| culture | immigration : `imsmetn`, `imdfetn`, `impcntr`, `imbgeco`, `imueclt`, `imwbcnt` ; mœurs : `freehms` ; valeurs de Schwartz : `ipstrgv` (État fort), `imptrad` (tradition), `ipfrule` (règles), `ipbhprp` (se comporter comme il faut) |
| repères | `lrscale` (gauche-droite 0-10), `euftf` (intégration européenne) |
| vote | `prtvt*fr` : parti voté à la dernière élection nationale, codage propre à la France, nom de variable qui change de round en round |

Limite : l'axe économique repose sur peu d'items dans le questionnaire commun ; l'axe culturel est
bien couvert.

**European Values Study.** France à toutes les vagues : 1981, 1990, 1999, 2008, 2017 (vérifié) ; N de
1 000 à 1 500 ; item « pour quel parti voteriez-vous, premier choix » présent de 1981 à 2008 (vérifié)
et dans la vague 2017 (de mémoire) ; fichier tendanciel 1981-2017 GESIS ZA7503, accès libre. La seule
source qui remonte avant 1988 avec des items stables, au prix d'un pas de neuf ans.

**ISSP.** France membre depuis 1996 (de mémoire). Modules pertinents : *Role of Government* 1996, 2006,
2016 (axe économique, vérifié) ; *Social Inequality* 1999, 2009, 2019 ; *National Identity* 2003,
2013, 2023 ; *Citizenship* 2004, 2014, 2023. Vote ou préférence partisane dans le bloc démographique
commun. GESIS, accès libre.

**CSES.** Composantes françaises 2002, 2007, 2012, 2017, 2022 (modules 2 à 6 ; 2012 dans le module 4
vérifié). Vote, gauche-droite, quelques items d'enjeux selon le module. GESIS, accès libre.

**European Election Studies.** Études d'électeurs 1989, 1994, 1999, 2004, 2009, 2014, 2019, 2024,
France incluse (vérifié) ; vote européen et vote national précédent, gauche-droite, attitudes
générales. GESIS.

## 4. Très grand N, échantillon auto-sélectionné

**La Boussole présidentielle** (CEVIPOF avec Kieskompas / VU Amsterdam ; 2012, 2017, 2022). Plus d'un
million d'utilisateurs en 2017 (vérifié). Chaque utilisateur répond à une trentaine d'items d'enjeux
et est positionné dans un espace à deux dimensions — c'est littéralement le graphique cible, avec
l'intention de vote. Les données ont été exploitées en recherche (Vitiello & Krouwel, *Revue
internationale de politique comparée* 2015 ; Vitiello, Jadot, Krouwel & Lefébure sur 2012). Accès
par convention avec le CEVIPOF, pas de dépôt public trouvé. Échantillon auto-sélectionné : à
repondérer sur une enquête probabiliste avant tout usage descriptif.

## 5. Compléments

- **Baromètre de la confiance politique** (CEVIPOF / OpinionWay, annuel depuis 2009, ≈ 3 000 en
  France en 2026, vérifié) : attitudes et intentions de vote ; diffusion des microdonnées non
  documentée, à demander au CEVIPOF.
- **Fractures françaises** (Ipsos pour Fondation Jean-Jaurès, Le Monde, Institut Montaigne,
  CEVIPOF ; annuel depuis 2013 ; N = 3 000, quotas, vérifié) : valeurs, immigration, économie, vote ;
  seuls les rapports sont publics.
- **Baromètre d'opinion de la DREES** (annuel depuis 2000 sauf 2003, ≥ 3 000 face-à-face, vérifié) :
  redistribution, protection sociale, inégalités — bon pour l'axe économique ; microdonnées en open
  data pour les vagues récentes, Progedo pour les anciennes ; présence d'un vote ou d'un
  positionnement gauche-droite non vérifiée.
- **Eurobaromètre** : auto-positionnement gauche-droite depuis 1973, mais items d'enjeux instables et
  vote irrégulier — utile en appoint seulement.

## 6. L'offre : positions des partis dans les deux dimensions

- **Chapel Hill Expert Survey**, fichier tendanciel 1999, 2002, 2006, 2010, 2014, 2019, 2024 (vérifié),
  téléchargement libre sur chesdata.eu. Variables `lrecon` (gauche-droite économique, 0-10) et
  `galtan` (libertaire-autoritaire, 0-10) — les deux axes du projet, mais dans l'espace des experts,
  pas dans celui des électeurs.
- **Manifesto Project (MARPOR)** : toutes les élections françaises depuis 1946, catégories agrégeables
  en deux dimensions.
- **Positions perçues** : les panels ENEF et les FES demandent aux répondants de placer les candidats
  sur les mêmes échelles qu'eux-mêmes. C'est la source à préférer : elle met l'offre dans l'espace
  où le vote se décide, et elle est déjà commensurable avec les électeurs.

## 7. Chemin recommandé

1. **ESS, 2002-2024.** Onze cartes à items strictement identiques, échantillon probabiliste, accès
   immédiat. C'est la version réelle des figures 2, 3 et 9 sur vingt ans, sans hypothèse de
   raccordement. Commencer par là.
2. **ENEF 2017 et ENEF 2024** (ouverts) pour deux cartes à très haute résolution (plus de 10 000
   points), avec les positions perçues des candidats — la version réelle des figures 10-11 et de
   l'estimation du modèle de choix.
3. **Post-électorales CEVIPOF 1988 → 2012** via le CDSP pour remonter à 1988 avec les items de
   Grunberg-Schweisguth, en passant d'abord par la banque de questions harmonisée pour fixer la liste
   des items présents à toutes les dates.
4. **EVS** pour les points 1981, 1990, 1999, comme repères isolés.
5. **CHES** pour confronter positions perçues et positions d'experts.
6. **Boussole présidentielle** si une convention est possible : le grand N permet d'estimer finement
   les bassins et les zones vacantes de 2012, 2017 et 2022.

## 8. Les points durs, dans l'ordre

1. **Comparabilité des items.** Le problème numéro un, identique à celui rencontré sur PISA. Un axe
   construit sur des items qui changent d'une vague à l'autre déplace les électeurs sans qu'ils aient
   bougé. La règle : fixer la liste d'items commune avant de regarder les données, tester l'invariance
   de mesure, et ne pas fusionner ESS et CEVIPOF dans un même axe.
2. **Échantillonnage.** La plupart des enquêtes CEVIPOF sont par quotas (sauf 1988 et 2012) ; les
   panels Ipsos sont des access panels en ligne ; l'ESS et ELIPSS sont probabilistes. Les niveaux
   absolus d'attitudes ne sont pas comparables entre ces familles, les structures internes le sont
   davantage.
3. **Échelles discrètes.** Auto-positionnements à 5, 7 ou 11 modalités : jitter obligatoire pour le
   nuage, lissage pour la densité (figure 12).
4. **L'offre dans l'espace des électeurs.** Préférer les positions perçues ; CHES en contrôle.
5. **Accès.** CDSP : inscription, fichiers restreints sur demande (Progedo-Quetelet). GESIS :
   inscription gratuite. ESS : inscription gratuite. Boussole : convention.
