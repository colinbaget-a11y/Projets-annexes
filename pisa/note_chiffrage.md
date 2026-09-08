# Combien vaut un point PISA ?

**La règle de pouce.** Une amélioration durable de **10 points du score PISA moyen** (moyenne des trois
domaines) est associée à **environ +1 % de productivité à très long terme**, une fois la population active
entièrement renouvelée. Fourchette des estimations institutionnelles : **+0,9 % à +1,6 %**.

**Le calcul France.** La France perd 28 points entre 2018 et 2025 → **−2,8 %, arrondi à −3 %**.

---

## 1. Ce que dit la littérature, ramené à une seule unité

| Étude | Choc étudié | Effet publié | Équivalent pour +10 points |
|---|---|---|---:|
| Égert, de la Maisonneuve & Turner (2022), OECD ECO WP 1709 | +25,5 pts (moyenne 3 domaines) | +3,4 à +4,1 % de PGF, long terme | **+1,3 à +1,6 %** |
| OCDE, *Étude économique de la France* (2024) | +29,2 pts (moyenne 3 domaines) | +2,7 % de productivité, à terme | **+0,9 %** |
| OCDE, *Adult Skills and Productivity* (2024, PIAAC 2023) | +10 % de score PIAAC | +18 % de productivité du travail | **+1,0 à +1,3 %** |
| CAE, *Focus* n° 91 (2022) | +10 pts en mathématiques | +0,6 à +1,4 % de productivité | +0,6 à +1,4 % *(à 15 ans)* |
| *Contrôle micro* — Hanushek, Schwerdt, Wiederhold & Woessmann (2015) | +1 écart-type PIAAC | +17,4 % de salaire horaire (France) | *+0,5 %* |

**Vérification des unités.** Les deux premières lignes portent explicitement sur la moyenne des trois
domaines : Égert et al. définissent leur mesure comme « the average scores for reading, maths and science » ;
l'Étude économique de la France chiffre le passage « au score moyen des dix meilleurs pays de l'OCDE dans
chacun des trois domaines », soit +29,2 points sur la moyenne (mathématiques 503, écrit 505, sciences 514 pour
le top 10 ; France 478,3 en 2022). Aucune des estimations retenues ne raisonne sur des points cumulés.
Le CAE fait exception dans l'autre sens — son scénario porte sur les mathématiques seules et à quinze ans,
c'est-à-dire avec un renouvellement partiel des cohortes : sa ligne est une borne basse et n'entre pas dans
la fourchette centrale.

**Ce qui a été converti.** Les lignes 3 et 5 sont publiées en fonction des scores PIAAC d'adultes, pas de PISA.
Le passage se fait par l'élasticité estimée par Égert et al. en appariant chaque cohorte adulte de PIAAC aux
scores PISA de la même cohorte : 0,278 avec les années d'études en contrôle. Ce n'est donc jamais un pour un —
10 points PISA ne font que 0,56 % de score PIAAC, soit 0,03 écart-type adulte. Le détail des chaînes est en
annexe (`chiffrage_pisa_pib.py` et `note_litterature.md`).

**Ce qui reste imparfait.** Les lignes 1, 2 et 4 sont des applications du même cadre de l'OCDE, et la ligne 3
partage avec elles le passage PISA → PIAAC : quatre estimations, mais deux maillons indépendants seulement.
Par ailleurs les lignes 1 et 2 portent sur la productivité globale des facteurs, la ligne 3 sur la
productivité du travail ; si le capital s'ajuste, l'effet sur le PIB par tête est environ une fois et demie
celui sur la PGF. Conserver la métrique publiée rend donc la règle de pouce plutôt prudente.

## 2. Le calcul

Moyenne des trois domaines, France, série comparable depuis 2006 (les sciences ne sont domaine majeur qu'à
partir de ce cycle) :

| 2006 | 2009 | 2012 | 2015 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| 493,0 | 497,0 | 499,7 | 495,7 | 493,7 | 478,3 | 465,7 |

Le niveau est plat de 2006 à 2018 ; toute la baisse est postérieure. **2018 → 2025 : −28 points.**
Par rapport à la moyenne 2006-2018, −30 points : le choix de la référence ne change rien.

> −28 points × 1 % pour 10 points = **−2,8 %, arrondi à −3 % de productivité de long terme.**
> Fourchette : −1,4 % (borne micro) à −4,5 % (borne macro haute).

Formulation correcte : si le niveau de compétences observé à PISA 2025 devenait durablement celui des
générations françaises à venir, alors une fois ces générations devenues l'ensemble de la population active,
le niveau de productivité serait inférieur d'environ 3 % à ce qu'il aurait été au niveau de 2018. C'est un
scénario de permanence, pas une prévision. Effet nul avant 2035, moitié réalisée vers 2050, complet vers 2075.

## 3. Trois choses qu'il ne faut pas mélanger

**Les estimations de niveau**, seules retenues ci-dessus. Elles répondent à la question « quel niveau de
productivité une fois les cohortes renouvelées ». Elles convergent autour de +1 % pour 10 points.

**Les régressions de croissance** de Hanushek et Woessmann traitent le niveau de compétences comme un
déterminant du *taux* de croissance. Dans la projection de l'OCDE de 2010 pour la France, +25 points valent
+24,3 % de PIB en 2090, soit **+9,7 % pour 10 points** — dix fois les estimations de niveau, et l'écart
continue de croître au-delà. Hypothèse économique beaucoup plus forte : les séries longues ne montrent aucun
changement durable des taux de croissance malgré l'explosion du capital humain, et les auteurs reconnaissent
qu'une régression de croissance conditionnelle ne distingue pas un effet de niveau d'une croissance
permanente. À garder en borne haute.

**Les rendements salariaux individuels** mesurent ce qu'un travailleur plus compétent gagne de plus, sans
externalité ni effet d'allocation des compétences entre entreprises. Ils donnent +0,5 % pour 10 points, soit
la moitié des estimations macro. Utile comme plancher et comme contrôle de cohérence, pas à additionner ni à
moyenner avec elles.

## 4. Réserves

1. **C'est un scénario de permanence.** Ne jamais écrire que PISA 2025 coûte 3 % de productivité à la France :
   si les scores remontent, la perte est transitoire et bien plus faible.
2. **Le passage de PISA à 15 ans aux compétences adultes est le maillon commun et le plus fragile.**
   L'élasticité vaut 0,278 ou 0,603 selon la spécification ; retenir la seconde doublerait toutes les lignes
   du tableau à la fois.
3. **L'écart entre l'estimation micro (+0,5 %) et les estimations macro (+1 à +1,6 %) n'est pas identifié.**
   Il correspond aux externalités et aux effets d'allocation, que les corrélations de panel entre pays captent
   sans les isoler.

---

*Calculs : `chiffrage_pisa_pib.py`. Chaînes détaillées, identifications et textes non accessibles :
`note_litterature.md`. Modèle de croissance de l'OCDE 2010 : `simulation_ocde2010.py`.
Accès aux fichiers PISA : `README.md`.*
