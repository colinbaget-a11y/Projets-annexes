# Avis interne de relecture sur le fond : valeur actualisée, contournement, générations

*Note relue : `synthese/note-reforme-fiscale.pdf`, version du 16/11/2026, avec `synthese/parties/*.tex`, `revue/methode_v2.md` et les sorties du modèle (`synthese/sorties/`). Avis interne, non publié.*

*Cet avis adopte une grille de lecture inspirée des travaux publics de Sylvain Catherine : patrimoine retraite, transferts entre générations, situation relative des retraités, charge fiscale sur le travail. Sur demande de l'auteur, il raisonne d'abord en professeur de finance : valeurs actualisées, puis moyens légaux d'échapper à l'impôt. Ce n'est pas l'avis de Sylvain Catherine, et aucune position ne lui est prêtée.*

*Les chiffres marqués [calcul de l'avis] sont des ordres de grandeur faits pour cette relecture ; les hypothèses sont données à chaque fois et les scripts sont cités à la fin. Ils sont à refaire proprement avant toute reprise dans la note.*

---

## Verdict en trois phrases

1. La direction est bonne et la note est honnête sur ses perdants. Mais elle raisonne en flux annuels là où ses deux grandes bascules sont d'abord des **prélèvements en capital**. Les deux visent en grande partie les mêmes ménages, retraités et propriétaires âgés des zones chères : environ **160 à 190 Md€ en valeur actualisée** sur les retraités actuels, et **140 à 190 Md€** sur les propriétaires actuels de terrains. La note ne les additionne pas et ne les assume pas.
2. La réforme du capital repose sur l'idée d'**imposer le bénéfice à sa sortie des sociétés**, mais la note ne protège pas cette sortie. Purge des plus-values au décès et à la donation, exit tax levée au bout de deux ou cinq ans, cession des titres d'une holding après purge : chacune de ces voies, légale, rend la sortie exonérable. La phrase « c'est un report, pas un taux final » est fausse en valeur actualisée.
3. L'**imposition individuelle** crée une fuite nouvelle que la note ne voit pas : salarier son conjoint, attribuer les revenus des biens communs, appliquer la franchise aux loyers. Elle profitera aux foyers qui peuvent répartir leurs revenus (indépendants, dirigeants, bailleurs), pas aux salariés. Aucune de ces erreurs n'est fatale et toutes se corrigent par des règles simples, mais il faut les corriger avant diffusion.

---

## 1. Au premier plan : valeur actualisée et contournement, réforme par réforme

### 1.1 Fusion IR-CSG-CRDS

#### Valeur actualisée

**Ce que la hausse de 15 Md€ fait au patrimoine retraite.** La note présente cette hausse comme un flux annuel, « le prix du gain d'efficacité ». Pour les retraités actuels, c'est une **décote d'environ 160 à 190 Md€** sur la valeur de leurs droits [calcul de l'avis].

- Le calcul applique aux 15 Md€ annuels le facteur d'annuité moyen du stock de retraités : 11 à 13 à 1-3 % réel, pour un âge moyen d'environ 76 ans. L'espérance de vie à 65 ans est de 23,6 ans pour les femmes et 20,0 pour les hommes (Insee, 2025 provisoire).
- Cela fait environ 4 % de leur patrimoine retraite : 370 Md€ de pensions en 2023 (DREES), multipliés par le même facteur, soit environ 4 300 Md€.
- C'est du même ordre que le stock entier des plus-values en report d'apport-cession (173 Md€ de plus-values, environ 50 Md€ d'impôt nominal). La note consacre pourtant beaucoup plus de place au second sujet.

**Répartition par génération.** Le transfert ne va pas seulement « des actifs vers les retraités » : il va **des plus de 40 ans environ vers les plus jeunes** [calcul de l'avis].

- Hypothèses : moyennes par adulte tirées du modèle (−412 € par an pour un actif, +822 € pour un retraité), retraite à 64 ans, 2 % réel, sans croissance des salaires.
- Résultat en valeur actualisée : un adulte de 30 ans gagne environ 3 000 €, un de 40 ans est à peu près neutre. Un de 50 ans perd environ 5 000 €, un de 60 ans environ 11 500 €, un de 64 ans environ 14 500 €.
- Les quinquagénaires et les sexagénaires actifs perdent : ils profitent de peu d'années de baisse sur leur salaire et paient la hausse sur toute leur retraite.
- C'est l'électeur médian. La note doit le dire et le chiffrer par cohorte.

**Le gain « en régime permanent » contient un gain de transition.**

- *Ce que dit la note.* Tableau 5 : 4,9 Md€ « en régime permanent ». Le mécanisme est que « les pensions déjà liquidées ne réagissent pas ».
- *Pourquoi c'est faux.* L'argument vaut pour le stock de retraités, dont l'impôt supplémentaire est un prélèvement forfaitaire. Il ne vaut pas pour les actifs. Pour eux, une pension future plus taxée est un salaire différé plus taxé.
- *L'incohérence interne.* Le coin total exclut les cotisations « avec contrepartie de droits ». Il suppose donc que les salariés valorisent leurs droits à pension. Le modèle suppose en même temps qu'ils ne voient pas que ces droits seront taxés davantage. On ne peut pas tenir les deux.
- *Ce qui en réduit la portée.* Le lien entre un euro de salaire en plus et la pension est faible en haut de l'échelle (aucun droit au-delà de 8 plafonds de la Sécurité sociale, régime de base plafonné à un plafond) et pour les bas salaires (minimum contributif). Or le gain vient surtout du dernier décile (2,8 Md€) et de la participation sous 2 Smic (1,4 Md€). Une bonne partie du gain survit donc probablement en régime permanent.
- *Correction.* Séparer « gain de transition » et « gain permanent ». Ou ajouter au coin des actifs la hausse d'impôt sur les pensions, multipliée par le taux d'acquisition marginal des droits. Et ne plus écrire « régime permanent » sans cette réserve.

#### Contournement

| Fuite | Importance | La note la voit ? | Dispositif simple qui la ferme |
|---|---|---|---|
| **Garder le bénéfice dans une société** (IS à 25 % contre le barème) | Forte en haut ; **réduite** en dessous. Le barème proposé (14 % jusqu'à 20 000 €, 30,3 % à 45 000 €, 50 % à 1 M€) donne un taux marginal d'environ 31 % à 100 000 € et de 34-35 % à 250 000 €, si la montée est linéaire. L'écart avec l'IS tombe à 6-10 points, contre environ 25 aujourd'hui (IR à 41 % plus CSG-CRDS). La fin du taux réduit de 15 % ferme les petites « boîtes à trésorerie ». | Non : c'est un **bénéfice non revendiqué** de la réforme. | Rien à ajouter en dessous de 250 000 €. Au-dessus, voir la fuite par la sortie (§ 1.4). |
| **Transformer un salaire en dividende** | Réduite. Le dividende supporte 48,6-49,1 % au total, contre 31-35 % d'impôt fusionné sur le salaire entre 60 000 et 250 000 €. L'arbitrage reste dicté par les cotisations, que la note ne touche pas. | Non. | Aucun. La note peut s'en prévaloir. |
| **Rémunération en titres** (actions gratuites, BSPCE, management packages) restée aux taux forfaitaires (catégorie D « hors champ » de l'annexe) | Moyenne en haut de l'échelle. | Non. | Dire que ces gains d'acquisition entrent dans l'impôt fusionné comme salaires, au-delà d'un plafond. |
| **Répartir ses revenus entre conjoints** (imposition individuelle) | **Nouvelle et forte** pour qui contrôle la forme de ses revenus. Exemple [calcul de l'avis, barème de la proposition] : couple mono-actif à 80 000 € avec deux enfants. Si le titulaire verse 30 000 € de salaire au conjoint pour un vrai travail dans l'entreprise, le cabinet ou la SCI, le couple économise **environ 5 000 € par an**, cotisations en sus, en partie contributives. Les allègements généraux rendent ce salaire peu coûteux autour de 1 à 1,6 Smic. Cela fait plus que compenser les +1 330 € que la note attribue à ce couple. Les mêmes effets passent par l'attribution des loyers et bénéfices des biens communs (régime de communauté), par la cession de parts de SCI au conjoint et par la double franchise d'activité. | **Non**. La note ne dit pas comment les revenus des biens communs sont attribués. | Règles d'attribution : (i) les revenus des biens communs ou indivis sont partagés selon une clé légale, sans option ; (ii) un salaire versé à un membre du foyer n'est déductible qu'au prix de marché, pour un travail réel, avec présomption ; (iii) une règle du type « revenu fractionné » canadien (TOSI, 2018) impose au taux du titulaire le revenu d'une entreprise familiale versé à un proche non actif. Le Royaume-Uni a connu ce contentieux (affaire *Arctic Systems*, Chambre des lords, 2007). **À défaut, la variante « quotient » ferme la fuite.** Dans le modèle de la note, elle ne coûte que 0,1 Md€ de gain (3,9 contre 4,0), mais ce modèle ne distingue pas le second apporteur. |
| **Franchise d'activité appliquée aux loyers** | Moyenne. Un couple de bailleurs exonère 8 000 € de loyers, et l'immobilier locatif devient plus attractif que l'épargne financière, y compris pour des retraités. | Oui, en partie (« une franchise sur les loyers ne rend pourtant aucun travail plus payant »), mais sans en tirer de conséquence. | Réserver la franchise aux salaires et aux bénéfices d'une activité personnelle (BIC et BNC professionnels), hors revenus fonciers et location meublée non professionnelle. |
| **Prendre sa retraite en capital plutôt qu'en rente** | Faible aujourd'hui, croissante. Les sorties en capital sont taxées à 7,5 % ou 12,8 % forfaitaires et restent « hors champ » (365 M€, 78 000 foyers ; PLF 2026, voies et moyens). La rente, elle, subit **28 % marginal** entre 12 500 et 25 000 € de pension. S'y ajoutent les rachats d'assurance-vie, absents du test « petite pension ». | Non. | Intégrer les sorties en capital à l'assiette, avec étalement (système du quotient). **Asseoir l'exonération des petites pensions sur les ressources du foyer**, y compris les revenus au PFU, et non sur le montant de pension de chaque retraité. Aujourd'hui, deux retraités à 12 000 € chacun ne paient rien, alors qu'une veuve à 24 000 € paie le taux de sortie. |
| **Résidence des retraités** | Faible, à vérifier. Les conventions attribuent souvent les pensions privées à l'État de résidence. Une hausse d'environ 4 % de l'impôt sur les pensions rend l'installation à l'étranger un peu plus attrayante pour les retraités aisés. | Non. | Vérifier le traitement conventionnel de l'impôt fusionné, qui intégrerait l'ancienne CSG, et le régime des non-résidents. |

#### Où la mesure détruit de la valeur sans rapporter

- Le **taux marginal de 28 %** entre 12 500 et 25 000 € de pension rapporte peu. Il fausse le choix entre rente et capital, et taxe à 28 % le supplément de pension gagné en travaillant plus longtemps (surcote). D'après les cas-types OpenFisca du projet (`ir_csg/sorties/courbes_openfisca.csv`), ce taux est aujourd'hui de 0 % jusqu'à environ 16 500 €, de 4 % entre 17 500 et 19 500 € et de 21 % au-delà de 21 500 €. À l'inverse, la réforme supprime les **marches de 68 à 77 %** aux seuils de CSG, ce qui est un vrai progrès. Le bilan est donc mitigé : plus lourd entre 12 500 et 21 000 €, comparable au-delà, sans les marches. La note dit que c'est « sans effet sur l'activité ». C'est inexact pour ceux qui n'ont pas encore liquidé leur pension : le choix de l'âge de départ est la principale marge d'offre de travail des seniors, et la note ne l'étudie pas.
- Les **montages de salariat familial** consomment des ressources réelles (conseil, cotisations, contentieux) sans rien produire. Au sens de Chetty (2009), que la note cite, c'est une vraie perte sèche.

### 1.2 Immobilier

#### Valeur actualisée

**Le taux national sur le sol est un prélèvement en capital.** 0,19 % de la valeur des terrains, soit environ 5,7 Md€ par an, se capitalise à l'annonce en une perte de **140 à 190 Md€** (à 4 et 3 %) pour les propriétaires actuels [calcul de l'avis]. Le taux de 3 % est cohérent avec les rendements locatifs et avec Koster et Pinchbeck. La note doit dire que c'est un rendement (r − g), pas un taux nominal. La redistribution communale est à somme nulle dans chaque commune, mais elle déplace beaucoup de valeur (Paris +122 %).

**Le cas central est absent.** La note donne deux cas extrêmes : rien ne passe dans les prix, ou tout y passe. Les études qu'elle cite pointent vers un troisième cas, qu'elle ne présente pas :

- la taxe foncière se capitalise (Koster et Pinchbeck ; Høj et al.) ;
- la baisse des droits va surtout à l'acheteur en France (Bachelet et Poulhès : l'acheteur a supporté toute la hausse de 2014).

Dans ce cas asymétrique, les propriétaires actuels perdent l'essentiel des 140 à 190 Md€ sans rien récupérer. L'acheteur gagne deux fois : un prix plus bas qui compense la taxe, et des droits divisés par deux. C'est ce cas qui transfère le plus **entre générations**. La phrase « plutôt qu'entre générations » ne vaut que dans le cas symétrique. **Il faut en faire le cas central**, ou au minimum le présenter.

**L'étalement protège la trésorerie, pas le patrimoine.**

- La redistribution communale étalée sur dix ans conserve encore environ 88 % de la perte actualisée [calcul de l'avis, 3 %].
- Le taux national s'applique d'emblée, et les prix réagissent dès l'annonce.

**Le report de paiement des propriétaires âgés** équivaut à un prêt viager consenti par l'État. Il est neutre en valeur actualisée si l'intérêt suit le taux d'emprunt de l'État, et il fait porter l'impôt par la succession. C'est le bon outil contre le cas « riche en logement, pauvre en revenu » (voir § 5). Il devrait être **proposé par défaut** aux retraités sous un seuil de ressources, ce que la note laisse ouvert.

#### Contournement

| Fuite | Importance | La note la voit ? | Dispositif |
|---|---|---|---|
| Démembrement, SCI, société à l'IS | Faible. La taxe foncière est due par le propriétaire ou l'usufruitier quelle que soit la structure. | Implicitement. | Aucun. |
| Déclaration de la valeur | Faible. L'évaluation est faite en masse par zone, sans déclaration du propriétaire. Le contentieux portera sur le **partage entre sol et bâti** des appartements : le sol étant taxé quatre fois plus, chacun aura intérêt à gonfler la part du bâti. | En partie (le partage entre maisons et appartements n'est « pas robuste »). | Barèmes nationaux de coût de reconstruction, sans déclaration individuelle. Recours seulement au-delà d'un écart de 30 %, comme prévu. |
| **Champ du taux national** | Moyenne. Le modèle ne couvre que les logements des particuliers (« non modélisé : locaux professionnels, résidences secondaires »). Si la loi suit ce champ, requalifier l'usage ou passer par une personne morale permettra d'y échapper. Les **terrains constructibles non bâtis**, cible classique de l'impôt foncier, y échapperaient aussi. | Non. | Assiette universelle (tous terrains, tous propriétaires), avec des exonérations explicites et chiffrées. |
| Droits de mutation actuels (cession de parts de SCI, meubles surévalués, prix minorés) | Leur intérêt **baisse** de moitié. | Non : bénéfice non revendiqué. | — |

#### Où la mesure détruit de la valeur sans rapporter

Pendant la transition, avant que la nouvelle assiette existe, la baisse des droits est financée par une hausse uniforme de la taxe actuelle (+20 à 24 %). Elle frappe proportionnellement plus les communes pauvres, où la taxe pèse déjà 0,52 % de la valeur contre 0,18 % dans les plus chères. Elle durera au moins quatre ans si l'on en juge par le Bade-Wurtemberg. Ce n'est pas une destruction de valeur, mais une **transition régressive** à dire ou à corriger : par exemple, financer la transition par le seul taux national, sur des valeurs provisoires tirées de DVF.

La note écarte, à juste titre, la révision de la valeur à chaque vente (verrou de type Proposition 13).

### 1.3 Impôt sur les sociétés

#### Valeur actualisée

**Les taux sont cohérents.** Les déductions sont actualisées à 5 % (taux des entreprises), le coût public au taux d'emprunt de l'État (3,25 %). L'écart entre la valeur pour l'entreprise (1,8 à 2,6 Md€ par année d'investissement) et le coût pour l'État (1,2 à 1,7 Md€) est l'argument même de la mesure : l'État prête à son taux à des entreprises qui actualisent plus cher. La note devrait le dire en ces termes.

**La « dette de transition » est un décalage de calendrier, pas un coût réel.** Avec un taux d'intérêt de 3,25 % et une croissance de 3 %, tout écart permanent de flux a une valeur actualisée énorme : les chiffres de dette sont donc très sensibles aux hypothèses. Mieux vaut présenter le coût actualisé par année d'investissement, ce que la note fait déjà, et reléguer la dette au second plan.

**La valeur pour les entreprises en perte est surestimée.** Le report en avant des déficits se fait sans intérêt et reste plafonné (1 M€ plus 50 % du surplus). Pour une jeune entreprise en perte, la déduction immédiate vaut donc beaucoup moins. Zwick et Mahon ne trouvent d'effet que chez les entreprises qui paient l'impôt. Correction possible : reporter avec intérêt, ou au moins avec indexation, les déficits créés par la déduction.

#### Contournement

| Fuite | Importance | La note la voit ? | Dispositif |
|---|---|---|---|
| Faire passer en « équipement » des agencements, des installations du bâtiment ou des logiciels | Moyenne. | Non. | Liste fermée par catégorie comptable et par durée d'amortissement, comme pour le suramortissement de 2015. |
| **Biens d'occasion, cession-bail, cessions intragroupe** : revendre un actif existant pour que l'acheteur déduise immédiatement sa valeur résiduelle | Moyenne. | Non. | Réserver la déduction aux **biens neufs** (première mise en service) et exclure les acquisitions entre entreprises liées. |
| Location plutôt qu'achat | Faible. Le bailleur déduit et transmet l'avantage par le loyer, ce qui est même souhaitable pour un preneur sans bénéfice imposable. | Non. | Surveiller le commerce de déductions : les États-Unis ont abandonné le *safe harbor leasing* un an après l'avoir créé (1981-1982). |
| **Déduction immédiate et intérêts déductibles** | Moyenne. Un équipement financé par emprunt obtient un taux effectif **négatif** : c'est une subvention. Les PME sous 3 M€ de charges financières nettes échappent au plafonnement des intérêts. | Non. | Le dire. Choisir entre accepter cette subvention, limitée, ou refuser la déduction des intérêts sur les biens déduits immédiatement. |
| **Attendre le palier de 2033** (50 % puis 100 %) | Faible à moyenne. Attendre le palier rapporte environ 1,6 % du prix (25 % × 6,5 %) [calcul de l'avis], plus qu'un mois de coût d'usage pour beaucoup de biens. Les achats se concentreront juste après le palier. | Non. La note voit le calendrier comme un gage de stabilité. | Une montée régulière (par exemple +10 points par an), ou l'éligibilité selon la date de commande. |
| Transfert de bénéfices | Forte. | Oui : financer par l'assiette plutôt que par le taux est le bon choix. | — |

#### Où la mesure détruit de la valeur sans rapporter

Peu de choses. Seuls la concentration des achats autour du palier et le commerce de déductions seraient à craindre.

### 1.4 PFU, holdings, transmissions

#### Valeur actualisée : « c'est un report, pas un taux final » est faux en valeur actualisée

Trois composantes s'ajoutent.

**(a) La holding capitalise presque sans impôt.**

- Avant distribution, la holding paie 1,25 % sur les dividendes de ses filiales (régime mère-fille) et environ 3 % sur les plus-values de participations. Placé directement, le même capital paierait 31,4 % chaque année sur ses revenus.
- À 5 % sur 25 ans, la holding de participations finit avec **environ 46 % de richesse en plus**, PFU final payé (83 % sur 40 ans) [calcul de l'avis].
- Pour une trésorerie placée en titres de portefeuille (IS à 25 %), l'avantage n'est que de quelques pour cent.
- La note raisonne comme si seul le PFU final comptait (« 100 € distribués aujourd'hui rapportent 68,6 €… »). Ce raisonnement suppose que le rendement est taxé de la même façon dedans et dehors, ce qui n'est pas le cas.

**(b) Le PFU final est différé sans intérêt.** Un euro d'impôt dû dans 30 ans vaut 0,31 € aujourd'hui à 4 %, 0,14 € dans 50 ans [calcul de l'avis]. Le stock en report d'apport-cession représente environ 50 Md€ d'impôt nominal (173 Md€ de plus-values à environ 30 %). Si le report se transmet aux héritiers sans effacement, l'État en récupère peut-être **8 à 15 Md€ en valeur actualisée**, et beaucoup moins si les holdings ne vendent jamais [calcul de l'avis].

**(c) La purge au décès et à la donation rend la sortie facultative.**

- Les héritiers reçoivent les titres de la holding avec un prix d'acquisition égal à leur valeur au décès.
- Ils peuvent les céder sans plus-value, à un tiers ou, avec un risque d'abus de droit, à leur propre société financée par emprunt.
- L'impôt latent sur **tous les bénéfices accumulés** disparaît alors, et pas seulement la plus-value en report.
- L'option « transmission du report sans effacement » ne ferme que la seconde fuite.

**Conséquence.** La note affirme que la faiblesse du système est « dans le circuit des holdings ». Pourtant, la seule correction qu'elle envisage vise le report, ce qui laisse ouverte la fuite principale.

**Correction compatible avec la contrainte sur les grandes fortunes : reprise du prix d'acquisition pour tous les titres transmis**, par donation comme par décès. Le bénéficiaire reprend le prix d'acquisition du donateur ou du défunt. Aucun impôt n'est dû à la transmission, donc pas d'impôt sans liquidité. L'impôt n'est dû qu'à la sortie réelle. C'est la logique que la note défend déjà pour le report. On peut y ajouter un **intérêt de retard sur l'impôt différé**, au taux de l'État et payable à la sortie, ou une durée maximale du report (par exemple une génération), avec paiement étalé.

#### Contournement

| Fuite | Importance | La note la voit ? | Dispositif |
|---|---|---|---|
| Choisir la date de distribution des dividendes | Forte quand le taux bouge. | **Oui** : stabiliser le taux est le bon remède. | — |
| Trésorerie passive des holdings | Forte en haut. | Oui, mais la note n'agit pas, à cause de la contrainte. | La reprise du prix d'acquisition ci-dessus suffit à rendre la sortie imposable. |
| **Donner avant de vendre** : donner la nue-propriété des titres avant la cession efface la plus-value | **Forte**. Pour une famille qui transmettra de toute façon, donner avant de vendre supprime tout le PFU sur la plus-value, sans coût supplémentaire. La jurisprudence ne sanctionne que les montages où le donateur récupère le prix. | **Non** (la note n'en parle que pour le report). | Reprise du prix d'acquisition du donateur. |
| **Partir à l'étranger avant la cession** | Moyenne à forte pour les grosses plus-values. Depuis la loi de finances pour 2019, l'exit tax sur les plus-values latentes est dégrevée au bout de deux ans, ou cinq au-delà de 2,57 M€ de titres (sources secondaires, à vérifier pour 2026). L'élasticité d'exil moyenne et faible que cite la note (Bach et al., 2025) ne mesure pas ce départ ciblé, calé sur une vente. | **Non**. | Revenir à un délai long (quinze ans avant 2019) pour les grosses participations. Ce durcissement n'alourdit rien pour ceux qui restent. |
| Holding animatrice et pacte Dutreil | Forte, hors champ. | Mentionnée (« une holding familiale transmise sous pacte Dutreil »). | Hors du sujet de la note, mais à citer : c'est le complément de la purge. |

#### Où la mesure détruit de la valeur sans rapporter

- L'expiration du report à toute transmission (PLF 2027) crée un impôt sans liquidité, qui force des ventes ou des emprunts. La note le voit.
- Le report transmis sans intérêt détruit peu de valeur réelle, car le capital circule sans impôt à l'intérieur de la holding. Il rapporte surtout peu, et il entretient des structures coûteuses en conseil.

---

## 2. Grosses erreurs de fond, par gravité

### 1. Les deux grandes bascules sont des prélèvements en capital qui ne sont ni chiffrés ni assumés

- **Ce que dit la note.** Les retraités paient « 15 Md€ de plus » (« c'est le prix du gain d'efficacité »). La taxe foncière monte pour le « propriétaire installé qui ne vend pas » (jusqu'à 22 000 € pour l'appartement médian parisien). Le tableau 5 additionne les recettes et les gains en flux annuels.
- **Pourquoi c'est un risque majeur.**
  - Environ 160 à 190 Md€ en valeur actualisée sur les retraités, et 140 à 190 Md€ sur les propriétaires de terrains, pèsent en partie sur les mêmes ménages.
  - Le cas du retraité parisien modeste qui cumule les deux (pension fusionnée et taxe foncière) a déjà été signalé (`revue_transversale.md` § 4).
  - Le « gain d'efficacité » d'environ 7 Md€ par an est petit à côté de ces transferts.
  - C'est surtout le transfert qui décidera du sort politique et constitutionnel de la réforme : rupture d'égalité, caractère confiscatoire pour des ménages âgés sans liquidité.
  - L'efficacité du prélèvement sur le stock de pensions vient justement de ce qu'on ne peut pas y échapper. C'est un argument d'efficacité, mais il ne dispense pas d'un argument de justice.
- **Ce qu'il faudrait changer.**
  - (i) Une ligne de valeur actualisée par cohorte et par statut de propriétaire, à côté des flux.
  - (ii) L'argument d'équité, aujourd'hui absent alors qu'il est solide. Selon le COR (rapport de juin 2026), le niveau de vie moyen des retraités est égal à celui de l'ensemble de la population en 2023 (2 473 € contre 2 468 € par mois), et supérieur de 6,5 % si l'on compte les loyers imputés. Le niveau de vie des 65 ans et plus atteint 99 % de la moyenne en France, l'un des plus élevés d'Europe. Les ménages retraités ont un patrimoine plus élevé. Ce niveau relatif devrait ensuite baisser.
  - (iii) Le report de paiement par défaut et l'exonération fondée sur les ressources (§ 1.1).

### 2. L'« imposition à la sortie » sans protection de la sortie

- **Ce que dit la note.** « Imposer le bénéfice quand il sort des sociétés est […] ce qui gêne le moins la croissance. » « C'est un report, pas un taux final. » « Le report ne devient une exonération que si la sortie n'a jamais lieu. »
- **Pourquoi c'est une erreur.**
  - En valeur actualisée, un report sans intérêt et sans échéance est une exonération partielle.
  - Le rendement capitalisé dans une holding de participations échappe en outre presque entièrement à l'impôt.
  - Surtout, la sortie se rend légalement non imposable par trois voies : purge au décès, donation avant cession, et départ à l'étranger, l'exit tax étant dégrevée au bout de 2 ou 5 ans.
  - L'architecture « PFU maintenu, imposition à la sortie » perd donc sa cohérence sur le point même que la note désigne comme la faiblesse du système.
- **Ce qu'il faudrait changer.** La reprise du prix d'acquisition pour tous les titres transmis, un intérêt sur l'impôt différé ou une durée maximale du report, et un délai long d'exit tax pour les grosses participations. Aucune de ces mesures n'alourdit la facture de ceux qui restent et ne vendent pas : elles respectent la contrainte posée sur les grandes fortunes.

### 3. Une imposition individuelle sans règles d'attribution

- **Ce que dit la note.** L'impôt individuel fait perdre les couples mono-actifs (+1 330 € à 80 000 €). Le risque est jugé constitutionnel, et la variante « quotient » sert de repli.
- **Pourquoi c'est une erreur.**
  - Le couple qui contrôle la forme de ses revenus récupère le fractionnement : salaire du conjoint, revenus des biens communs, double franchise. Il y gagne environ 5 000 € par an dans l'exemple du § 1.1.
  - Le salarié ne le peut pas. La perte calculée frappera donc surtout ceux qui ne peuvent pas s'organiser, et la recette attendue s'érodera.
  - L'argument d'efficacité de l'individualisation (l'emploi du second apporteur) n'est pas dans le modèle : dans les chiffres de la note, la variante « quotient » ne coûte que 0,1 Md€ de gain.
- **Ce qu'il faudrait changer.** Écrire les règles d'attribution (§ 1.1), ou faire de la variante « quotient » la référence. Celle-ci ferme à la fois la fuite et le risque constitutionnel.

### 4. Un gain « permanent » qui contient un gain de transition (gravité moyenne)

Voir § 1.1. Le chiffre de tête de la fusion (4,9 Md€) doit être séparé en deux parts : ce qui vient du stock de pensions déjà liquidées, gain de transition, et ce qui reste en régime permanent. Le second dépend de la façon dont les actifs perçoivent l'impôt sur leurs futures pensions. Il faut aussi corriger l'incohérence avec le traitement des cotisations contributives.

### 5. L'incidence de la bascule foncière : le cas central manque (gravité moyenne)

Voir § 1.2. Présenter le cas « taxe foncière capitalisée, droits non capitalisés », qui découle des sources de la note, et y chiffrer la perte des propriétaires actuels par âge.

---

## 3. Choix contestables mais défendables

- **Faire payer 15 Md€ aux retraités.** Le montant est défendable en efficacité (le stock de pensions ne réagit pas) comme en équité (données du COR ci-dessus). Il équivaut à environ 4 % des 370 Md€ de pensions, l'ordre de grandeur de quatre points de désindexation, mais il est plus transparent et plus progressif qu'une désindexation. La note devrait faire cette comparaison. Restent contestables :
  - la zone de sortie de l'exonération à 28 % marginal, entre 12 500 et 25 000 € ;
  - un test fondé sur la pension individuelle plutôt que sur les ressources du foyer.
- **Le 1 % le plus aisé paie 2,7 Md€ de moins pendant que les retraités paient 15 Md€ de plus.** La contrainte exige seulement de « ne pas monter », mais le barème le plus efficace qui la respecte allège le haut. C'est cohérent avec la logique d'efficacité. Le contraste sera pourtant lu comme « les retraités financent les hauts revenus ». Il faut au minimum montrer le barème qui laisse le 1 % le plus aisé à charge inchangée, et son coût en gain.
- **La franchise par enfant croît avec le taux marginal** (840 € par enfant en bas, jusqu'à 3 000 € à 50 %). Elle est défendable au nom de la capacité contributive, mais elle est plus généreuse en haut que le quotient familial plafonné.
- **Garder le PFU tel quel et ne pas taxer la trésorerie passive.** C'est défendable avec la contrainte posée, à condition de fermer les sorties exonérées (§ 2.2).
- **IS : fin du taux réduit, et calendrier en un seul palier.** La fin du taux réduit est défendable : elle ferme aussi les petites boîtes à trésorerie. Le palier unique de 2033 est contestable (§ 1.3).
- **Une transition foncière financée par une hausse uniforme de la taxe actuelle**, régressive pendant au moins quatre ans (§ 1.2).

---

## 4. Ce qui manque

1. **Une comptabilité par génération** : valeur actualisée par cohorte de chaque réforme et de leur somme. C'est le complément indispensable des tableaux par décile.
2. **Le choix de l'âge de départ.** La note dit les pensions « déjà liquidées » insensibles, mais elle ne regarde ni la liquidation, ni la surcote, ni le cumul emploi-retraite. Une pension nette plus faible pousse à partir plus tard ; une surcote taxée à 28 % pousse en sens inverse.
3. **Les successions, les donations et l'assurance-vie.** La logique « taxer ce qui ne réagit pas » s'applique aussi à la transmission du patrimoine des générations âgées. La note s'en tient à la part immobilière des droits de succession (12,5 Md€) et ne dit rien de la purge générale des plus-values. Sans aller jusqu'à proposer une réforme, elle doit dire pourquoi elle l'écarte.
4. **L'articulation avec la politique des retraites** : indexation des pensions, coût des retraites (13,1 % du PIB en 2023 selon la DREES) et risque de cumuler la hausse fiscale avec une désindexation décidée ailleurs.
5. **La mesure du niveau de vie.** Les tableaux classent les foyers par décile de revenu fiscal, sans loyers imputés ni patrimoine. Un retraité propriétaire de son logement y paraît pauvre. Il faut au moins un tableau par âge et par statut d'occupation, et une exonération des petites pensions fondée sur les ressources.
6. **Les recettes affectées.** La CRDS et une partie de la CSG financent la CADES et la Sécurité sociale. La fusion doit garantir l'affectation d'une fraction de l'impôt fusionné, sans quoi le calendrier d'amortissement de la dette sociale et la confiance de ses créanciers sont en jeu.
7. **Les conventions fiscales et les non-résidents**, après la fusion de la CSG dans un impôt sur le revenu (§ 1.1).

---

## 5. Ce qui est bien vu

- **Taxer le stock de pensions est un prélèvement efficace**, et la note dit sans détour qui paie (« l'emploi et les familles se financent pour l'essentiel sur les pensions »). Les données du COR lui donnent raison sur le fond. Le cas du retraité seul à 17 000 €, « aujourd'hui exonéré », est **exact** : son revenu fiscal tombe à 12 504 € grâce à l'abattement des plus de 65 ans, sous le seuil de CSG (OpenFisca, `ir_csg/sorties/courbes_openfisca.csv`).
- **Les taux sur le salaire et sur le capital se rapprochent entre 50 000 et 250 000 €** (environ 31-35 % contre 31,4 % de PFU), et la fin du taux réduit de l'IS ferme les petites boîtes à trésorerie. C'est la meilleure défense contre le contournement de toute la réforme, et la note ne la revendique pas.
- **Immobilier** :
  - la liquidité comme argument principal pour les jeunes acheteurs ;
  - la baisse des droits dès l'annonce ;
  - le refus de réviser la valeur à chaque vente (verrou de la Proposition 13) ;
  - le report de paiement des propriétaires âgés ;
  - les exemples de Philadelphie et de Karlsruhe ;
  - l'honnêteté sur la fragilité du partage entre maisons et appartements.
- **IS** :
  - financer par l'assiette plutôt que par le taux, au vu du transfert de bénéfices ;
  - la distinction entre déduction immédiate et baisse du taux, qui allège aussi les rentes ;
  - l'État « associé » ;
  - le coût actualisé aux deux taux, celui des entreprises et celui de l'État.
- **PFU** :
  - 2013 et 2018 forment un seul épisode ;
  - l'élasticité des dividendes n'est pas une perte sèche ;
  - la stabilité comme premier service ;
  - la critique de l'expiration à toute transmission (« taxe une structure plutôt qu'un gain »).
- **Méthode** : écart à l'existant, coin total, réaction réelle séparée de la réaction déclarative, trois jeux d'hypothèses, et l'optimum gardé comme étalon plutôt que comme proposition.

---

## 6. Fond et présentation

La présentation est réécrite par ailleurs ; cet avis ne porte que sur le fond. Quatre points de rédaction changent toutefois le sens et relèvent donc du fond :

- **Tableau 5, « régime permanent »** : faux pour la part du gain qui vient du stock de pensions (§ 2.4).
- **« C'est un report, pas un taux final »** (§ 4.1 de la note) : faux en valeur actualisée (§ 2.2 de l'avis).
- **« Plutôt qu'entre générations »** (§ 2.3 de la note) : vrai seulement dans le cas symétrique (§ 1.2).
- **Le titre « Des actifs vers les retraités »** (§ 1.4 de la note) se lit à l'envers : c'est la charge qui passe des actifs aux retraités. Écrire « La charge passe des actifs aux retraités ».

---

### Sources vérifiées pour cet avis

- COR, rapport annuel de juin 2026, partie 3, chapitre 2 (niveau de vie des retraités en 2023 ; comparaison européenne des 65 ans et plus) : [cor-retraites.fr](https://www.cor-retraites.fr/sites/default/files/2026-06/RA_Part3_Chap2.pdf).
- DREES, *Les retraités et les retraites*, édition 2025, fiche 10 (pensions de 369,9 Md€ en 2023, 13,1 % du PIB) et vue d'ensemble (17,2 millions de retraités fin 2023) : [drees.solidarites-sante.gouv.fr](https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse-documents-de-reference/250731_PANORAMAS-retraites).
- Insee, espérance de vie à divers âges, 2025 provisoire (23,6 et 20,0 ans à 65 ans) : [insee.fr](https://www.insee.fr/fr/statistiques/2416631).
- Exit tax, délais de dégrèvement de 2 et 5 ans depuis la loi de finances pour 2019 (sources secondaires, à confirmer pour 2026) : [etudes-fiscales-internationales.com](https://www.etudes-fiscales-internationales.com/archive/2026/06/15/regime-de-l-exit-tax-structure-et-enjeux-27174.html), [finary.com](https://finary.com/fr/blog/epargne/ou-placer/comment-investir/exit-tax-depart-france).
- Dossiers du projet : taux forfaitaires des sorties de retraite en capital et abattement des plus de 65 ans (`ir_csg/sorties/niches_crds.md`, `depenses_fiscales_ir_plf2026.csv`) ; cas-types OpenFisca (`ir_csg/sorties/courbes_openfisca.csv`) ; barème et effectifs de la proposition (`synthese/sorties/architectures_ircsg.txt`, `controles_purs.txt`).
- Non vérifiés ici, cités de mémoire et à confirmer sur les textes avant toute reprise (règle du dossier) :
  - précédents étrangers : affaire *Arctic Systems* (Royaume-Uni, 2007), règle canadienne TOSI (2018), *safe harbor leasing* américain (1981-1982) ;
  - IS : report en avant des déficits (1 M€ plus 50 %) et plafonnement des intérêts (3 M€ ou 30 % de l'Ebitda fiscal) ; quote-part d'environ 3 % sur les plus-values de participations ;
  - pensions et salaires : plafond de 8 PASS des droits Agirc-Arrco ; zone des allègements généraux ;
  - transmissions : purge des plus-values à la donation et au décès, et jurisprudence sur la donation avant cession ;
  - exit tax : délai de quinze ans avant 2019 ;
  - finances sociales : affectation de la CRDS et d'une part de la CSG à la CADES.
- Calculs propres à l'avis (facteurs d'annuité, valeurs actualisées par cohorte, capitalisation, holding, palier de l'IS) : `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/catherine/annuite.py` et `cohortes.py`. Ce dossier temporaire peut être effacé ; il faut refaire ces calculs dans un script du projet avant toute reprise.
