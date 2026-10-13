# Notes de littérature : attribuer la dette publique (Maastricht) aux sous-secteurs des APU en corrigeant des transferts

Rédigé le 13/10/2026. Convention : **[V]** = vérifié sur le document source (texte téléchargé dans `dette/lit/` ou page lue) ;
**[S]** = rapporté par une source secondaire (presse, résumé de recherche, amendement) sans lecture de l'original ;
**NON VÉRIFIÉ** = hypothèse ou souvenir à contrôler. Aucun chiffre n'a été inventé ; quand une source manque, c'est dit.

Fichiers locaux (texte extrait) : `dette/lit/*.txt` — voir la liste en fin de note.

---

## 0. Ordres de grandeur de départ (Insee, base 2020)

- **Dette Maastricht fin 2024 [V]** (Insee Première n° 2054, https://www.insee.fr/fr/statistiques/8574492, fig. 5) :
  État 2 687,0 Md€ ; ODAC 69,8 ; APUL 261,9 ; ASSO 286,6 ; total 3 305,3 Md€ (113,2 % du PIB).
  Part de l'État ≈ 81 %. Dette nette : État 2 575,4 ; ODAC 35,4 ; APUL 248,5 ; ASSO 203,6 ; total 3 062,9.
- **Définition [V]** (même page) : « La contribution à la dette d'un sous-secteur est égale à la dette de ce sous-secteur
  diminuée des passifs détenus par les autres administrations publiques. La somme des contributions à la dette des
  différents sous-secteurs est égale à la dette au sens de Maastricht de l'ensemble des administrations publiques. »
  → la répartition officielle est déjà **consolidée des créances croisées** mais **pas des transferts de flux**.
- **Solde 2024 [V]** : État −152,5 Md€ ; ODAC −1,7 ; APUL −16,7 ; ASSO +2,3 (ASSO hors CADES −13,3) ; APU −168,6.
  Transferts courants entre APU « consolidés » dans la colonne APU (note de la fig. 4).
- **Dette fin 2025 [V]** (Cour des comptes, RSPFP juin 2026, via vie-publique.fr/files/rapport/pdf/303867.pdf) : 3 460,5 Md€,
  115,7 % du PIB ; déficit 152,5 Md€ (5,1 pts).
- **Solde par sous-secteur en % du PIB [V]** (IPP 2026, tableau 1.1) : État −5,1 (2024), −4,3 (2025), −4,6 (2026 prév.) ;
  ODAC −0,1 ; APUL −0,6/−0,5/−0,4 ; ASSO 0,0/−0,2/0,0.
- **ASSO, détail [V]** (Cour des comptes RSPFP 2026, tableau 7, Md€, 2019→2025) : ASSO 12,1 ; −48,3 ; −19,7 ; 8,5 ; 11,8 ; 1,1 ; −6,7.
  Dont CADES 15,8 ; 16,1 ; 11,2 ; 18,0 ; 17,9 ; 15,5 ; 15,4. ASSO hors CADES −3,7 ; −64,4 ; −30,9 ; −9,5 ; −6,0 ; −14,4 ; −22,1.
  Note 35 : « La CADES est structurellement excédentaire puisque ses recettes, affectées au remboursement en capital de la
  dette sociale, sont comptabilisées comme telles en comptabilité nationale alors que ses dépenses ne le sont pas. »
- **Compte des ASSO 2025 [V]** (Fipeco, fiche « Le solde et la dette des administrations sociales », 05/05/2026) :
  recettes 796,8 Md€ dont **impôts 300,7**, cotisations 439,9, **transferts d'autres administrations 23,4** ; dépenses 803,5.
  Dette ASSO fin 2025 : 293 Md€ (9,8 % PIB), portée par CADES 129, Unédic 59, ACOSS/Urssaf 39. Dette ASSO > 1 % du PIB
  seulement en France et en Espagne dans l'UE (moyenne UE 2,4 %).
  → Point clé : **l'essentiel du financement « étatique » de la Sécu apparaît en comptabilité nationale comme impôts des
  ASSO (D2/D5), pas comme transferts D73** (voir §3).

---

## 1. Qui a déjà argumenté / calculé cela

### 1.1 Sylvain Catherine (Wharton, @sc_cath)
- **Aucune version écrite longue (Substack, tribune Les Échos/Le Point) trouvée** sur le thème précis « la dette publique
  est surtout sociale / l'État porte la dette de la Sécu ». X n'est pas lisible ici (HTTP 402) : ce qui suit vient des
  extraits de recherche et d'une reprise presse.
- **Calcul contrefactuel « retraites allemandes » [S]** : article JeChange (F. Tostivint, 18/08/2026,
  https://www.jechange.fr/credit/news/dette-france-58-pib-retraites-allemandes) reprenant un post X
  (https://x.com/sc_cath/status/2089127055153672583). Méthode : écart annuel France–Allemagne de dépense de pensions
  (agrégat SESPROS large : vieillesse, invalidité, survie, préretraite ; Eurostat SESPROS et nama_10_gdp) depuis 1995,
  converti en € de PIB français, traité comme déficit évité, capitalisé aux taux d'intérêt effectivement payés par la France.
  Résultat : dette 2025 de 57,5 % du PIB au lieu de 115,7 % → −58,2 pts, ≈ 1 740 Md€. Limites listées par l'article
  (recettes, PIB, taux constants ; discipline parfaite). **Ce n'est pas une ré-attribution par sous-secteur mais par
  fonction (retraites).**
- **Posts X [S]** (extraits) : distinction dette explicite / dette implicite des retraites (« probablement 2–3x » la dette
  publique ; valeur agrégée des promesses de pension ≈ 400 % du PIB, 12 000 Md€) ; le déficit d'un système par répartition =
  pensions − cotisations, et le redéfinir *après* transferts de l'État est circulaire
  (https://x.com/sc_cath/status/1939794029518233759) ; le taux de contribution employeur de l'État aux pensions des
  fonctionnaires s'ajuste pour équilibrer « par construction » (https://x.com/sc_cath/status/1896423037278314539) ;
  les comptes nationaux compteraient deux fois le déficit des retraites de la FP (https://x.com/sc_cath/status/1893799307045720390,
  argument NON VÉRIFIÉ). Tribune Le Figaro (2024, effort budgétaire à porter par les retraités) mentionnée dans un post
  (https://twitter.com/sc_cath/status/1773339256724803678) — texte non lu. Wikipédia FR « Dette publique de la France »
  le cite à l'appui d'un déficit des retraites de ~55 Md€/an [S, NON VÉRIFIÉ dans l'article].
- Émission Ecorama (Boursorama), 11/06/2025 [S] : baisse du niveau des pensions.

### 1.2 Jean-Pascal Beaufret (inspecteur général des finances honoraire) — **l'approche la plus proche du projet**
- **« Retraites obligatoires et déficits publics. Pour la clarté », *Commentaire* n° 182, été 2023, p. 245-254 [V]**
  (reproduit comme doc. n° 6 de la séance COR du 21/09/2023 :
  https://www.cor-retraites.fr/sites/default/files/2023-09/Doc_06_Retraites%20obligatoires_d%C3%A9ficits%20publics.pdf).
  Méthode « par fonction, consolidée » : le déficit public provenant des retraites = dépenses publiques de retraite (345 Md€
  en 2021) non financées par des prélèvements obligatoires affectés (cotisations 228 Md€ + impôts affectés 46 Md€).
  Les **subventions** (État aux régimes spéciaux 7,4 Md€ ; exonérations ciblées 5,1 ; CNAF→CNAV/MSA 9,8 ; Unédic→Agirc-Arrco 4,3 ;
  autres 0,3 = 27 Md€) et les **sur-cotisations** des employeurs publics (45 Md€ : écart entre taux FPE civils 74,3 %,
  militaires 126,1 %, CNRACL 30,6 % et un taux de référence de 16,5 %) sont traitées comme du déficit.
  Résultat : retraites financées « à 21 % par la dette publique, soit 71 Md€ en 2021 » (−2,8 % PIB). Répartition par régime :
  CNAV −12 ; Agirc-Arrco −2,0 ; MSA −5 ; fonctionnaires −45 (dont FPE 38, CNRACL 7) ; régimes spéciaux −8 Md€.
  « La solidarité contribue à la moitié des déficits publics annuels relatifs aux retraites. »
- **Note aux membres du COR, sept. 2023 [V]** (doc. n° 7 :
  https://www.cor-retraites.fr/sites/default/files/2023-09/Doc_07_Note%20J-P.%20Beaufret.pdf) : chiffres 2022 (dépenses
  360,7 Md€ ; cotisations 237,7 ; impôts 51,0 ; subventions 73,7). Argument d'attribution : les subventions de l'État ne sont
  pas des prélèvements obligatoires car « le déficit et l'endettement nouveau de l'État, qui verse 52 Md€ de subventions, ont
  représenté 33 % en 2021 et 31 % en 2022 de sa dépense totale » → **règle implicite de pro-rata** (chaque euro de transfert
  de l'État est financé à hauteur de la part de sa dépense couverte par l'emprunt). Il estime aussi que 41 Md€ des 136 Md€
  repris par la CADES proviennent du cumul des déficits de la branche vieillesse.
- **Beaufret (2026), « Les comptes de la Sécurité sociale et le redressement des finances publiques », *Commentaire*
  n° 193(1), p. 107-112** — cité par l'IPP 2026 [V pour la référence ; texte NON LU]. Selon l'IPP, il recommande de
  présenter les comptes « hors transferts » pour faire apparaître le « vrai » déficit de chaque administration, et liste
  trois critiques : (1) CAS Pensions hors ASSO ; (2) CADES (dans les ASSO) dont l'amortissement du capital est une opération
  financière, ce qui « redresse mécaniquement le solde des ASSO » ; (3) les transferts de l'État redressent le solde des ASSO.
- Audition devant une commission d'enquête de l'AN [S] (Revue *Conflits* n° 56, V. Fouquet, 01/05/2025,
  https://www.revueconflits.com/linsoutenable-poids-des-retraites-dans-les-deficits-et-la-dette-publics/) : les retraites
  « représentent 50 % de l'endettement supplémentaire » sur 2016-2024 (~1 000 Md€). Méthode non publiée dans l'article.
- Contre-position officielle [S] : Cour des comptes, « Situation financière et perspectives du système de retraites »,
  20/02/2025 (P. Moscovici : « Il n'existe aucun déficit caché ») — les contributions de l'État employeur sont des cotisations ;
  déficit 2025 prévu 6,6 Md€ ; ~15 Md€ en 2035, ~30 Md€ en 2045 (via lefildecarriere.fr ; rapport non téléchargé, ccomptes.fr bloqué).

### 1.3 IPP — Bach, Bozio, De Brouwer, Eryzhenskiy, « Qui est responsable du déficit public ? », *Perspectives budgétaires*,
chap. 1, juin 2026 [V] (https://www.ipp.eu/wp-content/uploads/2026/06/chapitre_FIPU_2026-2-2.pdf)
- Thèse : la présentation par sous-secteur « fait apparaître l'État comme principal responsable du déficit public » mais
  « masque des transferts financiers importants de l'État vers les collectivités locales et les organismes de protection
  sociale » ; une présentation « hors transferts » n'est pas plus pertinente : « attribuer un solde à chaque sous-secteur
  n'a de sens qu'à la condition que celui-ci dispose d'une autonomie décisionnelle ». Le vrai enjeu : distinguer « ce qui
  relève d'une action de l'État en délégation » de « transferts d'équilibre ». **Pas de chiffrage d'un solde corrigé.**
- Chiffres utiles : fig. 1.5 (flux 2024, Md€) — recettes budget général 357, déficit de l'État 154, prélèvements sur
  recettes 68 (collectivités), TVA/TICPE affectées 95, taxes affectées protection sociale 227, cotisations 482 … ;
  destinataires : protection sociale 842 (cotis. + taxes), collectivités locales 233, CAS Pensions 67 … (lecture du schéma :
  à recouper, les montants sont des flux d'un diagramme Sankey).
  Tableau A1.1 : part des transferts (budget général + taxes affectées + PSR) dans les recettes fiscales totales :
  collectivités 31,4 % (2014) → 27,3 % (2024) ; protection sociale (CAS pensions inclus) 37,4 % → 47,6 % ;
  total 68,8 % → 74,9 %. Fig. 1.6a : part des recettes fiscales affectées à protection sociale + collectivités 46,2 % (2013)
  → 55,5 % (2024) ; +9 pts pour la protection sociale (TVA compensant allègements ; CSG 2018).
  COFOG 2024 : dépenses vieillesse 13,5 % du PIB dont 10,8 pts ASSO et 2,3 pts État.
- Renvois : Aubert, Pedrono, Tô, Tochev, « Retraites des fonctionnaires d'État : faut-il changer la convention comptable ? »,
  IPP *Perspectives budgétaires* 2025, chap. 3 : **44 % (2020)** des contributions au CAS Pensions couvriraient un
  déséquilibre démographique non compensé (transfert implicite de l'État vers les régimes privés) [S via IPP 2026].
  Cour des comptes (RALFSS mai 2025) : la compensation des allègements généraux par fractions de TVA « pour solde de tout
  compte » a été défavorable à la Sécu : **−18 Md€ cumulés 2019-2024** sur son solde [S via IPP 2026 ; aussi repris dans des
  amendements : sous-compensation 2,4 Md€ en 2019 → 5,5 Md€ en 2024].

### 1.4 François Ecalle / Fipeco
- « La signification du déficit de la sécurité sociale », commentaire 19/06/2019 [V, page lue] : le solde de la Sécu
  « dépend du partage des dépenses de solidarité » et des impôts affectés (35 % des recettes ASSO en 2018 contre 2 % en 1980) ;
  « Le solde des comptes de la sécurité sociale, et par symétrie celui de l'Etat, n'a plus guère de signification » ;
  « seul le solde du compte des administrations publiques dans leur ensemble en a une ».
- « Le déficit et la dette de la sécurité sociale », 24/06/2020 [V, résumé de page] : propose que l'État reprenne
  intégralement les dettes maladie et famille (CADES/ACOSS + crise sanitaire) et la dette historique vieillesse + FSV
  « pour solde de tout compte ». Dette fin 2019 : ACOSS 22, CADES 89, ASSO 193 Md€.
- « Quel financement pour la sécurité sociale ? », note 18/02/2025 [V] : cotisations = 48 % du financement de la Sécu en 2023
  (90 % fin des années 1980), CSG 20 %, TVA 8 %, autres ITAF 8 % ; loi de 1994 (compensation intégrale) ; modalités
  instables (crédits, impôts affectés, transferts de dépenses — ex. APL reprises par l'État en compensation du pacte de
  responsabilité ; CSG 2018 ; TVA à l'ACOSS pour l'Unédic ; prélèvements sur le capital transférés à l'État).
- Fiche « Les recettes des APUL » (06/07/2026) [V] : voir §3.2.
- Pas trouvé de note Fipeco calculant explicitement une « dette de l'État corrigée des transferts ».

### 1.5 Cour des comptes
- RSPFP juin 2026 [V] (cf. §0) ; « Situation des finances publiques début 2026 » [téléchargé, cdc_situation_fp_debut2026.txt].
- Notes du CPO n° 8, « Les impôts et taxes affectés », sept. 2024 [V] (cf. §3).
- Rapport sur la situation financière des retraites (20/02/2025) [S].
- RALFSS 2025 (sous-compensation TVA, −18 Md€) [S via IPP].
- « Les finances locales, un mode de financement à redéfinir », RPA mars 2023 [référence via IPP, non lu].

### 1.6 Haut Conseil du financement de la protection sociale (HCFiPS)
- Rapport de juillet 2015 « sur la lisibilité des prélèvements et l'architecture financière des régimes sociaux » ;
  rapport d'étape juin 2013 sur « la clarification et la diversification des ressources » ; état des lieux 2018 (synthèse
  téléchargée : hcfips_synthese_2025.txt — malgré l'URL 2025, c'est la synthèse du rapport 2018) [références V, contenu
  peu exploité]. Rapport Charpy–Dubertret (oct. 2018, art. 27 LPFP 2018-2022) sur les relations financières État–Sécu,
  proposant de revoir le principe de compensation (non publié selon l'IFRAP) [S].

### 1.7 Autres
- **Nicolas Dufourcq, *La dette sociale de la France 1974-2024*, Odile Jacob, 2025** [S] : « 2000 milliards au minimum sont
  des prestations sociales versées depuis 40 ans à crédit » (p. 13, cité par Ph. Lemoine, *La Grande Conversation*/Terra Nova,
  08/12/2025 [V : lgc_dette_sociale_2025.txt]). Méthode (selon interviews [S]) : pro-rata — 57 % des dépenses publiques sont
  des prestations sociales ⇒ 57 % de la dette. Clé de répartition moyenne, pas de traçage des emprunts.
- **CESE, « Finances publiques : état des lieux et analyse de controverses »**, étude 2026-007, fév. 2026 [V] : dette ASSO
  194,4 Md€ (2019) → 286,5 Md€ (2024) ; CSG CADES 0,60 → 0,45 pt en 2024 (0,15 pt vers la CNSA).
- J.-P. Robin (Le Figaro, sept. 2024) : 438 Md€ sur 839 Md€ de hausse de dette 2018-2023 (52 %) imputés aux retraites [S] ;
  iFRAP : −420 Md€ sur 2018-2023 [S] ; M. Ferracci (France Culture, 18/09/2026) : ~400 Md€ des ~1 200 Md€ depuis 2017 [S].
  Toutes ces estimations reposent sur la lecture « subvention » des contributions de l'État employeur.
- **OFCE, Institut Montaigne, Rexecode** : rien trouvé qui décompose la dette par sous-secteur avec correction des
  transferts. **NON TROUVÉ** (ne pas affirmer d'absence sans recherche sur leurs sites).
- **Littérature académique internationale (transferts verticaux)** [V pour références] : Eyraud & Lusinyan (2013),
  « Vertical fiscal imbalances and fiscal performance in advanced economies », *J. Monetary Econ.* 60(5), 571-587
  (−10 pts de VFI ⇒ +1 pt de PIB de solde APU, 28 pays OCDE) ; Aldasoro & Seiferling, « Vertical fiscal imbalances and the
  accumulation of government debt », SAFE WP 61 [référence trouvée, contenu non lu]. Aucun article trouvé appliquant une
  correction des transferts à la répartition de la dette française par sous-secteur.

---

## 2. Chronologie des transferts de dette entre sous-secteurs (depuis 1990)

| Date | Opération | Montant | Sens | Source |
|---|---|---|---|---|
| 31/12/1993 | Reprise par l'**État** de la dette cumulée du régime général (prêt CDC à l'ACOSS d'oct. 1993) ; art. 105 LF 1994, loi 93-936 du 22/07/1993 ; service transféré au FSV | **110 MdF = 16,77 Md€** | ASSO → État | Sénat, rapport r02-248, annexe II (réponses CADES) [V] |
| 01/01/1996 | Ordonnance 96-50 : création CADES ; transfert de la dette ACOSS envers la CDC au 31/12/1995 + déficit prév. 1996 | **137 MdF** (maladie 82,311 ; famille 52,311 ; vieillesse 2,494 MdF) ≈ 20,9 Md€ | intra-ASSO (ACOSS → CADES) | Sénat r02-248 [V] |
| 1996-2005 | La CADES verse au budget de l'État 12,5 MdF/an 1996-2008 (créance de l'État 162,5 MdF) au titre des 110 MdF de 1993 ; réduit à 1,85 Md€/an en 2001, puis 4 × 3 Md€ (2002-2005) ; capital 16,77 Md€, total versé 23,38 Md€ | **≈ 23,4 Md€ versés** | ASSO → État (**la reprise de 1993 a été remboursée par la Sécu**) | Sénat r02-248 [V] ; CADES rapport AMF 2025 [V] |
| 1996 | Dette initiale CADES « 44,723 Md€ » = 20,886 (déficits) + 23,380 (dette reprise par l'État en 1994) | 44,7 Md€ | — | Wikipédia CADES [S ; cohérent avec Sénat] |
| 01/01/1998 | LFSS 1998 : dette ACOSS 1996-97 (11,4 Md€ + 2,6 déjà financés) + préfinancement 1998 | **13,2 Md€** | intra-ASSO | CADES AMF 2025 [V] |
| 2004-2006 | Loi 2004-810 art. 76 : déficits maladie ≤ 31/12/2003 + 2004 (10 Md€ au 01/09/2004, plafond 25 Md€) + 2005-2006 (plafond 15 Md€) | plafonds 25 + 15 Md€ (montants exécutés NON VÉRIFIÉS) | intra-ASSO | CADES AMF 2025 [V pour plafonds] |
| oct. 2007 | Apurement par l'État de ses dettes envers le régime général (dettes 2006 et antérieures) | **5,08 Md€** | État → ASSO (paiement d'arriérés) | Sénat, PLFR 2007 [S] |
| 30/12/2008 | Reprise par l'État de la dette du FFIPSA (régime agricole) avant sa suppression (LFSS 2009 art. 17) | **7,972 Md€** (+371 M€ vs déficit constaté) | ASSO → État | Sénat [S] ; Fipeco mentionne « le remboursement de la dette du régime agricole par l'Etat en 2008 » [V] |
| 2009 | LFSS 2009 art. 10 : maladie 2007-08 (8,8), vieillesse 2005-08 (14,1), FSV (≤ 4) + 0,2 pt de CSG | **27 Md€** | intra-ASSO | CADES AMF 2025 [V] |
| 2011-2018 | LFSS 2011 art. 9 : 68 Md€ (maladie, famille 2009-11 ; vieillesse 2009-10) + 62 Md€ (vieillesse 2011-18, plafond 10 Md€/an) ; +0,28 pt CSG, 1,3 % prél. capital, FRR 2,1 Md€/an 2011-2024 | plafonds 68 + 62 Md€ | intra-ASSO | CADES AMF 2025 [V] |
| 2012 | LFSS 2012 : déficits CCMSA | **2,467 Md€** | intra-ASSO | CADES AMF 2025 [V] |
| 2016 | LFSS 2016 art. 17 : vieillesse + FSV + partie famille/maladie | **23,6 Md€** | intra-ASSO | CADES AMF 2025 [V] |
| 2019 | LFSS 2019 art. 27 : reprise de 15 Md€ — **abrogée** par LFSS 2020 art. 25 | 0 | — | CADES AMF 2025 [V] |
| fin 2019 | Cumul transféré à la CADES depuis 1996 : 260,5 Md€ (171,4 amortis, 89,1 restant) | — | — | CADES AMF 2025 [V] |
| 2020-2024 | LO 2020-991 et loi 2020-992 du 07/08/2020 : **136 Md€** = 31 (déficits ≤ 2019 : maladie RG, FSV, vieillesse non-salariés agricoles, CNRACL) + 92 (déficits 2020-2023) + 13 (1/3 des emprunts au 31/12/2019 des établissements de santé du service public hospitalier). Exécution : 20 (déc. 2020-1074) ; 40 (2021) ; 40 (2022) ; 27,2 (2023) ; 8,8 (2024). Fin CADES reportée au 31/12/2033 | **136 Md€** | intra-ASSO (hôpitaux = ODASS, dans les ASSO) | CADES AMF 2025 [V] ; securite-sociale.fr REPSS 2.5.2 [V] |
| 2026 | LFSS 2026 : nouvelle reprise | **15 Md€** | intra-ASSO | REPSS 2.5.2 [V] |
| fin 2025 | Total transféré à la CADES depuis 1996 : **396,5 Md€** ; amorti 274,8 (69 %) ; restant 121,7 Md€ | — | — | REPSS 2.5.2 [V] |
| 2016 (rétro) | Reclassement de **SNCF Réseau** en APU (ODAC) à compter de 2016 (Insee/Eurostat, sept. 2018) : dette notifiée +35,8 Md€ fin 2016, +39,4 Md€ fin 2017 ; déficit +3,2 Md€ (2016), +2,2 (2017). Une fraction (~10 Md€) était déjà au passif de l'État | +35,8 Md€ | hors APU → ODAC | Insee CP 06/09/2018 [V] |
| 2014 (base 2010) | Intégration d'une partie de la dette de RFF dans la dette publique (+9,9 Md€ 2010, +10,0 2011, +10,5 2012), surtout sur l'État (révision État +14,7 Md€ en 2010) | ~10 Md€ | hors APU → État | Insee, fiche méthodo base 2010 [V] |
| 2020 / 2022 | Reprise par l'**État** de 35 Md€ de dette de SNCF Réseau : 25 Md€ au 01/01/2020, 10 Md€ en 2022 (annonce du 25/05/2018 ; base : 48,2 Md€ fin 2018) | **35 Md€** | **ODAC → État** (intra-APU depuis le reclassement) | Sénat PLF 2020-2022, budget.gouv [S] |

Pistes **NON VÉRIFIÉES** (à rechercher) : Charbonnages de France (dissolution 2007-2008, dette reprise par l'État) ;
SAAD (service annexe d'amortissement de la dette SNCF, 1991) ; EPFR/CDR (Crédit lyonnais) ; Unédic (dette garantie par
l'État, ~59-65 Md€, mais **pas** reprise) ; transfert des APL de la CNAF à l'État (2015-2016, transfert de dépense, pas de
dette) ; FOREC (créance 2000 apurée par la CADES en 2003-2004 : 1,283 + 1,097 Md€ [V, CADES AMF 2025]).

**Lecture pour le projet** : sur 1990-2025, les grands transferts de *stock* de dette **entre l'État et les ASSO** sont
limités et se compensent en partie (1993 : +16,8 Md€ pour l'État, remboursés 23,4 Md€ par la CADES 1996-2005 ; FFIPSA 2008 :
~8 Md€ ; SNCF Réseau : 35 Md€ ODAC→État). L'essentiel des reprises (396,5 Md€) est **interne aux ASSO** (ACOSS → CADES).
La « surpondération » de l'État vient donc des **flux** (transferts, compensations, impôts affectés), pas des reprises de stock.

---

## 3. Mécanismes de financement des autres sous-secteurs par l'État, et traitement en comptabilité nationale

### 3.1 Règle SEC 2010 / SFP 2014
- **SEC 2010 §1.78 [V]** (esa2010.txt) : « When a unit carries out a transaction on behalf of another unit (the principal)
  and is funded by that unit, the transaction is recorded exclusively in the accounts of the principal. As a rule, one should
  not go beyond this principle by trying, for instance, to allocate taxes or subsidies to ultimate payers or ultimate
  beneficiaries under the adoption of assumptions. An example is the collection of taxes by one government unit on behalf of
  another. A tax is attributed to the government unit that exercises the authority to impose the tax (either as a principal or
  through the delegated authority of the principal) and has final discretion to set and vary the rate of the tax. »
- **FMI, SFP/GFSM 2014 §5.33-5.36 [V]** (imf_gfsm2014.txt) : selon l'arrangement, les impôts reversés peuvent être
  « reassigned as tax revenue of that unit » **ou** enregistrés comme impôt de l'unité collectrice puis « grant » (transfert).
  Critère §5.34 : autorité pour imposer + « final discretion to set and vary the rate ». §5.35 : montants retenus au titre
  d'un « tax-sharing arrangement » = **current grants (1331/2631)**. §5.36 : si une unité a l'autorité ultime, tout l'impôt
  lui est attribué.
- **Pratique française [V]** : Insee enregistre les ITAF (CSG, CRDS, fractions de TVA, taxe sur les salaires, accises…) comme
  **impôts du sous-secteur affectataire**. Preuve textuelle : Insee Première 2054 (ASSO 2024) — « Les taxes et impôts sur la
  production accélèrent légèrement (+2,5 %), malgré la montée en charge de la réduction de la part de TVA affectée aux ASSO » ;
  compte des ASSO 2025 : impôts 300,7 Md€ vs transferts d'autres APU 23,4 Md€ (Fipeco/Insee). Pour les APUL, Fipeco : la
  fraction de TVA « est devenue le principal impôt reçu par les collectivités locales ».
  **Tension avec le critère §1.78 / GFSM §5.34** : en France le taux et la fraction sont fixés par le Parlement (en LF/LFSS),
  pas par l'affectataire. Aucun texte Insee/Eurostat justifiant explicitement ce choix n'a été trouvé → **NON VÉRIFIÉ**
  (à chercher : base 2020, notes méthodo Insee ; décisions Eurostat). Le CPO (note n° 8) ne tranche pas cette question
  comptable.
- **Pratique hétérogène dans l'UE [V]** (métadonnées Eurostat gov_10a_taxag) : Hongrie — l'IR des collectivités est
  comptabilisé en S1311 puis transféré en D.7 ; Islande — impôts et cotisations de S1314 comptés en S1311 puis transférés
  en D.7 ; Norvège — S1314 inclus dans S1311. → les comparaisons internationales de dette/solde par sous-secteur dépendent de
  cette convention.
- **Reprises de dette** : SEC 2010 §5.36 [V] — « Debt assumption and debt cancellation are capital transfers (D.9) and
  recorded in the capital account. » (Entre APU : D.99 consolidé au niveau S13.) MGDD (Eurostat 2019, chap. 7.2) et GFSM
  2014 annexe 3 (A3.26 s.) [repérés, non résumés].
- **Consolidation** : GFSM 2014 §3.161-3.162 [V] — élimination des flux intra/inter-gouvernementaux (grants, intérêts,
  impôts payés entre APU…) ; exceptions : cotisations employeur et impôts retenus à la source (re-routés via les ménages).

### 3.2 Collectivités locales (APUL) — Fipeco « Les recettes des APUL » (06/07/2026) [V]
- Recettes APUL 2025 : 320 Md€ (10,7 % PIB) : 59 % PO, 19 % transferts d'autres APU/UE, 16 % ventes. PO perçus 190 Md€ (2025).
- « Transferts financiers » de l'État (rapport sur les finances locales annexé au PLF 2026) : **152 Md€ en LFI 2025** =
  fiscalité transférée hors TVA 39 Md€ (DMTO, TICPE, TSCA) + **TVA transférée 53 Md€** + dégrèvements/subventions/amendes
  11 Md€ + **concours financiers 49 Md€** (dont 45 Md€ de prélèvements sur recettes, 4 Md€ mission RCT).
  **DGF 27 Md€ en 2025 (40 Md€ en 2014)** ; FCTVA 8 Md€. LPFP 2023-2027 : concours 53 → 56 Md€.
  PLF 2026 [S] : transferts élargis 155 Md€ ; concours 53,4-54,4 Md€ ; DGF 2026 32,6 Md€ (réintégration de la TVA régionale).
- Réformes (IPP 2026 encadré 2 [V]) : TH résidences principales supprimée (2021), compensée aux communes par la part
  départementale de TFPB ; départements : TFPB perdue, CVAE supprimée 2021 → fractions de TVA ; régions : DGF supprimée 2018,
  CVAE 2021 → TVA (2019 puis 2021). CPO n° 8 [V] : 2018-2022, suppression TH −20 Md€, CVAE −8 Md€, CET −1 Md€, compensées
  par **+37 Md€ d'affectations de TVA**.
- Constitution art. 72-2 (compensation des transferts de compétences) ; ratio d'autonomie financière stable 70-80 % mais
  autonomie fiscale en net recul (IPP) — OCDE : 48,1 % des ressources « discrétion + partage consenti » en 2023 [V via IPP].
- PSR : déduits des recettes de l'État en budgétaire mais **dépenses de l'État (transferts entre APU) en comptabilité
  nationale** (IPP note 4 [V]).

### 3.3 Sécurité sociale (ASSO)
- **Loi Veil du 25/07/1994** : compensation intégrale par l'État des exonérations (art. L.131-7 CSS ; dérogation possible
  en LFSS) [V via IPP/Fipeco/Sénat].
- **Compensation des allègements généraux par affectation d'impôts** (paniers fiscaux depuis 2006 ; logique « pour solde de
  tout compte » depuis 2011 ; fractions de TVA, bascule CICE 2019) [V : IPP « depuis 2011 … essentiellement des fractions de
  TVA » ; date 2006 NON VÉRIFIÉE ici]. Effet défavorable à la Sécu estimé par la Cour à −18 Md€ cumulés 2019-2024 [S].
- **TVA nette affectée à la Sécu** : 49,6 Md€ en 2025, 45,0 Md€ prévus en 2026 (−5,4 Md€ réforme des AG) [S : Sénat
  rapport r25-942 citant CCSS mai 2026] ; fraction de TVA brute 28,48 % (LFI 2023) → 28,57 % (LFI 2024) [S : budget.gouv].
- **ITAF (CPO n° 8, sept. 2024) [V]** : 462 Md€ d'impôts et taxes affectés en 2022 (39 % des PO, 18 % du PIB) dont 57 % aux
  ASSO (265 Md€ : RG 205,6 ; FSV 19,5 ; CADES 17,9 ; Unédic 15,8 ; MSA 4,8 ; autres 1,8) et 36 % aux APUL (165 Md€ : impôts
  locaux 68, fiscalité transférée 97). CSG 140 Md€, TVA 102 Md€. Hausse 2018-2022 des ITAF ASSO +69 Md€ dont **TVA en
  compensation d'exonérations +47 Md€**, CSG +15 Md€.
- **Coût des exonérations** [S, amendements citant annexes PLFSS] : 91,3 Md€ en 2024 (dont 2,9 Md€ non compensées) ;
  73,6 Md€ en 2022 vs 37 Md€ en 2013. À vérifier dans l'annexe 4 PLFSS.
- Transferts de dépenses : APL reprises par l'État en 2015 en compensation du pacte de responsabilité (IPP [V], Fipeco [V]).
- Pensions des fonctionnaires de l'État : payées par l'État (CAS Pensions) **hors ASSO** en comptabilité nationale ; cotisation
  employeur imputée (Fipeco [V], Beaufret [V]).
- CADES : excédent structurel ~15-18 Md€/an (amortissement = opération financière) [V Cour].

---

## 4. Approches pour attribuer déficits/dette entre sous-secteurs

1. **Officielle (SEC 2010 / Insee)** : solde par sous-secteur *après* transferts ; dette par sous-secteur consolidée des
   créances intra-APU (« contribution »). Les impôts affectés comptent comme recettes de l'affectataire. C'est cette
   présentation qui donne ~81 % de la dette à l'État.
2. **Consolidation APU (GFSM/SEC)** : seul le total S13 a un sens économique ; position de Fipeco (2019) [V] et, sur le
   fond, de l'IPP 2026 (« la véritable question n'est pas d'attribuer la source du déficit […] mais […] la gouvernance »).
3. **« Hors transferts » / soldes avant transferts** : Beaufret (2026) [via IPP] ; critiquée par l'IPP car chaque transfert
   correspond à une politique (compensation légale art. 72-2 C, loi Veil 1994).
4. **Par fonction (COFOG ou fonction sociale)** : Beaufret 2023 (retraites, 71 Md€ 2021 ; 73,7 Md€ de subventions 2022),
   Catherine 2026 (contrefactuel « dépense de pension allemande », −58 pts), Dufourcq 2025 (pro-rata 57 % ⇒ 2 000 Md€),
   Robin/iFRAP/Ferracci (retraites ≈ 400-500 Md€ de la dette depuis 2016-2017). En COFOG consolidé, les transferts entre APU
   s'éliminent, de sorte que la dépense est comptée chez l'**unité qui dépense finalement** (logique « final spender ») —
   **inférence** à partir de la consolidation GFSM §3.161 ; pas de texte Eurostat COFOG cité ici (NON VÉRIFIÉ).
5. **« Délégation » vs « transferts d'équilibre » (IPP 2026)** : imputer à l'État les dépenses déléguées qu'il doit financer,
   au sous-secteur les dépenses qu'il pilote ; non chiffré, nécessiterait de reconstruire le financement (non fait).
6. **Pro-rata de financement par l'emprunt** (implicite chez Beaufret 2023 : l'État finance ~1/3 de ses dépenses par
   l'emprunt en 2021-2022 ⇒ ~1/3 de ses subventions est de la dette) — candidat naturel pour une clé « final spender ».
7. **Littérature « vertical fiscal imbalance »** (Eyraud & Lusinyan 2013 ; Aldasoro & Seiferling) : relie la dépendance aux
   transferts à la dérive budgétaire, sans réattribuer la dette.
8. **IMF GFS guidance « final spender »** : GFSM 2014 ne pose pas de principe d'imputation des déficits au bénéficiaire
   final des transferts ; SEC 2010 §1.78 l'exclut même explicitement pour les impôts et subventions (« one should not go
   beyond this principle by trying […] to allocate taxes or subsidies to ultimate payers or ultimate beneficiaries ») [V].
   Toute correction « final spender » est donc un **retraitement analytique hors normes**, à présenter comme tel.

---

## 5. Points non résolus / à vérifier
- Texte intégral du thread X de S. Catherine et d'un éventuel écrit long (NON TROUVÉ).
- Justification méthodologique Insee de l'enregistrement des fractions de TVA comme impôts des ASSO/APUL (NON TROUVÉE).
- Montants exécutés des reprises CADES 2004-2006 et 2011-2015 (seuls les plafonds sont vérifiés).
- Charbonnages de France, SAAD, EPFR : montants et classement sectoriel (NON VÉRIFIÉ).
- Traitement en comptabilité nationale des dégrèvements de TH (2018-2022) payés par l'État (NON VÉRIFIÉ).
- Rapport Cour des comptes du 20/02/2025 sur les retraites et RALFSS 2025 (ccomptes.fr inaccessible depuis ce poste).

## 6. Fichiers dans `dette/lit/`
cades_amf_2025 (rapport semestriel CADES 2025, historique législatif) ; cdc_rspfp_2026 ; cdc_situation_fp_debut2026 ;
cese_2026_finances_publiques ; cor_retraites_deficits_publics_2023 (Beaufret, Commentaire 2023) ; cor_beaufret_note_2023 ;
cpo_note8_itaf_2024 ; esa2010 ; eurostat_mgdd_2019 ; imf_gfsm2014 ; insee_cp_2018_sncfreseau ; insee_rev_dette_2012_rff ;
insee_ip2054_apu2024.html ; insee_methodo_cptes_apu ; ipp_fipu2026_ch1_responsable_deficit ; lgc_dette_sociale_2025 ;
fipeco_solde_dette_asso.html ; fipeco_recettes_apul.html ; fipeco_financement_secu.html ; secu_eval_252.html (REPSS 2.5.2) ;
senat_r02-248_12.html (CADES, reprise 1993) ; hcfips_synthese_2025 (synthèse HCFiPS 2018) ; vp_299239 (CCSS juin 2019).
