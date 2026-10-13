# Agent A — Notes de vérification : théorie et preuves empiriques classiques sur la taxe foncière (LVT) et les taxes à taux différencié (split-rate)

Date de vérification : 13/10/2026. Les textes téléchargés et leurs extractions sont dans `lit/agentA/`.

Légende du statut de lecture :
- **[TEXTE LU]** : texte intégral lu, passages vérifiés directement.
- **[RÉSUMÉ]** : seul le résumé officiel a été lu (OpenAlex, RePEc ou éditeur).
- **[SECONDAIRE]** : l'information vient d'une source tierce citée.
- **NON VÉRIFIÉ** : aucune vérification n'a été possible.

## Corrections bibliographiques importantes (à reporter dans la note)

1. **Plassmann & Tideman (2000)** ont publié dans le *Journal of Urban Economics* 47(2):216–247, et non dans le *J. Real Estate Finance & Economics*. Les sources sont Crossref et RePEc.
2. **Brueckner & Kim (2003)** ont publié dans *International Tax and Public Finance* 10(1):5–23, et non dans le *Journal of Urban Economics*. Les sources sont Crossref et RePEc.
3. Le titre exact de **Feldstein (1977)** est « The Surprising Incidence of a Tax on Pure Rent: A New Answer to an Old Question ». Le sous-titre « a Ricardian analysis » est inexact.
4. **Palmon & Smith (1998)** occupent les pp. 1099–1111 du JPE 106(5). Crossref le confirme, et le PDF s'arrête bien p. 1111. RePEc indique 1099–1128 par erreur.
5. **Skaburskis (2003)** est **NON VÉRIFIÉ** : aucune publication de 2003 n'a été trouvée. Il existe en revanche Skaburskis, A. (1995), « The Consequence of Taxing Land Value », *Journal of Planning Literature* 10(1):3–21, doi:10.1177/088541229501000101. Ce texte n'a pas été lu, car le PDF trouvé est un scan sans couche texte.
6. **Shoup (1970)** n'établit pas la neutralité temporelle. D'après la citation qu'en donne Mills (1981), Shoup montre au contraire qu'une taxe sur la valeur du site agit comme une hausse du taux d'actualisation et peut donc ne pas être neutre (voir §10).
7. L'ouvrage Lincoln de **Dye & England** existe en deux versions distinctes : le livre collectif de 2009 et le *Policy Focus Report* de 2010. Il faut les citer séparément (voir §8).

---

## 1. Le théorème d'Henry George (HGT) : Arnott & Stiglitz (1979), Vickrey, Stiglitz (2015)

### Arnott & Stiglitz (1979) [TEXTE LU]

- **Citation** : Arnott, R. J. & Stiglitz, J. E. (1979). « Aggregate Land Rents, Expenditure on Public Goods, and Optimal City Size ». *Quarterly Journal of Economics* 93(4):471–500. doi:10.2307/1884466. PDF consulté via Columbia Academic Commons (doi:10.7916/D8086FW3).
- **Question** : quelle est la généralité du HGT, c'est-à-dire de l'égalité entre rentes foncières agrégées et dépenses en bien public dans une ville de taille optimale ? Une migration libre et concurrentielle conduit-elle à des tailles de ville optimales ? Quel lien existe-t-il avec la littérature sur la capitalisation ?
- **Méthode** : théorie. Le modèle résidentiel est monocentrique, avec un bien public local pur. Les résultats sont ensuite généralisés aux grandes économies spatiales.
- **Résultats (vérifiés dans le texte)** :
  - Le HGT, selon lequel les rentes foncières différentielles (DLR) égalent la dépense en bien public pur (P) à la taille optimale, est « far more robust than has previously been suspected ». Il tient lorsque trois conditions sont réunies : (i) l'économie est grande ; (ii) la répartition spatiale de l'activité est Pareto-optimale ; (iii) les rentes différentielles sont bien définies. « If any one of them is violated, Henry George's single tax on differential land rents may provide too much or too little tax revenue » (p. 498).
  - Dans l'exemple simple (ville circulaire, coûts de transport linéaires, lots unitaires), DLR = ½ ATC (coûts de transport agrégés). À la taille optimale, on a donc P = ½ ATC = DLR.
  - Les corollaires donnent un critère de taille : DLR > P ⇔ N > N\*, et DLR < P ⇔ N < N\*.
  - Avec une congestion du transport, la relation devient DLR + ACE = P, où ACE (« aggregate congestion externality ») est la recette d'un péage de congestion optimal (§2.5).
  - Selon le texte, la confiscation des rentes foncières est alors à la fois efficace et constitue le « single tax » qui suffit à financer le bien public (p. 472).
  - **Mise en garde des auteurs** : pour des hypothèses « compétitives » plausibles, la concurrence ne conduit pas à des villes de taille optimale et ne les soutient pas. « The Henry George Theorem may provide a rather poor explanation of the relationship between urban economic aggregates in a competitive economy. »
  - **Capitalisation** : avec des ménages hétérogènes, les écarts de rentes agrégées entre communes sous-estiment la valeur des aménités et surestiment celle des désaménités, y compris des taux d'imposition.
- **Limites** : modèle stylisé, résultats de statique comparative et non de politique fiscale opérationnelle.

### Vickrey [références vérifiées via la bibliographie d'Arnott & Stiglitz et Crossref]

- **Vickrey, W. (1977)**. « The City as a Firm ». Dans M. S. Feldstein & R. P. Inman (dir.), *The Economics of Public Services*, Londres, Macmillan, pp. 334–343. doi:10.1007/978-1-349-02917-4_13. Arnott & Stiglitz (note 3) rattachent le résultat à Mirrlees (1972), Starrett (1974) et Vickrey (1977). Dans des économies planifiées où la concentration spatiale vient des rendements d'échelle de la production, la taille optimale vérifie l'égalité suivante : degré de rendements croissants × valeur de la production = rentes foncières différentielles. Ce texte de Vickrey n'a pas été lu.
- **Citation de Vickrey reprise par *Tax by Design*** (p. 370–371, d'après Vickrey 1999, p. 17) : « The property tax is, economically speaking, a combination of one of the worst taxes—the part that is assessed on real estate improvements …—and one of the best taxes—the tax on land or site value ». Référence : Vickrey, W. (1999), « Simplification, Progression, and a Level Playing Field », dans K. Wenzer (dir.), *Land-Value Taxation: The Equitable and Efficient Source of Public Finance*, Armonk NY, M.E. Sharpe.
- **Vickrey (1970)** est cité par Oates & Schwab (1997) pour la notion de « standard value », c'est-à-dire une évaluation indépendante de l'usage. Il s'agit de « Defining Land Value for Taxation Purposes », dans D. M. Holland (dir.), *The Assessment of Land Value*, référence donnée par Mills 1981. Le texte n'a pas été lu.

### Stiglitz (2015), NBER WP, série en quatre parties [TEXTE LU : parties I et IV]

- **Citations** :
  - Stiglitz, J. E. (2015). « New Theoretical Perspectives on the Distribution of Income and Wealth among Individuals: Part I. The Wealth Residual ». NBER WP 21189, doi:10.3386/w21189.
  - Stiglitz, J. E. (2015). « … Part IV: Land and Credit ». NBER WP 21192, doi:10.3386/w21192.
  - Les parties II (w21190) et III (w21191) existent mais n'ont pas été lues.
- **Ce que Stiglitz dit de la taxation foncière** :
  - Part IV, résumé : « A significant amount of the increase in the wealth income ratio in recent decades is due to an increase in the value of land … Focusing on long run equilibrium, we show that **a tax on the returns on land (including capital gains) can lead to higher incomes and less inequality**. »
  - §1 : la richesse W et le capital productif K divergent à cause de la valeur capitalisée de la rente R/r. « If the returns to land are fully taxed (as they would be with the Henry George tax), [W] and [K] would be fully aligned. »
  - §2 (terre comme bien positionnel) : la taxe foncière augmente le coût d'usage (r + τ) et réduit l'écart entre richesse et capital.
  - §3 (dynamique, bulles foncières, épargne) : une taxe sur le rendement de la terre abaisse le locus d'équilibre du prix foncier. Elle entraîne ainsi « an increase in the capital labor ratio and an increase in wages, validating the common presumption that savings diverted into land investment (or speculation) is money that could otherwise have gone into real investment ». Une taxe sur les plus-values foncières accroît aussi K/L, avec un effet ambigu sur le prix de la terre. L'effet est plus fort si la recette est investie.
  - Part I, p. 9 : « And, indeed, a land tax can actually lead to higher wages ». La note 22 rappelle Arnott-Stiglitz : à taille optimale, DLR = dépense en biens publics locaux = ½ des coûts de transport agrégés. Elle précise aussi que la hausse de valeur foncière inclut une rareté artificielle (zonage).
- **Mécanisme** : c'est essentiellement celui de Feldstein (1977), à savoir la substitution de portefeuille de la terre vers le capital productif.
- **Limites** : modèles théoriques en état stationnaire et en plein emploi, sans estimation chiffrée.

---

## 2. Feldstein (1977) [RÉSUMÉ, plus mécanisme de source SECONDAIRE]

- **Citation** : Feldstein, M. (1977). « The Surprising Incidence of a Tax on Pure Rent: A New Answer to an Old Question ». *Journal of Political Economy* 85(2):349–360. doi:10.1086/260566.
- **Résumé officiel (OpenAlex)** : « The classic example of an unshiftable tax is the general tax on pure rental income. Since Ricardo, economists have believed that the annual net rental income of unimproved land falls by the amount of the annual tax and its price by the capitalized value of this tax. This paper shows that these conclusions are false, that the tax on pure land rents is at least partly shifted, and that the price of land may be increased by the imposition of a tax. Implications are suggested for the analysis of the corporate income tax and the taxation of natural resources. »
- **Mécanisme** [SECONDAIRE ; texte intégral NON lu] :
  - Dans un modèle de croissance à générations imbriquées avec épargnants de cycle de vie, la terre et le capital produit sont deux réserves de valeur substituables pour la retraite.
  - La taxe réduit la valeur de la terre. Si la richesse désirée par les ménages ne baisse pas d'autant, l'épargne se reporte sur le capital produit.
  - K/L et K/terre augmentent. Le taux d'intérêt baisse, ce qui accroît la valeur capitalisée de toute rente, et la productivité marginale de la terre (sa rente brute) augmente.
  - La taxe est donc en partie transférée vers le capital (rendement plus bas) et, côté salaires, vers les travailleurs, qui y gagnent. Le prix de la terre baisse moins que la valeur actualisée de la taxe, voire augmente.
  - Edenhofer, Mattauch & Siegmeier (prépublication PIK 2014, lue) résument que, selon Feldstein, la taxe n'est pas neutre « if there is an alternative in saving decisions to invest in land or capital ». Ils ajoutent que taxer les rentes des facteurs fixes « may enhance efficiency if there is capital underaccumulation » (Feldstein 1977 ; Fane 1984 ; Petrucci 2006).
  - Banzhaf & Lavery (2008, note 5) : « Feldstein (1977) also discusses the effect on savings decisions and the stock of productive capital ».
- **Débat** (références vérifiées via Crossref) :
  - Calvo, Kotlikoff & Rodriguez (1979), « The Incidence of a Tax on Pure Rent: A New (?) Reason for an Old Answer », *JPE* 87(4):869–874, doi:10.1086/260798. Selon le résumé d'Itaya (1997), le résultat de Feldstein disparaît si un motif de legs altruiste opératif est présent (neutralité à la Barro).
  - Fane (1984), « … The Old Reason for the Old Answer », *JPE* 92(2):329–333, doi:10.1086/261227.
  - Petrucci (2006), *J. Public Econ.* 90(4–5):921–933, en économie ouverte.
  - Aucun de ces textes n'a été lu en entier.
- **Pourquoi la taxe n'est pas pleinement capitalisée** : le taux d'actualisation r est endogène et la rente brute de la terre réagit à l'accumulation de capital induite. Le schéma ricardien (r et rente fixes) ne s'applique donc plus. Le résultat est sensible à l'usage de la recette et au motif de legs.

---

## 3. Oates & Schwab (1997), Pittsburgh [TEXTE LU, copie JSTOR]

- **Citation** : Oates, W. E. & Schwab, R. M. (1997). « The Impact of Urban Land Taxation: The Pittsburgh Experience ». *National Tax Journal* 50(1):1–21. doi:10.1086/NTJ41789240 (JSTOR 41789240). Réimprimé dans Oates (2004), Elgar, ch. 16.
- **Question** : quel a été l'effet du passage de Pittsburgh, en 1979–80, à un taux foncier « more than five times the rate on structures » sur l'activité de construction ?
- **Réforme (tableau 2, taux municipaux nominaux en millièmes)** :
  - Avant la réforme, le ratio était de 2:1 : en 1978, 49,5 millièmes sur le terrain contre 24,75 sur le bâti.
  - En 1979, le terrain passe à 97,5 millièmes et, en 1980, à 125,5, le bâti restant à 24,75. En 1983, le terrain atteint 151,5 et le bâti 27. En 1990, les taux sont de 184,5 et 32.
  - Le ratio d'évaluation est de 0,25, si bien que les taux effectifs valent un quart des taux nominaux.
  - Le comté et le district scolaire taxent terrain et bâti au même taux. Au total, le taux foncier n'est donc qu'un peu plus du double du taux sur le bâti (≈ 200–235 % selon les années).
  - Des abattements de trois ans sur les constructions neuves ont été mis en place au même moment.
- **Données** :
  - Valeur réelle des permis de construire (Dun & Bradstreet, 1960–89, ville seule, 15 villes de la Rust Belt).
  - Données du Census (1974–89), découpées entre ville et banlieue et entre résidentiel et non résidentiel.
  - Taux de vacance des bureaux du centre-ville.
- **Méthode** : comparaisons avant/après entre villes. Pour chaque ville, régression du log des permis sur une indicatrice post-1979 (modèle 1), avec une tendance en plus (modèle 2). Le modèle est ensuite augmenté du taux d'occupation des bureaux, pour Pittsburgh seulement.
- **Résultats chiffrés** :
  - **Tableau 3** : la valeur annuelle moyenne des permis à Pittsburgh passe de 181 734 k$ (1960–79) à 309 727 k$ (1980–89), soit **+70,43 %**, en dollars constants de 1982 et en milliers. La **moyenne des 15 villes, Pittsburgh compris, est de −14,42 %**. Seules deux villes progressent : Pittsburgh et Columbus (+15,43 %). Les autres reculent, de −11,5 % (Buffalo) à −67 % (Youngstown).
  - **Tableau 4** : Pittsburgh est la seule ville dont l'indicatrice est positive et significative dans le modèle 1 (0,467, t = 2,81). Dans le modèle 2, le coefficient vaut 0,929 (t = 3,41). Buffalo est également significative dans le modèle 2.
  - **Census** : la valeur totale des permis dans la ville de Pittsburgh augmente de plus de 250 %. Le non-résidentiel est multiplié par plus de trois, le résidentiel progresse peu, et la banlieue recule.
  - **Avec le taux d'occupation des bureaux** : LDB = 6,69 + 0,597 D + 0,057 R, avec D significative (t = 3,90). Un point d'occupation supplémentaire augmente les permis d'environ 5 %, et l'indicatrice reste significative.
  - Les auteurs estiment que l'abattement de trois ans réduit d'environ 15 à 20 % la valeur actualisée des impôts d'un projet à 90 % bâti, soit l'équivalent d'une subvention d'environ 1,5 % du prix. Ce montant n'explique qu'une petite partie du boom.
- **Conclusion des auteurs** : le moteur principal est la pénurie de bureaux (vacance inférieure à 1 % en 1980–81) combinée au programme Renaissance II. La LVT a joué « an important supporting role by enabling the city to avoid rate increases in other taxes that could have impeded development ». Citation pp. 18–19, reprise par Dye & England 2010 : « Our findings thus do not support some of the more extravagant claims … The contribution of land-value taxation is to be understood not in terms of any direct stimulus to development, for there is likely to be little or none if the tax is basically neutral. Rather, land-value taxation provides city officials with a tax instrument that generates revenues but has no damaging side effects on the urban economy. »
- **Limites** : une seule ville traitée, sans contrôle synthétique. La réforme coïncide avec Renaissance II, avec des abattements fiscaux et avec la pénurie de bureaux. Les permis de construire ne mesurent pas la densité. La section théorique couvre aussi l'effet de calendrier (voir §10).

---

## 4. Plassmann & Tideman (2000) [RÉSUMÉ via extrait de moteur de recherche et sources SECONDAIRES ; texte JUE NON lu]

- **Citation** : Plassmann, F. & Tideman, T. N. (2000). « A Markov Chain Monte Carlo Analysis of the Effect of Two-Rate Property Taxes on Construction ». *Journal of Urban Economics* 47(2):216–247. doi:10.1006/juec.1999.2140. **Ce n'est pas le JREFE.**
- **Données et méthode**, d'après l'extrait du résumé (Semantic Scholar via moteur de recherche) et la thèse de Plassmann (Virginia Tech, 1997, résumé lu) :
  - 15 communes de Pennsylvanie à deux taux, sur 1972–1994, comparées à 204 communes similaires à taux unique.
  - Les permis de construire sont modélisés comme un processus de Poisson à paramètre log-normal, estimé par MCMC (échantillonneur de Gibbs).
- **Résultat** : les villes à deux taux construisent significativement plus que sous un taux unique.
  - Dye & England (2010, lu) chiffrent cet effet à « an increase in residential construction on the order of 3 or 4 percent ».
  - Banzhaf & Lavery (2008, lu) : effet significatif sur le nombre de permis, mais « they do not find clear evidence that it increases the value of those permits ».
- **Thèse (résumé lu)** :
  - Un modèle binomial négatif sur 219 communes donne un effet positif mais non significatif.
  - Le modèle MCMC donne un effet « strong and significantly positive » sur le nombre de permis.
  - L'effet sur la valeur par permis n'est pas significatif, mais l'effet sur la valeur totale de la construction est positif et significatif.
- **Limites** : résultats sensibles à la spécification (binomial négatif contre Poisson-lognormal) et risque d'adoption endogène. Les écarts de taux effectifs sont faibles : selon la thèse, l'écart ajusté va de 0,16 % (Coatesville) à 12,17 % (Aliquippa) de la valeur de marché.
- **NON VÉRIFIÉ** : les coefficients exacts de l'article publié dans le JUE.

---

## 5. Banzhaf & Lavery (2010) [WP 2008 lu en entier ; RÉSUMÉ JUE lu]

- **Citation** : Banzhaf, H. S. & Lavery, N. (2010). « Can the Land Tax Help Curb Urban Sprawl? Evidence from Growth Patterns in Pennsylvania ». *Journal of Urban Economics* 67(2):169–179. doi:10.1016/j.jue.2009.08.005. Version de travail : « How "Smart" is the Split-Rate Property Tax? », Lincoln Institute WP08HB1 (2008) ; SSRN doi:10.2139/ssrn.1247862.
- **Question** : la taxe à taux différencié augmente-t-elle le ratio capital/terre et, surtout, la densité (davantage de logements plutôt que des logements plus grands) ?
- **Données** : secteurs de recensement (tracts) de Pennsylvanie à surface normalisée, recensements 1970–2000. Environ 18 villes de Pennsylvanie appliquent la taxe à taux différencié, la plupart l'ayant adoptée dans les années 1980.
- **Méthode** :
  - Régression en premières différences (variation décennale en %) avec effet fixe par tract, effets décennie et covariables retardées.
  - Variable d'intérêt : une indicatrice split-rate (SR) ou le ratio des taux terrain/bâti. Erreurs-types groupées par juridiction.
  - Appariement non paramétrique sur score de propension (Abadie-Imbens).
  - Décomposition : %Δpièces totales ≈ %Δpièces par logement + %Δlogements.
- **Résultats (WP 2008)** :
  - **Pièces totales** (proxy de capital/terre) : +5 à 6 points de croissance par décennie par rapport aux contrôles (modèles avec indicatrice), au cours des une ou deux premières décennies. Avec le ratio des taux, un ratio de 2:1 donne environ +1 point, et le ratio moyen de 4:1 environ +3 points.
  - **Taille des logements** : effet nul dans les modèles avec indicatrice. Dans les modèles avec ratio, l'effet est d'environ +0,2 point (+0,6 pour 4:1), soit environ un cinquième de l'effet total.
  - **Nombre de logements** : environ +5 points (indicatrice), et +0,6 point pour 2:1, soit environ +2 points pour 4:1. Les effets sur la population ne sont présents que dans les modèles avec indicatrice.
  - **Appariement** : effets de densité de +7 points (non pondéré) et +10 points (pondéré), non significatifs (p unilatéraux d'environ 0,29 et 0,18).
  - **Synthèse des auteurs** : +2 à +10 points sur la croissance de la densité de logements et 0 à +7 points sur la densité de population au cours des premières décennies, selon le modèle.
- **Résumé JUE** : « We confirm the theoretical prediction that the split-rate tax raises the capital/land ratio … the primary effect is in more housing units, rather than bigger units … We find adoption of the split-rate tax increases the number of housing units, and that these units follow a more dense pattern of development. »
- **Limites, selon les auteurs** :
  - Ils ne prétendent pas avoir montré une réduction de l'étalement. Appliquée en périphérie, une hausse de densité locale peut au contraire accroître l'étalement à l'échelle métropolitaine.
  - Leurs résultats contrastent avec Song & Zenou (2006), qui trouvent des aires urbaines plus compactes là où l'impôt foncier est plus élevé.
  - Échantillon limité à la Pennsylvanie. Effet de calendrier possible si l'évaluation se fait à l'usage courant (voir §10).
- **Remarque** : l'OCDE (2022, p. ~117) résume Banzhaf & Lavery comme trouvant une hausse « both [of] the total number of housing units and the average number of rooms per dwelling ». Cette lecture est imprécise : l'effet sur la taille des logements est modeste ou nul selon la spécification.

---

## 6. Brueckner & Kim (2003) [RÉSUMÉ lu ; Proposition 1 via Song & Zenou 2005, WP lu]

- **Citation** : Brueckner, J. K. & Kim, H.-A. (2003). « Urban Sprawl and the Property Tax ». *International Tax and Public Finance* 10(1):5–23. doi:10.1023/A:1022260512147. **Ce n'est pas le JUE.**
- **Question** : l'impôt foncier sur la propriété (terrain et bâti) favorise-t-il l'étalement urbain ?
- **Méthode** : modèle de ville monocentrique fermée avec marché foncier, propriétaires absents et préférences CES.
- **Résultat** :
  - Deux effets opposés s'affrontent. D'une part, l'effet « amélioration » ou hauteur des bâtiments : la taxe réduit le capital par hectare, donc la densité, et la ville s'étend. D'autre part, l'effet « taille des logements » : la taxe, répercutée sur le prix du logement, réduit la surface consommée, ce qui augmente la densité et contracte la ville.
  - Résumé : « a countervailing effect from lower dwelling sizes may dominate, raising densities and making cities smaller … this latter outcome is guaranteed under CES preferences when the elasticity of substitution sigma is high … numerical results for the Leontief case (σ = 0) suggest that the property tax encourages urban sprawl when substitution between housing and other goods is low ».
  - Seuil, d'après Song & Zenou (2005, WP Lincoln) : si σ ≥ 1, ∂x_f/∂θ < 0, c'est-à-dire que l'impôt réduit la taille de la ville. Si σ < 1, le signe est ambigu. Banzhaf & Lavery (note 4) confirment que le cas Cobb-Douglas et le cas σ > 1 garantissent l'effet « pervers ».
- **Implication pour la LVT** : passer de l'impôt sur la propriété à une taxe foncière n'entraîne pas nécessairement une densification. C'est une question empirique, d'où Banzhaf & Lavery (2010).
- **Limites** : propriétaires absents, ville fermée. Le seul résultat favorable à l'étalement est numérique (cas Leontief).

---

## 7. Mirrlees Review, *Tax by Design* (2011), chapitre 16 [TEXTE LU]

- **Citation** : Mirrlees, J., Adam, S., Besley, T., Blundell, R., Bond, S., Chote, R., Gammie, M., Johnson, P., Myles, G. & Poterba, J. (2011). *Tax by Design: The Mirrlees Review*. Oxford, Oxford University Press for IFS. Chapitre 16, « The Taxation of Land and Property », pp. 368–405. PDF libre sur ifs.org.uk.
- **Arguments clés** :
  - **Efficacité** : « Land, whether used for business or residential property, can be taxed at an arbitrarily high rate on economic efficiency grounds. » La valeur actualisée d'une LVT « would be reflected one-for-one in a lower price of land: the classic example of tax capitalization ». La perte en capital subie par les propriétaires à l'annonce de la taxe est son seul effet. Enfin, « Business property … should not be taxed » : c'est un intrant produit.
  - « The economic case for a land value tax is simple, and almost undeniable » (p. 373).
  - **Zonage et urbanisme** : en janvier 2009, dans le sud-est de l'Angleterre, un hectare valait environ 20 000 £ en terre arable, 1,3 M£ en terrain industriel et 2,5 M£ en terrain à bâtir résidentiel. Une LVT pourrait réduire marginalement l'incitation à demander un changement d'affectation, mais l'ampleur des gains en jeu rend ce risque peu probable. Les taxes sur la plus-value d'urbanisme (development ou betterment taxes de 1947, 1967, 1973 et 1976) ont échoué faute de crédibilité. Une LVT annuelle ne crée pas d'incitation à retarder.
  - **Calendrier (note 4)** : Bentick (1979) et Oates & Schwab (1997) montrent qu'une LVT peut biaiser le choix vers les usages à rendement précoce. Selon les auteurs, ce biais serait évité en taxant la valeur de « best use », même si cette valeur est encore plus difficile à évaluer, et il ne suffit pas à rejeter la LVT.
  - **Évaluation** : principal obstacle pratique, car il faut séparer la valeur du terrain de celle du bâti alors que les transactions sur terrains nus sont rares. Les auteurs rappellent toutefois que l'Angleterre compte environ 1,7 M de propriétés non résidentielles déjà évaluées par la VOA (environ 4 000 ETP en 2009–10), avec réévaluation tous les cinq ans. Ils ajoutent que « the figure for land value does not have to be exact … for the LVT to be efficient », l'imprécision créant cependant des iniquités. Ils citent les expériences du Danemark, des États-Unis et de l'Australie (Japon, Corée et Taïwan en note).
  - **Proposition** : remplacer les *business rates* (environ 24 Md£ en 2009–10, soit plus de 4 % des recettes) par une LVT sur les terrains commerciaux et agricoles, à revenu constant. Le taux serait d'environ **4 % de la valeur foncière par an**, introduit progressivement à partir d'environ 0,5 %, selon Muellbauer (2005). Les gains d'aubaine liés à la suppression des rates seraient compensés par les pertes d'aubaine liées à la LVT.
  - **Logement** : « We do not propose a separate tax on residential land value. » Les auteurs proposent de remplacer la council tax par une **housing services tax (HST)** proportionnelle à la valeur locative actuelle, sans plafond, pour les occupants propriétaires comme pour les locataires. Elle reviendrait à environ 0,6 % de la valeur du bien, soit environ 12 % de la valeur locative à revenu constant, avec un idéal de 17,5 % (taux de TVA). Le stamp duty land tax serait supprimé et sa recette remplacée par la HST (résidentiel) et la LVT (non résidentiel). Les auteurs recommandent aussi une allocation pour rendement normal en faveur des bailleurs.
- **Limites (selon les auteurs)** : la faisabilité administrative « cannot say conclusively ». D'où la recommandation d'une « thorough official effort to design a workable system ».

---

## 8. Dye & England (dir.) : Lincoln Institute

### a) Livre collectif de 2009 [table des matières lue ; chapitres NON lus]

- **Citation** : Dye, R. F. & England, R. W. (dir.) (2009). *Land Value Taxation: Theory, Evidence, and Practice*. Cambridge MA, Lincoln Institute of Land Policy. 248 p., ISBN 978-1-55844-185-9.
- **Chapitres** :
  - Dye & England, « The Principles and Promises of LVT » (p. 3).
  - Bourassa, « The U.S. Experience » (p. 11).
  - Franzsen, « International Experience » (p. 27).
  - Oates & Schwab, « The Simple Analytics of LVT » (p. 51).
  - Plummer, « Fairness and Distributional Issues » (p. 73).
  - Anderson, « A Review of the Evidence » (p. 99).
  - Coe, « The Legal Framework in the US » (p. 129).
  - Bell, Bowman & German, « The Assessment Requirements for a Separate Tax on Land ».
  - Bourassa, « The Political Economy of LVT ».

### b) Policy Focus Report de 2010 [TEXTE LU]

- **Citation** : Dye, R. F. & England, R. W. (2010). *Assessing the Theory and Practice of Land Value Taxation*. Policy Focus Report, Lincoln Institute, ISBN 978-1-55844-204-7. Ce rapport condense le livre.
- **Conclusions principales** :
  - « Land value taxation would enhance both the fairness and the efficiency of the property tax. » La taxe foncière est neutre vis-à-vis du calendrier et de la densité, alors que la taxation du bâti favorise vraisemblablement l'étalement. Plus de 30 pays ont mis en œuvre une forme de LVT.
  - **Sur les preuves empiriques** : « a number of studies … although the results are generally inconclusive ». Plus loin : « statistical results are usually inconclusive. Very few land value tax studies can satisfy the research standards … ».
  - **Encadré Scranton** : terrain taxé à 10,3 % et bâti à 2,2 % de la valeur imposable, pour un taux unique équivalent de 3,7 %. La baisse du taux municipal sur le bâti dépasse 40 %, mais celle du taux total (comté et écoles compris) n'est que de 8 %. Le ratio d'évaluation est de 7,1 % de la valeur de marché, et la variation du coût du capital n'atteint qu'environ 1 %, d'où un risque de biais de sélection.
  - **Synthèse d'Anderson (2009)** : Mathis & Zech (1983) ne trouvent aucun effet. Bourassa (1990) trouve un effet sur le résidentiel à Pittsburgh seulement. Oates & Schwab (1997) observent +70 % de permis. Plassmann & Tideman (2000) estiment +3 à 4 % de construction résidentielle. Lusht (1992, Melbourne) trouve un effet positif, mais avec un risque de sélection.
  - **Recommandations** : bonnes pratiques et réévaluations fréquentes, mise en place progressive des deux taux sur plusieurs années, et crédit d'impôt pour les ménages « land-rich but income-poor ».
- **Limites** : rapport de plaidoyer prudent, sans méta-analyse quantitative.

---

## 9. Capitalisation de l'impôt foncier

### Oates (1969) [TEXTE LU]

- **Citation** : Oates, W. E. (1969). « The Effects of Property Taxes and Local Public Spending on Property Values: An Empirical Study of Tax Capitalization and the Tiebout Hypothesis ». *JPE* 77(6):957–971. doi:10.1086/259584.
- **Données** : 53 communes résidentielles du nord-est du New Jersey, recensement de 1960 (valeur médiane des logements).
- **Méthode** : doubles moindres carrés (2SLS), avec instrumentation du taux de taxe et de la dépense par élève.
- **Résultat** : à dépense publique constante, une hausse du taux effectif de 2 % à 3 % réduit la valeur d'une maison type de 20 000 $ d'environ 1 500 $. Une capitalisation complète donnerait environ 2 260 $ (actualisation à 5 %, 40 ans). La capitalisation est donc d'**environ deux tiers**. Le taux effectif moyen est de 2,4 %.
- **Critique de King (1977)** : King, A. T., « Estimating Property Tax Capitalization: A Critical Comment », *JPE* 85(2):425–431, doi:10.1086/260574 [TEXTE LU]. Le taux de capitalisation implicite varie avec la valeur du logement : 40 % à 32 000 $ et 92 % à 14 000 $. En respécifiant le modèle avec le paiement d'impôt plutôt qu'avec le taux, King obtient une capitalisation d'environ 40 %.

### Palmon & Smith (1998) [TEXTE LU]

- **Citation** : Palmon, O. & Smith, B. A. (1998). « New Evidence on Property Tax Capitalization ». *JPE* 106(5):1099–1111. doi:10.1086/250041.
- **Données** : 501 ventes de maisons en 1989 dans 50 lotissements de la banlieue nord-ouest de Houston. Les districts de services municipaux (MUD) fournissent des services identiques mais appliquent des taux d'impôt très différents (de 2,30 $ à plus de 15 $ pour 1 000 $, moyenne 7,90 $), liés à l'historique de leur endettement. Ce dispositif permet d'éviter la corrélation entre taxes et services.
- **Méthode** : modèle hédonique non linéaire estimé par maximum de vraisemblance, avec taux de capitalisation ρ = ρn + βτ·τ.
- **Résultats** :
  - Avec ρn = 3 %, comme Yinger et al., la capitalisation est d'environ **62 %** (0,617 ; 0,564 à 0,639 selon les spécifications), significativement inférieure à 100 %. Elle est cependant bien supérieure aux **15–30 %** trouvés par Yinger et al. (1988) sous la même hypothèse.
  - Avec ρn = 6,5 %, valeur dérivée de Linneman & Voith (1991), la capitalisation est légèrement supérieure à 100 % mais non significativement différente d'une **capitalisation complète**.
- **Limites** : le taux d'actualisation est imposé et le résultat lui est proportionnel. Il s'agit d'un marché particulier : banlieue de Houston pendant le krach immobilier de 1989.

### Yinger, Bloom, Börsch-Supan & Ladd (1988) [NON lu ; résultat SECONDAIRE via Palmon & Smith]

- **Citation** : Yinger, J., Bloom, H. S., Börsch-Supan, A. & Ladd, H. F. (1988). *Property Taxes and House Values: The Theory and Estimation of Intrajurisdictional Property Tax Capitalization*. Academic Press (Studies in Urban Economics).
- **Méthode et résultat** : l'étude exploite des réévaluations au Massachusetts (Brockton et d'autres villes). Les taux de capitalisation sont de 15–30 % pour un taux d'actualisation net de 3 %, d'après Palmon & Smith (1998).
- **NON VÉRIFIÉ** : la liste exacte des villes et le chiffre par ville.

**Note pour la LVT** : ces études portent sur l'impôt foncier sur la propriété (terrain et bâti), pas sur une LVT pure. Le passage de « l'impôt est capitalisé dans les prix » à « une LVT serait capitalisée dans la valeur des terrains » est une inférence, qui reste soumise à l'objection de Feldstein (§2).

---

## 10. Neutralité temporelle : Shoup (1970), Bentick (1979), Mills (1981), Tideman (1982), Wildasin (1982), Skaburskis

### Références

- **Shoup, D. C. (1970)**. « The Optimal Timing of Urban Land Development ». *Papers of the Regional Science Association* 25(1):33–44. doi:10.1007/BF01935815 (aussi 10.1111/j.1435-5597.1970.tb01476.x). [RÉSUMÉ SECONDAIRE seulement]
  - Selon le résumé : modèle wicksellien modifié. La date optimale de développement dépend du taux d'actualisation, du taux de l'impôt foncier, des revenus d'un usage intérimaire et de l'évolution du « highest and best use ».
  - **Mills (1981, note 3) cite Shoup p. 39** : « It is interesting that the difference between this optimal development timing condition and the one found previously in the absence of a land tax is one sense in which a pure site value tax may not be perfectly neutral in its effect on resource allocation, as is frequently claimed ». Shoup est donc un précurseur de la **non-neutralité**, pas de la neutralité.
- **Bentick, B. L. (1979)**. « The Impact of Taxation and Valuation Practices on the Timing and Efficiency of Land Use ». *JPE* 87(4):859–868. doi:10.1086/260797. [NON lu]
- **Mills, D. E. (1981)**. « The Non-Neutrality of Land Value Taxation ». *National Tax Journal* 34(1):125–129. doi:10.1086/NTJ41862356. [TEXTE LU]
  - « It is true that a (less than 100 percent) tax on land income is neutral, but this does not extend necessarily to a tax on capitalized land value. » La somme actualisée des paiements est plus forte pour les flux de revenus tardifs.
  - Lorsque le marché foncier s'ajuste de façon endogène, la distorsion est atténuée sans être éliminée.
- **Tideman, T. N. (1982)**. « A Tax on Land Value Is Neutral ». *NTJ* 35(1):109–111. doi:10.1086/NTJ41862425. [NON lu]
- **Wildasin, D. E. (1982)**. « More on the Neutrality of Land Taxation ». *NTJ* 35(1):105–108. doi:10.1086/NTJ41862424. [NON lu]
- **Skaburskis (1995)**. *J. Planning Literature* 10(1):3–21, doi:10.1177/088541229501000101. [NON lu]. **« Skaburskis (2003) » est NON VÉRIFIÉ.**

### Explication (exemple numérique d'Oates & Schwab 1997, tableau 1 [TEXTE LU])

**Hypothèses** :
- Usage A immédiat : 1 000 $ par an à perpétuité.
- Usage B en attendant une période : 1 100 $ par an à perpétuité à partir de t = 1.
- Taux d'intérêt r = 10 %.
- Sans impôt, V_A = 10 000 et V_vacant = 11 000/1,1 = 10 000, d'où l'indifférence entre les deux usages.

**Cas 1 — taxe de 20 % sur la rente** : les deux valeurs baissent de 20 %, l'indifférence est préservée et la taxe est neutre.

**Cas 2 — taxe de 2 % sur la valeur foncière évaluée à l'usage courant** :
- Résultats : V_A = (1 000 − t·V_A)/r = 8 333 et V_vacant = 8 170. La taxe favorise donc A, le développement précoce.
- Mécanisme : les revenus futurs sont capitalisés dans la valeur actuelle et donc taxés avant d'être perçus. C'est « equivalent to raising the rate of discount by the amount of the tax rate on land » (Bentick ; Mills), soit une taxe sur l'attente.

**Cas 3 — taxe évaluée au « highest and best use »** :
- La base devient indépendante de l'usage choisi : toute parcelle est taxée comme si elle rapportait 1 000 $ en t = 1 puis 1 100 $ ensuite. On obtient V_A = 8 170 = V_vacant.
- La taxe redevient forfaitaire au sens économique : la décision du propriétaire ne modifie pas son impôt, donc **la neutralité est rétablie** (Wildasin 1982 ; Tideman 1982 ; « standard value » de Vickrey 1970).

**Précisions d'Oates & Schwab** :
- L'argument populaire selon lequel la LVT « pénalise le terrain vacant » est « simply incorrect ». La LVT pèse de la même façon que le terrain soit développé ou non, et c'est précisément pourquoi elle est neutre.
- Un « effet de liquidité » n'apparaît qu'en cas de contraintes de crédit. Bourassa (1990) n'en trouve aucune trace.
- **À Pittsburgh**, les évaluations étaient en principe fondées sur le highest and best use, mais en pratique elles résultaient de compromis et de contentieux. L'effet de calendrier « cannot be ruled out categorically » mais était « probably not of much importance ».

---

## 11. Pays appliquant une taxe sur le seul terrain, et OCDE (2022)

### OCDE (2022) [TEXTE LU]

- **Citation** : OECD (2022). *Housing Taxation in OECD Countries*. OECD Tax Policy Studies, No. 29, OECD Publishing, Paris. doi:10.1787/03dfe007-en. ISBN 978-92-64-86268-5 (pdf).
- **Constats** :
  - « Pure land taxes are found in only three OECD countries (New South Wales in Australia, Denmark and Estonia), while Finland and some municipalities in Hawaii and Pennsylvania, United States, apply higher tax rates on land than on buildings (i.e. split-rate taxation). » Un autre passage du rapport mentionne seulement la Nouvelle-Galles du Sud et le Danemark.
  - « Recurrent taxes on immovable property are considered one of the most economically efficient forms of taxation … in theory a pure land tax would be more efficient as it would not discourage investment in capital improvements, but most countries tax both land and improvements because of the practical difficulties of measuring the value of each separately. »
  - Les impôts récurrents sur la propriété immobilière représentent 1,03 % du PIB en 2019 (contre 0,94 % en 1965). Les impôts sur la propriété au sens large représentent environ 6 % des recettes fiscales en moyenne dans l'OCDE.
  - **Recommandation centrale** : renforcer l'impôt récurrent sur la base de valeurs régulièrement mises à jour et réduire les droits de mutation.
  - **Section split-rate** : « Split-rate taxes could help enhance housing supply and contain urban sprawl, but their success will partly depend on interactions with other land-use policies ». Le rapport mentionne que 85 % des propriétaires concernés en Pennsylvanie ont vu leur impôt baisser (Hartzok 1997, source militante). Il signale aussi les difficultés d'évaluation des terrains et l'inefficacité possible en cas de restrictions de hauteur.

### Pays : base et taux (sources officielles ou secondaires, vérification 10/2026)

**Nouvelle-Galles du Sud (Australie)** [site Revenue NSW lu]
- Base : valeur foncière non bâtie fixée par le Valuer General, moyenne sur trois ans, agrégée pour tous les terrains d'un même propriétaire.
- Seuil général : 1 075 000 AUD, gelé à partir de 2025. Taux : 100 $ + 1,6 % au-delà du seuil.
- Seuil premium : 6 571 000 AUD. Le taux de 2 % au-delà de ce seuil provient d'une source secondaire (Coutts Legal).
- Exonérations : résidence principale et production primaire.
- Chaque État australien a son propre impôt foncier (OCDE) ; leurs taux n'ont pas été vérifiés ici.

**Danemark (*grundskyld*)**
- Base : la grundskyld porte sur la valeur du terrain [lex.dk lu]. Depuis la réforme de 2024, la base est égale à 80 % de la valeur foncière de l'année précédente [EY Danemark, secondaire].
- Taux : de 2007 à 2023, le taux municipal était compris entre 16 et 34 ‰ [lex.dk]. Depuis 2024, il est compris entre 0 et 30 ‰, avec des plafonds par commune pour 2024–2028 allant de 3,1 ‰ (Frederiksberg) à 17,7 ‰ (Varde) [EY, secondaire ; **texte de loi NON vérifié**].
- Le Danemark taxe aussi la valeur des logements occupés par leur propriétaire (*ejendomsværdiskat* : 5,1 ‰ jusqu'à 9,2 M DKK, 14 ‰ au-delà [EY]) et le bâti commercial (*dækningsafgift*). Ce n'est donc pas un système « terrain seulement » au sens strict.

**Estonie (*maamaks*)** [site EMTA lu via moteur de recherche]
- Base : valeur imposable issue d'évaluations de masse ; taux fixés par les communes.
- Fourchettes 2025–2026 : 0,1–1 % pour le terrain résidentiel, 0,1–0,5 % pour les terres productives (agricoles), 0,1–2,0 % pour les autres terrains.
- Les anciennes sources donnent 0,1–2,5 %.
- **NON VÉRIFIÉ** : le régime d'exonération du terrain de la résidence principale après 2024.

**Hong Kong** [communiqués officiels via moteur de recherche]
- Pas de taxe sur le terrain seul. Les *rates* représentent 5 % de la valeur locative imposable (rateable value) du bien entier.
- La *Government rent*, égale à 3 % de cette même valeur, est due sur certains baux fonciers.
- Le foncier public est concédé à bail, avec des primes foncières (land premiums).
- **NON VÉRIFIÉ** : le poids des primes dans les recettes.

**Singapour** [IRAS via moteur de recherche]
- Pas de taxe sur le terrain seul : l'impôt porte sur la valeur locative annuelle (*annual value*) du bien.
- Les taux sont progressifs : 0–32 % pour les propriétaires occupants, 12–36 % pour les autres logements (2024), 10 % pour les autres biens.

**Finlande** : système à taux différencié appliqué au niveau national, selon l'OCDE. **NON VÉRIFIÉ** : les taux.

**Pennsylvanie** : environ 15 communes utilisaient la taxe à deux taux en 2010 (Dye & England) ; l'OCDE parle de « almost two dozen » communes l'ayant introduite à ce jour. Pittsburgh l'a abandonnée en 2001 après près de neuf décennies, en grande partie à cause de pratiques d'évaluation défaillantes dans le comté d'Allegheny : gel des évaluations en 1996, puis réévaluation en 2001 (Dye & England 2010, lu).

**Autres** : le Policy Focus Report de Dye & England énumère plus de 30 pays ayant une forme de LVT (Nouvelle-Zélande depuis 1849, Australie 1884, Danemark 1922, Estonie 1993, Taïwan, Kenya, etc.). L'Afrique du Sud est revenue à un impôt foncier sur la propriété en 2001 (loi nationale).
