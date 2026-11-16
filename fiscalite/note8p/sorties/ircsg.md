# Bloc IR-CSG-CRDS : un nouvel impôt sur le revenu, individuel, à quatre taux

Compte rendu pour l'assembleur (17/11/2026). Chiffres : `sorties/ircsg.json` et `sorties/ircsg_calculs.txt`. Scripts :
`calculs/ircsg_openfisca.py` (python3.13, droit actuel), `ircsg_modele.py` (noyau), `ircsg_explore.py` (balayage),
`ircsg_affinage.py` (barèmes ronds), `ircsg_proposition.py` (tout le reste), `ircsg_figures.py`, `ircsg_annexe.py`. Base : prélèvements de 2025, répartition de l'IRCOM des
revenus 2024 portée en 2025 (`synthese/modele_purs.py`), droit des revenus 2025 dans OpenFisca-France 176.1.
Statuts : [E] empirique publié, [S] simulation, [H] hypothèse, [C] choix.

## 1. Ce qui est proposé [C]

**Assiette.** Le revenu après cotisations sociales de chaque adulte : salaire brut moins cotisations salariales (avant
CSG), pension brute, allocations chômage, bénéfices des indépendants et revenus fonciers nets de cotisations. Les
revenus du capital mobilier et les plus-values restent au PFU (bloc capital), option pour le barème comprise. Les
versements d'épargne retraite restent déductibles dans les plafonds actuels (sinon la même épargne serait taxée deux
fois). Toutes les autres niches de l'IR du périmètre disparaissent, sauf celles liées à l'invalidité et à la dépendance
(demi-part des invalides, personnes à charge invalides, frais d'hébergement en établissement : 1,03 Md€, maintenus).

**Barème, individuel, le même pour tous les revenus** :

| Revenu après cotisations (par adulte) | Taux marginal |
|---|---|
| jusqu'à 12 000 € | 5 % |
| de 12 000 à 36 500 € | 20 % |
| de 36 500 à 120 000 € | 28 % |
| au-delà de 120 000 € | 45 % |

Quatre taux, trois seuils, aucune décote, aucun abattement, aucune règle de seuil appliquée à tout le revenu : l'impôt
et le revenu disponible sont continus partout. Le seuil de 36 500 € (calage exact : 36 472 €) est le seul paramètre
calé sur la recette. Le taux d'entrée de 5 % plutôt qu'un seuil d'exonération : à recette égale, un seuil de 10 000 €
à 0 % oblige à relever les taux de 20 et 28 % d'environ 1,3 point et fait perdre 0,7 Md€ de gain d'efficacité ; il
protège un peu mieux les très petits revenus (variante en annexe).

**Taux maximal : 45 %**, sur le revenu après cotisations, tous prélèvements personnels fusionnés compris (CSG, CRDS,
IR, CEHR ; un retraité paie en plus 0,3 point de CASA, hors périmètre). Il pourrait être de 40 % (gain +0,2 Md€, taux de 20/28 relevés de 0,3 point, 1 % le plus aisé −3,9 Md€) ;
nous gardons 45 % pour une progressivité réelle au sommet.

**Enfants : franchise de 6 000 € par enfant**, déduite du revenu imposable, même montant pour chaque enfant. Les
parents choisissent qui la déduit ; par défaut, le parent au revenu le plus élevé. Avec des taux croissants, c'est
aussi le choix qui minimise l'impôt du couple, et il ne touche jamais au taux du second apporteur de revenu, dont le
premier euro reste taxé à 5 %. Une règle « par moitié, reste transférable » ferait au contraire perdre au premier
parent une partie de la franchise à chaque euro gagné par le second : elle recréerait la désincitation. Parents
séparés : celui qui a l'enfant à charge ; résidence alternée : moitié chacun.

**Couples : impôt individuel.** Règles anti-transfert : salaire versé au conjoint déductible seulement au prix du marché
et pour un travail réel ; revenus des biens communs ou indivis partagés par moitié ; revenu d'une entreprise familiale
attribué à un proche qui n'y travaille pas imposé au taux de celui qui la contrôle (règle canadienne dite « TOSI »,
2018, non relue sur le texte).

**Retraités : droit commun.** Fin de l'abattement de 10 % (5,32 Md€ en 2025), des taux réduits et exonérations de CSG
des pensions, de l'abattement de l'art. 157 bis pour les plus de 65 ans (0,42 Md€, maintenu pour les seuls invalides,
part non chiffrée) et de la demi-part des anciens combattants de plus de 74 ans (0,48 Md€) (coûts : PLF 2026,
Voies et moyens t. II). Aucune franchise propre aux pensions : les petites pensions ne sont protégées que par le
taux d'entrée et par le minimum vieillesse (non imposable, hors périmètre). La CASA (0,3 % sur les pensions) est hors
périmètre et reste, comme contrepartie de la contribution de solidarité pour l'autonomie des employeurs.

**CEHR et CDHR.** La CEHR disparaît sur les revenus du barème : le taux de 45 % les absorbe (0,58 Md€ sur 1,39, part
estimée au prorata des revenus du barème dans le RFR des tranches concernées [H] ; le bloc capital retient 0,3 à
0,7). Sur les revenus du capital, nous supposons (bloc capital) qu'elle devient une majoration du PFU et que la CDHR,
tant qu'elle existe, est calculée en comptant comme impôt sur le revenu le nouvel impôt diminué de 9,7 % des revenus
du barème : son produit (0,62 Md€, presque tout sur le capital) est inchangé. Droit en vigueur (vérifié) : la CDHR
dure jusqu'à l'année dont la loi de règlement constate un déficit du budget général sous 3 % du PIB (LF 2026, loi
n° 2026-103) ; la CEHR jusqu'à un déficit public nul (art. 223 sexies CGI, BOFiP).

## 2. Taux marginaux aujourd'hui, sur une assiette comparable [S]

Par 100 € de revenu après cotisations en plus, salarié seul, OpenFisca (grille de 100 € jusqu'à 700 000 €) :

| Revenu après cotisations | Aujourd'hui | dont IR | dont CSG + CRDS | Proposition |
|---|---|---|---|---|
| moins de 20 700 € | 10,7 % | 0 | 10,7 | 5 % puis 20 % dès 12 000 € |
| 20 700 à 35 500 € (1,1 à 1,85 Smic) | 23,7 % | 13,0 (11 % + décote) | 10,7 | 20 % |
| 35 500 à 101 600 € | 35,7 % | 25,0 | 10,7 | 20 puis 28 % |
| 101 600 à 157 000 € | 44,5 % | 34 | 10,6 | 28 puis 45 % dès 120 000 € |
| 157 000 à 212 000 € | 48-49 % | 37-38 | 10,6 | 45 % |
| 212 000 à 286 000 € | 52-53 % | 41 | 10,7 | 45 % |
| au-delà de 286 000 € (CEHR 3 %) | 54,8 % | 41 + 3 | 10,7 puis 9,7 | 45 % |
| au-delà d'environ 550 000 € (CEHR 4 %) | 55,7 % (max. 56,7 %) | 42 + 4 | 9,7 | 45 % |

Les taux nominaux ne s'additionnent pas : la CSG (9,2 %) et la CRDS (0,5 %) portent sur 98,25 % du brut (100 %
au-delà de 4 plafonds), soit 10,7 % du revenu après cotisations sous le plafond et jusqu'à 10,3 % entre 4 et 8 plafonds
(la CSG frappe aussi les cotisations) ; l'IR de 45 % porte sur le revenu imposable, net de 6,8 points de CSG
déductible : 41,6 % du revenu après cotisations. Au sommet, IR + CSG + CRDS = 52,4 %, plus 2,8 ou 3,7 points de CEHR.
La CDHR ne joue pas pour un salarié (son taux moyen dépasse 20 %). Un retraité seul ne paie rien jusqu'à 18 000 €
de pension, puis 100 € de plus lui coûtent jusqu'à 778 € au franchissement d'un seuil de CSG (taux de CSG de régime
stable, sans alternance artificielle), 20 % de 21 500 à 35 000 €, 33 à 37 % jusqu'à 94 500 €, 46,8 % au-delà.
Figure g2 : « Le taux marginal ne dépasse plus 45 %, contre 52 à 56 % aujourd'hui en haut ». Figure g1 (demi-largeur,
salarié seul) : « Aujourd'hui, un impôt très progressif s'ajoute à une contribution proportionnelle de 10,7 % ».

## 3. Recette, périmètre et réconciliation [E]/[S]

Recette à tenir : 229,9 Md€ (IR des revenus du barème 86,6, CSG 135,8 dont 108,5 sur l'activité, 26,7 sur les
pensions, 0,6 sur le chômage, CRDS 7,6 ; 2025) + CEHR du barème 0,58 + invalidité et dépendance 1,03 = 231,5 Md€.
Recette du barème : 231,50 (écart −0,03). Un point sur tous les taux : 14,0 Md€ ; sur 20 et 28 % : 8,3 ; sur 45 % :
0,42 ; 1 000 € de franchise par enfant : 3,1 Md€.

Réconciliation de l'IR : comptes nationaux 2025, 103,6 Md€ ; IRCOM porté en 2025, 99,0 (l'écart de 4,6 recouvre la
CEHR, le calendrier, les non-résidents) ; le modèle retire 12,4 Md€ d'IR « du capital » (12,8 % de 90 Md€), quand le
bloc capital mesure 8,4 Md€ d'IR au PFU. **4,0 Md€ restent non attribués** : IR des dividendes et intérêts imposés au
barème par option (qui reste au bloc capital dans notre périmètre) et erreur d'imputation. Si toute cette somme était
en fait de l'IR sur les revenus du barème, la recette à tenir monterait de 4,0 Md€, soit +0,3 point sur tous les taux
(+0,5 sur 20 et 28 %). Autre fragilité : l'IR encaissé en 2025 (+7,9 % en un an) est peut-être un point haut
(≈ 4,5 Md€).

## 4. Qui paie [S]

Les actifs paient 11,3 Md€ de moins (−416 € par foyer), les retraités 12,9 Md€ de plus (+889 € ; 3,1 % des pensions).
Le 1 % le plus aisé paie 2,2 Md€ de moins, le dixième le plus aisé 2,9 Md€ de moins (déciles en annexe : de −690 € au
dixième à +526 € au quatrième, où les retraités sont nombreux). 13,8 M de foyers paient plus de 500 € de plus, dont
9,4 M de retraités ; 9,3 M paient plus de 500 € de moins.

Ménages types (OpenFisca aujourd'hui ; € par an ; figure g3, « Les familles et les actifs paient moins ; les petites
pensions et les couples à un revenu paient plus ») :

| Ménage | Aujourd'hui | Après | Écart |
|---|---|---|---|
| Jeune salarié au Smic (21 622 € brut) | 2 061 | 2 035 | −25 |
| Salarié à 2 000 € net/mois (30 318 € brut) | 3 714 | 3 578 | −137 |
| Couple biactif, 2 enfants, 60 000 € (36 + 24 k€) | 5 750 | 4 643 | −1 107 |
| Famille mono-active, 2 enfants, 40 000 € | 3 812 | 2 895 | −917 |
| Famille mono-active, 2 enfants, 60 000 € | 5 760 | 6 840 | **+1 080** |
| Famille nombreuse biactive, 3 enfants, 60 000 € | 5 718 | 3 443 | −2 275 |
| Famille nombreuse mono-active, 4 enfants, 45 000 € | 4 289 | 1 381 | −2 907 |
| Parent isolé, 2 enfants, au Smic | 2 061 | 359 | −1 702 |
| Couple sans enfant à un revenu, 80 000 € | 11 622 | 15 226 | **+3 603** |
| Cadre supérieur seul, 120 000 € | 31 809 | 25 277 | −6 533 |
| Dirigeant salarié seul, 250 000 € | 87 063 | 75 587 | −11 476 |
| Retraité seul, 12 000 € / 16 000 € / 20 000 € | 0 / 0 / 860 | 600 / 1 400 / 2 200 | **+600 / +1 400 / +1 340** |
| Couple de retraités, 30 000 € / 60 000 € | 1 290 / 8 402 | 2 400 / 8 400 | **+1 110** / 0 |

**Perdants à ne pas masquer.** (1) Les retraités modestes et moyens : +1 000 à +1 400 € entre 16 000 et 30 000 € de
pension pour une personne seule ; les retraités aisés, eux, gagnent (−1 000 € à 50 000 €, −6 000 € à 100 000 €). (2)
Les couples à un seul revenu, effet de l'impôt individuel : sans enfant, +660 € à 30 000 € brut, +2 200 € à 50 000,
+3 600 € à 80 000 ; avec deux enfants, gain jusqu'à 50 000 €, puis +1 100 € à 60 000, +1 800 à 80 000, +2 500 à
100 000 € ; avec trois enfants, perte au-delà de 70 000 € environ. En moyenne, les couples d'actifs où un conjoint
gagne tout perdent 2 900 € (sans enfant) et 1 200 € (avec enfants) ; ceux aux revenus proches gagnent 850 à 1 750 €.

**Familles.** Les familles de travailleurs gagnent : −1 130 € en moyenne pour un couple avec deux enfants, −1 100 à
−2 300 € pour les biactifs de 20 000 à 100 000 € ; familles nombreuses −2 300 à −2 900 € ; parents isolés −1 700 € au
Smic. Les familles mono-actives gagnent jusqu'à 50 000 € et perdent au-dessus (≤ 2,5 % du brut) : perte réelle mais
pas excessive ; la correction minimale, si on la veut, est l'étape intermédiaire (§ 6). Franchise par enfant : 4 000 €
(coût proche du quotient familial actuel, 13,8 Md€) fait perdre 1 500 € à la famille mono-active à 60 000 € et ramène
le gain moyen d'un couple avec deux enfants à −635 € ; 8 000 € coûterait 6,2 Md€ de plus que 6 000 € (+0,75 point sur les taux de 20 et 28 %). **Retenu : 6 000 €.**

## 5. Cas-types du récit [S]

- **Augmentation.** Salarié à 2 000 € net par mois (30 318 € brut par an), augmenté à 2 200 € net (33 350 € brut) :
  +2 689 € de revenu après cotisations. Il en garde 2 042 € aujourd'hui (24,1 % prélevés : il entre dans l'IR et sa
  décote) et 2 151 € après (20,0 %). Entre 1,1 et 1,85 Smic, le taux marginal passe de 23,7 % à 20 %. Contrepartie :
  entre 0,63 et 1,08 Smic, il monte de 10,7 % à 20 % (le taux moyen, lui, baisse : −25 € au Smic, −551 € à mi-temps).
- **Second conjoint.** Premier salaire de 35 000 € brut ; le second reprend un mi-temps au Smic (10 811 € brut).
  Aujourd'hui, l'impôt du couple augmente de 1 242 € (11,5 % du brut ; 9,5 % sur les 1 000 premiers euros, avec deux
  enfants 1 030 €). Système individuel : +479 € (4,4 % du brut, 5 % du revenu après cotisations), avec ou sans enfants.
  Mais l'impôt du couple sans enfant à un revenu passe de 3 336 à 4 408 € (+1 073) ; avec deux enfants, de 3 336 à
  2 008 €. Étape intermédiaire (quotient conjugal plafonné à 2 000 €) : le second salaire est taxé 18,4 %.
- **Famille avec deux enfants** (biactive, 60 000 €) : −1 107 € ; mono-active à 40 000 € : −917 € ; à 60 000 € : +1 080 €.
- **Famille nombreuse mono-active** (4 enfants, 45 000 €) : de 4 289 à 1 381 € (−2 907) ; 3 enfants, 35 000 € : −2 527.
- **Prolonger sa carrière à 63 ans** (né en 1962, pension inchangée par ailleurs) : salaire de 35 000 € brut ou pension
  de 20 000 € ; l'année de travail en plus rapporte 7 814 € nets aujourd'hui, 8 893 € après ; l'impôt sur l'écart de
  revenu tombe de 29,2 % à 19,5 %. À 50 000 € contre 28 000 € : 10 560 → 12 509 € (35,3 % → 23,3 %). Le droit actuel
  taxe moins la pension que le salaire, donc pénalise la prolongation ; l'alignement corrige cela.

## 6. Imposition individuelle : cible et étape intermédiaire [C]/[H]

Risque constitutionnel sérieux : le Conseil constitutionnel a censuré en 2012 (2012-662 DC, contribution sur les très
hauts revenus d'activité) une imposition assise sur chaque personne alors que l'IR l'est sur le foyer, deux foyers de
même revenu payant des sommes différentes selon sa répartition (lu dans des commentaires, texte officiel non relu ici).
La CSG, individuelle, est admise ; mais la censure de la ristourne de CSG en 2000 (2000-437 DC, charges de famille
ignorées) incite à garder une prise en compte des enfants (franchise). La loi devra invoquer un objectif d'intérêt
général explicite (emploi du second apporteur, neutralité entre formes de couple). **Cible : impôt individuel. Étape
intermédiaire possible : quotient conjugal plafonné** (l'impôt du couple est le plus élevé de l'impôt du revenu
partagé par moitié et de la somme des impôts individuels moins 2 000 €). Coût : gain d'efficacité 3,1 au lieu de 3,8
Md€, emplois +216 000 au lieu de +305 000, taux de 20/28 relevés de 0,8 point ; il protège les couples à un revenu (80 000 €
sans enfant : +2 070 € au lieu de +3 600 ; mono-active deux enfants à 60 000 € : −690 € au lieu de +1 080) mais taxe
le second salaire à 18 % au lieu de 4,4 %. Plafond de 4 000 € ou sans plafond : effets voisins.

## 7. Gains [S]/[H]

**Perte sèche** (méthode v2, `revue/methode_v2.md` ; indicateur d'efficacité, pas un supplément de PIB) ; jeux bas /
central / haut, en Md€ par an :

| Perception de la CSG d'aujourd'hui | Bas | Central | Haut |
|---|---|---|---|
| comme l'IR | 1,9 | **3,8** | 9,0 |
| à moitié (sur les heures et l'effort ; décision de travailler sur le salaire net) | 0,0 | 0,1 | 0,8 |
| pas du tout (idem) | −1,7 | −3,3 | −7,0 |
| à moitié, sur les deux marges | −1,0 | −2,4 | −4,4 |
| pas du tout, sur les deux marges | −3,6 | −8,2 | −16,8 |

Central, perception entière : 2,7 Md€ sur les heures et l'effort, 1,1 sur la participation. **Le gain s'annule si
moins de 48 % de la CSG d'aujourd'hui est perçu** (marge extensive vue en entier). C'est la conclusion qui peut changer :
le nouvel impôt, publié avec un barème, est supposé entièrement perçu ; si la CSG ne l'est pas, la fusion rend visible
un prélèvement caché et relève le taux perçu des salaires moyens (aujourd'hui 13 % d'IR entre 1,1 et 1,85 Smic, 20 %
demain). Aucun des 1 800 barèmes essayés ne reste gagnant si la CSG n'est pas perçue du tout (le meilleur, presque
proportionnel, 15 % jusqu'à 100 000 €, perd encore 1,2 Md€) ; tous restent gagnants sur la participation si la décision de travailler
se prend sur le salaire net (hypothèse raisonnable : la CSG y est déjà retirée). Le barème retenu est l'un des plus
robustes à progressivité comparable (5/20/30/45 % avec seuils 12 000 / 44 000 / 100 000 € : seuil de perception 55 %).
Variante plus efficace écartée : 8 % jusqu'à 14 000 €, 18 % jusqu'à 34 400 €, 28 % jusqu'à 120 000 €, 45 % (gain 4,3 Md€,
seuil de perception 41 %), qui taxerait une pension de 12 000 € à 960 € au lieu de 600 €.
Aucune étude ne mesure la perception de la CSG [H].

Si les actifs anticipent la taxation plus lourde de leurs futures pensions (+3,1 points de taux moyen, prélèvement
implicite 0,8 point sur le salaire), le gain central tombe à 3,3 (vu à moitié) ou 2,8 Md€ (vu en entier). Revenu
déclaré du dixième supérieur (non compté) : +3,4 Md€ de recette (1,7 à 5,1).

**Effets réels** (jeu central, perception entière ; bas–haut entre parenthèses) : participation +305 000 personnes
(122 000 à 610 000), surtout des seconds apporteurs et des temps partiels (revenu moyen d'entrée ~15 900 € brut) ;
revenu réel du travail +0,9 % (0,4 à 2,0), soit ~240 000 équivalents emplois moyens [H : 26 M d'ETP]. Fonction de
production Cobb-Douglas (part du travail 2/3) [H] : PIB potentiel +0,6 % à capital donné, +0,9 % (≈ 27 Md€) à long
terme si le capital s'ajuste. Si la CSG n'est perçue qu'à moitié : +0,3 % ; pas du tout : −0,2 %. Ce sont des
réactions d'offre de travail ; les emplois effectifs dépendent de la demande (Bozio et Wasmer chiffrent leur scénario
de coût du travail à 10 000-20 000 ETP, autre mécanisme). Élasticités [E] : participation 0,25 (0,10–0,50 ; Chetty,
Guren, Manoli et Weber, *NBER Macro Annual* 2013, surtout américaines ; Carbonnier 2021, 1 à 2 pour les femmes mariées
françaises, résumé seulement) ; revenu d'activité ≈ 0,2 au taux de l'IR, surtout par les mois travaillés, peu par les
heures (Lehmann, Marical et Rioux, *JPubE* 2013) ; trois fois moins au retrait des prestations (Sicsic, *Fiscal Studies*
2022) ; jeu central prudent 0,05 / 0,10 (méthode v2).

**Bozio et Wasmer (2024)** (« Les politiques d'exonérations de cotisations sociales : une inflexion nécessaire »,
rapport au Premier ministre remis le 3 octobre 2024, lu sur vie-publique.fr) : entre 1 et 1,6 Smic, 100 € de coût du
travail en plus ne donnent que 41 € de salaire net (taux marginal de 59 %, dû à la pente des allègements), avant IR et
prime d'activité ; le taux marginal effectif médian culmine à 63 % vers 1,1 Smic, par « l'entrée dans l'impôt sur le
revenu et la dégressivité de la prime d'activité » (d'après Sicsic et Vermersch, 2021) ; les auteurs ne prouvent pas
la trappe à bas salaires mais jugent qu'« aucune étude empirique ne vient réellement effacer ces craintes ». Leçon
retenue : le barème garde un taux constant de 20 % de 0,63 à 1,9 Smic, sans entrée dans l'IR ni décote vers 1,1 Smic.

## 8. Bouclage [C]

Montée en charge sur quatre ans, des deux côtés à la fois : chaque foyer paie (1 − λ) × ancien impôt + λ × nouveau,
λ = 0,25 / 0,5 / 0,75 / 1 de 2027 à 2030 ; recette constante chaque année par construction (statique). Table `annuel`
(Md€, niveau 2025) en 2030 et après : retraités +12,88 ; actifs −11,30 ; CEHR du barème −0,58 ; invalidité-dépendance
−1,03 ; écart de calage −0,03 ; total −0,05. Risque : le taux marginal du haut baisse (de 52-56 % à 45 %), ce qui incite à reporter des
rémunérations vers 2030 ; faire converger le haut dès 2027 créerait un écart de recette les premières années (non
chiffré ici).
CRDS : son extinction après 2033 est du droit en vigueur ; en 2034, tous les taux baissent de 0,54 point (7,6 Md€),
ni coût ni recette de la réforme. Coûts par point au § 3.

## 9. Limites qui peuvent changer la conclusion

1. Perception de la CSG (§ 7) : sous 48 % de perception, la fusion coûte en efficacité. 2. Foyers synthétiques : 60
points par tranche de RFR de l'IRCOM, ménages « purs » (actifs ou retraités), couples homogènes, quatre partages des
revenus, un enfant par parent isolé et deux par couple avec enfants, même composition dans toutes les tranches ;
charge actuelle répartie par cas-types OpenFisca sans niche ; les niches réelles (emploi à domicile, dons), les
retraités de moins de 65 ans, les ménages mixtes et les familles de trois enfants et plus ne sont pas représentés
(cas-types seulement). 3. Suppression des crédits d'impôt (emploi à domicile 7,0 Md€, garde d'enfants 1,8) héritée du
modèle : s'ils sont gardés, +0,6 point sur tous les taux. 4. Imputation de 4,0 Md€ d'IR (§ 3). 5. Haut de la
distribution : répartition des revenus au PFU entre tranches non publiée (le 1 % peut gagner de 0 à 4 Md€ selon la
convention). 6. Pas de réaction des retraités, pas de demande de travail, pas d'effet sur les frontaliers et non-résidents
(arrêt C-169/98 de la CJCE sur la CSG à expertiser). 7. Taux de CSG des pensions d'OpenFisca non relus sur une source
officielle.
