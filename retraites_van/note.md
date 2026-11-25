---
title: "Qui paie une réforme des retraites ?"
subtitle: "Valeur actualisée, par âge, de trois réformes de même effet sur les finances publiques"
date: "Document de travail, novembre 2026 — montants en euros de 2025"
lang: fr
geometry: margin=2.2cm
fontsize: 10pt
---

**En résumé.** À effet égal sur les finances publiques, la baisse des pensions épargne bien les jeunes actifs, mais
moins qu'on ne le croit, et elle devient la réforme la plus coûteuse pour tout actif de plus de 40 ans environ. Le
recul d'un an de l'âge de départ coûte beaucoup moins à chacun en transferts, parce que l'essentiel de son rendement
public vient du travail supplémentaire qu'il impose, et non d'une ponction sur les revenus.

# 1. La question et la méthode

**Trois réformes sont comparées à effet égal sur le solde public.** Le calage reprend les simulations présentées au
Conseil d'orientation des retraites le 26 mars 2026 par la DG Trésor, l'OFCE et I-MIP. Ces équipes ont simulé une
baisse des pensions de 6 Md€ ex ante, des hausses de cotisations salariales ou employeurs de 6 Md€ et un recul d'un an
de l'âge d'ouverture des droits, de 64 à 65 ans. À 20 ans, en moyenne des trois modèles, ces chocs améliorent le solde
primaire des administrations publiques de 0,12 point de PIB pour la baisse des pensions, 0,09 pour les cotisations
salariales, 0,06 pour les cotisations employeurs et 0,49 pour le recul de l'âge. Les leviers de 6 Md€ rapportent moins
que 6 Md€ parce qu'ils dépriment l'activité, donc les autres recettes. Pour obtenir les 0,49 point du recul de l'âge,
soit 14,6 Md€, il faut baisser les pensions de 23,7 Md€ ex ante (6,3 %), ou relever les cotisations salariales de
33,7 Md€ (2,5 points), ou les cotisations employeurs de 46,1 Md€ (3,4 points).

**La perte est la variation de la valeur actualisée des transferts nets reçus du système.** Pour chaque âge en 2026,
le modèle somme sur le reste de la vie, pondéré par la probabilité de survie et actualisé, les pensions perdues et les
cotisations supplémentaires. Les cotisations employeurs sont supposées retomber à terme entièrement sur les salaires,
comme le retient le COR. Le taux d'actualisation réel central est de 2 %, entre le rendement des OAT indexées longues
(1,3 % à 2,4 %) et le taux public de France Stratégie (3,2 % avec prime de risque). Le salaire réel croît de 0,7 %
par an (COR). La somme des pertes de toutes les générations, présentes et futures, est égale par construction à la
valeur actualisée du gain budgétaire, et le contrôle numérique le vérifie à $10^{-15}$ près.

**Pour le recul de l'âge, la perte ne compte pas le salaire de l'année travaillée en plus.** Celui qui travaille un
an de plus touche un salaire au lieu d'une pension. Si l'on suppose que son temps libre valait au moins ce salaire net,
il perd la pension de l'année. Celui qui n'est pas en emploi perd aussi sa pension, mais reçoit chômage, indemnités
journalières, invalidité ou minima sociaux, soit environ 30 % de la pension perdue selon les notes de la DREES et de la
DARES au COR (2022). Le modèle répartit sur les générations touchées une économie de pensions de 6,3 Md€ par an, déduite
de l'amélioration du solde des retraites dans les trois modèles (0,27 point de PIB), moins les cotisations versées par
les 217 000 personnes en emploi supplémentaire.

# 2. Résultats

**À effet public égal, un actif de 25 ans perd 19 000 € avec la baisse des pensions, 29 000 € avec la hausse des
cotisations salariales et 3 000 € avec le recul de l'âge** (tableau 1, figure 1). L'avantage de la baisse des pensions
pour les jeunes s'efface vers 40 ans. Au-delà, elle devient la réforme la plus coûteuse : à 55 ans, 26 000 € contre
9 000 € pour la hausse des cotisations, parce qu'il reste peu d'années de cotisation mais toute la retraite à vivre.

| Âge en 2026 | Baisse des pensions | Cotisations salariales | Cotisations employeurs | Recul de l'âge | Ressources restantes |
|:-:|--:|--:|--:|--:|--:|
| 25 ans | 18,7 (1,3 %) | 29,2 (2,0 %) | 39,9 | 3,0 (0,2 %) | 1 459 |
| 40 ans | 22,0 (1,8 %) | 22,5 (1,8 %) | 30,8 | 3,7 (0,3 %) | 1 245 |
| 55 ans | 26,4 (3,3 %) | 9,3 (1,2 %) | 12,7 | 4,5 (0,6 %) | 789 |
| 70 ans | 24,5 (6,2 %) | 0,2 | 0,3 | 0 | 398 |
| Né en 2026 | 14,3 | 21,8 | 29,8 | 2,2 | |

: Perte actualisée par personne, milliers d'euros de 2025 (en % des revenus d'activité et pensions restant à percevoir).
Réformes de même effet sur le solde public (0,49 point de PIB), r = 2 %, g = 0,7 %. Pour une génération future, la
perte est ramenée à 2026.

![Perte actualisée par âge, réformes de même effet sur le solde public (r = 2 %)](figures/f1_meme_effet_public.pdf){width=85%}

**À montant ex ante égal, l'actualisation seule ne rend la baisse des pensions que légèrement moins coûteuse pour les
jeunes** (figure 2). Pour 6 Md€ ex ante et r = 2 %, un actif de 20 ans perd 4 500 € par la baisse des pensions et
5 000 € par la hausse des cotisations. Les deux coûts sont égaux à 30 ans. À 50 ans, la baisse des pensions coûte 2,5
fois plus. L'intuition selon laquelle un euro de pension perdu dans quarante ans pèse bien moins qu'un euro de
cotisation versé aujourd'hui est juste, mais deux effets la contrebalancent presque entièrement :

- les cotisations s'étalent elles aussi sur quarante ans, de sorte que l'écart moyen de date entre l'euro cotisé et
  l'euro de pension est plus court qu'il n'y paraît ;
- surtout, un jeune actif touchera sa pension plus longtemps que les retraités d'aujourd'hui, et dans une population
  plus âgée. Une baisse de 1 % des pensions prélève donc sur sa vie davantage, rapporté à ses revenus d'activité, que ce
  qu'indique la coupe transversale d'aujourd'hui.

À 25 ans, la valeur actualisée des pensions futures représente 26 % de celle des revenus d'activité futurs, contre 28 %
pour le rapport entre pensions et assiette d'aujourd'hui. L'actualisation ne retire donc que 9 % au poids relatif de la
baisse des pensions. Si r est égal à la croissance (0,7 %), ce rapport monte à 39 % et la baisse des pensions coûte
plus cher que la hausse des cotisations à tout âge. À r = 3 %, il tombe à 19 %. Le résultat dépend donc d'abord de
l'écart entre le taux d'actualisation et la croissance, et l'allongement de la vie en compense une partie (sans lui, le
rapport serait de 22 % au lieu de 26 %).

![Même choc ex ante de 6 Md€ : perte par la baisse des pensions et par la hausse des cotisations, selon r](figures/f2_meme_montant_ex_ante.pdf){width=95%}

**Les retraités actuels ne supportent qu'une petite partie d'une baisse permanente des pensions** (figure 3). Un
retraité de 70 ans perd 24 500 €, mais les 65 ans et plus ne portent que 12 % de la valeur actualisée totale. Les actifs
de 20 à 59 ans en portent 32 %, les moins de 20 ans 11 % et les générations futures 40 %. Une baisse permanente des
pensions est d'abord une baisse des pensions futures des actifs d'aujourd'hui et de demain. Elle reporte moins
l'effort vers les générations futures qu'une hausse des cotisations, dont elles portent 54 %, mais l'écart est modeste.

![Répartition de la valeur actualisée de l'effort entre générations (âge en 2026), r = 2 %](figures/f3_qui_paie.pdf){width=85%}

**Le recul de l'âge coûte six à dix fois moins en transferts, au prix d'une année de travail en plus.** À effet public
égal, il retire aux actifs 3 000 à 4 800 € chacun, parce que seuls 4,4 Md€ des 14,6 Md€ de gain public viennent d'une
baisse de transferts nets. Le reste provient des impôts et cotisations prélevés sur la production des 217 000 seniors
qui travaillent plus longtemps. Ce coût en transferts dépend de la valeur que chacun accorde à son temps libre. Si l'on
comptait le salaire net de l'année supplémentaire comme un gain, sans rien soustraire pour le temps de loisir perdu, la
réforme deviendrait un gain moyen de 1 200 à 2 000 € par personne. Ce calcul n'a de sens que pour ceux qui auraient
volontiers travaillé plus longtemps. La valeur d'une année de vie à la retraite n'est pas mesurée ici, et c'est elle qui
fait le débat.

# 3. Sensibilité et limites

| Variante | Pensions 25 / 40 / 55 ans | Cotisations salariales 25 / 40 / 55 ans | Âge 25 / 40 / 55 ans |
|:--|:-:|:-:|:-:|
| Central (r = 2 %, g = 0,7 %, COR à 20 ans) | 18,7 / 22,0 / 26,4 | 29,2 / 22,5 / 9,3 | 3,0 / 3,7 / 4,5 |
| r = 1 % | 31,3 / 31,6 / 32,5 | 35,5 / 25,1 / 9,7 | 4,4 / 4,6 / 4,9 |
| r = 3 % | 11,4 / 15,5 / 21,6 | 24,3 / 20,2 / 8,9 | 2,1 / 2,9 / 4,1 |
| r = g = 0,7 % | 36,6 / 35,3 / 34,7 | 37,8 / 26,0 / 9,9 | 5,0 / 5,0 / 5,0 |
| Calage sur les effets à 5 ans | 16,8 / 19,7 / 23,6 | 19,8 / 15,2 / 6,3 | 2,3 / 2,8 / 3,4 |
| Économie de pensions de 0,30 pt de PIB par an d'âge (DREES) | inchangé | inchangé | 4,3 / 5,2 / 6,4 |
| Sans allongement de la vie | 16,3 / 19,9 / 24,8 | 29,0 / 22,4 / 9,3 | 2,9 / 3,6 / 4,5 |

: Perte actualisée par personne, milliers d'euros de 2025, réformes de même effet sur le solde public.

Le classement par âge résiste à toutes les variantes : la baisse des pensions épargne les moins de 35 ans, coûte autant
que la hausse des cotisations vers 40 ans et coûte nettement plus au-delà. Quatre limites peuvent déplacer ces chiffres.

- **Les effets macroéconomiques n'entrent dans la perte individuelle que par le calage.** Les modèles du COR prévoient
  moins d'emploi et des salaires plus bas après une hausse des cotisations, surtout patronales. Compter ces pertes
  alourdirait le coût de la hausse des cotisations pour les actifs.
- **Les profils sont des moyennes par âge.** Une baisse uniforme des pensions pèse davantage sur ceux qui vivent
  longtemps, plus souvent aisés et plus souvent des femmes. Le recul de l'âge pèse davantage sur ceux qui ont commencé
  tôt et sur ceux qui ne sont plus en emploi à 60 ans.
- **Une baisse de pensions en pourcentage rapporte davantage à mesure que la population vieillit**, de 24 à 29 Md€ entre
  2026 et 2060, alors que la hausse des cotisations rapporte un montant à peu près constant. À r = 2 %, la valeur
  actualisée des deux réformes est pourtant voisine (2 360 et 2 410 Md€).
- **L'économie de pensions d'un an d'âge est incertaine.** Les trois équipes du COR l'estiment entre 0,2 et 0,4 point de
  PIB pour le seul système de retraite. La perte individuelle liée au recul de l'âge est proportionnelle à ce chiffre.

**Sources.** COR, séance du 26 mars 2026, documents n° 2 et 3, et rapport annuel 2026 (chapitre 6, tableau 2.10 ;
dépenses 2025 de 401 Md€). Insee : bilan démographique 2025, projections de population 2026, enquête Emploi 2025,
revenu salarial 2023. Eurostat : table de mortalité 2024. DREES : retraités par âge, EACR-Ancetre 2024. DREES et DARES :
notes au COR du 27 janvier 2022. France Stratégie : guide de l'évaluation socioéconomique (2023). Code et données :
`retraites_van/` (`model.py`, `check.py`, `sensibilites.py`, `params.json` avec le statut de chaque paramètre).
