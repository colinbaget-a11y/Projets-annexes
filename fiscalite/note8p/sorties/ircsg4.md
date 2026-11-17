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
double compte [H argumentée]. **Recette à tenir** : 231,5 (cible v3) + 3,7 + 2,7 − 3,3 − 6,7 (financement net de l'ASPA) = **228,0 Md€**.

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

## 4. Barème final « bas et milieu » : 7,0 Md€ de financement externe [C]/[S]

Étape 1 (version à 5,5 Md€) : recette disponible −3,2 Md€ et frais réels +5,1 Md€ → +0,65 point uniforme. Étape 2
(arbitrage de l'assembleur, CIR supprimé) : 7,0 Md€ en croisière, paliers 1,5 (2029-2034), 2,5 (2035-2037), 4,5 (2038),
6,0 (2039), 7,0 (2040) ; ASPA nette 0,3 ; le reste (1,2 Md€ de plus que la version à 5,5) baisse les taux aux repères
0 à 3,5 Smic (poids 1/1/1/1/0,5, −0,10 point ; autres pondérations : mêmes résultats à 0,1 point près). **Barème final :
2,0 / 16,0 / 23,0 / 29,3 / 37,0 % aux points 0 / 1 / 1,5 / 2 / 3,5 Smic, 48 % dès 163 400 €.**

**Progressivité, dite honnêtement** : écart de taux moyen Smic–200 k€ **28,0 points, contre 26,8 aujourd'hui** : le nouvel
impôt est à peu près aussi progressif que le droit actuel (un peu plus jusqu'à 200 k€, moins au-delà). Le réduire
exigeait de baisser l'impôt au-dessus de 2 Smic : reculer le point haut à 229 000 € (6,7 Md€) ne gagnait que 1,7 point,
au profit du dixième le plus aisé ; 24 points coûteraient 9 Md€. Écarté (coût d'opportunité). Barème de chaque année :
impôt = (1 − k) × barème à recette constante (+1,07 point) + k × barème final (`annuel_final`, `bareme_points`,
`bareme_taux`).

## 5. Cas-types nets des niches [S] (OpenFisca 176.1, droit 2025 ; € par mois ; − = paie moins)

| Situation | Payé auj. (€/an) | Système | Niches | **Net** |
|---|---|---|---|---|
| Smic + 10 % d'heures sup. | 2 267 | −23 | +4 | **−18** |
| Smic sans HS | 2 061 | −28 | 0 | **−28** |
| Salarié 40 k€ brut | 5 779 | −40 | 0 | **−40** |
| Julie, 2 000 € net | 3 714 | −44 | 0 | **−44** |
| Biactifs 36+24 k€, 2 enfants gardés (assistante maternelle) | 2 250 | −151 | +292 | **+140** |
| Le même + aide à domicile 3 000 € | 750 | −151 | +417 | **+265** |
| Le même sans niche | 5 750 | −151 | 0 | **−151** |
| Parent isolé au Smic, enfant gardé (crédit restitué) | 811 | −97 | +104 | **+7** |
| Famille nombreuse 40+25 k€, 3 enfants | 6 195 | −207 | 0 | **−207** |
| Couple mono-actif 45 k€, 2 enfants | 4 289 | −74 | 0 | **−74** |
| Le même, conjoint à mi-temps au Smic | 5 319 | −115 | 0 | **−115** |
| Retraité seul 14 000 € | 0 | +83 | 0 | **+83** |
| Retraitée 30 000 €, aide à domicile 4 000 € | 1 287 | +50 | +167 | **+217** |
| Cadres 90+60 k€, dons, emploi à domicile, Pinel (gardé) | 21 846 | −284 | +365 | **+81** |

**Julie** (+200 € net par mois, soit +224 € après cotisations) garde 170 € aujourd'hui, **173 € demain** (prélèvement
sur le supplément 24 → 23 %) : à ce niveau (1,45 Smic), le barème continu ne change presque rien ; l'exemple de la note
ne doit plus annoncer un gain marginal. **Exemple honnête retenu** : un salarié seul qui passe de 2 à 3 Smic (3 600 → 5 400 € brut/mois,
+1 608 € après cotisations) en garde 1 035 € aujourd'hui, **1 096 € demain** (35,7 → 31,9 % prélevés) ; de 1,5 à 2 Smic,
579 → 590 € (27,5 → 26,2 %). Second conjoint à mi-temps : 9,5 → 4,9 % de son salaire.

## 6. Moyennes par catégorie [S] (€ par foyer et par an : système / niches / net)

Actifs −1 213 / +503 / **−710** ; retraités +422 / +445 / **+867** ; actifs seuls −672 net ; couples avec 1, 2, 3+
enfants −511, −1 127, −1 253 ; couples à un seul revenu **+2 018** ; parents isolés −726 ; retraités seuls +590 ;
couples de retraités +1 657. Déciles (net) : +37, +19, −7, −217, −214, −319, −395, −553, −502, **+528** ; perte des
niches de 90 € (D1) à 1 938 € (D10). L'ASPA (dépense) n'est pas dans ces moyennes. Bénéficiaires (montant moyen par bénéficiaire, sans supposer l'indépendance des
recours ; autres niches non ajoutées) : actifs du D5 employant un salarié à domicile +277 ; retraités du D5 qui en
emploient +2 037 ; familles du D5 avec garde −976 ; Girardin +13 000 à +16 000. **Part de gagnants et perdants : non
publiée** (distribution jointe niches × revenu × famille inconnue ; foyers types dans le modèle).

## 7. Minimum vieillesse [E]/[S]

ASPA différentielle, exonérée d'IR (CGI art. 81, 9° ; BOFiP), plafond 12 411 € (2025), pensions retenues en brut
(service-public.gouv.fr ; OpenFisca). Sans correction, une pension au niveau de l'ASPA paierait 813 €/an (68 €/mois).
**Règle retenue : ASPA calculée sur la pension nette du nouvel impôt** → revenu des allocataires inchangé jusqu'au
plafond ; à 13 000 € la hausse passe de 879 à 589 € ; au-delà de ≈ 13 300 € elle demeure (14 000 € : +998 €).
**Coût : 0,30 Md€ (0,27–0,38)** : 752 800 allocataires fin 2024 (DREES, Minima sociaux, éd. 2025, fiche 28 — vérifié),
pension supposée uniforme sous le plafond [H ; pension de droit direct moyenne 510 €/mois, DREES] → 0,24 ; nouveaux
éligibles 0,11 à plein recours, moitié au central (non-recours de 50 % des personnes seules, DREES). **Dépense sociale
(FSV), hors périmètre fiscal**, imputée sur l'enveloppe du bloc, dès 2029.

## 8. Efficacité, taux [S]

**Gain d'efficacité statique lié à la modification des incitations fiscales au travail, hors effets comportementaux
propres aux dispositifs supprimés : 3,0 Md€ par an (1,3-6,3)**, dont heures 0,70, participation 2,3 ;
≈ 245 000 ETP (100 000-500 000). Non chiffrés : heures supplémentaires (prix net d'une heure en baisse pour les
imposables), garde (coût net en hausse pour les parents qui travaillent, surtout les mères de jeunes enfants), emploi
déclaré à domicile (retour possible au travail dissimulé ; CPO : un taux de 40 % suffirait à le contenir), dons.
**Taux marginal ≤ 48 % partout** (≤ 50 % vérifié). Il monte de 0,6 à 1,07 Smic (Smic 10,7 → 16,0 %), entre 1,54 et
1,83 Smic, de 62 000 à 101 000 € et de 134 000 à 157 000 € ; il baisse à l'entrée dans l'IR (1,1 Smic 23,7 → 17,4 %)
et le taux moyen baisse (Smic 10,7 → 9,1 %) : arbitrage assumé en faveur de l'entrée en emploi. **Progressivité** : voir § 4 (28,0 points contre 26,8 ; taux effectifs niches comprises D1 4,6 → 6,5 %, D5 10,3 →
9,5, D9 15,5 → 14,7, D10 21,9 → 22,3 ; 400 k€ : 45,5 → 42,5 %).

## 9. Trajectoire (`annuel_final`) et passages de `note.tex` à corriger

λ = 0,25-1 (2027-2030) ; financement 0 (2027-2028), 1,5 (2029-2034), 2,5 (2035-2037), 4,5, 6,0, 7,0 (2040) ; total =
−financement chaque année (dont ASPA −0,3 dès 2029, ×λ) ; croisière : actifs −18,7 Md€, retraités +12,6, CEHR −0,6,
ASPA −0,3. Niches : 4,9 Md€ (2027) → 20,1 (2030) ; reports Girardin/PME 0,1 Md€/an 2027-2029, couverts par le barème.

`note.tex`, section « Travailler davantage » : taux « 1,5 / 15,5 / 22,5 / 28,7 / 36,4 %, 48 % à partir de 163 000 € » →
2,0 / 16,0 / 23,0 / 29,3 / 37,0 %, 48 % dès 163 400 € ; « plus élevé… entre 67 000 et 100 000 € » → 62 000-101 000 € et 134 000-157 000 € ;
« 112 Md€ » et titre de g11 → vraies niches 20 Md€ ; « frais réels restent déductibles » : ajouter qu'ils doublent (coût
5 Md€) ; Julie « 24 % » → remplacer par la progression 2 → 3 Smic (garde 1 035 € aujourd'hui, 1 096 € demain sur
+1 608 €/mois ; 35,7 → 31,9 %) ; retraités « 11,9 Md€ » → 12,6 ; « 16 000 € : 1 170 € » → 1 258 € ; « 12 000 € : 700 € »
→ 768 € ; « protégées… par le minimum vieillesse » → ASPA calculée sur la pension nette (0,3 Md€) ; « 1 500 € à
100 000 € » à recalculer (g3b) ; Karim « 11,5 → 4,4 % » → avec deux enfants 9,5 → 4,9 % ; Smic « 36 € » → 28 € ; 2 000 €
net « 57 € » → 44 € ; 3 Smic « 145 € » à reprendre ; couple biactif « 170 € » → 151 € ; « perd 101 € » → +140 € (garde),
+265 € (garde et aide) ; parent isolé 147 € → 7 € de gain net s'il fait garder son enfant ; cadre 120 k€ « 86 € » à
reprendre ; dixième supérieur « 4,4 Md€ de plus » → net +528 €/foyer ; « 5,5 Md€ issus de la taxe foncière et des niches
de l'IS » → 7,0 Md€ (dont CIR) ; perte sèche « 2,8 (1,2-6,1) » → 3,0 (1,3-6,3) ; ajouter : progressivité à peu près celle d'aujourd'hui (28,0 contre 26,8 points).

## Titres-messages proposés

- g1 « Le taux moyen baisse à tous les niveaux de salaire et reste aussi progressif qu'aujourd'hui »
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
