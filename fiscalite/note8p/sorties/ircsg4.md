# Bloc IR-CSG-CRDS, v4 : ce que rapportent vraiment les niches, et qui y gagne net

Compte rendu pour l'assembleur (révision finale v4, 19/11/2026). Chiffres : `sorties/ircsg4.json`, `sorties/ircsg4_calculs.txt`.
Scripts (depuis `fiscalite/`) : `note8p/calculs/ircsg4_donnees.py` (données CPO, DGFiP, Voies et moyens ; tableau par
dispositif), `ircsg4_frais.py` (frais professionnels), `ircsg4_modele.py` (décomposition du résidu, recette à tenir,
barème, distribution, efficacité, trajectoire), `python3.13 ircsg4_openfisca.py` (cas-types avec niches),
`ircsg4_cas.py` (cas nets, Julie, ASPA, `tab_cas_types.tex`), `ircsg4_figures.py` (g1, g2, g3, g3b, g11). Les scripts
v3 sont réutilisés sans modification. Statuts : [E] empirique, [S] simulation, [H] hypothèse, [C] choix.

## 1. Les données sur les niches (vérifiées)

Sources lues : CPO, *L'impôt sur le revenu, ses réductions et crédits d'impôt depuis 2017*, septembre 2026 (étude
pour la commission des finances de l'AN, 418 p., POTE 2024 ; PDF vie-publique.fr n° 304837 ; les graphiques des fiches
de l'annexe 4 ont été lus sur les pages en image) ; DGFiP Statistiques n° 41, novembre 2025 (PDF et classeur) ; Voies
et moyens t. II PLF 2026 (coût 2025). Le tome II du PLF 2027 n'a pas été trouvé sur les sites accessibles.

- [E] **12,8 M de foyers (30,9 %)** ont bénéficié d'une réduction ou d'un crédit en 2024, **1 520 € en moyenne**
  (« 1 500 € », DGFiP) : les deux ordres de grandeur supposés sont confirmés. 19,5 Md€ au total, dont 3,8 Md€ de
  réduction pour revenus de source étrangère (double imposition). Hors celle-ci : 15 Md€ (réductions 6,1, crédits 8,9 ;
  CPO). 14,3 M de foyers (34 %) remplissent une case ; 2/3 des 12,5 M de bénéficiaires effectifs ont moins de 1 000 € ;
  environ 200 foyers dépassent 100 000 €.
- [E] **45 % des crédits (4 Md€) vont à des non-imposés, dont 2 Md€ restitués** (DGFiP).
- [E] Répartition (CPO, tableau 15, groupes de revenu fiscal par part) : réductions 0,1 / 22,1 / 18,9 / 44,0 / 14,9 %
  (C01-40 / 41-80 / 81-90 / 91-99 / 100) ; crédits 19,1 / 33,5 / 14,2 / 25,7 / 7,4 % ; double imposition 89 % au dixième
  supérieur. Dixième le plus aisé : 54 % des RICI y compris revenus étrangers (DGFiP), 44 % hors (CPO). Les classes
  moyennes (C41-C80) ont 41 % des réductions pour 29 % de l'impôt avant RICI.
- [E] Par dispositif (CPO, fiches) : emploi à domicile 6,5 Md€, 5,1 M, coût 16/30/15/30/9 % ; dons 2,2, 4,9 M,
  0/29/21/37/13 ; garde 1,8, 1,9 M, 26/49/12/12/1 ; Pinel-Duflot 1,6, 0,39 M, 0/11/22/57/10 (coût jusqu'en 2036) ;
  Girardin 0,8, 59 000, 13 200 € en moyenne, 0/1/5/52/41 ; scolarité 0,47, 2,6 M ; dépendance 0,31. Les fiches donnent
  aussi les parts par âge, dont on déduit le partage actifs / plus de 65 ans (emploi à domicile 55 % aux 65 ans et plus ;
  dons 44 %). Cumuls (tableau 21) : 9,3 M de foyers n'utilisent qu'un dispositif ; dons + emploi à domicile 1,19 M ;
  emploi à domicile + garde 0,18 M ; 1,29 M en utilisent trois ou plus.

Tableau de travail par dispositif (coût, bénéficiaires, classement, traitement, part supprimable, profil, recette) :
`tableau_dispositifs` du json et annexe, tableau B.2. Classement : vraie niche (emploi à domicile, Girardin, DOM, PME,
heures supplémentaires, épargne salariale, demi-parts…), mesure du revenu (garde, syndicales, travaux fonciers),
externalité (dons), double imposition / conventions (revenus étrangers, non supprimable), gardé (invalidité, dépendance),
hors assiette sociale (titres-restaurant, apprentis).

## 2. Le résidu de 27,1 Md€ remplacé par une recette par dispositif [S]

**Recette des niches supprimées : 20,1 Md€ en régime de croisière** (statique) : 16,8 Md€ dans l'écart modèle
(emploi à domicile 7,0 ; dons 2,2 ; heures supplémentaires 2,2 ; garde 1,8 ; demi-parts 1,3 ; Girardin 0,9 ; scolarité
0,45 ; DOM 0,43 ; PME 0,16 ; divers 0,4) et 3,3 Md€ de revenus aujourd'hui exonérés que le modèle ne voit pas (épargne
salariale 2,5 après 15 % de report vers l'épargne retraite [H] ; IJ 0,6 ; impatriés 0,2). Pinel : 0 (engagements
honorés ; le droit actuel les éteint déjà). Montée : 19,7 Md€ la 1re année avant λ (reports Girardin, PME).

**Le résidu se décompose ainsi** (Md€) : frais réels au-delà du forfait 2,7 ; niches supprimées 16,8 ; invalidité-
dépendance gardées 1,0 ; revenus étrangers (moitié) + Pinel + divers non supprimés 3,7 ; **écart inexpliqué 2,7**. Le
modèle mettait 49 % du résidu au dixième supérieur ; les niches supprimées n'y sont qu'à 41 % (6,9 Md€), comme dans les
données. Le surplus du haut vient des revenus étrangers (non supprimables) et de l'écart inexpliqué (82 % au dixième
supérieur : représentation des très hauts revenus, partage barème/PFU, salaires de source étrangère hors modèle). Rien
de cet écart n'est compté comme recette.

**IR non attribué (4,0 Md€).** S'il relève en partie du barème, l'impôt observé du haut est sous-estimé et l'écart
inexpliqué surestimé d'autant : retirer l'écart inexpliqué de la recette couvre déjà cette hypothèse prudente, sans
double compte [H argumentée]. **Recette à tenir** : 231,5 (cible v3) + 3,7 + 2,7 − 3,3 − 5,5 = **229,2 Md€**.

## 3. Forfait de 10 % [H calée sur E]

Modèle de frais : distance aller médiane 8 km (Insee Première n° 1948), voiture 74 % (n° 1835), barème kilométrique
5 CV 2024, 205 jours, repas pour 25 % des salariés ; dispersion et seuil de gain calés sur les 5,87 M de déclarants et
36,1 Md€ de frais réels (2025). Le forfait vaut aujourd'hui environ 73 Md€ de déductions.

| Option | Déductions | Déclarants | Coût vs v3 |
|---|---|---|---|
| (a) suppression, frais réels gardés | 65 Md€ | 18,0 M | 5,1 Md€ (3,6 si recours deux fois moins élastique) |
| (b) forfait fixe 500 € | 71 | 15,0 M | 6,1 |
| (b) forfait fixe 1 000 € | 79 | 12,1 M | 7,4 |
| (b) 5 % plafonné à 2 000 € | 79 | 11,1 M | 8,3 |
| variante : frais réels au-delà d'une franchise de 1 000 € | 44 | 12,1 M | 0,6 |

**Recommandation [C] : (a).** La v3 supposait les frais réels inchangés (36 Md€) : sans forfait, tout automobiliste y a
intérêt ; la déclaration presque double. Un petit forfait coûte 300 à 460 € de recette par déclaration évitée : cher
payé. (a) n'a aucun paramètre et taxe le revenu net de ses coûts. Coût de conformité réel (18 M de déclarations) :
préremplir la distance domicile-travail. La franchise de 1 000 € est l'option la moins chère mais pénalise les longs
trajets (160 à 400 € par an) : à l'appréciation de l'auteur.

## 4. Barème recalé [C]/[S]

La recette disponible baisse de 3,2 Md€ (correction du résidu nette des recettes hors modèle) et les frais réels coûtent
5,1 Md€ : **ajustement uniforme de +0,65 point** des cinq premiers taux, forme et repères inchangés. **Barème final :
2,1 / 16,1 / 23,1 / 29,4 / 37,0 % aux points 0 / 1 / 1,5 / 2 / 3,5 Smic, 48 % dès 163 400 €.** (Sans financement
externe : +1,07 point.) Un ajustement ciblé sur 1,5-3,5 Smic exigerait +2,4 points au milieu et ruinerait le gain sur les
heures : écarté.

## 5. Cas-types nets des niches [S] (OpenFisca 176.1, droit 2025 ; € par mois ; − = paie moins)

| Situation | Payé auj. (€/an) | Système | Niches | **Net** |
|---|---|---|---|---|
| Smic + 10 % d'heures sup. | 2 267 | −21 | +4 | **−16** |
| Smic sans HS | 2 061 | −26 | 0 | **−26** |
| Salarié 40 k€ brut | 5 779 | −38 | 0 | **−38** |
| Julie, 2 000 € net | 3 714 | −42 | 0 | **−42** |
| Biactifs 36+24 k€, 2 enfants gardés (assistante maternelle) | 2 250 | −148 | +292 | **+144** |
| Le même + aide à domicile 3 000 € | 750 | −148 | +417 | **+269** |
| Le même sans niche | 5 750 | −148 | 0 | **−148** |
| Parent isolé au Smic, enfant gardé (crédit restitué) | 811 | −96 | +104 | **+9** |
| Famille nombreuse 40+25 k€, 3 enfants | 6 195 | −204 | 0 | **−204** |
| Couple mono-actif 45 k€, 2 enfants | 4 289 | −71 | 0 | **−71** |
| Le même, conjoint à mi-temps au Smic | 5 319 | −112 | 0 | **−112** |
| Retraité seul 14 000 € | 0 | +84 | 0 | **+84** |
| Retraitée 30 000 €, aide à domicile 4 000 € | 1 287 | +53 | +167 | **+219** |
| Cadres 90+60 k€, dons, emploi à domicile, Pinel (gardé) | 21 846 | −275 | +365 | **+90** |

**Julie** (+200 € net par mois, soit +224 € après cotisations) garde 170 € aujourd'hui, **173 € demain** (prélèvement
sur le supplément 24 → 23 %) : à ce niveau (1,45 Smic), le barème continu ne change presque rien ; l'exemple de la note
ne doit plus annoncer un gain marginal. Second conjoint à mi-temps : 9,5 → 5,0 % de son salaire.

## 6. Moyennes par catégorie [S] (€ par foyer et par an : système / niches / net)

Actifs −1 183 / +503 / **−680** ; retraités +449 / +445 / **+894** ; actifs seuls −649 net ; couples avec 1, 2, 3+
enfants −464, −1 086, −1 217 ; couples à un seul revenu **+2 057** ; parents isolés −711 ; retraités seuls +611 ;
couples de retraités +1 703. Déciles (net) : +39, +25, +7, −199, −193, −294, −364, −513, −452, **+609** ; perte des
niches de 90 € (D1) à 1 938 € (D10). Bénéficiaires (montant moyen par bénéficiaire, sans supposer l'indépendance des
recours ; autres niches non ajoutées) : actifs du D5 employant un salarié à domicile +277 ; retraités du D5 qui en
emploient +2 037 ; familles du D5 avec garde −976 ; Girardin +13 000 à +16 000. **Part de gagnants et perdants : non
publiée** (distribution jointe niches × revenu × famille inconnue ; foyers types dans le modèle).

## 7. Minimum vieillesse [E]/[S]

ASPA différentielle, exonérée d'IR (CGI art. 81, 9° ; BOFiP), plafond 12 411 € (2025), pensions retenues **en brut**
(service-public.gouv.fr ; OpenFisca) ; CSG sur l'ASPA non vérifiée sur texte. Une pension au niveau de l'ASPA ne paie
rien aujourd'hui ; demain **825 € par an (69 €/mois)** ; une pension de 8 000 € + 4 411 € d'ASPA paie 403 €, non
compensés. **Le texte ne doit pas dire que le minimum vieillesse protège les petites pensions.** Option : ASPA calculée
sur la pension nette du nouvel impôt (revenu des allocataires inchangé ; coût ≤ 825 € par allocataire, national non
chiffré faute de nombre vérifié) ; les pensions de 13 000 à 16 000 € paieraient encore 600 à 1 270 € de plus.

## 8. Efficacité, taux [S]

**Gain d'efficacité statique lié à la modification des incitations fiscales au travail, hors effets comportementaux
propres aux dispositifs supprimés : 2,9 Md€ par an (1,25-6,2)**, dont heures 0,65, participation 2,2 ; travail +0,9 %,
≈ 240 000 ETP (100 000-490 000). Non chiffrés : heures supplémentaires (prix net d'une heure en baisse pour les
imposables), garde (coût net en hausse pour les parents qui travaillent, surtout les mères de jeunes enfants), emploi
déclaré à domicile (retour possible au travail dissimulé ; CPO : un taux de 40 % suffirait à le contenir), dons.
**Taux marginal ≤ 48 % partout** (≤ 50 % vérifié). Il monte de 0,6 à 1,07 Smic (Smic 10,7 → 16,0 %), entre 1,54 et
1,83 Smic, de 62 000 à 101 000 € et de 134 000 à 157 000 € ; il baisse à l'entrée dans l'IR (1,1 Smic 23,7 → 17,4 %)
et le taux moyen baisse (Smic 10,7 → 9,1 %) : arbitrage assumé en faveur de l'entrée en emploi. **Progressivité : la
condition « taux moyens nettement moins progressifs que l'IR actuel » n'est pas remplie** : écart de taux moyen
Smic-200 k€ 26,8 → 28,0 points ; taux effectifs niches comprises D1 4,6 → 6,5 %, D5 10,3 → 9,5, D9 15,5 → 14,8,
D10 21,9 → 22,4. Moins progressif seulement au-delà de 200 000 €. Pour l'obtenir, il faudrait relever le bas ou baisser
le haut du barème : choix de l'auteur.

## 9. Trajectoire (`annuel_final`) et ce que l'assembleur doit changer

Fusion λ = 0,25-1 (2027-2030) ; financement 0 jusqu'en 2031 puis 1-5,5 Md€ (2032-2037) : total = −financement chaque
année ; croisière : actifs −17,9 Md€, retraités +13,0, CEHR −0,6. Recette des niches 4,9 Md€ (2027) → 20,1 (2030) ;
reports Girardin/PME : 0,1 Md€ par an de 2027 à 2029, couverts par le barème transitoire.

Dans `note.tex` (section « Travailler davantage ») devenus faux : les taux 1,5/15,5/22,5/28,7/36,4 ; « 112 Md€
d'élargissement » et le titre de g11 ; « frais réels gardés » sans hausse ; Smic −36 €/mois (→ −26) ; 2 000 € net −57
(→ −42) ; 3 Smic −145 ; couple biactif −170 ; « perd 101 € » (→ +144 avec garde, +269 avec garde et aide) ; Julie 24 %
(→ elle garde presque autant demain) ; retraités +11,9 Md€ (→ +13,0) ; 16 000 € +1 170 € ; « protégées par… le minimum
vieillesse » ; perte sèche 2,8 (1,2-6,1) (→ 2,9 ; 1,25-6,2) ; Karim 11,5 → 4,4 % (cas sans enfant ; avec deux enfants
9,5 → 5,0 %). Les retraités et couples à un revenu de la figure g3 v3 ne sont plus dans g3 v4 (voir g3b, tableau).

## Titres-messages proposés

- g1 « Le taux moyen baisse au Smic et au milieu, et reste aussi progressif qu'aujourd'hui »
- g2 « Le taux marginal monte en ligne droite, sans marche, et ne dépasse jamais 48 % »
- g3 « Hors niches, les actifs gagnent ; les familles qui font garder leurs enfants et les utilisateurs de niches
  perdent »
- g3b « Les salariés gagnent à tous les niveaux ; les petites pensions paient plus »
- g11 « Les vraies niches rapportent 20 milliards ; l'essentiel de la baisse des taux vient de la fusion elle-même »

Sources : [CPO, sept. 2026](https://www.vie-publique.fr/files/rapport/pdf/304837.pdf) ;
[DGFiP Statistiques n° 41](https://www.impots.gouv.fr/sites/default/files/media/9_statistiques/0_etudes_et_stats/0_publications/dgfip_statistiques/2025/num41_11/dgfip_stat_41.pdf) ;
[Voies et moyens t. II PLF 2026](https://www.assemblee-nationale.fr/dyn/dyn/contenu/visualisation/1087933/file/Voies_et_moyens_Tome_2_2026.pdf) ;
[Insee Première n° 1948](https://www.insee.fr/fr/statistiques/fichier/version-html/7622203/ip1948.pdf) ;
[barème kilométrique 2024](https://www.legifiscal.fr/actualites-fiscales/4094-ir-revalorisation-2025-bareme-indemnites-kilometriques.html) ;
[ASPA, service-public.gouv.fr](https://www.service-public.gouv.fr/particuliers/vosdroits/F16871) ;
[BOFiP, ASPA exonérée](https://bofip.impots.gouv.fr/node/6142).
