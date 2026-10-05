# Cadrage du projet : questions à trancher

Quatre chapitres sont écrits, vingt figures produites, et le socle de données réconcilie
exactement avec la comptabilité nationale. Mais ce socle est compatible avec plusieurs rapports
très différents, et je ne veux pas écrire cent cinquante pages avant de découvrir que je me suis
trompé sur l'objet. Ce fichier liste ce que j'ai besoin de savoir.

Chaque question est suivie de **ce que je ferai à défaut de réponse**. Les réponses données le
3 octobre 2026 figurent en tête ; les questions restées sans réponse gardent leur défaut.

## Réponses, 3 octobre 2026

| # | Question | Réponse retenue |
|---|---|---|
| 1 | Lectorat | Rapport de think tank. Les responsables politiques d'abord, puis les économistes, puis les citoyens. Pas un travail très quantitatif. |
| 2 | Commande | Think tank orienté centre droit, avec une équipe d'experts libérale. L'orientation ne doit pas être visible dans le texte : le rapport doit se lire comme une analyse, pas comme un plaidoyer. |
| 3 | Positions | Le rapport tranche sur les quatre blocs : patrimoine et transmissions, logement, travail et revenu, consommation et carbone. |
| 4 | Rendement | Constant. Variante chiffrée à un ou deux points de plus, puisqu'il y a du déficit — 5,1 points de PIB en 2025. |
| 5 | Transferts | Tous les transferts monétaires, y compris les prestations universelles. |
| 6 | Cotisations | Toutes traitées comme un impôt. |
| 7 | Retraites | Paramètres pris comme donnés ; seul leur financement est discuté. |
| 8 | Périmètre | Liste Eurostat pour tous les chiffres, et un encadré nommant ce qui en est exclu avec son ordre de grandeur. |
| 9 | Norme | Éventail de préférences sociales, sans en privilégier aucune. Pas d'inverse optimum. |
| 10 | Unité d'imposition | Une section du chapitre sur le travail, sans recommandation autonome. |
| 11 | Mobilité | Contrainte forte et assumée : la mobilité des bases borne d'emblée les taux sur le capital et sur le sommet du barème. |
| 12 | Droit | L'idéal d'abord, la version faisable ensuite. |
| 13 | Fiscalité locale | Chapitre dédié : assiette foncière réévaluée, pouvoir de taux réel, péréquation explicite. |
| 14 | Microdonnées | Aucun accès. |
| 15 | Chiffrage | Ordres de grandeur. Pas de simulation distributive. |
| 16 | Littérature empirique | Résumé pour tous les papiers, sans examen de la stratégie d'identification. |
| 17 | Maquettes de référence | À expliquer avant de choisir. Cours livré dans `05_maquettes_de_reference.md`. |
| 18 | Où trancher | Les quatre blocs, plus les trois pédagogies ci-dessous. |
| 19 | Précautions | Oui, tu me diras lesquelles. En attendant, je ne touche à rien de manifestement sensible. |
| 20 | Pédagogie | Les quatre dispositifs : encadrés « comment ça marche », un cas chiffré récurrent, une idée par figure, définitions en marge. |
| 21 | Rédaction | Je rédige les chapitres complets avec leurs figures, tu arbitres et tu réécris. |
| 22 | Format | Markdown dans le dépôt, bascule LaTeX quand une partie est stabilisée. |
| 23 | Traçabilité | Stricte. Aucun chapitre n'est fini s'il reste une marque **[à sourcer]**. |

## Décisions du 5 octobre 2026

Quatre questions restées ouvertes, ou rouvertes par la rédaction du cours.

| # | Question | Décision |
|---|---|---|
| 24 | Longueur | Environ 90 pages de corps, plus des annexes. Le corps doit se lire d'un bout à l'autre ; les développements techniques, la revue des élasticités et les maquettes de référence passent en annexe. |
| 25 | Registre | Celui d'un rapport public. Le mécanisme et les exemples chiffrés restent ; les personnages, le « vous », les questions au lecteur et les formules d'oralité disparaissent. Le détail figure en tête de `PLAN.md`. |
| 26 | Chiffrage | Cas types calculés sur le barème réel avec OpenFisca-France, en plus des ordres de grandeur. C'est une extension de la réponse 15 : sans cela, le rapport affirme la compensation d'une réforme sans la démontrer, et l'argument de Mirrlees sur la TVA ne tient pas. Toujours aucun accès aux microdonnées, donc aucun perdant nommé. |
| 27 | Architecture du capital | Cadre dual complété par l'exonération du rendement normal et une règle de partage pour les dirigeants ; côté entreprises, suppression des prélèvements sur intrants d'abord, puis deux routes présentées pour le biais d'endettement. Décision provisoire, à confirmer par le chiffrage d'ensemble. |

Ordre de travail retenu : la maquette d'ensemble à rendement constant avant la rédaction des
chapitres, puisque c'est elle qui peut invalider une recommandation.

---

**Le but global du rapport est d'être pédagogique.** C'est la consigne qui prime sur les autres
quand elles entrent en conflit : mieux vaut un chapitre que le lecteur comprend entièrement
qu'un chapitre exhaustif qu'il abandonne.

Trois demandes pédagogiques explicites, qui deviennent la troisième partie du rapport : la
taxation des retraités, le danger des taux marginaux élevés, et le danger d'un impôt du type
de celui que propose Gabriel Zucman.

### Ce que ces réponses impliquent, et que je signale

Compter toute cotisation comme un impôt est un choix défendable dans un exercice « from
scratch », parce qu'il garde dans le champ la question de savoir s'il faut une épargne retraite
obligatoire et publique. Mais il faut assumer sa conséquence : le coin fiscal français ainsi
mesuré est surestimé par rapport à un pays dont les retraites sont capitalisées, et une partie
des comparaisons internationales devient trompeuse si on ne le dit pas. La figure
`p2_salaire_pension.png` montre exactement ce que cette convention décide à elle seule.

Renoncer à tout chiffrage distributif a un coût précis : le rapport ne pourra pas démontrer
qu'une réforme est compensable, seulement l'affirmer. Or l'argument central de Mirrlees sur la
TVA — supprimer les taux réduits et compenser par le barème direct — ne vaut que si la
compensation est chiffrée. Je retiens donc un minimum qui ne coûte presque rien : les
distributions par décile déjà publiées par l'Insee, la DREES et l'IPP, qui ne sont pas des
microdonnées.

La composition de l'équipe ne change aucune conclusion, mais elle change ce qu'il faut défendre.
Quand les recommandations d'un rapport coïncident avec les préférences connues de ceux qui le
publient, la charge de la preuve monte au lieu de baisser : le lecteur hostile y verra un
plaidoyer, et le lecteur favorable ne le lira pas assez sévèrement. La consigne est donc que
l'orientation ne se voie pas, et le seul moyen fiable d'y parvenir n'est pas d'adoucir le style.

**C'est de laisser les conclusions inconfortables se tenir.** La théorie de la taxation optimale
produit plusieurs recommandations qu'un lectorat de centre droit n'attend pas, et ce sont elles qui
établiront que le rapport n'est pas une plaidoirie. L'impôt le plus efficient qui existe est un
prélèvement annuel sur la valeur du terrain, et il tombe intégralement sur les propriétaires
actuels par capitalisation. La non-taxation du loyer imputé des propriétaires occupants est une
subvention massive et régressive. La suppression des taux réduits de TVA n'a de sens
qu'accompagnée d'une hausse chiffrée des transferts, faute de quoi elle est exactement l'erreur
contre laquelle Mirrlees met en garde. Uniformiser le prix du carbone revient à le relever là où il
est quasi nul, c'est-à-dire sur l'industrie et l'agriculture. Et le niveau global de prélèvement
n'est pas le premier problème français, ce qu'un rapport de ce bord est tenté de faire passer au
premier plan.

Symétriquement, les recommandations qui vont dans le sens attendu — supprimer les prélèvements sur
les intrants, exonérer le rendement normal, corriger le biais d'endettement — doivent être les plus
solidement établies et les plus précisément chiffrées du rapport, puisque ce sont celles qu'on
soupçonnera d'être là par préférence.

**Dispositif retenu : chaque chapitre de réforme porte un passage « l'objection la plus forte ».**
Il énonce le meilleur argument contre la recommandation, pas une liste de limites de politesse, et
il dit ce qui le ferait l'emporter. C'est la contrepartie du fait que personne, dans l'équipe, ne
jouera ce rôle spontanément.

Mobilité des bases traitée en contrainte forte : c'est le choix le plus exposé du cadrage. Le
rapport affirmera que certains taux sont inatteignables parce que les bases partiraient, ce qui
est vrai mais invérifiable au niveau de preuve que nous nous donnons. Je dirai donc systématiquement
sur quoi repose chaque affirmation de mobilité, et je distinguerai les cas documentés — footballeurs
danois, inventeurs, régimes d'impatriés — des extrapolations.

Toutes les questions sont tranchées. Reste à nommer les sujets à traiter avec précaution,
question 19.

---

## A. Ce que le rapport est

**1. Qui le lit ?** Le registre, la longueur des démonstrations et la place des annexes
techniques ne sont pas les mêmes selon que la cible est un lectorat académique, une institution
qui doit pouvoir s'en servir, ou toi-même pour clarifier ta propre position. Dans le premier cas
il faut une défense complète de chaque hypothèse d'identification ; dans le deuxième, un chapitre
par bloc avec des recommandations numérotées et chiffrées ; dans le troisième, on peut laisser des
questions ouvertes en l'état.

*Défaut :* rapport destiné à être lu par des économistes et des praticiens de la politique
fiscale, démonstrations dans le texte, détails techniques en encadrés et annexes.

**2. Statut institutionnel.** Est-ce un travail personnel, ou quelque chose qui pourrait circuler
dans un cadre professionnel ? Cela décide si certaines positions doivent être présentées comme des
arbitrages documentés plutôt que comme des recommandations.

*Défaut :* travail personnel, liberté de conclusion, mais aucune affirmation qui ne tienne devant
un référé technique.

**3. Prend-il des positions ?** Une Mirrlees Review tranche : taux unique de TVA, fusion des deux
impôts sur le revenu, allocation pour rendement normal. L'alternative est d'exposer les arbitrages
sans choisir. La première option est plus utile et plus risquée.

*Défaut :* le rapport tranche, et dit explicitement à quelle condition empirique sa conclusion
s'inverserait.

---

## B. Le périmètre de l'exercice

**4. La contrainte de rendement est-elle fixée ?** C'est la question la plus structurante. La
Mirrlees Review raisonnait à rendement constant : elle demandait comment lever la même somme
mieux, pas combien lever. Si on fixe le rendement à 43,5 % du PIB, l'exercice porte uniquement sur
la structure, et chaque réforme doit être gagée. Si on laisse le niveau libre, il faut une théorie
du niveau optimal de dépense publique, c'est-à-dire un autre rapport, et bien plus de cent
cinquante pages.

*Défaut :* rendement constant comme scénario central, plus une variante chiffrée « même structure,
rendement inférieur de deux points » pour montrer ce que le niveau coûte indépendamment de la
structure.

**5. Les transferts sont-ils dans le périmètre ?** Un taux marginal effectif n'a aucun sens si on
exclut le RSA, la prime d'activité et les aides au logement : l'essentiel des pics du barème
français vient de leur dégressivité, pas de l'impôt. Mais les inclure ajoute un chapitre lourd et
déplace l'objet vers « prélèvements et transferts ».

*Défaut :* les transferts monétaires sous condition de ressources sont dans le périmètre, parce
qu'ils font partie du barème ; les prestations en nature et les assurances sociales contributives
restent dehors.

**6. Les cotisations sociales sont-elles un impôt ?** C'est la spécificité française qui n'a pas
d'équivalent britannique, et le point où le cadre de Mirrlees ne se transpose pas mécaniquement.
Mirrlees traitait les *National Insurance Contributions* comme un impôt sur le travail parce que
le lien britannique entre cotisation et droit est devenu ténu. En France, une cotisation
vieillesse achète des droits à peu près proportionnels : si l'actif perçoit ce lien, la cotisation
n'est pas un coin fiscal mais une épargne obligatoire, et elle ne distord pas l'offre de travail
de la même manière. Trois traitements possibles : tout en impôt ; séparer la part contributive de
la part redistributive et ne traiter en impôt que la seconde ; ou sortir entièrement le bloc
contributif du rapport.

*Défaut :* le deuxième. Je mesure la part contributive des 490 Md€ assis sur le travail, et je ne
traite en prélèvement distorsif que le reste. C'est un chantier à part entière, déjà identifié dans
`03_decoupages.md`, et il faut savoir s'il est au cœur du rapport ou en marge.

**7. Le système de retraite est-il redessiné ?** Distinct de la question 6 : on peut classer les
cotisations en salaire différé sans pour autant toucher aux paramètres du système. Si les
paramètres sont dans le périmètre, le rapport devient un rapport sur l'État social.

*Défaut :* paramètres pris comme donnés ; seul le mode de financement est discuté.

**8. Quel périmètre comptable ?** J'ai retenu la liste Eurostat, soit 1 270 Md€. Faut-il y ajouter
les prélèvements qui n'y figurent pas et qui fonctionnent comme des impôts : obligations d'emploi
et contributions assimilées, redevances quasi fiscales, et surtout les charges créées par la
réglementation sans passer par un prélèvement ?

*Défaut :* périmètre Eurostat pour tous les chiffres, avec un encadré nommant ce qui en est exclu
et son ordre de grandeur, sans le réintégrer.

---

## C. La norme

**9. D'où vient le jugement redistributif ?** Aucun résultat de taxation optimale n'existe sans
préférence sociale : le taux marginal optimal au sommet dépend du poids qu'on met sur un euro
supplémentaire pour un riche. Trois voies. Rester agnostique et présenter le barème optimal pour
un éventail de préférences, comme le faisait Mirrlees. Inverser le problème : prendre le système
français actuel comme s'il était optimal et en déduire les poids sociaux qu'il implique
*implicitement*, ce qui est le diagnostic le plus parlant parce qu'il révèle les incohérences —
là où les poids implicites deviennent négatifs, le système est dominé, c'est-à-dire qu'on peut
améliorer la situation de tout le monde à la fois. Ou fixer une fonction de bien-être explicite
et assumer le choix.

*Défaut :* l'inverse optimum comme diagnostic central, et l'éventail de préférences pour les
réformes proposées. Je ne fixe pas de fonction de bien-être à ta place.

**10. Quelle unité d'imposition ?** La France impose le foyer avec quotients conjugal et familial ;
le Royaume-Uni impose l'individu, et Mirrlees n'a donc pas eu à traiter la question. L'imposition
jointe fait peser sur le second apporteur de revenu un taux marginal calé sur le revenu du premier,
ce qui est précisément là où l'élasticité de l'offre de travail est la plus forte. C'est un des
rares endroits où un gain d'efficience et un gain d'équité entre conjoints vont dans le même sens,
et c'est politiquement explosif.

*Défaut :* un chapitre entier, individualisation comme point de départ, et chiffrage des perdants,
qui sont nombreux et identifiables.

**11. Quelle place pour la mobilité ?** Les résultats classiques sont établis en économie fermée.
Des bases mobiles — profits, hauts revenus, patrimoine financier — changent les conclusions sur le
capital et sur le sommet du barème. Faut-il prendre les élasticités de mobilité au sérieux, et
avec quel niveau de preuve ?

*Défaut :* oui, mais en distinguant ce qui est solidement estimé de ce qui est supposé, et en
donnant le taux au-delà duquel la conclusion change plutôt qu'un chiffre unique.

---

## D. Les contraintes

**12. Que signifie « from scratch » vis-à-vis du droit ?** Le droit de l'Union contraint la
structure des taux de TVA et interdit certaines différenciations ; la jurisprudence
constitutionnelle borne les taux marginaux agrégés et impose l'égalité devant les charges
publiques. Soit on construit le système idéal en ignorant ces bornes et on les traite ensuite, soit
on les tient pour des données.

*Défaut :* système idéal construit sans ces bornes, puis un chapitre « la version faisable » qui
dit ce que chaque contrainte coûte et laquelle mériterait d'être renégociée.

**13. Et la décentralisation ?** L'autonomie financière des collectivités est un principe
constitutionnel, et la réforme de la fiscalité locale des dernières années a supprimé des assiettes
sans en créer. Faut-il un échelon local doté d'un pouvoir de taux, et sur quelle assiette ?

*Défaut :* oui, principe retenu — une assiette immobile et visible pour le local — et un chapitre
dédié.

---

## E. Le niveau de preuve

**14. Quelles microdonnées as-tu accès ?** C'est la contrainte matérielle la plus sérieuse. La
quatrième partie du plan promet des gagnants et des perdants mesurés par simulation. Cela demande
des données individuelles de revenu et de consommation. L'enquête Revenus fiscaux et sociaux et
l'enquête Budget de famille ne sont pas en accès libre. As-tu une habilitation CASD, un accès
Progedo, ou un accès par ton institution ? Faute de quoi, je travaille sur données agrégées par
décile, ce qui donne des ordres de grandeur mais pas de perdants nommés.

*Défaut :* je suppose que non, et je construis la quatrième partie sur des cas types et des
distributions agrégées, en signalant partout ce qu'un accès microdonnées changerait.

**15. Jusqu'où va la simulation ?** Trois niveaux : raisonnement théorique avec ordres de grandeur ;
simulation statique qui calcule l'effet mécanique d'une réforme sans réaction de comportement ;
simulation avec réactions calibrées sur des élasticités. Le deuxième niveau est atteignable avec
OpenFisca-France, qui est ouvert. Le troisième suppose d'assumer des élasticités et devient
rapidement fragile.

*Défaut :* statique chiffré, plus un encadrement de l'effet comportemental par des bornes basse et
haute d'élasticité plutôt qu'un point central.

**16. Quel traitement de la littérature empirique française ?** Il existe un corpus français
estimé sur données françaises — réactions à l'impôt sur le revenu et aux cotisations, transmission
de la TVA dans les prix, effet des allègements sur l'emploi, barèmes effectifs par décile. Veux-tu
que je le mobilise au niveau d'un referee report pour les papiers qui portent une conclusion, ou
d'un résumé pour tous ?

*Défaut :* lecture approfondie pour les papiers dont dépend une recommandation chiffrée, mention
simple pour le reste.

**17. Quels pays servent de comparateurs, et quelles maquettes de référence ?** Deux choses
différentes. Les comparateurs : le Danemark et la Suède pour l'impôt dual sur le revenu, les
Pays-Bas pour le système par boîtes, l'Estonie pour la taxation des seuls profits distribués, le
Royaume-Uni comme terrain d'origine de la Review. Les maquettes théoriques déjà construites par
d'autres : la *X-tax* de Bradford, l'impôt sur les flux de trésorerie du comité Meade, l'impôt dual
nordique, l'allocation pour rendement normal retenue par Mirrlees. Le rapport doit-il se situer par
rapport à ces maquettes, ou construire la sienne ?

*Défaut :* les quatre comparateurs, et un chapitre qui positionne explicitement la proposition
française par rapport aux quatre maquettes, parce que ne pas le faire exposerait à réinventer une
solution déjà critiquée.

---

## F. Les points chauds

**18. Sur quels sujets veux-tu une position tranchée ?** Les candidats, par ordre de sensibilité
décroissante : la taxation des transmissions, qui est le point où l'écart entre ce que dit la
théorie et ce que supporte l'opinion est le plus large ; la taxation du stock de patrimoine ; les
taux réduits de TVA ; la fusion de l'impôt sur le revenu et de la contribution sociale généralisée ;
l'unité d'imposition ; le logement, c'est-à-dire la non-taxation du loyer imputé des propriétaires
occupants et les valeurs locatives de 1970 ; les impôts de production ; le prix du carbone sur les
carburants. Dis-moi lesquels doivent trancher et lesquels peuvent rester en arbitrage documenté.

*Défaut :* le rapport tranche partout, et consacre un développement proportionné à la résistance
attendue — donc le plus long sur les transmissions et le logement.

**19. Y a-t-il des sujets à traiter avec précaution ?** Pour des raisons institutionnelles ou
parce que tu as déjà une position publique dessus.

*Défaut :* aucun, et je te signale si j'arrive sur un terrain qui me paraît en relever.

---

## G. Méthode de travail

**20. Quel rythme de livraison ?** Un chapitre à la fois, soumis avant de passer au suivant ? Ou
une partie entière ? Les quatre fichiers actuels sont des blocs de travail, pas des chapitres
rédigés au format final.

*Défaut :* un chapitre à la fois, avec les figures, et je ne passe au suivant qu'après ton retour.

**21. Qui rédige ?** Je peux produire le socle quantitatif et les figures et te laisser le texte,
ou rédiger les chapitres que tu corriges. Les deux demandent un travail très différent de ma part.

*Défaut :* je rédige, tu corriges.

**22. Quel format final ?** Les fichiers sont en Markdown dans le dépôt. Cent cinquante pages avec
figures numérotées, renvois et bibliographie suggèrent plutôt LaTeX avec une compilation en PDF.
Faut-il basculer maintenant, tant que le volume est faible ?

*Défaut :* on reste en Markdown pour la rédaction, avec une structure de fichiers qui permet une
conversion LaTeX sans réécriture, et on bascule quand une partie entière est stabilisée.

**23. Quelle règle de traçabilité ?** Aujourd'hui, tout chiffre doit renvoyer à un fichier de
`donnees/`, et les affirmations non sourcées portent la marque **[à sourcer]** — il en reste huit
dans le chapitre 3. Je maintiens cette règle, et je ne publie pas un chapitre qui en contient
encore ?

*Défaut :* oui, règle maintenue, et un chapitre n'est considéré comme fini que sans marque
résiduelle.

---

## Ce que je fais en attendant

Les chantiers suivants ne dépendent d'aucune de ces réponses, et je peux les lancer sans risque de
travail perdu : la base de taux effectifs d'imposition des sociétés de la Commission, pour le
diagnostic dette contre fonds propres ; le partage du foncier entre terrain et bâti dans les 50 Md€
d'impôts sur la détention ; les prix implicites du carbone par énergie et par usage ; et le
nommage des 27 Md€ que la liste Eurostat laisse en « autres taxes ».
