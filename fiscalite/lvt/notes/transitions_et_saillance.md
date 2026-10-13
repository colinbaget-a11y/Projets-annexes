# Agent D : notes de lecture (introduction progressive d'un impôt foncier, transitions réelles)

Date : 13/10/2026. Les PDF et les textes extraits sont dans `scratchpad/lit/agentD/`.
Codes de lecture : **[TI]** = texte intégral lu (au moins les parties clés) ; **[R]** = résumé officiel seulement ; **[S]** = source secondaire (presse, blog, association) ; **NON VÉRIFIÉ** = affirmation non confirmée par une source primaire.

Accès réseau : plusieurs sites australiens (treasury.act.gov.au, apps.treasury.act.gov.au, taxpolicy.crawford.anu.edu.au, revenue.act.gov.au, vu-9.eprints-hosting.org) ont été bloqués par le proxy ou ont renvoyé 403. Les rapports d'évaluation de l'ACT n'ont donc **pas** été lus en texte intégral.

---

## A. Capitalisation des hausses futures ou différées, saillance, anticipations

### A1. Bradley (2017) : inattention aux hausses différées de l'assiette (Michigan)
- **Référence** : Bradley, Sebastien (2017). « Inattention to Deferred Increases in Tax Bases: How Michigan Home Buyers Are Paying for Assessment Limits ». *Review of Economics and Statistics* 99(1) : 53-66. DOI 10.1162/REST_a_00597 (vérifié via Crossref).
- **Cadre** : avec la Proposal A (1994), la valeur imposable (*taxable value*) d'un bien ne peut croître chaque année que de min(inflation ; 5 %) tant que le propriétaire reste le même. Elle est « décapée » (*uncapping*) et ramenée à la valeur de référence (SEV, environ 50 % de la valeur de marché) l'année qui suit une vente. L'acheteur hérite donc temporairement de l'impôt bas du vendeur, puis subit une hausse prévisible l'année suivante.
- **Question** : les acheteurs capitalisent-ils le caractère temporaire de l'impôt initial ?
- **Méthode** (selon le résumé) : l'auteur estime le degré de capitalisation des écarts de cotisation largement idiosyncratiques entre logements comparables, écarts créés par les plafonds d'évaluation. Les données portent sur Ann Arbor d'après le résumé de l'IPPSR. Le détail des données et de la spécification est NON VÉRIFIÉ (texte intégral non accessible).
- **Résultat clé (résumé officiel)** : les acheteurs sont « woefully inattentive to the temporary nature of their initial tax obligations ». Il en résulte une **surévaluation de près de 10 000 $ pour le logement moyen**.
- **Résultats secondaires (IPPSR/MSU, résumé de 2015)** : environ **30 M$ de surpaiement cumulé à Ann Arbor en 2005**. L'effet est plus fort chez les ménages modestes. Quand une information sur la future valeur imposable est fournie, le surpaiement baisse fortement, voire disparaît [S].
- **Portée pour la note** : une hausse programmée, mais peu visible, de la base est **mal anticipée**. Les acheteurs paient trop cher, puis découvrent la hausse après l'achat. Un calendrier de transition doit donc être **affiché** (dans les annonces, les actes, les simulateurs), sinon la capitalisation « au moment de l'annonce » postulée par la théorie ne se produit pas.
- **Lu** : [R] + [S]. Texte intégral non accessible (MIT Press 403, pas de version en libre accès d'après OpenAlex et Semantic Scholar).

### A2. Cabral & Hoxby (2012, révisé en 2015) : saillance et révoltes fiscales
- **Référence** : Cabral, Marika et Caroline Hoxby (2012, révisions avril 2013 et février 2015). « The Hated Property Tax: Salience, Tax Rates, and Tax Revolts ». NBER Working Paper 18514. https://www.nber.org/papers/w18514. Non publié en revue à ma connaissance (à vérifier).
- **Question** : la saillance de la taxe foncière (paiement par un ou deux gros chèques par an) explique-t-elle son impopularité, ses taux et l'adoption de plafonds (« tax limits ») ?
- **Données** : États-Unis entiers en 1980, 1990 et 2000, à un niveau géographique fin (block groups). Part des emprunteurs qui paient via un compte séquestre (*tax escrow*), lequel fond l'impôt dans la mensualité.
- **Identification** : variable instrumentale. L'escrow est instrumenté par le ratio d'actifs de *mortgage servicing* de holdings bancaires présentes localement, mais dont l'activité est surtout hors de l'État (ratio « SALO »).
- **Validation de la saillance** : les ménages en escrow déclarent leur impôt beaucoup moins précisément. L'écart-type de l'écart déclaré/réel du taux est de 14,3 mills avec escrow contre 3,2 mills sans [TI].
- **Magnitudes [TI]** :
  - Une hausse de 10 points de la part des emprunteurs en escrow donne des taux de taxe foncière **plus élevés d'environ 3 mills**. Le taux moyen est de 11,5 mills, avec un écart-type de 5,8. Un écart-type d'escrow équivaut ainsi à environ 1,2 écart-type de taux.
  - La même hausse de 10 points réduit de 0,76 le nombre de plafonds en vigueur (moyenne 2,76). Elle réduit de 37 % la probabilité qu'un plafond global ait été adopté, et de 33 % celle d'un plafond strict (10 mills ou moins).
- **Attention** : le résumé imprimé en tête du PDF de 2015 dit qu'une hausse d'un écart-type de l'escrow « produces about a one standard deviation **decrease** in property tax rates ». Cela contredit le corps du texte, qui dit « raises ». L'interprétation économique du corps (moins saillante, donc taux plus hauts et moins de révoltes) est cohérente. Il faut citer le corps du texte, pas le résumé.
- **Portée** : la visibilité de l'impôt alimente la résistance politique. Pour une LVT, mensualiser ou prélever à la source réduit la saillance, donc la résistance. C'est aussi un enjeu de transparence démocratique.
- **Lu** : [TI] (PDF NBER, 63 p.).

### A3. Elinder & Persson (2017) : réforme suédoise de 2008, effets d'annonce
- **Référence** : Elinder, Mikael et Lovisa Persson (2017). « House price responses to a national property tax reform ». *Journal of Economic Behavior & Organization* 144 : 18-39. DOI 10.1016/j.jebo.2017.09.017. Version de travail : IFN WP 1029 (2014), « Property Taxation, Bounded Rationality and House Prices ».
- **Réforme** : en 2008, la taxe foncière nationale suédoise (1 % de la valeur fiscale, elle-même d'environ 75 % de la valeur de marché) est remplacée par une redevance communale. Le taux passe à 0,75 % et la cotisation est plafonnée à 6 000 SEK. Le gain annuel moyen est de 4 900 SEK, soit une valeur actualisée moyenne de 245 000 SEK pour un prix moyen de 1 778 000 SEK. Le calendrier offre plusieurs annonces successives : annonce de l'Alliance le 4 juillet 2006 (Almedalen), élection de 2006, réforme de l'impôt sur les terrains, annonce finale le 20 septembre 2007, mise en œuvre en 2008.
- **Données** : registres, 101 449 ventes sur environ 2,5 ans.
- **Identification** : doubles différences. Les biens de valeur fiscale inférieure à 800 000 SEK (baisse de taux seule) servent de témoin ; les biens au-dessus (plafond) sont traités, avec plusieurs tranches d'intensité.
- **Résultats [TI]** :
  - Pour la grande majorité des biens, **aucun effet sur les prix, ni à l'annonce ni après la mise en œuvre**.
  - Pour la tranche supérieure à 2,4 M SEK de valeur fiscale (4 023 biens) : +1,5 à +4 points dès la première annonce, puis **+7,7 à +8,3 points à l'annonce finale**. La capitalisation complète théorique est d'environ 11,5 à 15 %, et on ne peut pas la rejeter pour ce segment.
  - La capitalisation est partielle dans les sous-marchés à prix élevés, à population diplômée et à offre contrainte.
  - Les auteurs invoquent la rationalité limitée et la faible saillance.
- **Portée** : quand un changement de taxe foncière est annoncé à l'avance, il ne se capitalise pas toujours, ni à l'annonce ni à l'application, sauf là où les enjeux sont élevés. Cela relativise la crainte d'un « choc de prix » à l'annonce d'une transition. Mais cela signifie aussi que les acheteurs ne « paient » pas le nouvel impôt d'avance : il tombe sur les propriétaires en place au fil de l'eau.
- **Lu** : [TI] de la version de travail de 2014 ; [R] de la version publiée.

### A4. Bai, Li & Ouyang (2014) : expérimentations de Shanghai et Chongqing (2011)
- **Référence** : Bai, Chong-En, Qi Li et Min Ouyang (2014). « Property taxes and home prices: A tale of two cities ». *Journal of Econometrics* 180(1) : 1-15. DOI 10.1016/j.jeconom.2013.08.039 (auteurs vérifiés via Crossref).
- **Réforme** (KPMG China Alert, février 2011 [S, cohérent]) : entrée en vigueur le 28 janvier 2011.
  - **Shanghai** : seuls les achats **nouveaux** sont taxés, à savoir le 2e logement ou les suivants des familles résidentes, et les achats de non-résidents. Taux de 0,6 % (0,4 % dans certains cas). Assiette = (surface − exonération) × prix unitaire × 70 %. Exonération de 60 m² par membre du foyer.
  - **Chongqing** : maisons individuelles existantes et nouvelles, et logements haut de gamme. Taux progressif de 0,5 % à 1,2 %. Exonération de 180 m² (maisons existantes) ou de 100 m² (nouvelles).
- **Méthode** : approche de contrôle synthétique par panel de Hsiao, Ching & Wan (2012). Ce n'est pas le contrôle synthétique d'Abadie au sens strict. Panel des prix moyens de 31 villes et provinces.
- **Résultats (résumé)** : le prix moyen baisse de **11 à 15 % à Shanghai** et **augmente de 10 à 12 % à Chongqing**. Les auteurs l'attribuent à un report de la demande du haut de gamme (taxé) vers les biens moins chers.
- **Contre-évaluation** : Du, Zaichao et Lin Zhang (2015). « Home-purchase restriction, property tax and housing price in China: A counterfactual analysis ». *Journal of Econometrics* 188(2) : 558-568. DOI 10.1016/j.jeconom.2015.03.018. Même famille de méthodes, avec choix des villes témoins par validation croisée. La taxe de Chongqing **réduit le taux de croissance annuel des prix de 2,52 points**, celle de Shanghai n'a **pas d'effet significatif** [R].
- **Portée** : deux études de même méthode aboutissent à des signes opposés. Les estimations agrégées au niveau ville sont fragiles. Une taxe à **assiette étroite** (bien neuf, second logement, haut de gamme) provoque des effets de report entre segments.
- **Lu** : [R] pour les deux articles ; [S] (KPMG) pour les paramètres de la réforme.

### A5. Lutz (2015) : taxe foncière et investissement résidentiel (New Hampshire)
- **Référence** : Lutz, Byron (2015). « Quasi-Experimental Evidence on the Connection between Property Taxes and Residential Capital Investment ». *American Economic Journal: Economic Policy* 7(1) : 300-330. DOI 10.1257/pol.20120017. Version de travail : FEDS 2009-18, « Fiscal Amenities, School Finance Reform and the Supply Side of the Tiebout Market ».
- **Choc** : la réforme du financement scolaire de 1999 au New Hampshire. Des dotations forfaitaires réduisent fortement la charge foncière dans environ 80 % des communes ; d'autres paient un excédent à l'État.
- **Résultats** (version de 2009 [TI], conclusions confirmées par le résumé de 2015 [R]) :
  - Le choc moyen, égal à 15 % des recettes foncières locales, fait croître l'investissement résidentiel de **11 à 22 %**. Cela implique une élasticité de l'ordre de −1. Le stock de capital est supérieur d'environ 2 % au bout de quelques années.
  - Dans la couronne de Boston (offre inélastique), le choc se **capitalise dans les prix** au lieu de déclencher de la construction.
  - Les communes allégées durcissent leur réglementation d'usage des sols (version de 2009).
- **Portée** : l'effet d'une variation de taxe foncière (en partie sur le bâti) se répartit entre prix et quantités selon l'élasticité de l'offre. Pour une LVT pure, la théorie prévoit une capitalisation dans le prix du sol. Une transition qui allège le bâti peut stimuler la construction là où l'offre est élastique.
- **Lu** : [TI] de la version de 2009 ; [R] de la version de 2015.

### A6. Ferreira (2010) et Wasi & White (2005) : effet de verrouillage des plafonds d'évaluation (Proposition 13)
- **Ferreira, Fernando (2010)**. « You can take it with you: Proposition 13 tax benefits, residential mobility, and willingness to pay for housing amenities ». *Journal of Public Economics* 94(9-10) : 661-673. DOI 10.1016/j.jpubeco.2010.04.003.
  - **Cadre** : la Proposition 13 (1978) fixe un taux de 1 % de la valeur à l'achat, avec une revalorisation de 2 % par an au plus. Les Propositions 60 et 90 permettent aux ménages dont le chef a 55 ans ou plus de **transférer** l'avantage fiscal vers un nouveau logement.
  - **Données** : recensement de Californie de 1990, formulaire long à usage restreint.
  - **Identification** : régression sur discontinuité à 55 ans.
  - **Résultat** : la mobilité (sur 5 ans) est d'environ 4 % à 54 ans contre 5,2 % à 55 ans, soit **+1,2 point, environ 25 %** de plus [TI de la version de travail Wharton 526]. Les consentements marginaux à payer pour les caractéristiques du logement sont biaisés d'environ 100 % à la hausse sans correction de l'endogénéité des prix.
- **Wasi, Nada et Michelle J. White (2005)**. « Property Tax Limitations and Mobility: The Lock-in Effect of California's Proposition 13 ». NBER WP 11108 [R].
  - De 1970 à 2000, la durée moyenne d'occupation en Californie augmente de 1,04 an pour les propriétaires et de 0,79 an pour les locataires, par rapport aux États de comparaison.
  - L'effet croît avec la taille de la subvention implicite : +0,11 an à Bakersfield (subvention d'environ 110 $/an), **+2 à 3 ans** dans les villes côtières (subvention de plusieurs milliers de $).
- **Portée** : une transition par « clause du grand-père » ou par plafonds individuels attachés au **propriétaire** (avantage perdu à la vente) crée un **verrouillage** proportionnel à l'avantage. C'est exactement l'inverse de l'objectif de mobilité qu'on recherche en remplaçant les DMTO. Le cas danois (rabais perdu à la vente) relève de cette logique. Il faut donc préférer des lissages attachés au **bien** et dégressifs dans le temps (comme la *stigningsbegrænsning* danoise, maintenue à la vente) ou un report de paiement.
- Voir aussi Hodge, Sands & Skidmore (2015), « Assessment Growth Limits and Mobility: Evidence from Home Sale Data in Detroit, Michigan », *National Tax Journal* 68(3) : 573-599 (titre vérifié via Crossref ; contenu NON LU).
- **Lu** : Ferreira [TI de la version de travail] ; Wasi-White [R].

### A7. Autres preuves sur l'annonce et l'anticipation (2015-2026)
- **Økland, Andreas (2021)**. « Capitalisation of a Recurring Tax on Properties: Evidence from a Local Property Tax Reform ». Version de travail Skatteforsk/NMBU, 28 octobre 2021, présentée au séminaire Syracuse/Maxwell ; mention « please do not cite » [TI].
  - **Réforme** : Oslo instaure une taxe foncière en **2016**, après l'élection de septembre 2015 ; la plateforme de coalition date d'octobre 2015. Le taux est de **2 ‰ en 2016 (maximum légal pour une première année), puis 3 ‰ en 2017**, comme annoncé à l'automne 2015. L'assiette est de 80 % de la valeur de marché estimée, avec un abattement de 4 M NOK par logement.
  - **Identification** : la taxe ne s'applique qu'à une moitié de zones denses homogènes situées de part et d'autre de la frontière communale. Doubles différences avec des « dates d'événement » : sondages au T1 2015, élection, introduction.
  - **Résultat** : la capitalisation complète impliquerait −3 % sur les biens concernés (au-dessus de 6,3 M NOK). Les estimations sont proches de zéro, voire positives. Dans 11 spécifications sur 15, −3 % est hors de l'intervalle de confiance à 95 %. Pas d'effet sur les volumes de transactions.
  - **Limite** : taux effectif faible (moins de 0,1 % pour le segment étudié).
- **Borge, Lars-Erik et Jørn Rattsø (2014)**. « Capitalization of Property Taxes in Norway ». *Public Finance Review* 42(5) : 635-661 [R]. Transactions de 1997-1999 et instruments. Capitalisation **complète** à des taux d'actualisation réalistes. Cette étude est en coupe transversale et ne porte pas sur une annonce.
- **Giertz, Seth H., Rasoul Ramezani et Kurt J. Beron (2021)**. « Property tax capitalization, a case study of Dallas County ». *Regional Science and Urban Economics* 89 : 103680 [métadonnées vérifiées via Crossref ; contenu NON LU]. Selon un résumé tiers, la valeur des logements baisse d'au moins 6,7 % l'année suivant un vote, mais l'effet ne persiste pas. À vérifier avant de le citer.
- **Rappel sur la Norvège (règle légale de progressivité)** : la loi de 1975 sur la taxe foncière (*eigedomsskattelova*, Lovdata) prévoit :
  - § 13 : la **première année**, le taux ne peut excéder **1 ‰** (2 ‰ avant la modification du 20/12/2019, ce qui explique les 2 ‰ d'Oslo en 2016) ; ensuite, le taux ne peut augmenter de plus de **1 ‰ par an**. Une hausse plus rapide est permise pour les terrains non bâtis (*huslause grunneigedomar*, jusqu'à 3 ‰ par an d'après la synthèse de la page Lovdata ; ce détail est à vérifier dans le texte).
  - § 11 : le taux général va de 1 à 7 ‰, avec un **plafond de 4 ‰ pour les logements**.
  - C'est un exemple de **montée en charge progressive inscrite dans la loi** [TI de la page Lovdata via outil].
- Høj et al. (2018) et Nielsson et al. (2024), sur les prix danois à l'annonce de 2004 et de 2017, sont traités ailleurs : non refaits ici.

### A8. Report de paiement (deferral) et circuit breakers
- **Shan, Hui (2010)**. « Property taxes and elderly mobility ». *Journal of Urban Economics* 67(2) : 194-205. DOI 10.1016/j.jue.2009.08.004. Version de travail : FEDS 2008-50 [TI].
  - **Données** : HRS (Health and Retirement Study) et base des programmes d'allègement par État.
  - **Identification** : variable instrumentale, à partir des programmes d'allègement.
  - **Résultat** : +100 $ de taxe foncière annuelle entraîne **+0,76 point de taux de mobilité sur 2 ans** chez les propriétaires de plus de 50 ans, soit +8 % par rapport à une base de 9 %.
  - **Fait clé sur le recours aux programmes** (tiré de Baer 1998, AARP, milieu des années 1990) : taux médian de participation des éligibles d'environ **90 % pour les exonérations de résidence principale** (*homestead exemptions*), d'environ **40 % pour les homestead credits et les circuit breakers**, et de **moins de 1 % pour les programmes de report (deferral)**. Explication avancée : la répugnance des personnes âgées à grever leur maison d'une hypothèque légale (comme pour les prêts viagers). Les reports sont pourtant jugés par les universitaires comme l'outil le plus ciblé et le moins coûteux.
- **Bowman, John H., Daphne A. Kenyon, Adam Langley et Bethany P. Paquin (2009)**. *Property Tax Circuit Breakers: Fair and Cost-Effective Relief for Taxpayers*. Lincoln Institute of Land Policy, Policy Focus Report, mai 2009 [TI partiel].
  - Participation aux circuit breakers : Maine 41 % des éligibles (Harkness 2006) ; Wisconsin 43 % (DOR 2004).
  - Enquête AARP (Baer 1998) : 2,5 % des répondants éligibles avaient demandé l'aide ; un peu plus de 30 % se savaient éligibles. Selon les États, la participation va de 13-15 % (Rhode Island) à 72-100 % (district de Columbia), avec une médiane de 40 %.
  - Raisons du non-recours : méconnaissance, sentiment de ne pas en avoir besoin, lourdeur administrative, réticence à déclarer ses revenus.
  - Le versement via l'impôt sur le revenu réduirait le non-recours.
  - En 2009, 16 États n'avaient aucun circuit breaker.
  - Les auteurs suggèrent le report ou le prêt sur fonds propres pour les chocs temporaires.
- **Colombie-Britannique (Property Tax Deferment Program)** :
  - Page officielle des taux (gov.bc.ca) : avant 2026, le programme « régulier » (55 ans et plus, conjoints survivants, personnes handicapées) portait intérêt au **taux préférentiel moins 2 points**, soit 2,95 % entre octobre 2025 et mars 2026. Le programme « familles » était au taux préférentiel. **Depuis 2026, les deux sont au taux préférentiel plus 2 points, soit 6,45 %** [vérifié sur la page officielle via outil]. La capitalisation mensuelle mentionnée par la presse est NON VÉRIFIÉE sur la page officielle.
  - Nombre de participants : plus de 36 000 en 2014 selon la presse ; environ 78 000 ménages en 2026 selon un agrégateur. Ces chiffres sont **NON VÉRIFIÉS** en source primaire.
  - C'est un contre-exemple à la « take-up < 1 % » américaine. Le programme est non soumis à condition de ressources et bon marché, ce qui l'a fait croître fortement (+53 % en 4 ans selon le Seniors Advocate BC [S]). C'est aussi une mise en garde : un taux inférieur au marché devient une niche pour des propriétaires aisés (critiques de presse en 2017 [S]). La hausse du taux en 2026 corrige ce point.
- **Danemark** : depuis 2024, *indefrysning* = prêt de l'État, porteur d'intérêt, pour toute hausse future de l'impôt foncier total (voir B10).
- **Massachusetts** : Munnell (CRR Boston College, avril 2025) qualifie le recours au report local de « particulièrement faible » et propose un report à l'échelle de l'État (jusqu'à 60 % de la valeur, gain moyen d'environ 4 755 $/an) [S]. Chiffre de participation non donné dans la page lue.
- **Portée pour la note** : un mécanisme de report n'atténue réellement les cas de « riche en patrimoine, pauvre en revenu » que s'il est **automatique ou par défaut** (inscription par défaut sur l'avis d'impôt, comme au Danemark), **peu stigmatisant** et administré par l'administration fiscale. Le taux d'intérêt doit être proche du coût de financement public : trop bas, il crée une niche ; trop haut, personne n'y recourt.

---

## B. Designs de transition réels

### B9. Territoire de la capitale australienne (ACT, Canberra) : remplacer les droits de mutation par des « general rates » sur la valeur du sol (depuis 2012)
- **Design** :
  - Annonce au budget 2012-13, dans la lignée de la revue fiscale Quinlan de 2012.
  - Programme sur **20 ans** : réduction progressive de la *conveyance duty* (droits de mutation) et suppression de la taxe sur l'assurance, compensées par une hausse des *general rates* (impôt local annuel), avec un objectif de neutralité budgétaire.
  - Les general rates sont calculés sur la **valeur moyenne non bâtie** (*average unimproved value*, AUV) du terrain, selon un barème progressif par tranches plus une part fixe. Le gouvernement fixe une enveloppe de recettes et répartit selon l'AUV ; la facture ne suit donc pas mécaniquement la variation de la valeur.
  - Moyenne sur 3 ans selon les descriptions historiques ; un article récent évoque un passage à 5 ans. Ce point est **NON VÉRIFIÉ**.
  - Paramètres 2025-26 (*Canberra Times*, 2025 [S]) :
    - part fixe de 926 AUD (maisons) et 985 AUD (logements en copropriété) ;
    - nouvelle tranche à **0,5734 %** pour une AUV d'au moins 1 M AUD ;
    - recettes des rates résidentiels prévues à 600,5 M AUD en 2025-26, contre 525,9 M AUD en 2024-25 ;
    - hausse moyenne des rates résidentiels de 3,75 %/an dans la phase lancée en 2020 ;
    - médiane à Forrest de 15 155 AUD contre 2 281 AUD à MacGregor.
- **Évaluations** :
  - **Nassios, Jason, Nicholas Sheard et Philip Adams (2020)**. *The economic and efficiency impacts of altering elements of the ACT's tax mix*. Centre of Policy Studies (Victoria University), rapport pour ACT Treasury, avril 2020 [R, via les métadonnées EPrints de VU].
    - Modèle d'équilibre général VURMTAX : décomposition historique 2012-2018. Le PIB régional (GSP), l'investissement, la consommation et les salaires réels sont plus élevés en 2018 qu'en l'absence de réforme.
    - Partie économétrique : **une baisse de 10 % des droits payés par transaction est associée à +6 % de ventes** (coefficient de 0,6) et à **+2 % des valeurs foncières non bâties** (coefficient de 0,2). Effet sur le prix moyen des transactions positif mais **non significatif**.
    - Nassios & Giesecke (*The Conversation*, 10/03/2025 [S]) répètent l'élasticité de 0,6. Environ 80 % du gain économique modélisé dans l'ACT vient de la suppression des droits de mutation.
  - **Breunig, Robert, Hai Anh La, Ralf Steinhauser, Robert Tanton et Yogi Vidyattama (2020)**. *Analysis of the impacts and outcomes of the ACT tax reform*. TTPI (ANU) et NATSEM (Université de Canberra), 5 mai 2020. **Non lu** : site bloqué. D'après Smith & Hermans (Prosper, 2020 [S]) :
    - environ +200 logements locatifs par mois ;
    - loyers des quatre quintiles inférieurs en baisse de 2 à 16 % selon la spécification ;
    - loyers du quintile supérieur en hausse.
  - **Vidyattama, Yogi, Jinjing Li, Robert Tanton et Hai Anh La (2023)**. « Changing Housing Taxation Composition: A Review of Policy in the Australian Capital Territory ». *Urban Policy and Research* 41(2) : 182-194. DOI 10.1080/08111146.2023.2167818 [R, paraphrasé]. Microsimulation : hausse de la rotation du parc ; baisse des droits et des rates payés par la plupart des familles vulnérables ; mais la forte hausse des prix peut annuler ce gain.
  - **Smith, Warwick et Jesse Hermans (2020)**. *The Second Interval: evaluating the ACT's 20 year Land Value Taxation transition after 8 years*. Prosper Australia (association pro-LVT) [S].
    - Erreur moyenne absolue des prévisions de recettes de 7,9 % (2006-07 à 2011-12), contre 2,6 % après la réforme.
    - Taux commercial passé de 0,73 % (2011) à 3 %-5,15 % (2019), avec suppression de la *land tax* commerciale.
    - Propriétaire moyen : +3 648 AUD cumulés en 8 ans, alors que la valeur de son terrain a gagné 63 681 AUD.
    - Part des achats par des accédants (en valeur) passée d'environ 60 % (2012) à environ 78 % (2020).
    - Le dispositif d'aide aux retraités n'a pas été sur-sollicité.
- **État en 2025-2026** :
  - Liptak (*Substack*, 2026 [S]), qui cite une évaluation officielle de 2019 et une analyse de Pegasus Economics remise à la commission des budgets :
    - sur 7 ans, rates +793 M AUD contre −855 M AUD de droits de mutation et taxe sur l'assurance, soit 62 M AUD de moins qu'en l'absence de réforme ;
    - GSP +302 M AUD (+0,11 %) ;
    - recettes des rates : 209 M AUD en 2011-12, 944,2 M AUD prévus en 2026-27 ;
    - rates à environ **29 % des recettes propres, stables à partir de 2025-26**, ce qui signale une **substitution enlisée** ;
    - droits de mutation encore à environ 10 % en 2029-30 ;
    - Pegasus juge « extrêmement improbable » le respect de l'échéance de 2032.
    - Ces chiffres sont **NON VÉRIFIÉS en source primaire**.
  - **Budget 2026-27** (communiqué du gouvernement de l'ACT et dépêches PwC, Grant Thornton et CityNews, juin 2026 [S convergentes]) :
    - **suppression des droits de mutation pour tous les primo-accédants à partir du 1/7/2026**, sans condition de prix ni de revenu ;
    - exonérations élargies aux pensionnés, aux bénéficiaires du NDIS et aux acheteurs sans bien depuis 5 ans ;
    - rates en hausse moyenne de 8 % (composante générale), facture moyenne +5 %.
- **Enseignements** :
  1. Une transition **très longue** (20 ans) est politiquement soutenable, mais elle s'enlise quand la hausse des rates devient visible ; les rates sont très saillants (cf. Cabral-Hoxby).
  2. L'effet sur les transactions est rapide et mesurable (élasticité d'environ 0,6).
  3. Le débat sur la neutralité budgétaire est permanent : les opposants (Property Council) contestent la neutralité.
  4. Les gouvernements finissent par cibler la suppression des droits sur les primo-accédants plutôt que de poursuivre la bascule générale.
- **Lu** : [R] + [S]. Rapports officiels non accessibles.

### B10. Danemark : réforme de 2024 (nouvelles évaluations après 10 ans de gel, rabais, plafonds, gel par prêt)
- **Contexte** :
  - Les évaluations foncières ont été **suspendues en 2013** après les critiques de Rigsrevisionen.
  - L'évaluation des logements de 2011 a été reconduite (comme évaluations de 2013, puis de 2015 et 2017) [S convergentes : lex.dk, tax.dk, regeringen.dk].
  - Le gel nominal de l'*ejendomsværdiskat* (taxe sur la valeur du logement) date de 2002 : assiette plafonnée à la valeur de 2001 plus 5 %, ou à celle de 2002 si elle est plus basse.
  - Le plafond de croissance de la base de la *grundskyld* (taxe sur le terrain), le *grundskatteloft*, date de 2003 (régulation annuelle de 7 % au plus).
  - Accord politique *Tryghed om boligbeskatningen* de mai 2017, loi de 2023 (ejendomsskatteloven), application au **1/1/2024**.
- **Mécanismes** :
  1. **Principe de précaution** : l'assiette est de **80 % de la valeur évaluée** (abattement de 20 %), pour la taxe sur le logement comme pour la grundskyld (tax.dk, Den juridiske vejledning C.H.4.1.2 [TI via outil]).
  2. **Baisse des taux** en contrepartie de la hausse des valeurs. Environ 4 propriétaires sur 5 paient moins selon Nykredit, cité par *The Local* [S]. Le taux de 0,51 %, et 1,4 % au-dessus d'environ 9,2 M DKK, vient de sources secondaires : NON VÉRIFIÉ en source officielle.
  3. **Skatterabat** (rabais fiscal) pour les propriétaires occupants ayant acquis avant le 31/12/2023 : il garantit que l'impôt foncier total ne soit pas plus élevé qu'avec les anciennes règles. Il est **maintenu pendant toute la durée de détention** et **disparaît à la vente**. Le texte de l'accord du 10/11/2023 le confirme : « bortfalder ikke ved salg, som det er tilfældet med skatterabatten for ejerboliger » [TI].
  4. **Stigningsbegrænsning** (plafonnement de la hausse) de la grundskyld pour les biens non couverts par le rabat (locaux professionnels, etc.) : au plus **4,75 % par an de la grundskyld « pleinement introduite »** (5 % dans l'accord de 2017), et **3,5 % pour le logement social (almene boliger) jusqu'en 2040**. Ce plafond est **attaché au bien et ne tombe pas à la vente** [TI, aftaletekst du 10/11/2023]. En 2024, la grundskyld pouvait encore monter d'au plus 2,8 % [S].
  5. **Taxe sur l'emprise des locaux professionnels** (*erhvervsdækningsafgift*) : plafonnement de 10 %/an créé par l'accord du 10/11/2023, rétroactif au 1/1/2022. Coût d'environ 1,1 Md DKK (2022-24) et 0,8 Md DKK (2025-30) après retours fiscaux. En plus, environ 10 Md DKK d'allègements prévus dans la réforme [TI].
  6. **Indefrysning** (gel par prêt) :
     - tout propriétaire occupant (personne physique) peut **geler** les hausses futures de la taxe sur le logement et de la grundskyld au-delà de 250 DKK, par rapport à 2024 ou à l'année d'achat pour la première, à 2017 ou à l'année d'achat pour la seconde ;
     - le gel prend la forme d'un **prêt de l'État porteur d'intérêt**, remboursable à la vente et garanti par une sûreté légale non inscrite ;
     - on s'inscrit par défaut ou on se désinscrit via le *forskudsopgørelse* (déclaration préalable) ;
     - le prêt municipal pour les retraités est transféré à l'administration fiscale ;
     - une ligne de prêt complémentaire (*tillægslån*) garantit qu'aucun propriétaire ne puisse geler moins qu'avant (fiche du Skatteministeriet, janvier 2023 [TI]).
     - Taux de 2,66 % en 2025 [S, NON VÉRIFIÉ].
  7. **Communication** : en 2023, les évaluations provisoires des locaux professionnels sont affichées en même temps que l'impôt correspondant, et les échéances de paiement repoussées de 2 mois (accord du 10/11/2023).
- **Problèmes rencontrés** : erreur de calcul du rabais pour environ 733 000 propriétaires (rabais trop élevé) [S, NON VÉRIFIÉ].
- **Pourquoi ces outils** : sortir d'un gel de plus de 10 ans crée des sauts individuels énormes. Le rabais sert de **clause du grand-père** (personne ne perd au jour J) et le plafond lisse les hausses. Le prix est double : un **verrouillage** (rabais perdu à la vente, cf. A6) et une **iniquité horizontale** durable entre anciens et nouveaux propriétaires.
- **Lu** : [TI] aftaletekst du 10/11/2023 et fiche indefrysning de janvier 2023 ; [TI via outil] tax.dk ; [S] pour les taux.

### B11. Allemagne : Bade-Wurtemberg, Bodenwertmodell (première année 2025)
- **Modèle** : loi régionale (LGrStG BW). Assiette = surface × *Bodenrichtwert* (valeur de référence du sol de la zone). Taux de base légal (*Steuermesszahl*) réduit de 30 % pour le logement. On applique ensuite le taux communal (*Hebesatz*). Les bâtiments sont ignorés [S : ministère des Finances BW, IHK].
- **Transparenzregister** (registre de transparence) du ministère des Finances BW :
  - en ligne le **9/9/2024**, retiré le **30/6/2025** ;
  - il publie, pour chaque commune, une **fourchette** (et non une valeur unique) de taux communaux « neutres en recettes », non contraignante [S : communiqués officiels de BW lus via outil].
- **Auswertung du Bund der Steuerzahler BW** (15/09/2025) [S, chiffres lus sur la page de l'association] :
  - **720 communes sur 1 101 (65 %)** ont un taux communal dans la fourchette neutre, **338 au-dessus** (près d'un tiers), 43 en dessous ;
  - environ 40 % des communes au-dessus le sont de moins d'environ 5 % ; environ 18 % de l'ensemble ont augmenté leurs recettes d'au moins environ 5 % ;
  - les taux vont de moins de 100 % à plus de 1 000 % ;
  - l'association rappelle que le taux communal seul ne mesure pas la charge.
  - Taux médian régional de 290 % au 30/06/2025 (Destatis, via Grundradar [S]).
- **Déplacements de charge documentés** (BdSt et documents municipaux [S]) :
  - part du résidentiel dans l'impôt foncier : **Mannheim 56 % → 63 %, Freiburg 61 % → 70 %, Ravensburg 54 % → 70 %** ;
  - Karlsruhe : taux communal neutre, mais déplacement des locaux professionnels vers le logement, en particulier vers les maisons individuelles ; près de la moitié des biens paient moins ;
  - exemples à Obersulm : maison sur 555 m², d'environ 294 € à environ 434 € ; maison sur 1 102 m², d'environ 356 € à environ 776 € ; appartement, d'environ 193 € à environ 71 €.
  - Le ministère confirme que les appartements et les immeubles collectifs paient souvent moins, et que les maisons sur grands terrains paient plus.
- **Contentieux** : le **Bundesfinanzhof** (cour fédérale des finances) juge la LGrStG BW **conforme à la Constitution** (affaires II R 26/24 et II R 27/24).
  - Communiqué de presse du **20/05/2026** (LTO) ; DATEV mentionne une audience ou une décision au 22/04/2026, date à vérifier sur l'arrêt.
  - Motifs : la référence au seul sol est compatible avec l'égalité (art. 3 GG) ; la typisation par valeur de zone est admise ; une preuve d'une valeur inférieure est possible (écart d'au moins 30 %).
  - Le BFH avait déjà validé le modèle fédéral (décembre 2025 selon LTO ; une autre source dit 12/11/2025, date à vérifier).
- **Études académiques 2024-2026 (ZEW, ifo, IW)** sur les effets distributifs en BW : **aucune trouvée**. Löffler et Siegloch (2024) sont traités ailleurs.
- **Lu** : [S] uniquement ; aucune étude scientifique de première année trouvée.

### B12. Pennsylvanie : Pittsburgh (2001), Altoona, Harrisburg
- **Hughes, Mark Alan (2006)**. *Why So Little Georgism in America: Using the Pennsylvania Case Files to Understand the Slow, Uneven Progress of Land Value Taxation*. Lincoln Institute WP06ZK1 [TI des passages sur Pittsburgh].
  - En 2006, sur 33 communes : 16 en taxe à deux taux (*split-rate*), 5 l'ayant abandonnée, 12 l'ayant envisagée sans l'adopter.
  - **Pittsburgh** : taxe à deux taux de 1913 à 2001, avec un ratio d'environ 6:1 (environ 5,77 selon Hanson).
  - **Chaîne causale de l'abandon** :
    1. En 1996, le comté d'Allegheny **gèle les évaluations 5 ans** (et licencie 42 évaluateurs).
    2. En 1997, un juge ordonne une réévaluation complète des 550 000 biens par un prestataire (Sabre Systems), **et** le passage de l'évaluation fractionnelle à la valeur de marché pleine.
    3. En janvier 2001, les avis finaux montrent pour la première fois la décomposition sol/bâti et l'impôt à deux taux. La valeur foncière évaluée bondit de **+81 %**, contre +43 % pour le bâti. La valeur totale passe de 8,91 à 13,35 Md$ (+50 %).
    4. Les taux de 2001 avaient été fixés sur une part foncière projetée d'environ 20 %, mais la part réelle atteint environ 30 % selon un conseiller municipal (avant : 10 %). Le contrôleur du comté estime les parts à 4-20 % avant et 22-29 % après.
    5. La méthode d'évaluation du foncier (calcul résiduel) est contestée : sur-évaluation dans les quartiers modestes selon le contrôleur de la ville.
    6. Moins d'une semaine plus tard, le président du conseil municipal propose de revenir à un taux unique, ce qui est fait en 2001.
  - **Leçon** : ce n'est pas le principe de la LVT qui a échoué, mais une **réévaluation-choc après un gel, sans lissage**, combinée à un changement de base et à des taux fixés sur des projections erronées.
  - Le chiffre de « plus de 130 000 recours » circule (progress.org [S]) : **NON VÉRIFIÉ**.
- **Hanson, Andrew (2021)**. *Split-Rate Taxation and Business Establishment Location: Evidence from the Pennsylvania Experience*. Lincoln Institute WP21AH1 [TI].
  - Tableau 1 (d'après Yang 2014, mis à jour en 2020) : **Altoona 2003-2016** ; Harrisburg 1975 et toujours en vigueur en 2017, avec un ratio moyen de 5,33 ; Pittsburgh 1913-2000 ; Coatesville 1991-2004 ; Oil City 1989-2002 ; Steelton 2000-2007.
  - Doubles différences sur les County Business Patterns 1994-2017 : l'adoption d'une taxe à deux taux (ratio moyen de 7,73) est associée à **+60 à 107 établissements**, effet qui s'érode de 3,3 à 5,5 établissements par an (environ 5 %).
- **Altoona** (*Altoona Mirror*, 6/6/2016 [S]) :
  - taxe partiellement fondée sur le sol à partir de **2002** (2003 selon Hanson) ;
  - **100 % sur le sol en 2011**, avec un taux sur le sol de 394 mills, car le sol ne représentait qu'environ 1/7 de la valeur évaluée ;
  - le conseil municipal décide en juin 2016 de **revenir à la taxe classique à partir de 2017** ;
  - motifs : bénéfices non démontrés, confusion, taux sur le sol jugé dissuasif par le maire, frein supposé au rachat de terrains vagues ; recommandation du coordinateur Act 47 (ville en difficulté financière) ;
  - la taxe municipale ne représentait qu'environ un quart de la facture totale (école et comté exclus).
  - Une proposition de retour à mi-chemin a été rejetée.
  - La date de « 2017 » de la question correspond à la **première année sans LVT** ; la décision date de 2016.
- **Harrisburg** : taxe à deux taux depuis 1975 (Hughes 2006 ; Hanson 2021 : toujours active en 2017). Son statut en 2025-2026 est **NON VÉRIFIÉ**.

### B13. Nouvelle-Zélande : passage des communes de la valeur du sol (LV) à la valeur bâtie (CV)
- **McCluskey, William, Arthur Grimes et Jason Timmins (2002)**. *Property Taxation in New Zealand*. Lincoln Institute WP02WM1 [TI].
  - La LV domine de la Seconde Guerre mondiale aux années 1980. Le retour vers la CV commence à partir de 1985, surtout dans les grandes villes.
  - Avant 1976, abandonner ou adopter la LV exigeait un **vote des contribuables** ; ce n'est plus le cas, seule une consultation publique est requise.
  - **Depuis 1989, 9 collectivités sur 57 initialement en LV sont passées à la CV** : Dunedin 1989, Tasman 1991, Banks Peninsula 1992, South Waikato 1993/94, Invercargill 1994, South Taranaki 1994, Otorohanga 1996, Hutt City 1997, Franklin 1999/2000. Aucune n'a fait l'inverse.
  - Les collectivités qui ont basculé ont un revenu moyen par tête plus élevé en 1991 : 18 139 NZD contre 16 861 NZD, différence significative à 5 %. Il s'agit d'une association, sans causalité.
  - Article publié : McCluskey, William, Arthur Grimes, Andrew Aitken, Suzi Kerr et Jason Timmins (2006), « Rating Systems in New Zealand: An Empirical Investigation into Local Choice », *Journal of Real Estate Literature* 14(3) : 381-398 [R, NON LU].
- **Colegrave, Fraser et Tom Winter (Insight Economics) (2019)**. *Analysis of the Current and Past Use of Council Rating Tools in New Zealand*. Rapport final pour la NZ Productivity Commission, 7/5/2019 [TI].
  - Collectivités fixant la taxe générale (*general rates*) sur la CV : **51 % en 2007 → 71 % en 2019** ; sur la LV : **47 % → 29 %** ; sur la valeur locative annuelle (AV) : 2 % → 0 %.
  - Part des recettes de la taxe générale levées sur CV : **41 % → 88 %** ; sur LV : 33 % → 12 %.
  - Hors Auckland, **12 collectivités sont passées de LV à CV depuis 2007, contre 1 en sens inverse**. La fusion d'Auckland (2010) généralise la CV.
  - Les collectivités en LV appliquent plus souvent, et à des niveaux plus élevés, des coefficients majorés pour les entreprises et des coefficients résidentiels.
- **Gemmell, Norman, Arthur Grimes et Mark Skidmore (2019)**. « Do Local Property Taxes Affect New Building Development? Results from a Quasi-Natural Experiment in New Zealand ». *Journal of Real Estate Finance and Economics* 58(2) : 310-333. DOI 10.1007/s11146-017-9651-y [R].
  - La fusion d'Auckland de 2010 entraîne un passage LV → CV dans certaines ex-communes.
  - Doubles différences : **effets sur les travaux d'agrandissement et de transformation, aucun effet détecté sur la construction neuve**, sur seulement 2 ans après la fusion.
- **Raisons du basculement** : peu documentées empiriquement. L'association avec le revenu est établie, la causalité ne l'est pas. Les explications usuelles (capacité contributive perçue, « bénéfice » des services) sont NON VÉRIFIÉES dans les textes lus.

### B14. Corée du Sud : feuille de route pour aligner les valeurs officielles sur le marché (2020), puis abandon
- **Sources** : presse coréenne (Seoul Shinmun 20/03/2024, Economist.co.kr 23/11/2022, Dailian, Segye, Taxwatch) [S]. Aucune étude académique lue.
- **Feuille de route de 2020** (gouvernement Moon) : porter progressivement le **taux de réalisation** (*현실화율*, rapport entre valeur officielle et prix de marché) à **90 % d'ici 2035**, avec des échéances plus rapides pour les biens chers (calendrier détaillé par tranche de prix NON VÉRIFIÉ ; la presse cite 2025, 2027 et 2030 selon la tranche).
- **Ratio de la juste valeur de marché** (*공정시장가액비율*) de l'impôt global sur la détention immobilière (종부세, *jongbuse*) : 80 % de 2008 à 2018, relevé chaque année jusqu'à **95 % en 2021** et 100 % prévu en 2022 [S]. Il est ramené au **plancher légal de 60 % en 2022**.
- **Retour en arrière** :
  - en novembre 2022, les taux de réalisation de 2023 sont ramenés au niveau de 2020 : appartements 72,7 % → 69,0 % ; maisons individuelles 60,4 % → 53,6 % ; terrains 74,7 % → 65,5 % [S] ;
  - le 19/03/2024, le ministère du Territoire annonce **l'abandon** de la feuille de route, qui nécessite une loi. Le taux de 69 % est maintenu 4 ans de suite d'après le *Kyunghyang Shinmun* (mars 2026) [S].
  - La presse lie la feuille de route, qualifiée de « feuille de route de hausse d'impôts », à la **défaite électorale aux élections locales de 2022** [S, interprétation journalistique].
  - Août 2026 (UPI [S]) : projet de refonte du jongbuse pour 2028, avec des taux selon la valeur et non plus selon le nombre de logements, et un seuil relevé de 1,2 à 1,4 Md KRW pour un logement unique.
- **Portée** : c'est le cas d'école d'une **montée en charge programmée par la base** (réévaluation graduelle) **interrompue par l'alternance politique**, dans un contexte de forte hausse des prix (2020-2021). Un calendrier long ne suffit pas s'il coïncide avec une envolée des prix qui fait exploser les cotisations. D'où l'intérêt de **plafonds de hausse annuelle en montant** (Danemark, Norvège) plutôt que de taux de convergence en pourcentage de la valeur.
- **Taïwan** : non traité, faute de sources solides trouvées dans le temps imparti.

---

## Synthèse transversale (pour la note)
1. **Les hausses futures annoncées sont mal capitalisées** (Bradley 2017 ; Elinder-Persson 2017 ; Økland 2021). Il ne faut ni compter sur un « choc de prix à l'annonce », ni supposer que les acheteurs « paient » d'avance l'impôt futur. La saillance compte (Cabral-Hoxby) : informer, c'est-à-dire afficher l'impôt futur à la vente, corrige le biais (Bradley, résumé IPPSR).
2. **Les réévaluations-chocs après un gel tuent les réformes** (Pittsburgh 2001 ; cf. Corée 2020-2024). Il faut des réévaluations régulières, des **plafonds de hausse annuelle** et des taux recalibrés sur les valeurs **réelles** et non projetées.
3. **Un lissage attaché au propriétaire crée du verrouillage** (Proposition 13 : Ferreira, Wasi-White). Il faut privilégier un lissage attaché au bien (Danemark : stigningsbegrænsning maintenue à la vente) ou un **report de paiement par défaut**. Le skatterabat danois, perdu à la vente, crée un verrouillage.
4. **Le report de paiement n'est utilisé que s'il est simple, par défaut et bon marché** (Shan : moins de 1 % aux États-Unis ; Colombie-Britannique : forte croissance, puis hausse du taux en 2026).
5. **Une montée en charge légale très lente est possible** (Norvège : 1 ‰ la première année, +1 ‰/an au plus, plafond de 4 ‰ pour les logements).
6. **Les transitions longues s'enlisent** (ACT : 20 ans, stagnation des rates à environ 29 % des recettes propres, bascule ciblée sur les primo-accédants en 2026). L'effet sur les transactions est rapide (élasticité d'environ 0,6).
7. **Un registre de taux « neutres en recettes » non contraignant** (BW) ne garantit pas la neutralité dans un tiers des communes. Le passage à une assiette sol déplace la charge vers les **maisons individuelles sur grands terrains** et le résidentiel, et l'éloigne du commerce.
