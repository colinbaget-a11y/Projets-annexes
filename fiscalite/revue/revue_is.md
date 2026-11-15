# Revue de la note IS « Ne pas toucher au taux, mieux déduire l'investissement »

Sorties de `simulation_is.py` reproduites sur une copie ; [calcul] : calcul du relecteur.

## Verdict

La thèse (déduire l'investissement plutôt que baisser le taux, financer par l'assiette) est orthodoxe et sert la croissance. Mais le paquet n'est pas à recette constante : après la transition, il relève l'IS de 2,5 à 5 Md€ par an, surtout sur les TPE, et l'argument opposé à 28 % frappe son propre financement. L'étape à 50 % rapporte très peu en PIB ; la simulation, juste dans sa mécanique, omet les intérêts de la dette. Tout se corrige sans changer de thèse.

## Problèmes, du plus grave au moins grave

### 1. Une hausse durable de l'IS, que la note reproche à 28 %

*Passages* : « Le financement par l'assiette suffit pour le régime permanent » ; contre 28 % : « une hausse permanente, deux à quatre fois supérieure au coût de long terme ».

*Problème* : l'assiette rapporte 3,5 à 4,4 Md€ par an pour toujours ; la déduction coûte, par millésime actualisé, 0,9 à 1,3 Md€ à 50 %, 1,8 à 2,6 à 100 %. En l'an 10, le paquet dégage +3,5 à +5,0 Md€ par an à 50 %, +2,5 à +4,3 à 100 % [calcul], soit 1 à 2 points d'IS. Le financement vaut 1,3 à 3 fois le coût de long terme de la déduction totale : c'est le reproche fait à 28 %.

*Correction* : dimensionner le financement au coût actualisé du régime final (1,1 à 2,6 Md€ selon l'actualisation). Options : les trois niches (1,3 à 1,7 Md€), complétées par une partie du taux réduit (le réserver aux sociétés opérationnelles, hors revenus passifs de holdings et SCI) ; ou tout garder pour rembourser la bosse, puis rendre l'excédent par un point de taux (2,5 Md€). Les niches seules financent 50 %, pas 100 % : la dette dériverait de 0,5 à 2,4 points de PIB [calcul]. Fonder l'argument contre 28 % sur ce que la hausse frappe (rentes mobiles), pas sur son montant.

### 2. Le gain de croissance n'est jamais chiffré

*Passage* : « le stock d'équipements [...] augmenterait de quelques pour cent à long terme ».

*Problème* : stock éligible fin 2025 : 541 Md€ (Insee 8.212), dépréciation ≈ 14 %, revenu du capital ≈ 3,3 % du PIB. Élasticité du stock de 0,5 à 1,6, sur 75 % du stock : déduction totale (coût d'usage −3,4 à −4,8 %), +0,04 à +0,19 % du PIB à long terme, 0,1 % au centre (3 Md€) ; à 50 % (−1,7 à −2,4 %), +0,02 à +0,1 % [calcul]. Chodorow-Reich et al. : +1,8 % de capital à dix ans pour la seule déduction.

*Correction* : ajouter ce chiffrage ; l'essentiel du gain exige 100 %.

### 3. Le taux réduit n'est pas un forfait pour beaucoup ; Bernini et Treibich sont publiés

*Passages* : « la somme ne dépend d'aucune de ses décisions » ; « une hausse de 4 % [...] est fragile et non publiée ».

*Problème* : 18,2 Md€ de base à 15 % en 2018 pour ≈ 760 000 bénéficiaires (2019) : 24 000 € en moyenne, plafond 38 120 € [calcul]. Sous le plafond, la suppression porte le taux marginal de 15 à 25 % et le coût du capital non éligible de +2,3 à +5,9 % ; sur les équipements, la déduction de 50 % ne fait que compenser (−0,15 %) [calcul]. Or les petites entreprises réagissent le plus (Zwick et Mahon : +95 %), par la trésorerie. Et l'étude est publiée : *Industrial and Corporate Change* 25(5), 2016, p. 829-845 ; son résumé annonce +29 % de capital pour un taux divisé par deux, plus d'exportations, moins de croissance de l'emploi (seul le résumé a été lu).

*Correction* : citer et discuter la version publiée ; distinguer sociétés au-dessus du plafond (forfait) et en dessous (taux marginal).

### 4. Simulation : mécanique juste, conventions à revoir

Calcul par millésime correct. À corriger :
- *Actualisation* : au taux d'emprunt public (3 à 3,5 %, hypothèse), la déduction totale coûte 1,1 à 1,9 Md€ par millésime, non 1,8 à 2,6. L'écart entre ce taux et celui des entreprises est un gain que la note ignore.
- *Intérêts* : absents du solde cumulé. À 3-3,5 %, la déduction totale immédiate creuse 19 à 46 Md€, regagnés en 11 à 29 ans (non 18-40 et 10-22) ; à 50 %, 3 à 11,5 Md€ en 5 à 10 ans.
- *Explication fausse* : le coût permanent ne vient pas de ce que « l'avance a une valeur » : à croissance nulle, il est nul. Les chiffres « au bout de sept ans » sont de l'an 10.
- *Bases* : les non-imposables ne coûtent jamais rien, alors que leurs déductions deviennent des déficits imputés plus tard ; assiette de 2022, coût de 2027 ; après la décision du Conseil d'État, 2,7 Md€ est un plafond.

### 5. Le point de référence cache une baisse de 5 à 7 Md€ pour les grands groupes

« Laisser la contribution exceptionnelle s'éteindre comme prévu » : 7,5 Md€ en 2025, ≈ 7 en 2026, 5 attendus du PLF 2027 (article supprimé en première lecture selon Légifiscal). C'est une baisse pour ≈ 450 groupes, quand la note juge la France sans marge budgétaire. *Correction* : la chiffrer par rapport à 2026 et au PLF 2027.

### 6. Un second palier non daté

« Quand les finances publiques le permettent » contredit le grief d'instabilité et repousse l'essentiel du gain. Légiférer dès 2027 50 % six ans puis 100 % : creux de 3 à 19 Md€ (assiette haute) ou 8 à 33 Md€ (basse), intérêts compris [calcul].

### 7. Corrections ponctuelles

- Conseil d'État 2025 : vise les sociétés de tout groupe, intégré ou non, de plus de 10 M€ de chiffre d'affaires, surtout familial ; les filiales de grands groupes étaient déjà exclues par la détention à 75 % par des personnes physiques (impots.gouv.fr, 14 avril 2026).
- Plafonnement des intérêts : seulement au-delà de 3 M€, donc rien pour les PME ; avec déduction totale, le taux marginal effectif d'un équipement financé par dette passe de −7 % à −33 % environ [calcul, intérêt 5 %].
- « L'État devient un associé » : seulement à 100 % et si les pertes sont symétriques, ce que le plafonnement de l'imputation empêche.
- Taux minimal : le pilier 2 neutralise en principe les écarts temporaires (fiscalité différée) ; l'argument est la redondance.
- OBR : « cité par l'IFS (2023) » ; ajouter que le Royaume-Uni (2023) et les États-Unis (2025) ont rendu la déduction totale permanente [secondaire].
- Tax Foundation : 16e en 2026 ; « moins d'un point » : 1,02 en linéaire.

## Questions

### 1. Économiste académique
D'accord sur le cœur (Chodorow-Reich et al., tableau 7 : 2,5 contre 9,9 % de recette par point de capital, vérifié). Il contesterait les § 1 à 4 et le mélange des mécanismes : trésorerie (Zwick et Mahon) ou coût d'usage (Maffini et al.). L'extrapolation suppose le second ; si c'est le premier, priver les petites sociétés du taux réduit affaiblit l'effet. Transfert de bénéfices : la note tient.

### 2. Éditorialiste de centre droit
D'accord sur 25 %, la fin de la contribution, la stabilité, le CIR gardé. Objections : le Sénat (2026) et l'Assemblée (2025) voulaient porter le plafond à 100 000 € ; le taux implicite des grandes entreprises (14,3 % en 2022) est inférieur à celui des micro (19,0 %) et des PME (21,4 %), que la note ignore (Insee) ; l'IS des TPE monterait de 17 à 21 % si le coût leur revient (2,2 à 2,7 sur 13,1 Md€) ; hausse nette déguisée (§ 1) ; priorité aux impôts de production. Garder le taux réduit des sociétés opérationnelles (§ 1) désarme l'essentiel.

### 3. Croissance
Signe sûr, ampleur modeste (§ 2) ; à 50 %, le capital des TPE sous le plafond renchérit.

### 4. Système, faisabilité, perdants
Rien d'impossible. La déduction totale immédiate coûterait 15,5 Md€ l'an 1 (0,5 point de PIB) : commencer à 50 % est sage. Ses pertes s'imputent dans la limite de 1 M€ plus 50 % du bénéfice : elle sert d'abord les entreprises déjà rentables ; chiffrer un report hors plafond. Paient beaucoup plus : TPE sous le plafond (+67 % d'IS, 3 000 € pour 30 000 € de bénéfice), 4 250 € au-delà ; entreprises des zones (ZRR : ≈ 8 500 € par bénéficiaire, IR et IS) ; 1 065 utilisateurs de la boîte à brevets (avantage moyen 1,2 M€, réduit de moitié) ; grands groupes de recherche (0,57 Md€).

### 5. Familles
Aucun effet, comme le dit la note.

### 6. Grandes fortunes
Par rapport au droit permanent, presque rien : une holding ou SCI à l'IS perd au plus 4 250 € (dividendes reçus taxés 1,25 % au lieu de 0,75 %) ; pour les grands groupes, CIR et brevets (0,8 à 1,2 Md€) compensent à peu près la déduction (inférence, sans ventilation par taille). Par rapport à 2026, nettement moins (§ 5). Même avec la note PFU (apport-cession, 0,5 Md€), la contrainte est respectée.

## Non vérifié
Taux d'emprunt public ; article 219 sur Légifrance ; Bernini et Treibich au-delà du résumé ; droits américain et britannique (BDO, RSM, IFS) ; pilier 2 en droit français ; suite de l'article 15 du PLF 2027.
