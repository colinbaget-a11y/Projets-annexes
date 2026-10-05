# Refaire le système fiscal français : plan détaillé

Rapport d'environ 90 pages, hors annexes, sur ce que serait le système fiscal français s'il était
reconstruit à partir de zéro. Publié par un think tank ; les responsables politiques en premier
lecteur, les économistes et les citoyens ensuite.

Deux consignes commandent le reste et peuvent entrer en tension. Le rapport doit être
**pédagogique** : mieux vaut un chapitre entièrement compris qu'un chapitre exhaustif abandonné en
cours de route. Et il doit avoir **le registre d'un rapport public** : il se cite, il s'oppose, il
engage celui qui le signe. La section suivante dit comment les deux tiennent ensemble.

---

## Le registre

Un rapport public explique les mécanismes aussi concrètement qu'un cours, mais il ne raconte pas
d'histoire et ne s'adresse pas au lecteur. Le CPO, le CAE et la Cour des comptes exposent des
calculs qu'on peut refaire, avec des montants, des cas chiffrés et des tableaux ; ils n'emploient
ni la première ni la deuxième personne, ne posent pas de questions au lecteur et ne nomment pas de
personnages. C'est exactement la ligne à tenir.

**Ce qui reste du cours.** Le mécanisme exposé pas à pas plutôt que nommé. Les exemples chiffrés
qu'on peut refaire au crayon. Les ordres de grandeur rapportés à ce que l'impôt rapporte. Les
figures nombreuses, une idée par figure. Les phrases d'ouverture de paragraphe qui portent
l'argument, de sorte qu'on puisse suivre la thèse en ne lisant qu'elles.

**Ce qui disparaît.** Les personnages : « un ménage qui place 1 000 € », et non « Anne et Bruno ».
Le « vous » et le « on » qui désignent le lecteur. Les questions rhétoriques. Les formules
d'oralité (« c'est tout le problème », « voilà pourquoi »). L'apostrophe (« il faut expliquer
pourquoi on applique… ») devient une constatation.

**Ce qui s'ajoute.** Chaque chiffre porte sa source dans le texte ou en note, et chaque
recommandation son coût et son gage. L'incertitude est dite par son ampleur (« estimé entre 0,2
et 0,3 sur données françaises »), jamais par une formule d'atténuation. Les recommandations sont
numérotées et reprises telles quelles au chapitre de synthèse.

Le cours `cours/refaire-l-impot.tex` reste un document de travail : son registre est plus libre que
celui du rapport, et sa matière doit être réécrite, pas transposée.

---

## Les règles du jeu

Les vingt-trois questions de cadrage ont été tranchées le 3 octobre 2026 (`CADRAGE.md`), et quatre
décisions s'y sont ajoutées le 5 octobre. Dix commandent la lecture du plan.

1. **Rendement constant.** Le rapport demande comment lever 1 270 Md€ mieux, pas combien lever.
   Chaque proposition est gagée. Une variante chiffre ce que coûterait de lever un à deux points de
   PIB de plus, puisque le déficit est de 5,1 points en 2025.
2. **Toute cotisation est un impôt.** Convention assumée, dont la figure `p2` montre la portée : le
   coin fiscal français ainsi mesuré est surestimé par rapport à un pays dont les retraites sont
   capitalisées, et le rapport le dit là où il compare.
3. **Tous les transferts monétaires sont dans le périmètre**, y compris les prestations
   universelles : sans eux, un taux marginal effectif ne veut rien dire.
4. **Les paramètres des retraites sont donnés.** Seul leur financement est discuté.
5. **Périmètre Eurostat** pour tous les chiffres, avec un encadré nommant ce qui en est exclu.
6. **Pas de fonction de bien-être imposée.** Les résultats valent pour un éventail de préférences
   redistributives, et le rapport dit à partir de quelle préférence sa conclusion bascule.
7. **La mobilité des bases est une contrainte forte**, assumée comme telle. En contrepartie, chaque
   affirmation de mobilité dit sur quoi elle repose et sépare les cas documentés des extrapolations.
8. **Chiffrage sur cas types** (décision du 5 octobre, qui étend le cadrage initial). Les trois
   ménages types sont calculés sur le barème réel avec OpenFisca-France, avant et après chaque
   réforme ; aucun accès aux microdonnées, donc aucun perdant nommé et aucune distribution estimée
   au-delà de celles déjà publiées par l'Insee, la DREES et l'IPP.
9. **L'idéal d'abord, le faisable ensuite**, mais dans le même chapitre : chaque chapitre de bloc
   dit ce que le droit permet, plutôt qu'un chapitre juridique séparé.
10. **Traçabilité stricte.** Tout chiffre renvoie à un fichier de `donnees/` ou à une source de
    `sources/`. Un chapitre n'est fini que sans marque **[à sourcer]** résiduelle.

L'orientation du think tank ne doit pas être visible : le rapport doit se lire comme une analyse et
non comme un plaidoyer. Trois conséquences, qui portent sur ce qu'il faut démontrer et non sur les
conclusions. Chaque fois qu'une réforme améliore l'efficience au détriment de la progressivité, le
rapport dit **par quoi** elle est compensée, et le chiffre sur les cas types. Les recommandations
qui vont dans le sens attendu — supprimer les prélèvements sur les intrants, exonérer le rendement
normal, corriger le biais d'endettement — sont les plus solidement chiffrées du rapport, puisque ce
sont celles qu'on soupçonnera d'être là par préférence. Et les conclusions que ce bord n'attend
pas — l'impôt sur le sol qui tombe sur les propriétaires actuels, le loyer imputé, la compensation
sans laquelle la réforme de la TVA n'est que la moitié d'une proposition, le prix du carbone sur
l'industrie et l'agriculture — sont développées plutôt qu'escamotées.

---

## Ce qu'on emprunte à *Tax by Design*, et ce qu'on écarte

**Le chapitre d'ouverture traite de la politique de la réforme fiscale.** La section 1.3 de *Tax by
Design* explique pourquoi les mauvais impôts survivent : presque toute réforme fait des perdants
identifiables et des gagnants diffus, un gouvernement qui a besoin d'argent cherche donc les
prélèvements dont les perdants sont difficiles à nommer, et la complexité qui en résulte n'est pas
un accident.

**Le chapitre pivot confronte l'idéal et l'existant dans un tableau à deux colonnes.** Le
tableau 20.1 est le document le plus cité de la Review parce qu'il tient en deux pages. Le rapport
en construit l'équivalent français ; le cours en contient déjà une première version
(tableau `tab:synthese`).

**Une formule de synthèse, posée tôt et tenue jusqu'au bout.** Mirrlees tient en trois mots dont
chacun travaille : un système *progressif*, *neutre*, jugé *comme un système*. Le rapport a besoin
de son équivalent ; il reste à l'écrire.

**Ce qui est écarté : l'appariement théorie / application en deux chapitres par assiette.** Mirrlees
sépare le chapitre théorique du chapitre appliqué pour chaque base. Sur 90 pages, cela ferait
quatorze chapitres de six pages et obligerait le lecteur à faire deux fois le trajet. Le rapport
suit le cours : **un chapitre par bloc**, qui va du mécanisme à la réforme chiffrée. La théorie
commune — perte sèche, élasticité, incidence — est posée une seule fois en première partie.

**Ce qui est écarté aussi : la séparation en deux volumes.** Les développements techniques vont en
annexe.

---

## Les dispositifs

- **Les encadrés « comment ça marche »** : une page détachable qui construit un mécanisme depuis
  zéro. Prévus : la remontée de la TVA le long de la chaîne de production ; la perte sèche qui croît
  avec le carré du taux ; taux marginal et taux moyen ; le rendement normal ; la fabrication d'un
  taux marginal par un transfert dégressif ; l'effet de l'inflation sur un impôt assis sur le
  rendement nominal ; la conversion d'un impôt sur le stock en taux sur le flux.
- **Le test du statu quo**, une fois par chapitre de bloc. Deux questions : si ce prélèvement
  n'existait pas, serait-il instauré aujourd'hui ? et si on l'abolissait, qu'est-ce que cela
  subventionnerait ? La seconde rappelle que ne pas taxer quelque chose, c'est en subventionner
  l'usage.
- **Trois ménages types**, suivis d'un chapitre à l'autre et calculés sur OpenFisca : un couple au
  voisinage du salaire minimum avec deux enfants, locataire ; une personne seule au salaire moyen,
  accédant à la propriété ; un couple de retraités propriétaires sans emprunt, au niveau de vie
  médian. Ils couvrent les transferts, le logement et la frontière entre actifs et retraités.
- **L'objection la plus forte**, une fois par chapitre de bloc : le meilleur argument contre la
  recommandation, et ce qui le ferait l'emporter.
- **Une idée par figure**, dont la légende décrit et dont la conclusion est portée par le texte.
- **Définitions en marge**, et un glossaire final.

La charte des figures est celle du dépôt : composition en serif, palette sobre — bleu `#003399`,
vert `#1f7a4d`, ocre `#c79100`, gris `#6b6b6b` —, grille horizontale légère, sources et note de
lecture composées en texte sous l'image et non dans l'image (`figures/nu/<figure>_note.tex`).

---

# Le plan

## Synthèse pour les décideurs (6 p.)

Les dix réformes rangées par certitude du gain ; ce qu'il ne faut pas changer ; le coût et le
financement de chacune à rendement constant ; ce que gagnent et perdent les trois ménages types, et
par quoi ils sont compensés.

## Première partie — Le système et la façon de le juger (≈ 22 p.)

**1. Ce que la France lève, et sur quoi.** Le niveau (43,5 % du PIB) et ce qu'il coûte ; une
structure qui pèse sur le travail et la production ; même niveau que le Danemark, structure opposée ;
123 prélèvements, 474 dépenses fiscales ; pourquoi les mauvais impôts survivent. Encadré sur ce que
la liste Eurostat laisse dehors.
*Matériau : `01_etat_des_lieux.md`, `03_decoupages.md`, cours ch. 11.* → `s1`, `s4`, `g1`, `g3`,
`g4`, `g5`, `h1`.

**2. Ce qu'un impôt détruit.** La perte sèche et sa croissance au carré du taux ; l'élasticité, et
le fait qu'elle dépende en partie de ce que la loi permet ; le sommet des recettes et pourquoi il
n'est pas un objectif.
*Matériau : cours ch. 1, `06_lecons_taxation_optimale.md` modules 1-2.* → `c1`, `c25`, `c29`.

**3. Qui le paie, et comment juger un système.** L'incidence, qui ne suit pas l'étiquette ; le
raisonnement sur une vie entière ; la progressivité jugée sur l'ensemble des prélèvements et des
transferts ; l'éventail de préférences sociales et le point où chaque conclusion bascule ; la
mobilité des bases, cas documentés et extrapolations séparés.
*Matériau : cours ch. 2 et 3.* → `c3`, `c20`, `r6`.

## Deuxième partie — Bloc par bloc (≈ 48 p., huit chapitres de six)

**4. Produire.** Les 119,3 Md€ assis sur un facteur de production, dont 77 Md€ sans fonction
corrective ; la cascade d'une taxe sur le chiffre d'affaires ; l'impôt sur les sociétés, son biais
en faveur de la dette, et le fait que son taux effectif n'est pas un outlier. Suppression des
prélèvements sur intrants, en commençant par le chiffre d'affaires ; déduction d'un rendement normal
sur les fonds propres nouveaux. **C'est le gain le plus sûr du rapport et celui qu'on soupçonnera
d'être là par préférence : il doit être le mieux chiffré.**
*Matériau : cours ch. 4 et 5.* → `s3`, `h3`, `g6`, `c7`, `c23`, `r4`.

**5. Travailler.** Les 490 Md€ assis sur le travail ; les deux impôts sur le revenu qui ne partagent
ni assiette ni unité ni barème ; les allègements et leurs pentes ; les transferts dégressifs et les
pics qu'ils fabriquent ; le coin marginal de 64,6 % à 67 % du salaire moyen. Lisser le creux
au-dessus du salaire minimum ; fusionner impôt sur le revenu et CSG. Une section sur l'unité
d'imposition, sans recommandation autonome.
*Matériau : cours ch. 6.* → `s2`, `m3`, `m4`, `p2`, `g2`.

**6. Consommer.** Les 206 Md€ de TVA, trois taux, une assiette effective de 51 % contre 55 % dans
l'OCDE ; l'arithmétique qui montre qu'un taux réduit donne plus d'euros au ménage aisé ; les deux
vrais problèmes techniques, services financiers et logement occupé par son propriétaire.
Rapprochement des taux réduits du taux normal, **avec sa compensation chiffrée sur les trois ménages
types**, sans laquelle la proposition est incomplète.
*Matériau : cours ch. 7.* → `c3`, `r7`.

**7. Épargner.** Un même rendement réel supporte de 0 à 55 % selon l'enveloppe ; rendement normal,
prime de risque et rente ; ce que l'inflation fait à un impôt assis sur le rendement nominal, et le
seuil au-dessous duquel épargner appauvrit. Un seul régime : rendement normal exonéré, assiette
indexée, ce qui dépasse au barème.
*Matériau : cours ch. 8, `05_maquettes_de_reference.md`.* → `p4`, `c5`, `c30`, `r8`.

**8. Détenir et se loger.** Les 48 Md€ assis sur la détention, sur des valeurs locatives de 1970 ;
les 17 Md€ de droits de mutation ; la non-taxation du loyer imputé. Réviser l'assiette d'abord ;
déplacer ensuite la charge de la transaction vers la détention ; séparer le terrain du bâti.
**Conclusion que le lecteur n'attend pas : l'impôt sur le sol est le plus efficient qui existe, et
il tombe sur les propriétaires actuels par capitalisation.**
*Matériau : cours ch. 9.* → `g10`, `r9`. **À construire :** partage terrain/bâti dans les 48 Md€.

**9. Transmettre.** 20,8 Md€ de droits de succession, premier rendement de l'OCDE rapporté au PIB,
obtenus avec des taux élevés sur une assiette percée (pacte Dutreil, assurance vie, démembrement).
Élargir l'assiette et baisser les taux, à rendement constant. **Développement le plus long du
rapport, proportionné à la résistance attendue.**
*Matériau : cours ch. 9, CAE n° 69, Cour des comptes 2025.* → `r10`.

**10. Polluer.** Un prix implicite du carbone qui varie du simple au quadruple ; 41 % des émissions
de l'industrie sans aucun prix. Étendre le prix sans le relever ; quotas aux enchères ; reversement
forfaitaire. **Conclusion que le lecteur n'attend pas : un prix unique le relève sur l'industrie et
l'agriculture.**
*Matériau : cours ch. 10.* → `m1`, `m2`, `g12`.

**11. Financer les collectivités.** Des assiettes supprimées sans être remplacées, une autonomie de
taux résiduelle, un financement par transferts qui coupe le lien entre la décision de dépense et son
coût. Assiette foncière réévaluée, pouvoir de taux réel, péréquation explicite.
**Chapitre entièrement à écrire.**

## Troisième partie — Trois débats (≈ 21 p.)

Les titres décrivent et ne concluent pas, puisque l'orientation ne doit pas se voir.

**12. Les taux marginaux élevés.** Où ils se trouvent en France : plus haut en bas de l'échelle
qu'au sommet. Ce que mesurent les études françaises, et ce qu'elles ne mesurent pas.
*Matériau : `cours/elasticites-france.tex`.* → `c25`, `c29`, `c26` à `c28` en annexe.

**13. La fiscalité des retraités.** Niveau de vie relatif de 94 % contre 90 % dans l'Union, pauvreté
de 12,4 % contre 21,4 % chez les moins de 18 ans ; 9,1 € de prélèvements sociaux sur 100 € de
pension contre 20,8 € sur un salaire, dont 11,3 ouvrent des droits ; l'abattement de 10 % et le taux
de CSG. Ce que rapporterait un alignement, paramètres de retraite inchangés, et la transition lente
qu'il exige. **Chapitre à écrire ; la matière chiffrée existe (`p1`, `p2`, `extract_pedagogie.py`).**

**14. Un impôt plancher sur les très grands patrimoines.** Le problème réel qu'il vise : du revenu
économique logé dans des holdings, où les dividendes reçus des filiales sont exonérés à 95 %.
L'arithmétique qui convertit un impôt sur le stock en taux sur le rendement. La valorisation des
titres non cotés et la trésorerie quand rien n'est distribué. Les départs, la sous-déclaration, et
le précédent néerlandais de décembre 2021. Les instruments qui visent le même problème sans taxer le
patrimoine. **L'objection la plus forte est ici celle des partisans de l'impôt ; elle doit être
présentée à sa pleine force.**
*Matériau : cours ch. 8, `cours/elasticites-france.tex`.* → `p3`.

## Quatrième partie — Le système reconstruit (≈ 15 p.)

**15. Le système à rendement constant.** Le tableau à deux colonnes, bon système contre système
français. Les recommandations numérotées avec leur coût et leur gage. Ce que lève chaque assiette
après réforme. Les trois ménages avant et après. **À construire : la maquette elle-même.**

**16. Un à deux points de PIB de plus.** 30 à 60 Md€, pris sur les assiettes avant les taux :
dépenses fiscales, taux réduits, assiette des transmissions, carbone hors carburants routiers.

**17. Dans quel ordre, et ce que le droit permet.** La séquence de mise en œuvre, et le fait qu'une
réforme annoncée se capitalise dans les prix avant d'entrer en vigueur. Les contraintes du droit de
l'Union sur la structure des taux de TVA, de la jurisprudence constitutionnelle sur l'égalité devant
les charges publiques, de l'autonomie financière des collectivités : ce que chacune empêche, ce que
cela coûte, laquelle mériterait d'être renégociée. **[à sourcer]** pour chacune.

## Annexes

Les trois ménages types et leur paramétrage. Les réactions à l'impôt estimées sur données françaises
(`cours/elasticites-france.tex`, avec `c26` à `c28`). Les quatre maquettes de référence
(`05_maquettes_de_reference.md`). Périmètre, sources et traçabilité. Glossaire.

---

## Le gabarit des chapitres de bloc

1. L'argument en une phrase.
2. Un exemple chiffré qu'on peut refaire.
3. Ce que montrent les données, françaises et comparées.
4. Ce qu'il faudrait faire, chiffré et gagé, en recommandations numérotées.
5. Qui y gagne et qui y perd : les trois ménages types, et les distributions par décile publiées.
6. L'objection la plus forte, et ce qui la ferait l'emporter.
7. Ce que le droit permet.
8. Le test du statu quo.

---

## L'architecture retenue pour le capital

Décision provisoire du 5 octobre, à confirmer par le chiffrage parce qu'elle a un coût à gager.

**Pour les ménages**, le cadre dual complété par une exonération du rendement normal et par une
règle de partage pour les dirigeants de leur propre société. Le prélèvement forfaitaire unique créé
en 2018 *est* un impôt dual ; il lui manque ces trois pièces. Le rapport présente donc la réforme
comme l'achèvement de ce qui a été commencé, et non comme une importation nordique.

**Pour les entreprises**, l'ordre compte plus que la maquette : la suppression des prélèvements
assis sur une base indépendante du résultat passe avant tout, parce que c'est le seul gain qui ne
dépend d'aucune hypothèse de comportement. La correction du biais d'endettement vient ensuite, et
le rapport propose deux routes qui diffèrent par le risque et non par l'ambition : la déduction d'un
rendement normal sur les apports nouveaux, plus ciblée mais exposée à l'imposition minimale mondiale
à 15 % ; ou l'imposition des seuls bénéfices distribués, plus simple mais qui décale les recettes et
autorise un report indéfini.

**Écarté :** le rendement présumé néerlandais, qui est un impôt sur le stock déguisé. Il entre au
chapitre 14 comme contre-épreuve, pas comme proposition.

**À vérifier avant d'écrire le chapitre 4 :** l'interaction précise des deux routes avec
l'imposition minimale mondiale, y compris du côté estonien ; et l'ordre de grandeur du coût d'une
déduction sur apports nouveaux en France.

---

## Où en est le travail

| Chapitre | État | Ce qui manque |
|---|---|---|
| Synthèse | à écrire | dépend du chapitre 15 |
| 1 à 3 | matière complète | réécriture au registre du rapport |
| 4 à 10 | matière complète | réécriture, cas types, section « ce que le droit permet » |
| 11 | rien | tout |
| 12 | matière complète | réécriture |
| 13 | matière chiffrée | rédaction |
| 14 | matière partielle | valorisation des non-cotés, instruments alternatifs |
| 15 à 17 | rien | la maquette d'ensemble, qui commande le reste |

**Prochaine étape, décidée le 5 octobre : la maquette d'ensemble du chapitre 15.** C'est elle qui
contraint tout : si les comptes ne tombent pas à rendement constant, certaines recommandations des
chapitres de bloc devront changer, et mieux vaut le découvrir avant d'avoir rédigé.

---

## Méthode de travail

Un chapitre à la fois, avec ses figures, soumis avant de passer au suivant. Je rédige, tu arbitres
et tu réécris.

Rédaction en Markdown, avec une structure de fichiers convertible en LaTeX sans réécriture ; bascule
vers LaTeX quand une partie entière est stabilisée, en reprenant la chaîne du cours
(`cours/refaire-l-impot.tex`, `graphiques.py`, macro `\figbloc`).

Chaque chiffre renvoie à un fichier de `donnees/` ou à une source téléchargée dans `sources/`. Les
affirmations non traçables portent la marque **[à sourcer]** et sont résolues avant qu'un chapitre
soit considéré comme fini.

La littérature empirique est mobilisée en résumé, sauf lorsqu'un résultat porte seul une
recommandation chiffrée : la stratégie d'identification est alors examinée, et le rapport dit ce
qu'elle établit exactement. Le complément sur les élasticités donne le modèle de cet examen.

## Fichiers

| Fichier | Contenu |
|---|---|
| `CADRAGE.md` | les vingt-trois questions de cadrage, les réponses du 3 octobre et les décisions du 5 octobre |
| `01_etat_des_lieux.md`, `03_decoupages.md` | matériau du chapitre 1 |
| `02_cadre_theorique.md` | première version du cadre, absorbée par `06` |
| `04_mirrlees_applique.md` | diagnostics de *Tax by Design* répliqués |
| `05_maquettes_de_reference.md` | les quatre maquettes de taxation du capital |
| `06_lecons_taxation_optimale.md` | les quinze enseignements |
| `07_ou_changer.md` | les neuf écarts |
| `cours/refaire-l-impot.tex` | le cours en treize chapitres, document de travail |
| `cours/elasticites-france.tex` | les réactions à l'impôt estimées sur données françaises |
| `extract_*.py`, `panorama.py`, `classification.py` | données |
| `graphiques*.py` | figures et charte partagée |

## Sources déjà mobilisées

Eurostat *National Tax Lists* (juillet 2026) et comptes nationaux ; *Évaluation des voies et
moyens*, tome II, annexe au PLF 2026 ; OCDE (TaxBEN, *Taxing Wages*, *Corporate Tax Statistics*,
*Effective Carbon Rates*, *Revenue Statistics*) ; Urssaf et service-public.gouv.fr pour les taux
2026 ; IFS, *Tax by Design* (2011) ; dix rapports publics français (CAE n° 49, 50, 53, 69 et
Focus n° 118 ; CPO sur la TVA, le logement et l'industrie ; Cour des comptes sur la sécurité
sociale, le pacte Dutreil et le budget de l'État) ; douze travaux académiques sur données
françaises depuis 2010.

## Sources à mobiliser ensuite

*Voies et moyens* tome I et liste des taxes affectées, pour nommer les 27 Md€ laissés en « autres
taxes ». Annexes au PLFSS et données Urssaf, pour le détail des cotisations. Commission européenne,
base de taux effectifs d'imposition des sociétés, pour le biais de financement. Insee, DREES et IPP,
distributions par décile publiées. OpenFisca-France, pour les trois ménages types. Documentation de
l'imposition minimale mondiale, pour l'interaction avec la déduction des fonds propres.
