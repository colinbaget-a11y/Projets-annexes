# Registre des hypothèses et des chiffres : partie IS

Contrôle du 16 novembre 2026, avant la réécriture de `synthese/parties/is.tex` selon `synthese/CHARTE_NOTE.md`.
Ce registre est la source du tableau d'annexe « Hypothèses fortes et chiffres non vérifiés » de la partie IS.

**Fichiers relus.** `is/README.md`, `is/simulation_is.py` et sa sortie, `is/figures_is.py`, `is/notes/is_recherche.md`,
`is/donnees/is_chiffres.csv`, `synthese/perte_seche_autres.py` et sa sortie, `revue/methode_v2.md`,
`revue/methode_perte_seche.md`, `revue/verif_is_pfu.md`, `revue/revue_is.md`, `revue/verif_litterature_is_pfu.md`,
`synthese/parties/is.tex`.

**Recalcul indépendant.** Le script `verif_is.py` n'importe pas `simulation_is.py`. Il réécrit les plans d'amortissement,
le coût par millésime, la dette et les taux effectifs, et il relit les sources primaires. Sortie : `verif_is_sortie.txt`.
Les sensibilités sont calculées sur le script corrigé par `supplement.py`. Les trois fichiers sont dans
`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_is/`.

Sources relues : copies locales des recherches précédentes, dans les dossiers `is_*` et `inv_*` du même scratchpad.
Téléchargement fait pour ce contrôle : statistiques des recettes de l'OCDE, dans `.../scratchpad/verif_is_dl/oecd_rev/`.

**Avant correction, le script reproduit sa sortie octet pour octet, et le recalcul indépendant retrouve tous ses
chiffres.**
- Coût de la première année : 15,53 et 14,03 Md€.
- Coût en année 8 : 1,99 et 1,36 Md€.
- Valeur actualisée : 2,55 et 1,76 Md€ à 5 % ; 1,74 et 1,19 Md€ à 3,25 %.
- Dettes, points de taux et seuils des petites sociétés : identiques.

**La mécanique est juste ; une erreur de calibrage touche les ressources.**
- Les bénéfices de 2022 étaient portés en 2027 à 3 % par an. Or le bénéfice fiscal n'a crû que d'environ 1 % par an
  de 2023 à 2025, selon les chiffres officiels.
- La valeur d'un point de taux, le rendement de la fin du taux réduit et celui d'un IS à 28 % étaient donc surestimés
  d'environ 9 %.
- Après correction, les conclusions tiennent : l'assiette finance le régime permanent, la transition coûte une dette
  de 3 à 46 Md€, et la baisse finale du taux reste de 0,6 à 1,2 point. Plusieurs chiffres de `is.tex` changent
  toutefois (§ 5).

---

## 1. La méthode en clair

**Coût de la déduction immédiate.** Une machine achetée 100 € est aujourd'hui déduite par fractions sur sept ans.
- La déduire en une fois ne change pas le total déduit, seulement sa date.
- Chaque année, l'État perd 25 % de l'écart entre la déduction nouvelle et l'ancienne, sur tous les achats faits depuis
  la réforme. Les achats antérieurs gardent leur plan d'amortissement.
- Ce calcul s'applique à l'investissement en machines et en matériel informatique des sociétés non financières :
  84 Md€ en 2025, porté à 89 Md€ en 2027 (+3 % par an).
- Seule la part faite par des sociétés imposables compte : 75 % au centre, 60 à 90 % en variante.

Le profil du coût en découle.
- **Première année** : le coût est élevé, puisque l'État rend d'un coup l'impôt sur les déductions futures.
- **Années suivantes** : il décroît, parce que les machines achetées après la réforme n'ont plus d'annuités à déduire.
- **Dès la huitième année** : il ne reste qu'un coût permanent. La formule fermée, vérifiée, est τ·s·I·(1 − z(g)),
  où z(g) est la valeur des déductions actualisée au taux de croissance g de l'investissement. Ce coût n'existe que
  parce que l'investissement croît ; à croissance nulle, il serait nul.

**Coût actualisé par millésime.** C'est le coût économique d'une année d'investissement : τ·s·I·(1 − z), où z est la
valeur actuelle des déductions pour 1 €. Il est calculé au taux des entreprises (5 %) et à celui de l'État (3,25 %).

**Ressources.** Elles sont statiques et en euros de 2027.
- **Assiette** :
  - fin du taux réduit de 15 % : 10 points sur 27 Md€ de bénéfices de 2022 ;
  - CIR apprécié au niveau du groupe et fin des exonérations zonées : chiffrages du CPO ;
  - avantage de la boîte à brevets réduit de moitié : la moitié de la dépense fiscale.
- **Taux** : 28 % sur les 251 Md€ de bénéfices de 2022 imposés au taux normal, avec 0 à 1,5 % de base perdue par point
  de taux.

**Dette de transition.** La dette de chaque année vaut celle de l'année précédente, intérêts de 3,25 % compris, moins
le solde de l'année (ressources moins coût). Les ressources croissent de 3 % par an. On repère le maximum de la dette et
l'année où elle s'éteint. L'excédent permanent, rapporté à la valeur d'un point de taux, donne la baisse de taux
possible une fois la dette remboursée.

**Petite société.** Elle perd au plus 4 250 € par an (10 points sur 42 500 €). La déduction immédiate lui fait gagner
τ·I·(z nouveau − z ancien) par année d'investissement. Le seuil de compensation est l'investissement annuel qui égalise
les deux.

**Croissance et bien-être.**
- *PIB.* Le gain vaut part du revenu de ce capital × élasticité × baisse du coût d'usage × 75 %.
- *Perte sèche.* C'est le triangle d'Harberger sur le capital, (r+δ)·K·ε·(m₁² − m₀²)/2, où m est le coin fiscal sur le
  coût d'usage. Pour un IS à 28 %, on ajoute le coût réel du transfert de bénéfices, κ·τ̄·ΔB.

---

## 2. Chiffres clés : vérification

Dans le tableau, « dég. » désigne l'amortissement dégressif, « lin. » l'amortissement linéaire et « VA » la valeur
actualisée. La colonne « Après correction » donne les valeurs du script corrigé, en euros de 2027 sauf mention.

| Chiffre de `is.tex` | Recalcul indépendant | Après correction | Statut |
|---|---|---|---|
| Recette de l'IS (non chiffrée dans `is.tex`) | IS net : 59,9 Md€ (2025), 60,3 (2026 révisé), 58,5 (PLF 2027) ; hors contribution exceptionnelle (ligne 1441 de l'état A, 5,2 Md€ en 2027), contribution sociale (1,5) et pilier 2 (0,5 en 2026) | — | Vérifié (PLF 2027, texte et état A) |
| Un point de taux = 3,2 Md€ en 2027 | 278 × 1,159 / 100 = 3,22 | **2,95** (2,66 si le taux réduit est maintenu) | **Erreur** (E1) |
| Déduction totale, an 1 : 14 à 15,5 Md€ | 14,03 (dég.) et 15,53 (lin.) ; 11,2 à 18,6 pour une part imposable de 60 à 90 % | inchangé | OK |
| Coût permanent dès l'an 8 : 1,4 à 2,0 Md€ | 1,36 et 1,99 ; formule fermée identique | **1,3 à 2,0** (plan dégressif selon le BOFiP), en euros de 2034, soit 1,1 à 1,6 en euros de 2027 ; +3 % par an ensuite | Arrondi (E2) ; préciser l'année des euros |
| VA par millésime : 1,8 à 2,6 Md€ (5 %) et 1,2 à 1,7 (3,25 %), « soit 0,5 à 0,8 point » | 1,76 à 2,55 ; 1,19 à 1,74 | 1,7 à 2,6 (**0,6 à 0,9 point**) ; 1,2 à 1,7 (**0,4 à 0,6 point**) | « 0,5 à 0,8 » mélange deux taux d'actualisation et un point de 3,2 Md€ |
| Déduction de 50 %, an 1 : 7 à 7,8 Md€ | 7,02 et 7,76 | inchangé | OK |
| Marche de 2033 (passage à 100 %) | 9,0 à 10,8 Md€ en an 7 | inchangé | Absente du texte (déjà relevée, C6) |
| Assiette : 3,5 à 4,9 Md€ | 3,52 et 4,92 | **3,5 à 4,6** | Erreur (E1) |
| — fin du taux réduit : 2,2 à 3,1 | bas 1,7 × 1,03⁸ = 2,15 ; haut 2,7 × 1,159 = 3,13 | **2,2 à 2,9** | Erreur sur le haut (E1) ; bas conventionnel (H14) |
| — CIR au niveau du groupe : 0,6 | 0,569 × 1,06 | 0,59 | OK (chiffre du CPO vieilli, H16) |
| — zones : 0,55 | 0,524 × 1,06 ; **le CPO chiffre l'IR et l'IS ensemble** | 0,54 (à lire « IR et IS ») | **Libellé faux** (E4) |
| — brevets : 0,2 à 0,6 | 1,258 / 2 × 1,06 = 0,64 | 0,2 à 0,62 | OK ; borne basse conventionnelle (H15) |
| IS à 28 % : 5,1 à 8,7 Md€ | 5,06 et 8,73 | **4,6 à 8,0** | Erreur (E1) |
| 100 % dès 2027 : dette de 17 à 45 Md€, remboursée en 10 à 28 ans | 17,0 à 45,4 ; ans 10 à 28 | **18 à 46 ; 10 à 28 ans** | Erreur (E1) |
| Calendrier 50 % puis 100 % : dette de 2 à 32 Md€, remboursée en 4 à 25 ans | 2,1 à 31,9 ; ans 4 à 25 | **3 à 32 ; 4 à 25 ans** | Erreur (E1) |
| Taux réduit maintenu : la dette « n'est jamais remboursée » | Jamais en 40 ans sauf dans un cas (dégressif, 1,8 Md€ de niches : vers 2075) | inchangé | À nuancer |
| Baisse finale de 0,6 à 1,2 point | 0,59 / 1,03 / 0,75 / 1,18 | **0,64 / 1,02 / 0,82 / 1,20** : toujours 0,6 à 1,2 | OK. Elle n'est possible qu'une fois la dette éteinte, **de 2031 à 2052** selon les cas : à dire |
| Petite société, phase à 50 % : avance de 2 300 € pour 20 000 € | 2 321 € | inchangé | OK |
| Seuil de compensation : 220 000 € (110 000 € à 100 %) | 222 645 et 111 322 € à r = 5 %, régime actuel linéaire | inchangé | OK, mais très sensible à r (H23) : 126 000 à 150 000 € (63 000 à 75 000 € à 100 %) si r = 8 à 10 % ; 329 000 € (164 000 €) si l'entreprise amortit aujourd'hui en dégressif |
| IS + PFU sur 42 500 € distribués : 41,7 puis 48,6 % | 41,69 et 48,55 % | la sortie affiche 48,55 | OK |
| Gain de PIB : 0,04 à 0,2 %, 0,1 % au centre | 0,044 à 0,201 % ; 0,107 % | 0,106 % (PIB Insee : 2 991 Md€) | OK ; financement non compté (H20) |
| Triangle évité : 0,05 à 0,16 Md€ | linéaire : 0,05 à 0,16 ; dégressif : 0,02 à 0,08 | inchangé | Écrire **0,02 à 0,16** |
| 28 % : perte sèche « +0,04 sur le capital » | +0,02 à +0,06 si les équipements ne sont pas déduits | Dans le paquet, les équipements sont déduits et leur coin reste nul. La hausse frappe les bâtiments : **+0,04 à +0,30** | Mauvaise comparaison (E5) |
| 28 % : transfert de bénéfices, 0 à +3,8 | 0,265 × 4,5 % × 322 = 3,84 | **0 à +3,2** (base au taux normal de 266 Md€) | Erreur (E6) |

**Ordres de grandeur.**

*Déduction immédiate.*
- La première année coûte 26 % de l'IS net de 2027, contre 12 % au Royaume-Uni (10 Md£ pour 82 Md£, IFS). L'écart
  s'explique en partie : le Royaume-Uni déduit déjà en une fois 1 M£ d'investissement par an et par entreprise
  (*annual investment allowance* permanente), ce qui sort de son chiffrage l'essentiel de l'investissement des PME
  (IFS, copie locale).
- Le coût actualisé (1,7 à 2,6 Md€) est du même ordre que les 1 à 3 Md£ britanniques.

*Valeur d'un point de taux, avant correction.* Le chiffre de 3,22 Md€ supposait un IS brut liquidé de 77 Md€ en 2027.
Trois repères s'y opposent :
- 68,4 Md€ en 2022 (DGFiP) et 68,6 Md€ en 2023 (CPO 2025) ;
- un IS net à payer de 62 Md€ en 2022 (DGFiP), qui descend à 58,5 Md€ prévus en 2027 ;
- une croissance du bénéfice fiscal de +1 %, 0 % et +1 % de 2023 à 2025.

Corrigé, l'IS brut implicite est de 71 Md€. Le point vaut 2,84 à 2,98 Md€ si le bénéfice croît de 0 à 2,5 % par an
en 2026 et 2027.

*Stock d'équipements.* Le stock de 541 Md€ est confirmé (512,1 + 28,8). La consommation de capital fixe rapportée au
stock vaut 14,5 %, ce qui valide δ = 0,14.

---

## 3. Hypothèses fortes

Format du tableau d'annexe : hypothèse ; où elle joue ; ce qu'elle change si elle est fausse. Les effets sont calculés
avec le script corrigé ; « S3 » désigne le calendrier 50 % puis 100 %, « S4 » la déduction totale dès 2027.

| # | Hypothèse (valeur retenue) | Où elle joue | Si elle est fausse |
|---|---|---|---|
| H1 | **75 % de l'investissement éligible est fait par des sociétés imposables** (60 à 90 %). Aucune donnée publiée : ni la DGFiP ni l'Insee ne croisent l'investissement et la situation fiscale. | Tous les coûts (proportionnels), la dette, le gain de PIB, le triangle | La première année coûte 11,2 Md€ (60 %) à 18,6 Md€ (90 %). Pour S3 dans le cas bas, la dette maximale passe de 32 à **15 ou 51 Md€**, remboursée en 17 ou 37 ans. À 90 %, S4 dans le cas bas **ne se rembourse pas en 40 ans**. C'est l'hypothèse qui pèse le plus. |
| H2 | Les sociétés imposables utilisent toute la déduction l'année même. Les non-imposables (25 %) ne coûtent jamais rien. | Profil du coût | Avec le plafonnement des déficits (1 M€ plus 50 %), une partie de la déduction devient un déficit reporté : la première année coûte moins. Les déficits des non-imposables finissent par être imputés : le coût de long terme est un peu plus élevé. Effet net non chiffrable sans microdonnées. |
| H3 | Assiette éligible : machines (hors transport) et matériel informatique des SNF, 84,1 Md€ en 2025. Ni matériel de transport, ni bâtiments, ni entreprises à l'IR. | Tous les coûts | Avec le matériel de transport (42 Md€), la première année coûte **23,3 Md€** au lieu de 15,5. Ouvrir la mesure aux entreprises à l'IR, comme les suramortissements actuels, ajouterait au plus 14,5 Md€ d'assiette : l'investissement de toute l'économie dans ces actifs est de 98,6 Md€ (Insee 8.221), contre 84,1 pour les SNF. |
| H4 | Durée d'amortissement type : 7 ans | Coût, VA, coin fiscal, seuil de la petite société | À 5 ans : première année 15,0 Md€, VA 1,9, coin 3,7 %. À 10 ans : première année 15,9 Md€, VA **3,5**, coin 7,0 %, coût permanent 3,0 Md€. |
| H5 | Régime actuel entièrement linéaire, ou entièrement dégressif. Les deux bornes sont données ; leur mélange réel n'est pas publié (pas de dotations par mode). | Toutes les fourchettes | C'est la principale source des fourchettes : première année 14,0 ou 15,5 Md€ ; VA 1,7 ou 2,6 Md€ ; dette S3 de 8 ou 32 Md€ dans le cas bas. |
| H6 | Croissance nominale de l'investissement : g = 3 % (Insee : 3,2 % par an de 2022 à 2025, 3,9 % de 2019 à 2025) | Coût permanent, dette, ressources | À 2 % : coût permanent de 1,25 Md€ (linéaire, an 8) ; dette S3 de 26 Md€ dans le cas bas, remboursée en 22 ans. À 4 % : 2,81 Md€ ; 39 Md€, remboursée en 30 ans. |
| H7 | **Croissance du bénéfice fiscal de 2 % par an en 2026 et 2027** (2023 à 2025 : chiffres officiels). Le tome I des Voies et moyens du PLF 2027, qui donne 2026 et 2027, n'est pas en ligne. | Point de taux, taux réduit, IS à 28 % | De 0 à 2,5 % : point de 2,84 à 2,98 Md€ ; taux réduit de 2,75 à 2,89 ; 28 % statique de 7,7 à 8,1. Effet faible. |
| H8 | Taux d'actualisation des entreprises : 5 % nominal | z, coût d'usage, coin, gain de PIB, triangle, seuil de la petite société | À 8 % : z linéaire de 0,77 au lieu de 0,85. Coin de 7,5 % au lieu de 5,1 : le gain de la déduction et le triangle sont plus grands. Le seuil de la petite société tombe à 150 000 € (75 000 € à 100 %). |
| H9 | Taux d'emprunt de l'État : 3,25 % | Dette, durée de remboursement | De 2,5 à 5 % : dette S3 de 30,5 à 35,8 Md€ dans le cas bas, remboursée en 24 à 29 ans. Le cas haut ne bouge pas. |
| H10 | Pas d'investissement supplémentaire suscité dans le chiffrage budgétaire | Coût des premières années | Avec +10 % d'investissement (ordre de Zwick et Mahon), la première année coûte 1,7 Md€ de plus à 100 % (0,8 à 50 %), récupérés ensuite par l'impôt sur les rendements. |
| H11 | Ressources et coûts au rendement plein dès 2027 ; pas de décalage des acomptes et du solde | Profil annuel de la dette | Le calendrier budgétaire décale de quelques mois à un an recettes et coûts, dans le même sens. L'ordre de grandeur de la dette ne change pas ; les années précises, si. |
| H12 | **Semi-élasticité des bénéfices déclarés de 0 à 1,5 % par point**, appliquée à tous les bénéfices. Elle est mesurée sur les filiales de multinationales (Beer, de Mooij et Liu, 2020). | Rendement du 28 %, perte sèche | Les PME ne transfèrent pas de bénéfices : la borne de 4,6 Md€ est pessimiste. À l'inverse, les choix d'implantation (marge extensive) ne sont pas comptés. |
| H13 | **Coût réel du transfert de bénéfices, κ de 0 à 1**, appliqué à tout le taux moyen (26,5 %) | Perte sèche du 28 % | Le coût privé marginal d'un euro transféré égale l'écart de taux avec le pays d'accueil, pas le taux français entier. κ = 1 revient à compter comme perte nationale l'impôt payé à l'étranger par des actionnaires français. Avec un pays d'accueil à 12,5-15 %, la borne haute serait environ moitié moindre (+1,5 au lieu de +3,2 Md€). |
| H14 | Fin du taux réduit : rendement statique, avec une borne prudente de 2,15 Md€, soit 75 % du statique (coût officiel de 2019 ramené à 10 points, porté à 3 % par an) | Ressources, dette dans le cas bas | La borne basse n'est pas une estimation. Les réactions (passage à l'IR, rémunération en salaire) et la jurisprudence du Conseil d'État de 2025 (chiffre d'affaires apprécié au niveau du groupe) ne sont pas chiffrées. |
| H15 | Boîte à brevets : 0,62 Md€ si la base reste, 0,2 Md€ si elle fuit (borne arbitraire) | Ressources | 0,4 Md€ d'écart ; la dette se déplace de quelques Md€. |
| H16 | CIR au niveau du groupe : 0,57 Md€ (CPO 2025) | Ressources | Ce chiffre n'est pas une estimation nouvelle. C'est une estimation de 2021 sur les liasses de 2016 (470 M€ en 2019), vieillie par la croissance de la dépense fiscale. Incertitude inconnue. |
| H17 | Zones : 0,52 Md€ (2025), portés à +4 % jusqu'en 2027 | Ressources | Le chiffre du CPO couvre l'IR et l'IS ; la part de l'IS n'est pas publiée. Les ZRR sont en extinction (fin d'incidence en 2032), les FRR montent en charge (5 puis 60 M€) et les ZFU-TE sont fermées aux entrées après 2025 : plutôt stable que croissant. Effet au plus de 0,5 Md€. |
| H18 | r + δ = 0,19 (r = 5 % nominal, δ = 14 %) | Triangle, gain de PIB | Avec r réel de 3 %, r + δ = 0,17 : le triangle et le PIB baissent d'environ 10 %. |
| H19 | **Élasticité du stock d'équipements au coût d'usage : 0,5 à 1,6** (1,6 : Maffini et al., version de travail ; 0,5 : sans source) | Gain de PIB (0,04 à 0,2 %), triangle | Effet proportionnel. Le mécanisme est contesté : si la déduction agit surtout par la trésorerie (Zwick et Mahon), l'effet dépend de la taille et de la rentabilité, et supprimer le taux réduit l'affaiblit chez les petites sociétés. |
| H20 | Le gain de PIB ne compte pas l'effet du financement | Gain de PIB | La fin du taux réduit renchérit le capital des sociétés sous le plafond. Taux marginal effectif sur les bâtiments : 13 % → 22 % ; sur les équipements pendant la phase à 50 % : 12,1 % → 11,5 %, à peu près inchangé. Bernini et Treibich (résumé) : diviser le taux par deux accroît le capital de 29 %. L'effet net du paquet n'est pas chiffré et peut être nettement inférieur à 0,1 % du PIB. |
| H21 | Taux normal de 25 % pour tous (contribution sociale de 3,3 % et contribution exceptionnelle ignorées) | Coûts | Pour les grandes entreprises, le taux de 25,825 % renchérit la déduction d'environ 3 % sur leur part : négligeable. |
| H22 | Référence = droit permanent : la contribution exceptionnelle s'éteint | Récit « à recette constante » | Par rapport à 2026, le paquet est une baisse de 7 Md€ pour quelque 450 groupes (nombre non vérifié). Par rapport au PLF 2027, de 5 Md€. |

---

## 4. Chiffres vérifiés ici, et ceux qui ne le sont pas

### 4.1 Vérifiés sur source primaire dans ce contrôle

| Chiffre | Valeur | Source (copie lue) |
|---|---|---|
| Investissement éligible des SNF en 2025 | 75,524 + 8,534 = 84,06 Md€ | Insee, comptes nationaux base 2020, tableau 8.212 (juillet 2026), `is_insee_T_8212_fr/` |
| Stock fin 2025 ; consommation de capital fixe 2025 | 512,1 + 28,8 = 540,9 Md€ ; 77,3 Md€ (14,5 % du stock moyen) | Idem |
| Matériel de transport ; bâtiments non résidentiels ; génie civil (fin 2025) | flux 42,1 Md€ ; stocks 399,9 et 648,0 Md€ | Idem |
| Investissement de toute l'économie dans ces actifs, 2025 | 85,3 + 13,3 = 98,6 Md€ | Insee, tableau 8.221 |
| Bénéfices de 2022 par taux | 27 (15 %), 202 (25 %), 39 (26,5 %), 10 (27,5 %) ; total 277,9 ; déficits 113 | DGFiP Statistiques n° 21, fichier xlsx, graphique 2 |
| IS brut et bénéfices par taille, 2022 | TPE 13,1 / 60,3 ; PME 18,9 / 75,9 ; ETI 15,8 / 62,2 ; GE 20,6 / 79,5 Md€ ; IS net à payer 62 Md€ | DGFiP n° 21, tableau 2 et texte |
| Croissance du bénéfice fiscal | 2022 +3,5 % ; 2023 +1 % (révisé, au lieu de +14 %) ; 2024 0 % (au lieu de −1,9 %) ; 2025 +1 % ; 2026 +2,5 % (prévision) | Voies et moyens, tome I, PLF 2025 et PLF 2026 |
| IS net | 59,9 (2025), 61,6 (LFI 2026), 60,3 (2026 révisé), 58,5 (PLF 2027) | PLF 2027, tableau des recettes fiscales nettes |
| IS brut (budget) | 86,8 / 85,0 / 83,9 Md€ (LFI 2026, 2026 révisé, PLF 2027) | PLF 2027, état A, ligne 3 |
| Contribution exceptionnelle | 7,5 Md€ en 2025 ; 5,0 Md€ en 2027 « en diminution de 2,0 Md€ par rapport à 2026 » ; ligne 1441 de l'état A : 5,2 Md€ ; ligne distincte de l'IS net | DGFiP Statistiques n° 43 ; PLF 2027 |
| CIR | 7 800 / 8 068 / 8 041 M€ (2024 à 2026) ; 17 593 entreprises | VM tome II, PLF 2026, n° 200302 |
| Boîte à brevets | 1 199 / 1 258 M€ (2024 et 2025) ; 1 065 entreprises ; norme : taux normal | VM tome II, PLF 2026, n° 210326 |
| ZRR, FRR, ZFU-TE | 411 / 430 / 376 M€ (fin d'incidence en 2032) ; − / 5 / 60 M€ ; 107 / 89 / 89 M€ ; toutes « IR et IS » | VM tome II, PLF 2026, n° 220104, 220109, 220102 |
| CIR au niveau du groupe | 569 M€ (2025), vieilli depuis 470 M€ (2019), sur les liasses de 2016 | CPO, sept. 2025, p. 104 et 130-131 |
| Zones | 524 M€ d'**IR et d'IS** (FRR 355, ZFU 102, AFR 56, autres 11), d'après les données du PLF 2025 | CPO 2025, tableau n° 12 et p. 129 |
| Taux réduit | 2,2 Md€ en 2019 (760 000 entreprises) ; 2,6 Md€ en 2014 (670 000) | CPO, juin 2023 |
| Taux implicites, 2022 | 17,5 % au total ; PME 21,4 % ; micro 19,0 % ; GE 14,3 % | Insee Analyses n° 112 |
| Taux effectifs OCDE, 2025 (taux fixes, 38 pays) | Taux moyen composite 23,61 % (moyenne 22,24 %, 13e) ; taux marginal composite 14,97 % (16,49 %, 24e) ; équipements 9,82 % (10,40 %, 21e) ; bâtiments 7,33 % (12,09 %, 26e) ; stocks 30,09 % (21,80 %, 6e) | OCDE, DSD_ETR@DF_ETR_BASELINE, recalculé sur `is_oecd_etr_all/etr.csv` |
| Taux légal OCDE de la France | 25,825 % (2022-2024) ; 36,13 % (2025-2026) | OCDE, `is_oecd_cit/cit.csv` |
| **IS en % du PIB** (nouveau) | France 2,35 % en 2023 (moyenne OCDE 3,75 %, médiane 3,41 %, **32e sur 38**) ; 2,25 % en 2024 (3,62 %, 31e sur 36) ; Allemagne 2,2 ; Royaume-Uni 3,4 ; États-Unis 2,2 | OCDE, Revenue Statistics (DSD_REV_COMP_OECD@DF_RSOECD, impôt 1200, administrations publiques), téléchargé dans `verif_is_dl/oecd_rev/` |
| Fin du plan dégressif | L'exercice d'acquisition compte pour une année entière : un bien de 7 ans s'amortit en 7 exercices, pas en 8 | BOFiP, BOI-BIC-AMT-20-20-30, § 260 et exemple § 350 |
| Royaume-Uni | Environ 10 Md£ par an au départ ; coût final de 1 à 3 Md£ par année ; *annual investment allowance* fixée à 1 M£ de façon permanente | IFS, *Green Budget* 2023, chapitre 10 |
| PIB 2025 | 2 991 Md€ | Insee (`donnees/pib_france_cp_meur.json`) |

Ont été vérifiées sur les sources par `revue/verif_litterature_is_pfu.md` et ne sont pas reprises ici :
- Tax Foundation : rangs, taux de 36,1 % contre 24,2 % de moyenne, récupération des coûts 15e puis 16e, 88 % contre
  86 % ;
- Zwick et Mahon ; Maffini et al. (version de travail) ; Chodorow-Reich et al. (tableau 7) ;
- Beer, de Mooij et Liu ; Bernini et Treibich (résumé seulement) ;
- Sénat (2026) ; CPO (2023, 2025) ; minimum mondial (BOFiP).

### 4.2 Non vérifiés sur source primaire : à signaler dans le texte

| Chiffre ou fait | Pourquoi | Statut à afficher |
|---|---|---|
| Croissance du bénéfice fiscal en 2026 et 2027 | Le tome I des Voies et moyens du PLF 2027 n'est pas en ligne ; le PLF dit seulement « moins dynamique qu'anticipé » puis « plus modérée » | Hypothèse de 2 % par an |
| Environ 450 redevables de la contribution exceptionnelle ; nombre d'entreprises à 36,1 % (3 Md€ de chiffre d'affaires et plus) | Source : le cours ; ni la DGFiP n° 43 ni le PLF 2027 ne le donnent | Chiffre non vérifié |
| Part de l'investissement faite par des sociétés imposables (75 %) | Aucune statistique | Hypothèse (H1) |
| Mélange linéaire / dégressif des équipements | Dotations par mode non publiées | Hypothèse (H5) |
| Part de l'IS dans les 524 M€ des zones | Dépenses fiscales communes à l'IR et à l'IS | Non publié |
| Ventilation de la base à 15 % par type de société (holdings, sociétés immobilières, professions libérales) | Aucune statistique | Non publié |
| Bénéfice moyen au taux réduit, « environ 24 000 € » | Base de 2018 divisée par le nombre de bénéficiaires de 2019 ; on ne connaît pas le nombre de bénéficiaires de 2022 | À dater (« 2018-2019 ») |
| Taux d'emprunt de l'État de 3,25 % | Hypothèse du script | Hypothèse (H9) |
| Élasticité de 0,5 (borne basse) | Sans source | Hypothèse (H19) |
| Prise en compte de la contribution exceptionnelle par l'OCDE | Déduite des données (taux identiques en 2024 et 2025) | Déduction de l'auteur |
| Part de dette dans le financement des taux effectifs de l'OCDE | Note de méthode non lue | Non vérifié : c'est pourquoi le taux marginal « fonds propres » calculé ici (§ 6) ne se compare pas au 9,8 % de l'OCDE |
| Article 15 du PLF 2027 supprimé en première lecture | Légifiscal (source secondaire) | Non vérifié |
| « Jusqu'à 3,0 Md€ avec le plafond de 42 500 € » (`is_recherche.md` § 3.2, `verif_is_pfu.md` E2) | **Faux** : le plafond de 42 500 € vaut pour les exercices clos à compter du 31 décembre 2022, donc pour la plupart des exercices de 2022. La base de 27 Md€ l'intègre déjà. | Ne pas reprendre |

---

## 5. Erreurs corrigées (scripts modifiés et relancés ; aucun fichier `.tex` touché)

**E1. Les bénéfices de 2022 étaient portés en 2027 à 3 % par an (× 1,159) ; c'est désormais × 1,061.**
- *Constat.* La croissance du bénéfice fiscal a été de +1 % (2023), 0 % (2024) et +1 % (2025), selon les Voies et
  moyens.
- *Correction.* Dans `is/simulation_is.py`, `A22` et `A25` sont calculés à partir de ces taux, avec +2 % par an en
  2026 et 2027 (hypothèse H7).
- *Ce qui change :*
  - valeur d'un point : 3,22 → **2,95 Md€** ;
  - fin du taux réduit : 3,13 → **2,87** ;
  - assiette : 4,9 → **4,6** dans le cas haut (3,5 inchangé dans le cas bas) ;
  - IS à 28 % : 5,1-8,7 → **4,6-8,0** ;
  - dettes : S3 dans le cas haut 11,2 → 15,2 Md€ en linéaire et 2,1 → 2,7 en dégressif ; S4 dans le cas haut
    35,2 → 37,3 et 17,2 → 18,5 ; années de remboursement : linéaire 14 → 16 et 16 → 18 ;
  - baisse finale en points : 0,59 / 1,03 / 0,75 / 1,18 → 0,64 / 1,02 / 0,82 / 1,20.

**E2. Le plan dégressif s'étalait sur 8 exercices ; il en compte 7 (BOFiP, § 260).**
- *Ce qui change* : z passe de 0,8945 à 0,8966.
  - Coût permanent en an 8 : 1,36 → 1,33.
  - VA à 5 % : 1,76 → 1,73 ; VA à 3,25 % : 1,19 → 1,17.
  - Dette S3 dégressive dans le cas bas : 7,9 → 7,6.
- C'est négligeable, mais la fourchette « 1,4 à 2,0 » devient « 1,3 à 2,0 ».

**E3. Constantes et affichage.**
- PIB 2025 : 2 950 → 2 991 Md€ (Insee). PIB 2027 : 3 100 → 3 173 Md€.
- Le taux cumulé de 48,55 % est désormais affiché tel quel ; la sortie donnait 48,5, à cause d'un arrondi de virgule
  flottante.
- Effet sur les résultats : moins de 0,002 point de PIB.

**E4. Zones.** Le libellé devient « IR et IS ». Le montant reste celui du CPO porté en 2027 (0,54) ; voir H17 pour une
lecture plus prudente.

**E5. `synthese/perte_seche_autres.py` : perte sèche d'un IS à 28 % inclus dans le paquet.**
- *Ajout.* Une ligne qui suppose les équipements déduits, donc à coin nul quel que soit le taux. La hausse renchérit
  alors les bâtiments non résidentiels imposables : **+0,04 à +0,14 Md€** avec δ = 3,1 %, **+0,09 à +0,30** avec
  δ = 12,3 %.
- *Ligne existante.* « IS à 28 %, linéaire » (+0,02 à +0,06) suppose des équipements non déduits ; elle est gardée.
- *Tableau de `is.tex`.* Il cite +0,04 pour le financement par le taux. Retenir plutôt **« +0,05 à +0,3 sur le
  capital »**, ordre de grandeur inchangé à côté du transfert de bénéfices.

**E6. `perte_seche_autres.py` : base du transfert de bénéfices.**
- *Constat.* Le script prenait 322 Md€ : toute la base, taux réduit compris, portée à 3 % par an. Or la hausse à 28 %
  ne touche que la base au taux normal, 251 × 1,061 = 266 Md€.
- *Ce qui change* : κ = 1 donne **+2,1 à +3,2** au lieu de +2,6 à +3,8 ; κ = 0,5 donne +1,1 à +1,6.
- Le bloc PFU du même fichier, modifié en parallèle par un autre agent, n'a pas été touché ; sa sortie est inchangée.

**Autres fichiers.**
- `is/figures_is.py` : la note de figure est mise à jour (3,5 à 4,6 ; 4,6 à 8,0 ; croissance du bénéfice fiscal).
  **La figure n'a pas été régénérée** : `figures/is_01_cout_deduction*` reste cohérente avec le `is.tex` actuel et sera
  refaite à la réécriture.
- `is/README.md` : chiffres clés mis à jour.

**À corriger dans `is.tex` lors de la réécriture** (en plus des chiffres du § 2) :
1. Dire que le coût permanent est en euros de 2034 et croît avec l'investissement.
2. Dire la marche de 2033 : 9 à 11 Md€.
3. Dater la baisse finale du taux : pas avant 2031, et 2052 dans le cas le plus défavorable.
4. Pour le taux réduit maintenu, écrire « pas remboursée en 40 ans ».
5. Donner le seuil de compensation de la petite société comme une fourchette selon son taux d'actualisation.
6. Écrire « 0,02 à 0,16 » pour le triangle évité.
7. Pour les zones, écrire « exonérations d'IR et d'IS ».

---

## 6. Calculs manquants pour la nouvelle architecture : faits ici ou faisables

Les résultats viennent de `verif_is_sortie.txt` et de la sortie de `supplement.py`. Les taux effectifs « style
Devereux-Griffith » sont une illustration à conventions explicites : financement par fonds propres, r réel de 5 %,
inflation de 2 %, δ = 14 % pour les équipements et 3,1 % pour les bâtiments, z actualisé au taux nominal, rendement de
20 % pour le taux moyen. Les **niveaux** ne se comparent pas à ceux de l'OCDE (§ 4.2) ; les **écarts** entre variantes
sont le message.

### 6.1 Situation actuelle (sous-section 1) : faisable, fait

- **Recette.**
  - IS net de 59,9 Md€ en 2025, soit 2,0 % du PIB.
  - S'y ajoutent la contribution exceptionnelle (7,5 Md€ en 2025, environ 7 en 2026), la contribution sociale
    (1,5) et le pilier 2 (0,5 en 2026).
  - Avant remboursements et dégrèvements, dont le CIR (8 Md€), l'IS brut budgétaire vaut 85 Md€ (2026).
- **Comparaison internationale.** La France a le taux légal le plus élevé de l'OCDE pour les plus grands groupes
  (36,1 %, contre 24,2 % en moyenne ; Tax Foundation) et un taux moyen effectif un peu au-dessus de la moyenne (23,6 %
  contre 22,2 %). Mais l'IS ne rapporte que **2,35 % du PIB (2023), contre 3,75 % en moyenne : 32e sur 38**.
  - Ce contraste fait un bon point de départ pour un lecteur novice : taux affiché élevé, recette faible.
  - Explications possibles : déficits (113 Md€ en 2022), CIR, profits transférés. Aucune n'est mesurée ici.
  - Un graphique est faisable avec le fichier téléchargé : IS en % du PIB pour les 38 pays.
- **Taux affichés.**
  - 25 % ; 25,825 % avec la contribution sociale (chiffre d'affaires d'au moins 7,63 M€, abattement de 763 000 €) ;
    15 % jusqu'à 42 500 € ;
  - 30,98 % et 36,13 % avec la contribution exceptionnelle (chiffre d'affaires d'au moins 1 Md€ et d'au moins 3 Md€,
    exercices 2025 et 2026).
- **Taux effectifs.**
  - OCDE : taux marginal de 15,0 % au total et de 9,8 % pour les équipements, au niveau ou sous la moyenne.
  - Insee : IS hors crédits / excédent net d'exploitation de 17,5 % ; GE 14,3 %, micro 19,0 %, PME 21,4 %.
  - DGFiP : IS brut / bénéfices de 21,7 % (TPE), 24,9 % (PME), 25,4 % (ETI) et 25,9 % (GE).
  - Leçon pédagogique : sur le bénéfice fiscal, les grandes entreprises paient le taux légal ; c'est sur l'excédent
    d'exploitation (déficits, mère-fille, plus-values, intégration) qu'elles paient moins.
- **Qui paie.** Part de l'IS brut en 2022 :
  - TPE 19 %, PME 28 %, ETI 23 % ;
  - GE 30 %, soit 400 entreprises au sens statistique.
  - La contribution exceptionnelle porte en plus sur les seuls grands groupes (7,5 Md€).

### 6.2 Réforme naïve : une baisse générale du taux (sous-section 3) : faisable, fait

| Baisse du taux normal (taux réduit gardé) | Coût statique 2027 | Avec retour de bénéfices (1 à 1,5 % par point) |
|---|---|---|
| −1 point (24 %) | 2,7 Md€ | 1,7 à 2,0 |
| −3 points (22 %) | 8,0 | 5,4 à 6,2 |
| −5 points (20 %) | 13,3 | 9,3 à 10,7 |

- **À qui elle profite.** En proportion des bénéfices de 2022 au taux normal : GE 32 %, ETI 25 %, PME 28 à 30 %,
  TPE 13 à 16 %. La fourchette tient à une hypothèse : la base à 15 % est placée chez les TPE, entièrement ou aux trois
  quarts. Elle profite aussi aux profits du capital déjà installé et aux rentes.
- **Effet sur l'investissement en équipements, à coût égal.** La déduction totale vaut, en valeur actualisée, 0,87 point
  de taux (2,55 Md€ pour un point de 2,95 Md€).
  - Le même coût affecté à une baisse du taux ramène le coin des équipements de **5,09 % à 4,86 %**. La déduction
    totale le ramène **à 0**.
  - Taux marginal effectif (convention ci-dessus) : 20,7 % aujourd'hui ; 19,8 % à 24 % ; 16,3 % à 20 % ; **0 %** avec
    la déduction totale.
  - Littérature : Chodorow-Reich et al. (2026, modèle calé) donnent un coût par point de capital quatre fois plus
    élevé pour une baisse de taux. Il n'existe aucune évaluation causale française de la baisse de 33,3 à 25 %
    (France Stratégie 2023 ne sépare pas ses effets).
- **Taux moyen effectif d'un projet en équipements rentable** (20 %).
  - Aujourd'hui 23,6 % ; avec la déduction totale **18,8 %**, soit presque autant qu'un taux de 20 % (18,9 %), pour un
    coût actualisé d'environ 2,6 Md€ par an contre 13,3 statiques.
  - En revanche, pour un projet en bâtiments ou un bénéfice mobile, seule la baisse du taux agit. C'est la vraie limite
    de l'argument, à dire.

### 6.3 Proposition comparée à aujourd'hui (sous-section 4) : faisable, fait

| Équipement (convention Devereux-Griffith) | Coin sur le coût d'usage | Taux marginal | Taux moyen (20 %) |
|---|---|---|---|
| Aujourd'hui, linéaire 7 ans | 6,9 % (5,1 % au taux nominal de 5 % du script) | 20,7 % | 23,6 % |
| Aujourd'hui, dégressif | 4,7 % | 15,1 % | 22,1 % |
| 50 % immédiat | 3,4 % | 11,5 % | 21,2 % |
| 100 % immédiat | 0 | 0 | 18,8 % |
| 28 % avec 100 % immédiat | 0 | 0 | 21,0 % |
| Petite société sous le plafond : aujourd'hui (15 %) | 3,6 % | 12,1 % | 14,2 % |
| Petite société : réforme, phase à 50 % | 3,4 % | 11,5 % | 21,2 % |
| Petite société : réforme à 100 % | 0 | 0 | 18,8 % |
| Bâtiment, 25 % / 28 % / petite société à 15 % | — | 22,0 / 24,7 / 13,0 % | 24,0 / 26,9 / 14,4 % |

Coût d'usage des équipements : −4,8 % (linéaire) ou −3,3 % (dégressif) avec la déduction totale.

Message pour un graphique avant/après : la proposition annule le coin sur les équipements. Mais pour une petite société
sous le plafond, pendant la phase à 50 %, elle ne fait que compenser la fin du taux réduit sur ses équipements et
renchérit ses bâtiments (13 % → 22 %).

Faisable, non fait : reproduire exactement les conventions de l'OCDE pour donner « 9,8 % → x % ». Il faut pour cela la
note de méthode (part de dette, δ = 17,5 %, inflation de 1 %).

### 6.4 Arbitrages (sous-section 5) : faisable, fait sauf mention

- **50 % ou 100 %.**
  - Première année : 7,0-7,8 contre 14,0-15,5 Md€.
  - VA par millésime : 0,9-1,3 contre 1,7-2,6 Md€.
  - PIB à long terme : 0,05 contre 0,11 %.
  - Triangle évité : 0,04-0,12 contre 0,02-0,16 Md€.
  - Taux marginal sur les équipements : 11,5 contre 0 %.
- **Calendrier.**
  - 100 % dès 2027 : dette de 18 à 46 Md€, remboursée en 10 à 28 ans. Pic de 45,6 Md€ en 2033, soit 1,2 % du PIB
    (38 Md€ de 2027).
  - 50 % puis 100 % : 3 à 32 Md€, remboursée en 4 à 25 ans. Pic de 32,4 Md€ en 2038, soit 0,74 % du PIB.
- **Taux réduit.**
  - Le garder : il manque 2,2 à 2,9 Md€ par an, et la dette n'est pas remboursée en 40 ans.
  - Le supprimer : une petite société perd au plus 4 250 € par an.
  - Le réserver aux sociétés opérationnelles : **non chiffrable** (pas de ventilation de la base).
  - Relever le plafond à 100 000 € (Sénat) : **non chiffrable** sans la distribution des bénéfices par société.
- **Financement.**
  - Assiette : 3,5 à 4,6 Md€ ; perte sèche presque nulle, mais une hausse d'IS sur les TPE et les zones.
  - 28 % : 4,6 à 8,0 Md€ ; perte sèche de +0,05 à +0,3 sur le capital et de 0 à +3,2 par le transfert de bénéfices.
- **Contribution exceptionnelle prolongée deux ans (5 Md€ en 2027 et 2028) et affectée à la transition.**
  - Calendrier : dette de 32 → 18 Md€ dans le cas linéaire bas (remboursée en 20 ans au lieu de 25). Elle disparaît
    dans les cas dégressifs.
  - 100 % dès 2027 : 45 → 33,5 Md€.
  - Une variante prudente garde donc l'essentiel : déduction totale dès 2027 et transition financée par le dernier
    prélèvement sur les grands groupes. Le coût est de rompre la promesse de non-reconduction.
- **Cas types de petites sociétés** : faisables par `petite_societe`.
  - 30 000 € de bénéfice : +3 000 € d'IS.
  - Au plafond : +4 250 €.
  - Avance de 2 321 € (50 %) ou de 4 643 € (100 %) pour 20 000 € d'équipements.
  - Seuil de compensation de 126 000 à 223 000 € (50 %) selon le taux d'actualisation.

### 6.5 Transition (sous-section 6) : faisable, fait sauf mention

- **Profil du coût.** Phase à 50 % : 7 à 7,8 Md€ en 2027, puis en baisse ; marche de 9 à 11 Md€ en 2033 ; coût
  permanent de 1,3 à 2,0 Md€ dès 2034.
- **Dette et durées.** Voir § 6.4. La baisse finale du taux de 0,6 à 1,2 point n'est possible qu'après extinction de la
  dette : 2031 (dégressif, assiette haute), 2041, 2043 ou **2052** (linéaire, assiette basse).
- **Sensibilité à la part imposable (H1).** À 90 %, le calendrier crée une dette de 51 Md€ dans le cas bas, remboursée
  en 37 ans, et la déduction totale immédiate ne se rembourse pas. Le texte doit le dire.
- **Coût de transition et coût permanent.**
  - Transition : la dette, soit le cumul des avances.
  - Coût permanent : 1,3 à 2,0 Md€ par an, ou 1,7 à 2,6 Md€ en valeur actualisée par millésime.
  - Ressource permanente : 3,5 à 4,6 Md€, d'où l'excédent rendu par le taux.
- **Faisable, non fait.** Décaler recettes et coûts selon le calendrier des acomptes et du solde (H11), ce qui demande
  une hypothèse simple de décalage d'un an. Chiffrer le report des déficits des non-imposables (H2) demanderait des
  microdonnées : non faisable.
- **Hors calcul.** Constitutionnalité (rétroactivité, égalité devant les charges publiques pour la fin du taux réduit) ;
  faisabilité administrative (la déduction immédiate simplifie : plus de plan d'amortissement fiscal pour ces biens,
  mais une divergence entre comptabilité et fiscalité).

Sources web : [OCDE, Revenue Statistics, API SDMX](https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,/.TAX_REV.S13.T_1200._T.PT_B1GQ.A?startPeriod=2018&format=csvfilewithlabels) ;
recherche infructueuse du tome I des Voies et moyens du PLF 2027 (aucun résultat primaire ;
[Légifiscal, présentation du PLF 2027](https://www.legifiscal.fr/actualites-fiscales/4656-presentation-plf-2027.html)
seulement).
