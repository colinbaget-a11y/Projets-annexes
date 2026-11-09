# Revue de littérature : chômage, natalité, partage des revenus dans le couple, unité d'imposition

*Note de travail pour la fusion IR-CSG-CRDS (novembre 2026). Chaque chiffre provient d'un document ouvert et lu (PDF ou page officielle), sauf mention « non vérifié » ou « calcul propre ». Les PDF sont dans `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/litB/`.*

---

## 1. Allocations chômage : élasticité de la durée au montant

### Études et résultats

| Étude | Question / données | Identification | Résultat (élasticité de la durée au montant, ε) | Limites |
|---|---|---|---|---|
| **Schmieder & von Wachter (2016)**, *Annual Review of Economics* (NBER WP 22564) | Synthèse | Revue | Tableau 2 : 18 estimations, 5 pays. **Médiane 0,53 ; fourchette 0,1-2**. États-Unis seuls : médiane 0,38 (0,1-1,2), toutes sauf deux < 0,7. Les élasticités au montant sont « un peu plus élevées » que celles à la durée potentielle (médiane 0,37 en Europe, Tableau 1). | Hétérogénéité des définitions : durée d'indemnisation ou durée sans emploi. Les effets macro sont plutôt plus faibles que les effets micro (Crépon et al. 2013 en France, Lalive et al. 2015). |
| **Card, Johnston, Leung, Mas, Pei (2015)**, *AER P&P* 105(5) | Missouri, données administratives 2003-2013 | Régression à coude (RKD) au plafond de l'allocation hebdomadaire | **ε ≈ 0,35 avant la récession (2003-2007) ; 0,65-0,9 en 2008-2013** | L'élasticité augmente avec le chômage. Contexte américain : indemnisation courte. |
| **Landais (2015)**, *AEJ: Policy* 7(4) | CWBH, 5 États américains, années 1970-1984 | RKD (coudes du barème) | D'après le résumé, la réponse de l'effort de recherche vient « autant des effets de liquidité que de l'aléa moral ». SW (2016, tableau 2) retiennent une élasticité de 0,29 pour cette étude. | Je n'ai pas ouvert l'article (seulement le résumé AEA et le tableau de SW). |
| **Kolsrud, Landais, Nilsson, Spinnewijn (2018)**, *AER* 108(4-5) (version lue : IZA DP 9185, 2015) | Suède, registres administratifs sur le chômage, les revenus et le patrimoine, 1999-2007 | RKD sur les coudes du barème qui dépendent de la durée | **ε_D,b = 1,53 (0,13)** pour une hausse du montant sur tout l'épisode. Au taux de remplacement de 0,8, cela équivaut à **ε_D,1−r = −0,38** (élasticité au « net du remplacement »). Le coût d'aléa moral est plus faible quand la hausse intervient tard dans l'épisode. Conclusion : aucune justification à un profil d'allocation décroissant. | Taux de remplacement très élevé au coude. La version publiée en 2018 n'a pas été relue ; ses chiffres peuvent différer. |
| **Comité d'évaluation de la réforme de l'assurance chômage 2019-2021 (Dares, avril 2025)** ([vie-publique](https://www.vie-publique.fr/files/rapport/pdf/298088.pdf)) | Réforme du SJR (fins de contrat à partir d'octobre 2021) : **SJR −25 % et AJ −18 % en moyenne**, durée potentielle allongée. Données MiDAS. Équipes Paris-Cité, IPP et Unédic. | Doubles différences : comparaison avant/après réforme et entre allocataires plus ou moins touchés selon la part d'intercontrats | Une baisse de 10 % du SJR réduit la durée sans emploi **de 1,4 à 5 %**. Si l'on attribue tout l'effet à l'AJ, **une baisse de 10 % de l'AJ réduit la durée sans emploi de 4 à 7 %, soit ε ≈ 0,4-0,7**. Unédic : +3,5 à +5,7 points de reprise d'emploi à 3 mois (taux de base 38 %) ; durée −12 %, **ε_AJ = 0,7**. Paris-Cité : −10 jours (−6 %) avant le premier emploi. | **L'effet passe entièrement par des contrats de moins de 6 mois**, sans effet sur les CDI ni sur les CDD de plus de 6 mois. Population très particulière (parcours fractionnés). Contexte de sortie de crise sanitaire. |
| Idem, **dégressivité** (3 % des allocataires, salaire > 4 900 € bruts) | Baisse jusqu'à 30 % de l'allocation à partir du 7e mois | Évaluations Dares et Unédic | Pour les allocataires concernés au taux de 30 % : durée indemnisée −2 mois environ, durée de non-emploi salarié −1,5 mois environ. Ajustement dès le différé d'indemnisation. Pas d'effet sur le type de contrat ni sur le salaire. **Les effets de comportement dépassent le tiers des économies mécaniques.** | Population aisée, surtout masculine. |
| **Le Barbanchon (2016)**, *Labour Economics* 42 | France : durée potentielle portée de 7 à 15 mois pour des travailleurs peu employables | Régression sur discontinuité | Taux de sortie vers l'emploi −28 % (environ +2,5 mois de chômage), sans effet sur la qualité de l'emploi retrouvé | Porte sur la durée potentielle, pas sur le montant. **Lu seulement au niveau du résumé et de la note IPP.** |
| **Le Barbanchon, Rathelot, Roulet (2019)**, *JPubE* 171 (NBER WP 23406) | Salaire de réserve déclaré à l'inscription à Pôle emploi | Doubles différences sur une réforme de la durée potentielle, plus une discontinuité selon l'âge | Le salaire de réserve ne répond pas à la durée potentielle : **les élasticités supérieures à 0,006 sont exclues** | Porte sur la durée potentielle, pas sur le montant. Le canal de la sélectivité est quasi nul ; la réponse passe par l'effort de recherche. |

### Exemple chiffré (calcul propre)
- La réforme supprime l'exonération de fait et soumet l'ARE au barème commun. **Hypothèse : allocation nette −5 %.** Avec ε compris entre 0,3 et 0,7 (fourchette du comité pour l'AJ et des RKD américains hors récession), la durée de chômage indemnisé ou de non-emploi baisse de **1,5 % à 3,5 %, valeur centrale −2,5 % (ε = 0,5)**.
- Ordre de grandeur en jours : la baisse de 10 jours mesurée par Paris-Cité correspond à 6 % de la durée, soit une durée de base d'environ 165 jours (déduction propre). Une baisse de 2,5 % représente alors **environ 4 jours de chômage en moins par épisode**.
- Avec ε = 1,5 (Suède), la baisse atteindrait 7,5 %. C'est un majorant.
- Je n'ai pas vérifié ici le régime actuel de CSG sur l'ARE : taux dépendant du revenu fiscal de référence et seuil d'exonération lié au Smic journalier. Il faut le contrôler dans la circulaire Unédic de l'année.

### Taxer les allocations est-il « efficace » ?
- **Logique de Baily-Chetty.** Le gain fiscal d'une baisse du montant net est à peu près égal à ε (coût d'aléa moral) : chaque euro retiré procure ε euros d'économie supplémentaire grâce au retour plus rapide à l'emploi. Le comité le confirme pour la dégressivité (effets de comportement supérieurs au tiers des effets mécaniques). La perte porte sur l'assurance.
- **L'arbitrage n'est pas tranché.**
  - Landais (2015) : environ la moitié de la réponse est un effet de liquidité, qui n'est pas une distorsion. Le coût d'efficacité est donc inférieur à ce que suggère ε.
  - Le comité souligne la contrainte de consommation des allocataires peu dotés en épargne.
  - Les effets macro sont plus faibles que les effets micro.
  - En France, l'effet passe par des contrats courts, pas par l'emploi durable.
- **Lecture raisonnable.** Une baisse de quelques % du net est un levier de second ordre sur la durée (−1,5 à −3,5 %). Elle est peu coûteuse en efficacité et améliore légèrement les finances de l'Unédic. Elle ne peut pas être présentée comme une politique d'emploi.

---

## 2. Fécondité et incitations financières

### France
- **Laroque & Salanié** (IZA DP 3575, 2008 ; publié dans *J. Applied Econometrics* 29(2), 2014, version publiée non relue).
  - Données : enquêtes Emploi 1997-1999 et simulateur fiscal-social.
  - Identification : modèle structurel de choix discret entre activité et fécondité. La variation vient du fait que les salaires (de la femme et du conjoint) modifient les prestations.
  - Résultat : effet notable pour le **1er et le 3e enfant**, faible pour le 2e. Une allocation inconditionnelle de **150 €/mois** (coût ≈ **0,3 % du PIB**) ferait passer le taux annuel de naissance de l'échantillon de **15,5 % à 17,7 % (+2,2 points)**, avec une activité féminine en baisse de 0,5 point.
  - Limites : modèle statique, pas de distinction entre calendrier et descendance finale, pas de modes de garde.
- **Landais (2003)**, « Le quotient familial a-t-il stimulé la natalité française ? », *Économie publique* 13.
  - Données : tabulations fiscales 1915-1998.
  - Identification : quasi-expériences du **plafonnement du QF (1981)** et de la **demi-part pour le 3e enfant (1980)**.
  - Résultat : effet sur les hauts revenus « positif, mais toujours extrêmement faible », diffus sur 5 à 10 ans ; « les très hauts revenus sont légèrement plus sensibles ». Aucun coefficient n'est visible sur la page lue ; PDF complet non accessible.
- **Elmallakh (2023)**, *Demography* 60(5).
  - Réforme étudiée : **mise sous conditions de ressources de l'allocation de base de la PAJE (avril 2014)**, avec AB pleine (184,62 €/mois), moitié ou nulle. Il ne s'agit pas de la modulation des allocations familiales de 2015.
  - Données et identification : SRCV appariée aux revenus fiscaux, environ 3 000 ménages dans l'échantillon d'estimation, régression sur discontinuité aux seuils.
  - Résultat : pour les ménages qui perdent toute l'AB, probabilité de naissance **−2 points à l'annonce et −0,7 point à la mise en œuvre** (base 5,3 %), soit **−38 % et −13 %, élasticité de 0,38 et 0,13**. L'effet porte sur les enfants supplémentaires, pas sur l'entrée en parentalité. La perte d'AB représente 2,4 à 3 % du revenu par enfant de moins de 3 ans.
  - Limites : petit échantillon et effet d'annonce difficile à séparer. L'article qualifie l'AB antérieure d'« universelle » ; je n'ai pas vérifié sur les textes (CSS, art. L. 531-3) si un plafond de ressources s'appliquait déjà avant 2014.
- **Plafonnements du QF de 2013-2014 et modulation des AF de 2015 : je n'ai trouvé aucune évaluation causale.** Le Sénat (rapport sur la PPL 21-181) écrit qu'aucune étude n'a établi de lien causal. La revue IGAS (2024) juge l'effet des prestations « positif mais très limité » ; c'est un résumé de recherche, le document n'a pas été lu en entier. Les rapports de la Cour des comptes ne sont pas accessibles d'ici.

### International
- **Milligan (2005)**, *REStat* (NBER WP 8845).
  - Dispositif : allocation à la naissance du Québec (ANC, 1988-1997), jusqu'à 8 000 $ CAN.
  - Données et identification : recensements canadiens, triple différence (introduction puis suppression).
  - Résultat : **+12 % de fécondité chez les éligibles, +25 % au montant maximal**. 1 000 $ de plus la première année donnent +16,9 % ; **élasticité 0,107**.
  - Hétérogénéité : les populations proches de l'AFDC ne réagissent pas, **les revenus plus élevés réagissent davantage**.
- **Cohen, Dehejia, Romanov (2013)**, *REStat* (NBER WP 13700).
  - Données : panel de femmes mariées en Israël, 1999-2005.
  - Identification : variation de l'allocation pour l'enfant marginal (effet prix), allocations inframarginales comme instrument du revenu.
  - Résultat : l'allocation marginale moyenne augmente la fécondité de **7,8 %**, avec un effet aussi en fin de vie féconde. **Aucun effet dans le haut de la distribution des revenus.**
- **González (2013)**, *AEJ: Policy* 5(3) (IZA DP 5994).
  - Dispositif : chèque bébé espagnol unique de **2 500 €** (juillet 2007).
  - Identification : discontinuité selon la date de naissance.
  - Résultat : naissances **+6 % environ**, dont une partie par la baisse des IVG ; mères plus longtemps hors de l'emploi. Une version ultérieure (González & Trommlerová, BSE WP 1153) indique **+3 %** (résumé seulement).
  - **Calcul propre du coût par naissance supplémentaire** : 2 500 × 1,06/0,06 ≈ **44 000 €** (≈ 86 000 € avec +3 %).
- **Lalive & Zweimüller (2009)**, *QJE* (IZA DP 1613, 2005).
  - Dispositif : congé parental autrichien allongé de 12 à 24 mois en 1990.
  - Résultat : **+4,9 points (+15 %) de probabilité d'un enfant supplémentaire à 3 ans, +3,9 points à 10 ans**, donc pas seulement un effet de calendrier.
- **Raute (2019)**, *JPubE* (NBER WP 23793).
  - Dispositif : **Elterngeld (2007), congé indemnisé proportionnellement au salaire**, avec un gain allant jusqu'à 21 000 € pour les plus diplômées.
  - Données : Mikrozensus 2003-2012 et registres de retraite.
  - Résultat : fécondité **jusqu'à +22 % pour les diplômées du supérieur relativement aux peu diplômées**, effet tiré par le milieu et le haut des distributions d'éducation et de revenu. **1 000 € de droits donnent +0,78 naissance pour 1 000 femmes par an (+2,1 %) ; élasticité ≈ 0,19.**
- **Riphahn & Wiynck (2017)**, *J. Popul. Econ.* 30(4).
  - Dispositif : réforme du Kindergeld de 1996.
  - Données et identification : Mikrozensus et SOEP, doubles différences.
  - Résultat : **effet non significatif pour les bas revenus, effet positif pour les revenus plus élevés au 2e enfant.**
- **Bergsvik, Fauske, Hart (2021)**, *PDR* 47(4). Revue systématique de 35 études (quasi-)expérimentales, lue au niveau du résumé publié.
  - Les crèches augmentent la descendance finale.
  - **Les transferts monétaires n'ont que des effets temporaires.**
  - Les congés parentaux ont des effets plus forts qu'on ne le pensait, et **les couples à hauts revenus en bénéficient davantage**.
- **Kearney, Levine, Pardue (2022)**, *JEP* 36(1).
  - Le déclin de la fécondité américaine depuis 2007 n'est expliqué par aucun facteur économique ou politique mesurable ; les auteurs évoquent un changement de priorités des cohortes.
  - Les politiques natalistes produisent des hausses modestes et surtout de court terme.
  - D'après Stone (2020), cité par KLP et non vérifié : **200 000 $ ou plus par naissance supplémentaire**.
- **Reader, Portes, Patrick** (*Popul. Res. Policy Rev.* 2025 ; IZA DP 15203), sur la limite à deux enfants au Royaume-Uni. Le résumé de 2025 indique « peu ou pas de baisse » de la fécondité de rang 3 et plus chez les ménages modestes. Le communiqué LSE de 2022 évoquait environ 5 600 naissances de moins par an (moins de 1 %). Lu au niveau des résumés seulement.

### Réponse à la question de l'auteur : quelle formule pour D5-D10 ?
**Mécanisme.**
- Le coût d'un enfant comprend un coût direct, qui croît avec le revenu, et surtout un coût d'opportunité : salaire et carrière perdus par la mère. Ce dernier croît fortement avec le revenu potentiel.
- Un forfait par enfant représente une part décroissante de ce coût quand le revenu monte. C'est cohérent avec Cohen et al. (aucun effet en haut de la distribution) et avec le faible effet attendu pour D5-D10.
- **Classement probable de l'efficacité par euro, pour D5-D10 :**
  1. **Prestation parentale proportionnelle au salaire et versée autour de la naissance** (type Elterngeld), complétée par l'offre de garde. Elle compense précisément le coût d'opportunité au moment de la décision. C'est la seule formule avec une preuve causale solide d'effet dans le haut de la distribution (Raute ; Lalive-Zweimüller ; Bergsvik et al.).
  2. **Avantage fiscal croissant avec le revenu (type QF, plafonné).** Il cible bien D5-D10. Mais il est étalé sur 18 à 25 ans et versé à tous les enfants déjà nés ou qui seraient nés de toute façon : il est donc très inframarginal. Sa preuve d'efficacité est faible (Landais 2003 : effet « extrêmement faible ») et il n'existe aucune évaluation des baisses de plafond de 2013-2014. Elmallakh (2023) et Riphahn-Wiynck (2017) montrent que les ménages aisés réagissent aux montants, ce qui laisse penser qu'un QF n'est pas sans effet, sans qu'on puisse le chiffrer.
  3. **Forfait par enfant** (crédit d'impôt ou allocation) : effet réel mais faible et surtout temporaire (Milligan, González, Laroque-Salanié), concentré sur les rangs 1 et 3. Pour D5-D10, son montant relatif au coût de l'enfant est trop faible pour peser.
- **Force de la preuve : moyenne à faible.** Aucune étude ne compare directement les trois formules dans un même pays. Les élasticités de fécondité au montant sont modestes et convergentes : 0,1 à 0,2 dans Milligan, Cohen et al. et Raute ; 0,13 à 0,38 dans Elmallakh. Une partie de l'effet est un effet de calendrier.
- **Coût par naissance supplémentaire** : de quelques dizaines de milliers d'euros pour un chèque ciblé à la naissance (calcul propre sur González) à plus de 200 000 $ pour des transferts larges (Stone via KLP, non vérifié).
- **Implication pour la réforme.** Une majoration par enfant du barème lissé fonctionne comme un QF : elle est utile pour l'équité horizontale, mais son effet nataliste est faible. Pour un objectif nataliste en D5-D10, il vaut mieux **concentrer le soutien sur les 1 à 3 premières années** et le rendre proportionnel au revenu d'activité perdu.

---

## 3. Partage des revenus dans les couples (France)

**Source principale : Morin, *Insee Première* n° 1492 (mars 2014).** Données ERFS 2011, couples hétérosexuels de 20 à 59 ans hors étudiants. Les revenus comprennent les revenus d'activité et de remplacement (chômage, retraites), mais pas les revenus du patrimoine ni les prestations. Les chiffres ci-dessous proviennent du fichier de données Insee `ip1492.xls`.

- **Part moyenne de la femme : 36,4 %**, en hausse depuis 33,0 % en 2002. Elle est de 40,3 % quand les deux perçoivent un revenu et de 44 % quand les deux travaillent à temps complet. 75 % des femmes gagnent moins que leur conjoint.
- **Distribution de la part de la femme en 2011 (% des couples) :**

| Part de la femme | 0 | ]0-10[ | 10-20 | 20-30 | 30-40 | 40-50 | 50-60* | 60-70 | 70-80 | 80-90 | 90-100 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| % des couples | 12,9 | 4,5 | 6,2 | 10,2 | 17,7 | 23,4 | 14,8 | 4,8 | 1,8 | 0,8 | 0,7 | 2,2 |

  *Dont 1,0 % de couples où les deux revenus sont nuls, comptés à 50 %. En 2002, 19,1 % des femmes n'avaient aucun revenu.

- **Part moyenne de la femme par décile de revenu du couple :** profil en cloche, plus bas aux deux extrémités.

| Décile | D1 (< 17 000 €) | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 (> 76 600 €) |
|---|---|---|---|---|---|---|---|---|---|---|
| Part moyenne de la femme (%) | 32,7 | 26,8 | 32,7 | 37,4 | 40,3 | 40,5 | 41,4 | 41,3 | 38,0 | 33,4 |

- **Femmes inactives sans revenu, par décile de revenu du couple :** 52,6 % en D1, 34,1 % en D2, 14,7 % en D3, 3,5 à 8,2 % de D4 à D9, **8,5 % en D10**. Part des femmes à temps complet : 12 % en D1, 60 à 67 % de D5 à D10.
- **Selon la configuration du couple :**
  - Les deux à temps complet : 44 % des couples, part de la femme 44 %.
  - Femme à temps partiel : 20 % des couples, part 34 %.
  - Seul l'homme travaille : **21 % des couples, part 13 %**.
- **Selon les enfants et le statut :** part de 39 % sans enfant, 38 % avec 1 enfant, 36 % avec 2 enfants, **27 % avec 3 enfants ou plus** (27 % de ces femmes sans revenu). Couples mariés 34 %, non mariés 41 %.
- **Mise à jour 2018** (Insee Analyses Île-de-France n° 151, 2022, données Fidéli, couples de 25 à 65 ans hors couples de retraités et hors couples à moins de 10 000 €).
  - Au niveau national, la femme gagne en moyenne **32 % de moins que son conjoint, contre 42 % en 2011**.
  - Elle est la principale contributrice dans 22 % des couples hors Île-de-France.
  - En Île-de-France, sa part est de 45 % dans les couples modestes ou intermédiaires et de 34 % dans les plus aisés.
  - Calcul propre : un écart de 32 % correspond à une part d'environ 40 % en rapport des moyennes.
- **Couples de retraités.**
  - Aubert & Bonnet (blog IPP, décembre 2025 ; données EIR et EDP, ménages entrés en retraite en 2020) : retraite personnelle moyenne **1 330 €/mois pour les femmes mariées contre 2 160 € pour les hommes mariés**. Calcul propre : part de la femme ≈ **38 %**.
  - Insee, *Femmes et hommes* 2022 (données 2019) : écart de pension de droit direct de **39 % chez les 65 ans et plus** (37 % pour l'ensemble), de 24 % en incluant réversion et majorations. La réversion représente 20 % de la retraite des femmes de 65 ans et plus.
  - **Je n'ai pas trouvé de distribution publiée** de la part de la femme dans les couples retraités, ni la proportion de couples retraités dont un membre n'a aucune pension.

---

## 4. Unité d'imposition : individualisation et second apporteur de revenu

- **Allègre, Périvier, Pucci (2021)**, *Économie et Statistique* 526-527.
  - Méthode : modèle Ines, législation 2018, ERFS 2014 vieillie, sans effets de comportement. Le quotient conjugal vaut environ 10 Md€.
  - **Individualisation complète : +7 Md€ de recettes, 46 % des couples mariés ou pacsés perdants, perte médiane de 1,5 % du revenu disponible, 60 % des perdants dans les 3 derniers déciles.**
  - Quotient conjugal réduit à 1,5 part avec option : +3,8 Md€. Plafonnement au niveau du QF : +3 Md€, 7 % de perdants, dont 83 % en D8-D10.
  - Avec l'individualisation, les perdants de D2-D4 perdent 2,6 à 3 % de leur revenu disponible en médiane : ce sont des couples mono-actifs modestes qui deviennent imposables.
- **André & Sireyjol (2021)**, même numéro (Ines, IR 2017).
  - La conjugalisation et la familialisation rapportent ensemble **27,7 Md€** à 13 millions de ménages ; 1,1 million de ménages y perdent.
  - **40 % de l'effet vient de la conjugalisation, 60 % de la familialisation.**
  - Les **15 % les plus aisés captent 48 % des gains de la conjugalisation**, contre moins de 25 % pour la moitié la plus modeste.
- **Eidelman, *Insee Analyses* n° 9 (2013)**, revenus de 2010 : **60 % des couples mariés ou pacsés paient moins d'impôt qu'en déclarations séparées**. Le gain croît avec l'écart de revenus et le niveau de revenu ; la décote et la PPE jouent en sens inverse pour 21 % des couples imposés conjointement.
- **Offre de travail : Kabátek, van Soest, Stancanelli (2014)**, *Labour Economics* 27 (résumé publié lu).
  - Méthode : modèle de choix discret estimé sur des couples français.
  - Passer de l'imposition commune à l'imposition séparée **augmenterait les heures de travail de l'épouse de 3,7 %**, réduirait son travail domestique de 2,0 % et les heures du mari de 0,8 %.
- **Non vérifiés ici** : une note IPP spécifique sur l'individualisation, Carbonnier, Bargain et al. pour la France.

---

## Ce qu'on peut écrire dans la note
1. « Les estimations quasi-expérimentales situent l'élasticité de la durée de chômage au montant de l'allocation autour de 0,5 en médiane (18 estimations, Schmieder & von Wachter 2016). En France, l'évaluation de la réforme du SJR conclut qu'une baisse de 10 % de l'allocation journalière réduit de 4 à 7 % la durée sans emploi (comité d'évaluation, Dares, 2025). »
2. « Soumettre l'ARE au barème commun, soit une baisse d'environ 5 % du net, raccourcirait les épisodes de chômage de 1,5 à 3,5 %, c'est-à-dire de quelques jours. L'effet est réel mais de second ordre, et il passe surtout par des reprises de contrats courts (comité 2025). »
3. « La dégressivité de 2021 a raccourci d'environ un mois et demi la durée de non-emploi des allocataires aisés concernés, et ses effets de comportement représentent plus d'un tiers des économies mécaniques (comité 2025). Taxer l'allocation procure donc un double dividende budgétaire, au prix d'une moindre assurance. »
4. « Les incitations financières ont un effet positif mais modeste sur la fécondité : l'élasticité des naissances au montant des prestations est d'environ 0,1 à 0,2 (Milligan 2005 ; Cohen, Dehejia & Romanov 2013 ; Raute 2019). En France, la mise sous conditions de ressources de l'allocation de base de la PAJE en 2014 a réduit la probabilité d'avoir un enfant supplémentaire chez les ménages aisés exclus (élasticité de 0,13 à 0,38, Elmallakh 2023). »
5. « Aucune évaluation causale des baisses du plafond du quotient familial de 2013-2014 n'est disponible. L'étude des réformes du QF de 1980-1981 conclut à un effet "positif, mais toujours extrêmement faible" sur la fécondité des hauts revenus (Landais 2003). »
6. « La seule formule dont l'efficacité nataliste est démontrée dans le haut de la distribution est la prestation parentale proportionnelle au salaire : l'Elterngeld allemand a augmenté la fécondité des diplômées du supérieur de jusqu'à 22 % relativement aux moins diplômées (Raute 2019). »
7. « Un forfait par enfant pèse peu face au coût d'opportunité des parents aisés : en Israël, l'allocation n'a aucun effet dans le haut de la distribution des revenus (Cohen et al. 2013). Les transferts monétaires n'ont en général que des effets temporaires (Bergsvik et al. 2021). »
8. « En 2011, la femme apportait en moyenne 36 % des revenus des couples de 20 à 59 ans. Cette part était de 40 à 41 % entre le 5e et le 8e décile de revenu du couple, mais de 33 % dans le décile le plus aisé. 13 % des femmes en couple n'avaient aucun revenu propre (Insee Première 1492). »
9. « L'individualisation complète de l'IR rapporterait environ 7 Md€ ; 46 % des couples mariés ou pacsés y perdraient, pour une perte médiane de 1,5 % de leur revenu disponible, et 60 % des perdants appartiennent aux trois déciles supérieurs (Allègre, Périvier & Pucci 2021). La conjugalisation profite d'abord aux 15 % les plus aisés, qui en captent 48 % des gains (André & Sireyjol 2021). »
10. « Remplacer l'imposition commune par l'imposition séparée augmenterait les heures de travail des épouses d'environ 3,7 % (Kabátek, van Soest & Stancanelli 2014). »

## Paramètres pour la modélisation
- **Couples d'âge actif : part de la femme dans les revenus individuels du couple** (activité et remplacement). Tirer la part dans la distribution par tranches de 10 points de l'Insee Première 1492 (ERFS 2011) :
  - 0 % : 12,9 % ; ]0-20[ : 10,7 % ; 20-40 : 27,9 % ; 40-50 : 23,4 % ; 50-60 : 14,8 % ; 60-100 : 8,1 % ; 100 % : 2,2 %.
  - Moyenne cible de 36 % ; uniforme à l'intérieur de chaque tranche.
- **Variation par décile de revenu du couple** : recaler la moyenne par décile sur 33 / 27 / 33 / 37 / 40 / 41 / 41 / 41 / 38 / 33 %. Recaler la part de femmes sans revenu sur 53 / 34 / 15 / 8 / 5 / 5 / 4 / 4 / 5 / 9 % (inactives sans revenu, figure 6).
- **Actualisation vers 2024-2026** : l'écart moyen est passé de 42 % à 32 % entre 2011 et 2018 (Fidéli). Variante prudente : décaler la moyenne à environ 40 % (calcul propre) en réduisant la masse en 0 % d'environ un tiers, de 12,9 % vers environ 9 %. **Cette valeur est une hypothèse, pas une source.**
- **Avec enfants** : abaisser la moyenne à 27 % pour 3 enfants ou plus, dont 27 % de femmes sans revenu (contre 38 % et 10 % pour 1 enfant).
- **Couples de retraités** : part de la femme dans les pensions personnelles du couple d'environ 38 % (Aubert & Bonnet, IPP 2025, génération partie en 2020 ; Insee FH 2022 : écart de droit direct de 39 %). Faute de distribution publiée, utiliser une loi centrée sur 38 % avec un écart-type de l'ordre de 15 points (hypothèse). La réversion n'est pas concernée tant que les deux conjoints sont vivants.
- **Tests de sensibilité** : part uniforme de 50 % (individualisation neutre) et part de 0 % pour 21 % des couples (mono-actifs, figure 1).
