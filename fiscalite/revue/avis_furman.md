# Avis interne sur le fond : « Taxer mieux plutôt que davantage »

*16 novembre 2026. Avis interne, non publié. Version relue : `synthese/note-reforme-fiscale.pdf` (26 pages), avec
`synthese/parties/*.tex`, `revue/methode_v2.md` et les sorties du modèle (`synthese/sorties/`). L'avis applique la
grille d'analyse publique de Jason Furman : pragmatisme de centre gauche, arithmétique budgétaire, analyse
distributive, préférence pour la déduction immédiate de l'investissement plutôt que pour la baisse du taux de l'IS,
attention aux coûts de transition, au réalisme des effets de croissance et aux effets d'annonce. Il ne parle pas en
son nom et ne lui prête aucune citation.*

*Repères : **[N]** chiffre de la note ; **[M]** sortie du modèle du dépôt ; **[R]** calcul de relecture avec le
modèle et la grille de barèmes de la note (`synthese/modele_purs.py`, `architectures_ircsg.py`), jeu central sauf
mention, à refaire par l'auteur avant tout usage ; **[W]** vérifié en ligne (sources en fin d'avis).*

## Verdict en trois phrases

1. La méthode tient : la note mesure le gain par rapport à l'existant et à recette égale, sépare la réaction réelle
   de la réaction déclarative et ne compte pas les recettes comportementales. Elle préfère aussi la déduction
   immédiate à une baisse du taux de l'IS et garde le PFU stable. Je n'y ai pas trouvé d'erreur de calcul qui
   renverserait ses conclusions.
2. Le cœur de la proposition IR-CSG pose en revanche un vrai problème de fond. Sous la contrainte affichée (« aucun
   décile ne bouge de plus de 500 € »), le barème retenu baisse fortement l'impôt des hauts salaires : entre 150 000
   et 400 000 € brut, leur taux marginal passe d'environ 45-54 % à 32-37 %, et le 1 % du haut paie 2,7 Md€ de
   moins. Ce sont les retraités qui financent, pour 15 Md€. Plus de la moitié du gain d'efficacité affiché vient
   justement de cette baisse au sommet, c'est-à-dire de l'élasticité que personne n'a mesurée.
3. La note laisse aussi s'éteindre la contribution exceptionnelle des grands groupes sans compter ces 5 à 7 Md€ dans
   son bilan, et elle ne tranche pas sur le report d'apport-cession. Le paquet risque donc d'être lu comme une
   baisse d'impôt pour le haut payée par les retraités. Ce n'est pas défendable dans cette grille, et c'est inutile :
   les corrections proposées ci-dessous coûtent peu en efficacité.

## 1. Grosses erreurs de fond, par gravité

### 1.1 Le barème proposé baisse fortement l'impôt des hauts salaires, et c'est de là que vient l'essentiel du gain

**Ce que dit la note.** Le barème monte de 14 % au premier euro à 30 % à 45 000 €, « puis une montée lente jusqu'à
50 % à 1 M€ » (§ 1.5). Il est choisi comme le plus efficace parmi ceux qui ne changent la charge moyenne d'aucun
décile de plus de 500 € et « n'alourdissent pas » celle du 1 % du haut. Le gain est de 4,9 Md€ (63 % du gain
atteignable). La franchise de 4 000 € est présentée comme une mesure « pour l'emploi ». Le bilan d'ensemble (§ 5)
écrit : « Le dirigeant salarié. Son taux marginal passe de 55 % environ (avec la CEHR) à 50 %. »

**Pourquoi c'est une erreur ou un risque majeur.**

- *Le profil réel des taux marginaux n'est pas montré, et la phrase du § 5 le décrit mal.* Dans le code
  (`ir_csg/exercices.py`, `bareme_lineaire`), le taux monte en ligne droite *en euros* entre 45 000 € et 1 M€. Il
  vaut donc 31,4 % à 100 000 € de revenu imposable, 32,4 % à 150 000 €, 34,5 % à 250 000 € et 39,7 % à
  500 000 € [R]. Le prélèvement marginal actuel d'une personne seule salariée (IR + CSG + CRDS, sans la CEHR, par
  euro de revenu après cotisations, OpenFisca) est de 35,6 % jusqu'à 100 000 € brut. Il atteint 44,7 % à 150 000 €,
  48,7 % à 200 000 €, 52,4 % à 250 000-300 000 € et 54,4 % à 400 000 € [M]. La baisse va donc de 12 à 18 points
  entre 150 000 et 400 000 € brut. Le passage « de 55 à 50 % » ne vaut qu'au-delà de 1 M€ de revenu.
- *Des déciles stables ne veulent pas dire des gagnants modestes.* Sur les cas-types du modèle, une personne seule
  salariée paie 4 300 € de moins à 100 000 € brut (−17 %), 9 200 € de moins à 150 000 € (−21 %), 31 000 € de moins
  à 300 000 € (−28 %) et 48 000 € de moins à 400 000 € (−30 %). Ces montants ne comptent pas la CEHR, qui
  disparaît aussi. Dans le même temps, un retraité seul de 74 ans à 17 000 € de pension, qui ne paie rien
  aujourd'hui, paie 1 260 € (7,4 % de sa pension), et le salarié au Smic paie 61 € de plus [R].
- *Le gain vient surtout du haut, pas de l'emploi.* La sortie du modèle décompose les 4,9 Md€ ainsi : 3,4 sur la
  marge intensive, dont 1,7 pour les 90-99 % et 1,1 pour le 1 %, et 1,4 seulement sur la participation [M]. Le
  dixième du haut fournit donc 2,8 Md€, 57 % du gain, avec une élasticité du revenu « réel » de 0,10 que
  `methode_v2.md` reconnaît n'avoir « aucune séparation mesurée du réel et du déclaratif ». La participation
  rapporte même moins dans la proposition (1,4) que dans le barème neutre sans franchise (1,8), parce que le taux
  d'entrée passe de 2 % à 14 % après la franchise. L'affirmation « aucun gain ne repose sur une réaction
  déclarative » est vraie par construction. Mais le gain repose sur la marge la moins documentée, et le récit de
  la note (« l'emploi et les familles se financent pour l'essentiel sur les pensions ») ne décrit pas la
  proposition : ce sont les familles et les hauts salaires qui se financent sur les pensions.
- *Le choix coûte cher pour peu de gain.* La consigne du commanditaire est de ne pas *alourdir nettement* la
  facture des grandes fortunes, pas de l'*alléger*. Dans la grille de barèmes de la note, le plus efficace des
  barèmes qui laissent le 1 % à peu près neutre (+0,1 Md€) est : 14 % au premier euro, 28,3 % à 45 000 €, 50 %
  dès 250 000 €. Il donne un gain de 4,5 Md€ (2,1 à 10,2) au lieu de 4,9 (2,3 à 11,1) [R]. Les 2,7 Md€ rendus au
  1 % n'achètent donc que 0,3 Md€ de gain (0,2 à 0,9 selon le jeu), environ 12 centimes par euro transféré. Même
  dans ce barème, un salarié seul à 300 000 € brut paie encore 15 000 € de moins qu'aujourd'hui [R]. Avec,
  en plus, un abattement de 5 % sur les pensions, le gain est de 4,3 Md€ (2,0 à 9,8), les retraités paient
  11,8 Md€ de plus au lieu de 15,2, et le 1 % paie 0,4 Md€ de moins [R]. Avec l'abattement de 10 %, le gain est de
  3,9 Md€, la hausse des retraités tombe à 8,6 Md€ et le 1 % reste neutre [R].
- *Au sommet, l'incertitude va dans le mauvais sens.* La note reconnaît que sa convention centrale (taux actuel de
  32 à 37 %) est « difficile à concilier avec le barème ». Dans la convention « haut », plus proche du droit, le 1 %
  gagne 4,5 Md€ et non 2,7. Les foyers de 0,9 à 9 M€ gagnent alors 6 à 13 points de leur revenu, et la recette
  n'est tenue qu'en relevant le taux du milieu de 30,3 à 31,1 % [M, `controle_hauts_purs.txt`]. La CEHR n'est pas
  comptée dans ces écarts.

**Ce qu'il faudrait changer.**

1. Remplacer la contrainte « le 1 % ne monte pas » par « le 1 % ne bouge pas » (par exemple ±0,5 Md€). C'est une
   seule ligne dans `architectures_ircsg.py` : `abs(c["top1_Md"]) <= 0.5` au lieu de `c["top1_Md"] <= 0`.
   Présenter l'écart de gain comme le prix d'une baisse au sommet. Le barème retenu peut aussi utiliser cette marge
   pour réduire la charge des retraités.
2. Montrer le profil des taux marginaux jusqu'à 500 000 € et les cas-types à 150 000, 300 000 et 1 M€ brut, CEHR
   comprise. Corriger la phrase « 55 → 50 % ».
3. Décomposer le gain en participation, milieu et dixième du haut dans le tableau 1, et dire en clair que la part
   du haut repose sur une élasticité supposée.
4. Arrêter le barème seulement après le calage de la part des revenus au PFU au sommet, que la note annonce
   elle-même comme « le premier travail à faire ».

### 1.2 La recette « constante » dépend d'une référence qui fait disparaître 5 à 7 Md€, et aucune transition d'ensemble n'est chiffrée

**Ce que dit la note.** Tableau 4 : la contribution exceptionnelle sur les grands groupes « s'éteint (référence) :
−7 par rapport à 2026, −5 par rapport au PLF 2027 ». Tableau 5 : « Ensemble : 0 » ; pour l'IS, « 0 en régime
permanent ; dette de transition de 2 à 32 ».

**Pourquoi c'est une erreur ou un risque majeur.**

- Prendre le droit permanent comme référence est une convention défendable, à condition de l'afficher. Ici, par
  rapport au budget réellement en discussion, le paquet n'est pas à recette constante. Il comporte une baisse de
  5 Md€ par an (7 par rapport à 2026) pour environ 450 groupes, sans financement. Le déficit est encore au-dessus de
  3 % du PIB : c'est la condition d'extinction de la CDHR que la note cite elle-même. Dans ce contexte, cette
  baisse n'est pas un détail de présentation.
- Cette baisse est en outre une baisse de taux légal : de 36,1 % à 25,8 % pour les plus grands groupes. C'est
  exactement le type de mesure que le § 3.2 juge le moins efficace, parce qu'elle allège les profits du capital
  déjà installé et les rentes. Une partie revient aux actionnaires des grands groupes : elle s'ajoute donc au
  problème distributif du § 1.1.
- La première année, en reprenant les chiffres de la note : déduction de 50 %, −7 à −7,8 Md€ ; financement par
  l'assiette, +3,5 à +4,9 ; contribution exceptionnelle, −5 à −7. Cela fait un écart de 7 à 11 Md€ en 2027
  avant toute réaction. La revue transversale du 15 novembre demandait déjà un tableau année par année. Il manque
  toujours.

**Ce qu'il faudrait changer.** Donner le tableau 5 avec deux références, le droit permanent et le PLF 2027, et une
ligne par année de 2027 à 2032 pour l'ensemble des quatre réformes, en comptabilité nationale. Il faut ensuite soit
financer la fin de la contribution exceptionnelle (par exemple en l'éteignant au rythme où la dette de transition de
l'IS est remboursée, ou en la remplaçant par une mesure permanente d'assiette), soit écrire qu'il s'agit d'une baisse
d'impôt non financée de 5 Md€. Séparer enfin la dette de transition du coût permanent dans le solde, et pas
seulement en valeur actuelle.

### 1.3 Report d'apport-cession : la note identifie la plus grosse niche du haut, puis ne choisit pas, avec un argument en partie faux

**Ce que dit la note.** Elle présente trois traitements sans en choisir aucun (tableau 5 : « selon le traitement du
report »). Elle écarte l'expiration à toute transmission parce qu'elle « taxe une structure plutôt qu'un gain
réalisé ». Elle écrit elle-même que « le report ne devient une exonération que si la sortie n'a jamais lieu, ce que
permet l'effacement au décès ». Le stock atteint 173 Md€ en 2024, et 84 foyers concentrent 23,5 Md€ des entrées de
2023.

**Pourquoi c'est une erreur ou un risque majeur.**

- Dans le cas que la note décrit (apport, *puis vente*), le gain est réalisé, puisque l'apport est un échange et que
  la holding a encaissé le prix. C'est l'impôt qui est différé. Le cas de la holding Dutreil qui n'a rien vendu
  est l'exception : il se traite par un paiement différé ciblé, pas en renonçant à la règle.
- L'effacement au décès est l'équivalent français du *step-up in basis* américain. Dans la grille de centre gauche,
  c'est la première niche à fermer : en 2015, l'administration Obama, dont Furman présidait le Council of Economic
  Advisers, a proposé de traiter le décès comme une réalisation, avec une franchise [W].
- La variante de repli de la note (report transmis aux héritiers) est la plus fragile. Les États-Unis ont voté le
  *carryover basis* en 1976 et l'ont abrogé en 1980, avant son application, après l'avoir jugé inapplicable [W].
  Elle prolonge en outre le report sans limite dans une holding.
- La contrainte du commanditaire porte sur *la somme* des réformes. La fusion rend 2,7 Md€ au 1 % (4,5 dans la
  convention « haut »). Fermer l'effacement rapporterait au moins 2 Md€ par an en régime de croisière selon la note,
  et ramènerait le haut à peu près à la neutralité sur l'ensemble du paquet. Sans choix sur ce point, la réforme 4
  se résume à « PFU maintenu ».

**Ce qu'il faudrait changer.** Choisir. Dans cette grille, le bon choix est la fin de l'effacement au décès et à la
donation, avec un paiement étalé et différé tant que les titres d'une société opérationnelle ne sont pas cédés. À
défaut, l'expiration quand la holding vend et garde le produit en actifs passifs, et le report transmis dans les
autres cas. Compter la recette dans le tableau 5 et dans le bilan des grandes fortunes.

### 1.4 Immobilier : pendant la transition, la baisse des droits est financée par une hausse de l'impôt le plus régressif, et rien ne garantit que cette transition finisse

**Ce que dit la note.** Les droits de mutation baissent dès l'annonce. « Le temps d'établir les valeurs », la baisse
est financée par une hausse « uniforme et temporaire » de 20 à 24 % de la taxe foncière actuelle. Le Bade-Wurtemberg
a mis plus de quatre ans entre sa loi et le premier impôt, et la révision des valeurs locatives de 1970 « a été
reportée à 2031 ».

**Pourquoi c'est une erreur ou un risque majeur.** La baisse des droits est immédiate et presque irréversible. Le
financement définitif dépend d'une réforme d'évaluation que la France repousse depuis cinquante ans. Le tableau 3
de la note montre ce que donne la taxe relevée : 0,65 % de la valeur dans les communes pauvres, 0,22 % dans les
communes riches. Si la nouvelle assiette prend du retard, le résultat durable est une baisse des droits plus une
hausse de l'impôt le plus régressif du système. Cette hausse frappe les retraités propriétaires l'année même où la
fusion leur demande 15 Md€ de plus. En outre, le seuil d'exonération des plus de 75 ans dépend du revenu fiscal de
référence, que la fusion modifie.

**Ce qu'il faudrait changer.** Ne pas adosser la transition aux valeurs de 1970. Une assiette provisoire du sol à la
commune (prix des terrains de la commune tirés de DVF, multiplié par la surface cadastrale de la parcelle, comme dans
le modèle de la note) est à expertiser juridiquement, mais elle serait déjà dans la bonne direction. Il faut aussi
une extinction automatique de la surtaxe à date fixe, avec une clause de repli qui ne soit pas la base de 1970. Le
report de paiement doit être proposé par défaut aux propriétaires âgés modestes pendant la transition. L'autre
solution (baisser une partie des droits tout de suite, le reste à l'entrée en vigueur de la nouvelle assiette)
réduit le risque budgétaire mais recrée l'attente que la note veut éviter : il faut le dire et trancher.

## 2. Choix contestables mais défendables

- **Taxer les pensions comme les salaires (+15 Md€).** C'est cohérent : équité horizontale, base peu réactive, et un
  effet favorable sur l'âge de départ, que la note ne compte pas. Mais une bonne part du « gain permanent » est un
  prélèvement de transition sur les retraités actuels. En régime permanent, l'impôt sur les pensions futures est un
  impôt différé sur le travail des actifs d'aujourd'hui. La note compte d'ailleurs les cotisations « sans contrepartie
  de droits » dans le coin fiscal : alourdir l'impôt sur les pensions réduit cette contrepartie. Et chaque mesure
  d'atténuation (quatre ans de transition, petites pensions) rogne exactement le gain affiché. À présenter comme un
  gain obtenu avec des comportements myopes, avec une variante où l'impôt futur sur les pensions compte en partie
  comme un impôt sur le travail.
- **Franchise par enfant plutôt que chèque : la comparaison se fait à coût inégal.** Le tableau 1 juge le chèque de
  742 € « moins favorable » aux familles. Mais il coûte 0,9 point, contre 1,5 pour la franchise. Dans la
  configuration de la proposition, un chèque remboursable de **même coût** vaut 1 219 € par enfant [R]. Avec le
  barème réoptimisé sous la même contrainte, les parents isolés gagnent 520 € au lieu de 234 €, un couple avec deux
  enfants à 30 000 € gagne 2 690 € au lieu de 1 930 €, et la moyenne des couples avec deux enfants est à peu près la
  même (−1 280 contre −1 195 €). Le gain d'efficacité tombe en revanche à 4,2 Md€ au lieu de 4,9 [R]. L'arbitrage
  est réel, mais il doit être présenté ainsi. La franchise vaut 6 000 € fois le taux marginal du parent, soit
  jusqu'à 3 000 € par enfant au taux de 50 %. Elle n'est pas remboursable : elle est perdue pour les parents dont le
  revenu imposable est inférieur à la franchise.
- **Imposition individuelle.** Elle est bonne pour les seconds revenus. Mais la note juge elle-même le risque
  constitutionnel « sérieux ». La proposition devrait donc aussi être chiffrée dans sa variante de repli (quotient
  conjugal), et pas seulement le barème neutre.
- **Déduction immédiate à 50 % jusqu'en 2032, puis 100 %.** Un palier annoncé crée un effet d'annonce : attendre
  janvier 2033 fait gagner τ(1 − z), soit environ 1,2 à 1,9 % du prix d'une machine (z de 0,925 à 0,95 à 50 %)
  [R]. Les achats de fin 2032 seront décalés, et l'étude de Zwick et Mahon que la note cite montre que les
  entreprises jouent ce calendrier. La note ne le mentionne pas. Une montée par paliers annuels de quelques points
  rend l'incitation à attendre négligeable. On peut aussi passer à 100 % tout de suite pour les PME, chez qui l'effet
  sur la trésorerie est le plus fort et le coût le plus faible.
- **Fin du taux réduit de l'IS pour financer la déduction.** C'est défendable, puisque c'est en grande partie un
  transfert inframarginal. Mais avec les chiffres de la note, l'effet net de la réforme de l'IS sur le bien-être va
  de +0,1 à −0,7 Md€. Le total « environ 7 » compte zéro pour cette perte. Il faut l'écrire : l'intérêt de la réforme
  est la stabilité et le coût budgétaire, pas l'efficacité.
- **Fusion étalée sur quatre ans.** C'est raisonnable pour les retraités. Mais au sommet, un taux marginal qui
  baisse d'environ quatre points par an pousse les dirigeants à reporter leur rémunération. La note documente
  elle-même ce comportement pour les dividendes en 2013 et en 2018. La recette ne restera pas « à peu près constante
  chaque année ». Le problème disparaît en grande partie si l'on corrige le barème comme au § 1.1.
- **Prémisse de la contrainte sur les grandes fortunes.** Les éléments que la note cite (départs de 0,02 à 0,23 %
  du centile du haut par point d'imposition effective, Bach et al., 2025) ne justifient pas d'aller au-delà de la
  neutralité. C'est un argument de plus pour viser « inchangé » plutôt que « en baisse ».

## 3. Ce qui manque

- **Incidence combinée par âge et par patrimoine.** Il faudrait voir ensemble ce que paie le retraité propriétaire :
  fusion, surtaxe foncière de transition, taxe sur le sol, exonération des plus de 75 ans. Il faudrait aussi voir ce
  que paient les chômeurs : leurs allocations entrent dans l'assiette sans franchise d'activité, et une version
  antérieure du modèle chiffrait leur hausse à 3 Md€ (`ir_csg/note-efficace.tex`). La version actuelle ne les isole
  pas. Une hausse de l'impôt sur l'assurance chômage est une baisse cachée du taux de remplacement : elle doit être
  dite.
- **Affectation et droit applicable.** La fusion réunit une recette de l'État (IR), de la Sécurité sociale (CSG) et
  de la CADES (CRDS). La CADES est tenue par une règle organique : son amortissement ne doit pas dépasser fin 2033
  [W]. La note ne dit pas comment l'impôt fusionné est partagé, ni dans quelle loi (LFI ou LFSS) il est voté. Le
  droit européen soulève une autre question. En 2000, la CJCE a jugé contraire au règlement de coordination des
  régimes de sécurité sociale le prélèvement de la CSG et de la CRDS sur des résidents qui travaillent et sont
  affiliés dans un autre État membre [W]. Un impôt de résidence unique change donc qui paie (frontaliers, retraités non résidents) et fait
  entrer les 132 Md€ de CSG dans le champ des conventions fiscales. L'effet sur la recette est à expertiser.
- **Tableau des recettes année par année et par administration** pour l'ensemble du paquet (voir § 1.2).
- **Déduction immédiate et déductibilité des intérêts.** Une machine financée par emprunt avec déduction immédiate a
  un taux marginal effectif négatif. En calcul illustratif (taux d'intérêt de 5 %, amortissement sur sept ans,
  IS à 25 %), il passe d'environ −10 % aujourd'hui à environ −33 % [R]. Il faut dire si le plafonnement actuel des
  charges financières suffit (il ne touche probablement pas la plupart des PME, ce qui reste à vérifier), ou s'il
  faut l'adapter.
- **L'argument de stabilisation.** Les droits de mutation suivent le cycle immobilier, alors que les départements
  financent des dépenses sociales qui montent en bas de cycle. Remplacer la moitié des droits par une recette
  stable sur le sol est un argument fort pour la réforme, et il est absent.
- **L'arbitrage entre salaire et dividende après la fusion.** Avec le barème proposé, un dirigeant à 300 000 €
  paierait environ 35 % sur un euro de salaire en plus, hors cotisations, contre 48,6 % sur un euro de dividende.
  Aujourd'hui, c'est environ 52 % contre 48,6 %. Le sens de l'optimisation s'inverse, et la note ne dit pas ce que
  cela fait à la recette de l'IS et du PFU.
- **La marge de l'âge de départ en retraite**, qui joue en faveur de la fusion mais n'est pas comptée.

## 4. Ce qui est bien vu

- **La méthode.** Le gain est mesuré par rapport à l'existant, à recette égale, avec trois jeux d'hypothèses. La
  note refuse de laisser l'optimiseur choisir et montre que les rendements sont décroissants : environ deux tiers du
  gain atteignable sans bouleverser la répartition. Elle ne finance rien avec les 1,9 à 5,7 Md€ de recettes
  comportementales. C'est exactement la prudence budgétaire qu'on attend.
- **La modestie sur la croissance.** Elle annonce 0,2 % du PIB, avec une fourchette d'un facteur six, et non un
  « choc de croissance ». Pour l'IS, elle distingue le gain de production (0,1 % du PIB) du gain de bien-être
  (0,05 à 0,16 Md€) : le capital supplémentaire doit être rémunéré.
- **L'IS.** La note préfère la déduction immédiate à la baisse du taux et l'explique bien : la baisse du taux allège
  les profits du capital installé et les rentes. Elle la finance par l'assiette plutôt que par un taux à 28 %,
  distingue le coût de transition du coût permanent et nomme les perdants (professions libérales, petites holdings).
- **Le PFU.** La note refuse de le baisser : 44 % du gain irait au centile du haut, sans effet réel mesuré après
  2018. Elle lit correctement les épisodes de 2013 et 2018 comme un report des distributions plutôt qu'une perte
  d'activité.
- **L'immobilier.** La revue des études est solide et honnête : capitalisation, régressivité des évaluations de
  masse, Pittsburgh contre Philadelphie, verrou de la Proposition 13. La note refuse aussi la réévaluation à chaque
  vente.
- **La franchise d'activité et la suppression des marches de CSG des retraités.** La direction est bonne, même si,
  dans la proposition finale, la franchise ne fait pas ce que le texte lui attribue (§ 1.1).
- **La transparence.** Le transfert vers les retraités est écrit noir sur blanc, ainsi que le risque
  constitutionnel et l'incertitude sur les très hauts revenus.

## 5. Fond et présentation

Les remarques ci-dessus portent sur le fond. Quatre points de rédaction en relèvent pourtant, et doivent être
corrigés quelle que soit la réécriture en cours :

1. la phrase « 55 → 50 % » du § 5, qui décrit mal le barème ;
2. le récit « franchise pour l'emploi », que la décomposition du gain contredit ;
3. le « 0 » du tableau 5, qui cache le choix de la référence ;
4. la comparaison entre franchise et chèque, faite à coût inégal.

Les autres remarques de forme (figures, ordre des sections) relèvent de la réécriture et ne sont pas traitées ici.

## Sources vérifiées en ligne pour cet avis

- CJCE, 15 février 2000, *Commission c/ France*, C-169/98 (CSG) et C-34/98 (CRDS) : [communiqué de la Cour](https://curia.europa.eu/fr/actu/communiques/cp00/aff/cp0009fr.htm) ; [CLEISS, C-169/98](https://www.cleiss.fr/docs/jurisprudence/c169-98.html).
- CADES, règle organique d'amortissement (article 4 bis de l'ordonnance 96-50, échéance de 2033) : [Conseil d'État, avis sur les règles organiques encadrant les transferts à la CADES](https://conseil-etat.fr/avis-consultatifs/derniers-avis-rendus/au-gouvernement/avis-relatif-a-l-interpretation-des-regles-organiques-encadrant-le-transfert-de-deficits-a-la-caisse-d-amortissement-de-la-dette-sociale-cades).
- *Carryover basis* voté en 1976, reporté, abrogé en 1980 : [notes statutaires, 26 U.S.C. § 1015](https://www.govinfo.gov/content/pkg/USCODE-2011-title26/pdf/USCODE-2011-title26-subtitleA-chap1-subchapO-partII-sec1015.pdf) ; [audition du Sénat de 1979](https://www.finance.senate.gov/imo/media/doc/hrg%2096-35.pdf).
- Proposition Obama de 2015 de traiter le décès comme une réalisation : [McGuireWoods, janvier 2015](https://www.mcguirewoods.com/client-resources/alerts/2015/1/state-union-surprise/) ; [Venable, janvier 2015](https://www.venable.com/insights/publications/2015/01/state-of-the-2016-budget-preparing-for-potential-c).

## Annexe : refaire les calculs de relecture

Tous les calculs [R] utilisent le modèle de la note sans le modifier, dans le jeu central sauf mention :
`modele_purs.evalue`, `modele_purs.cas_type`, `architectures_ircsg.bareme`, `cale_t1` et `cale_d`, avec les options
de la proposition (`F=4000, fam="franchise", Fp=12500, Fp_degressif=True`).

- **1 % neutre.** On reprend la grille de barèmes de la proposition, mais on remplace la contrainte sur le 1 % par
  `abs(top1_Md) <= 0.5`. Les variantes avec abattement sur les pensions utilisent `abat_pens = 0.05` ou `0.10`, sur
  une grille réduite.
- **Chèque à coût égal.** On cherche le montant du chèque qui donne le même `cale_d` que la franchise par enfant sur
  le barème neutre, avec la franchise d'activité et les petites pensions. Ce montant remplace ensuite
  `modele_purs.CHEQUE`, et l'on refait la recherche de barème de la proposition.
- **Taux marginaux actuels.** Ils sont tirés de `ir_csg/sorties/courbes_openfisca.csv` : (impôt à brut + 1 000 €
  moins impôt à brut), rapporté à la variation du revenu après cotisations.
