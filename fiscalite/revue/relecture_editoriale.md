# Relecture éditoriale finale : « Taxer mieux plutôt que davantage » (16/11/2026)

J'ai relu la note comme son lecteur visé : un décideur intelligent, intéressé par l'économie, qui ne connaît pas bien
la fiscalité française. J'ai lu les sources LaTeX de l'introduction, des cinq sections et des annexes, regardé toutes
les figures, et comparé les chiffres repris dans `introduction.tex` et `ensemble.tex` avec ceux des parties et des
sorties des scripts (`synthese/sorties/`, `is/sorties/`, `pfu/sorties/`, `sorties/calculs_foncier.txt`).

Compilation (depuis `synthese/`, deux passes de pdflatex) : aucune erreur, aucun renvoi indéfini, 101 pages (100
avant). Le seul avertissement « Overfull » (2 pt) vient d'un tableau généré (`tab_is_transition_complet.tex`) et existait
déjà.

Fichiers modifiés : `synthese/parties/introduction.tex`, `ircsg.tex`, `annexe_ircsg.tex`, `foncier.tex`, `is.tex`,
`pfu.tex`, `ensemble.tex`, et le PDF recompilé. Je n'ai touché ni au document maître, ni aux scripts, ni aux figures,
ni aux tableaux générés.

---

## 1. Ce que j'ai corrigé, partie par partie

### Introduction
- J'ai défini la CSG et la CRDS à leur première occurrence ; elles n'étaient données que par leur sigle.
- « À la marge, le système doit leur être plus favorable » (contrainte sur les familles) se lisait de deux façons :
  « un peu » ou « au taux marginal ». La phrase dit maintenant : « le nouveau système doit leur être, au total, un
  peu plus favorable qu'aujourd'hui ».
- Dans « Où va la note », le résumé du gain (7 Md€, de 2,5 à 15) dit désormais sur quoi il repose surtout :
  l'hypothèse invérifiée selon laquelle les salariés réagissent à la CSG comme à l'impôt sur le revenu. C'est la
  fragilité principale selon la section 5, mais l'introduction ne la mentionnait pas.
- Le renvoi « exposées en Annexe E » devient « exposées à l'Annexe E ».

### Partie 1 : IR-CSG
- **Chapeau ajouté avant 1.1.** C'était la seule partie, avec l'IS, à commencer sans phrase d'accroche. Il donne trois
  anomalies concrètes déjà chiffrées plus loin (retraité contre salarié, second salaire, 500 € de pension qui coûtent
  600 €), la thèse, et le prix à payer (les pensions).
- Le titre de la figure 1 énonce maintenant un résultat : « La CSG rapporte deux tiers de plus que l'impôt sur le
  revenu : 132 Md€ contre 80 ».
- **Écart 8,8 % / 9,4 % du PIB.** Les deux chiffres se suivaient sans explication. Le texte précise maintenant que
  l'OCDE ajoute « quelques autres prélèvements » (la note de la figure les montre).
- J'ai défini à leur première occurrence le coin fiscal, la prime d'activité, l'élasticité (avec un exemple chiffré :
  10 % de moins laissés au salarié, 2 % de salaire en moins), le RSA activité (« l'ancêtre de la prime d'activité »),
  la CADES et l'ACOSS.
- **Saut de raisonnement corrigé.** La phrase « Cette fusion ne remplit donc aucun des trois objectifs » visait des
  objectifs qui n'étaient pas ceux qu'énumère la phrase. Or la réforme naïve unifie bien l'assiette et allège le
  premier salaire d'une personne seule. La phrase devient « échoue donc sur trois points », ce qui la rend cohérente
  avec « les trois limites de la réforme naïve ».
- **Phrase obscure.** « Il ne change pas la décision de travailler d'un retraité » devient : le taux élevé ne change
  rien pour qui est déjà retraité, mais il réduit ce que rapporte un départ plus tardif, effet que le modèle ne mesure
  pas.
- **« Le 1 % ne bouge pas » est maintenant nuancé.** La disparition de la CEHR (contribution exceptionnelle sur les
  hauts revenus) sur les revenus du barème n'est pas comptée dans cette partie. Le texte renvoie au bilan de la
  section 5.3, conformément à `sorties/synthese_ensemble.txt`, §5.
- « Convention centrale du modèle » était employé sans explication. J'ai ajouté un renvoi à la discussion de cette
  fragilité, qui vient plus loin dans la même sous-partie.
- **Tics de rédaction supprimés** : « doit être dit avec précision ». J'ai aussi réécrit une phrase opaque sur
  l'élasticité du dixième le plus aisé : « aucune étude ne sépare la réaction réelle de la simple optimisation des
  déclarations ».
- J'ai découpé en trois paragraphes la fin de 1.6, qui mêlait collecte, engagements et droit (constitutionnel et
  européen).
- **Tableau déplacé en annexe.** `tab_ircsg_trans` (hausses annuelles selon la durée) faisait double emploi avec la
  figure `ircsg_n16_transition`, qui en reprend les cinq lignes principales. J'ai gardé la figure dans le corps et mis
  le tableau complet dans l'annexe A, avec un court paragraphe « La transition ». Le texte renvoie aux deux.

### Partie 2 : Immobilier
- **Le titre 2.1 contredisait sa figure.** « Prélevés surtout sur les ventes » alors que la figure montre 69 Md€ sur la
  détention et 25 sur les ventes. Nouveau titre : « Cent seize milliards, dont vingt-cinq sur les ventes, et une taxe
  foncière figée en 1970 ». J'ai aussi nuancé la phrase d'accroche (« lourdement au moment où l'on achète et, le reste
  du temps, sur des valeurs de 1970 »).
- **Le compte de la détention ne bouclait pas.** Le texte donnait 42 + 9 + 8 = 59 Md€ pour un total annoncé de 69.
  J'ai ajouté la dizaine de milliards d'« autres prélèvements », détaillés d'après la note de la figure.
- J'ai défini le CPO et DVF (« Demandes de valeurs foncières »).
- **Trois études transformées en paragraphe.** La liste à puces (France, Finlande, Allemagne) devient un paragraphe
  qui les fait dialoguer. Il se termine par la conséquence pour la suite : la réaction des ventes, dont dépend presque
  tout le gain, est l'hypothèse la plus incertaine de la partie.
- **Titre 2.5 rendu parlant.** « Cinq choix pour le décideur » devient « … : les premiers points de baisse des droits
  sont les plus rentables ».
- **Chiffre corrigé : taux départemental de Paris** (voir §2 ci-dessous).
- Le renvoi « en annexe Annexe B » était cassé à l'affichage. Il devient « dans l'Annexe B ».

### Partie 3 : IS
- **Chapeau ajouté avant 3.1.** Il explique le mécanisme (une machine est déduite par fractions, donc l'impôt frappe
  l'investissement marginal), situe le débat public sur le taux, et énonce la thèse.
- J'ai défini l'intégration fiscale, le suramortissement de 2015 (sans date ni taux affirmés de mémoire) et la boîte à
  brevets.
- **Incohérence apparente expliquée.** Le texte citait des taux marginaux effectifs de l'OCDE (9,8 % pour les
  équipements), puis donnait 20,7 % pour une machine, sans dire pourquoi. Une parenthèse précise maintenant que ce
  sont deux conventions différentes et que seuls les écarts entre réformes se comparent (d'après l'annexe C, H26).
- **Tics supprimés** : « qu'il faut reconnaître », « que la figure montre sans fard », « et il faut l'écrire ». J'ai
  aussi remplacé « ce paragraphe » par « cette sous-partie ».
- **Titre 3.5 rendu parlant.** « Quatre arbitrages : le rythme, le financement… » devient « Quatre arbitrages, dont
  le plus politique : supprimer le taux réduit des petites sociétés ».

### Partie 4 : PFU
- **Titre de figure aligné sur le texte.** Celui de `pfu_n02` disait « plus de la moitié des plus-values » quand le
  texte et la figure donnent 70 %. Il devient « … et 70 % des plus-values imposées ».
- **Titre de figure aligné sur le texte.** Celui de `pfu_n08` disait « environ 2 Md€ … 4 Md€ » quand le texte et la
  synthèse donnent 1,9 et 3,6. J'ai repris ces deux chiffres.
- J'ai défini le prélèvement libératoire de 2013 et le pacte Dutreil.
- **Passage clarifié sur la CEHR.** « La CEHR … n'est pas reprise en majoration » supposait connue une majoration du
  PFU dont la note n'avait jamais parlé. Le texte explique maintenant qu'on pourrait la garder sous forme d'une
  majoration de 3 ou 4 points, et que le bilan d'ensemble y renonce.
- **Redite supprimée.** La fin de « Reste le haut de la distribution » répétait la section 5.3 : convention « haut »,
  2,8 Md€, CEHR, contribution exceptionnelle. Elle tient maintenant en un renvoi et les deux leviers propres à la
  partie.
- **Coquille de sens corrigée** : « sans impôt sans trésorerie » devient « sans exiger d'impôt de qui n'a rien
  vendu ».
- **Titre 4.5 rendu parlant** : « Cinq réglages à trancher ; le plus sûr est de ne plus toucher au taux ».

### Partie 5 : les quatre réformes ensemble
- **Chiffre corrigé : le couple à un revenu avec trois enfants**, qui paierait 785 € de plus avec la variante du
  quotient conjugal (voir §2).
- « L'exonération des petites pensions s'arrête à 12 500 € » était inexact. Elle n'est totale que jusqu'à 12 500 €,
  puis décroît jusqu'à 25 000 €.
- « Moins que le couple biactif » n'avait pas de référent dans le tableau. Le texte précise : un couple biactif au
  même revenu, qui gagne 2 900 €.
- **Le titre de la figure `ensemble_n03` était faux tel qu'écrit.** Il annonçait 1,1 milliard « entre −1,7 et +0,2 »,
  alors que 1,1 n'est pas dans cet intervalle. Il distingue maintenant la convention centrale (1,1) des deux autres
  lectures des données (de −1,7 à +0,2).
- **Titres rendus parlants.** Quatre titres descriptifs énoncent maintenant un résultat ou une décision :
  - 5.4 : « Sept ménages : le retraité modeste perd 7,8 % de sa pension, le jeune couple qui achète gagne 3 000 € par
    an » ;
  - 5.5 : « Gagnants et perdants : de la valeur passe des générations âgées aux plus jeunes » ;
  - 5.6 : « Ce qui reste fragile, à commencer par la perception de la CSG » ;
  - 5.7 : « Six décisions que les chiffres ne prennent pas à la place du décideur ».
- **Redites et tics supprimés.**
  - La phrase « Ce n'est pas une hausse de taux, c'est la fin d'une exonération… » répétait mot pour mot la partie 4 ;
    je l'ai supprimée.
  - J'ai retiré les tics « doit être lu pour ce qu'il est » et « qu'il faut dire ».
- **Affirmation corrigée en 5.6.** « Comme le trouvent les études françaises » devient « comme le trouvent Bérard et
  Trannoy (2018) pour la France » : Bachelet et Poulhès trouvent au contraire un effet durable dans les marchés
  détendus.

### Annexes
- Annexe A : ajout du paragraphe « La transition » et du tableau `tab_ircsg_trans`, déplacé du corps.

---

## 2. Incohérences de chiffres trouvées, et ce que j'en ai fait

| Endroit | Dans le texte | Dans les sorties | Traitement |
|---|---|---|---|
| `ensemble.tex`, 5.4 : couple à un revenu, 3 enfants, variante du quotient conjugal | « il paierait 785 € de plus » | `sorties/arbitrages_prop_ircsg.txt`, variante « barème recherché sous les mêmes contraintes » : c3m_60 **+102**. Le chiffre +785 est celui de la variante au barème inchangé (même fichier, l. 12), écrit en dur dans `synthese_ensemble.py`, l. 507 | **Corrigé** : « 100 € de plus qu'aujourd'hui ». C'est la convention de la partie 1 (`tab_ircsg_arbcas`, colonne Quotient : +102). Le texte de `synthese_ensemble.py` reste à corriger (je n'ai pas touché au script) |
| `foncier.tex`, 2.5 et tableau `tab:fon_arb` : taux départemental | « 0,11 % à Paris » | `calculs_foncier.txt` : « de 0.11 à 0.84 % ; **Paris 0.119 %**, Creuse 0.845 % » (le minimum, 0,106 %, est un autre département ; l'annexe B le dit bien) | **Corrigé** : 0,12 % à Paris et 0,85 % dans la Creuse, en précisant « valeurs du modèle » pour ne pas confondre avec le 0,12 % national, exprimé en valeurs de l'Insee |
| Titre de la figure `ensemble_n03` | « 1,1 milliard … entre −1,7 et +0,2 » | `synthese_ensemble.txt` : central +1,13 ; convention « haut » −1,69 ; IR imputé corrigé +0,15 | **Titre réécrit** (voir §1) |
| Figure `ensemble_n03` (image) | étiquette « +0,1 : IR du capital corrigé » | 0,15 ; le tableau et le texte disent +0,2 | Non corrigé (figure). À aligner dans `figures_ensemble.py` |
| Figure `is_n04` (image) | « Taux à 24 % : 2,6 Md€ par an » | `calculs_note_is.txt` : 2,66 ; le texte dit 2,7 | Non corrigé (figure, simple arrondi). À aligner dans le script |
| Titre de la figure `pfu_n02` | « plus de la moitié des plus-values » | 70 % des plus-values imposées (figure et texte) | **Titre aligné** |
| Titre de la figure `pfu_n08` | « environ 2 … 4 Md€ » | 1,90 et 3,62 | **Titre aligné** |
| Titre 2.1 de la partie Immobilier | « prélevés surtout sur les ventes » | 69 Md€ sur la détention, 25 sur les ventes | **Titre corrigé** |
| `foncier.tex`, 2.1 : détention | 42 + 9 + 8 = 59 Md€ annoncés comme formant 69 | inventaire : 69,0 (dont environ 10 d'« autres », note de la figure) | **Complété** |

**Ce que j'ai vérifié et trouvé cohérent :**
- **Gain d'efficacité.** 220,1 Md€ de recette de la fusion. Optimum à 8,1 Md€, qui rendrait 25 Md€ au dixième le plus
  aisé ; la proposition en garde 60 %. Gain total de 6,9 Md€ (de 2,5 à 15,4), dont 71 % pour la fusion et 28 % pour
  l'immobilier ; 9,3 Md€ à long terme ; 5,2 à 6,1 Md€ de gain permanent ; −0,1 ou 3,3 Md€ selon la perception de la
  CSG.
- **Trajectoire et dette.** Dette cumulée au plus haut à 32 Md€ en 2032, éteinte vers 2040 ; 23 Md€ et 2037 sans la
  compensation du haut ; 59 et 5 Md€ dans les cas défavorable et favorable. La trajectoire année par année et la dette
  ont été recalculées à partir des soldes.
- **Baisses d'impôt du droit en vigueur.** Fin de la contribution exceptionnelle sur l'IS : 70 Md€ sur dix ans.
  Extinction de la CRDS : 7,4 et 1,0 Md€, et le PFU passe à 30,9 %.
- **Retraités et propriétaires.**
  - Retraités : +20,8 Md€ par an, soit une perte de 200 à 245 Md€ en valeur actualisée.
  - Propriétaires de logements : 150 Md€ de valeur perdue à l'annonce.
  - Transition de l'immobilier : déficit de 14,3 Md€ (11,6 si les ventes reprennent) ; 7 et 32 Md€ sur trois et dix
    ans.
- **IS.**
  - Dette de transition : 22,9 Md€ en 2033, éteinte en 2042. Puis baisse du taux normal de 0,9 point.
  - Si 90 % de l'investissement est imposable : 35 Md€ ; dans le cas défavorable : 57 Md€. Avec une dernière année
    de contribution exceptionnelle : 23 → 16 Md€.
- **Haut de la distribution.**
  - Fin de l'effacement : 2,5 Md€ en moyenne (de 0,7 à 6,8), 3,3 Md€ la dixième année.
  - CEHR : 1,4 Md€ en tout, dont 0,9 au titre de la majoration sur le capital.
  - Le tableau du bilan du haut a été refait colonne par colonne.
- **Fusion IR-CSG.** Dans la variante « IR imputé corrigé », le taux de 50 % est atteint à 212 000 €, et un décile
  bouge de 560 €. Abattement de 5 % : 17,2 Md€ ; franchise de 4 000 € : 13,5 Md€.
- **Les sept ménages de 5.4** : 1 005, 248, 523, 285, 8 105, 12 083, −10 917, −1 477, 5 021, 25 120, 37 680, 1,57 M€
  et 12,56 M€.
- **Chiffres de la partie IR-CSG** contrôlés sur `naive_ircsg.txt`, `proposition_ircsg.txt` et
  `arbitrages_prop_ircsg.txt` : déciles, cas-types, taux marginaux, décomposition du gain (2,3 / 2,6 / 2,9 / 2,2 /
  0,25), 10 332 et 1 047 barèmes.
- **Chiffres de la partie Immobilier** contrôlés sur `calculs_foncier.txt` : dixièmes, cas-types, arbitrages,
  capitalisation, report, transition.
- **Seul écart d'arrondi : 8 105 contre 8 110.** Le tableau `tab_fon_cas` arrondit à la dizaine les droits en moins
  de l'appartement lyonnais ; la synthèse donne le chiffre exact. Sans conséquence.

---

## 3. Problèmes de fond ou de structure que je n'ai pas pu régler seul, par ordre d'importance

### Importants
1. **Ni sommaire ni résumé pour cent pages.** Le lecteur visé n'a aucun moyen de s'orienter, sinon le dernier
   paragraphe de l'introduction. Je recommande deux ajouts au document maître, qui relève de l'orchestrateur et que je
   n'ai pas modifié :
   - un `\tableofcontents` après le bloc de titre (les titres de sous-parties racontent maintenant l'histoire) ;
   - une page « L'essentiel » : les quatre réformes en une phrase chacune, cinq ou six chiffres (gain, dette, retraités,
     haut de la distribution, fragilité de la CSG) et les six décisions.
2. **La neutralité du haut n'est qu'approchée, alors que le titre de la section 5 l'affirme.** Le titre et
   l'introduction disent « un haut à peu près neutre ». Or, dans la convention centrale, le 1 % paie +1,1 Md€ après
   suppression de la CEHR (de −0,9 à +6,1). Il ne revient à 0 qu'avec le barème adouci au-delà de 150 000 € (« V2 »),
   qui coûte 1,1 Md€ au budget et porte la dette à 40 Md€. DECISIONS.md (décision 3) demande |Δ 1 %| ≈ 0. L'auteur doit
   trancher : adopter V2 dans la proposition, ou assumer +1,1 Md€ dans le titre de la section 5.
3. **Tout le gain repose sur la perception de la CSG.** Si les salariés ne la perçoivent pas aujourd'hui, le gain
   total tombe à −0,1 Md€. La note le dit (parties 1 et 5, et désormais l'introduction). Mais un décideur demandera
   aussitôt s'il existe une version de la réforme dont le gain ne dépend pas de cette hypothèse, par exemple en ne
   comptant que la marge extensive (2,3 Md€, conservée dans ce calcul). Une phrase ou un chiffre de ce type renforcerait
   beaucoup la note.
4. **Chaque tableau de la section 5 est doublé par une figure qui montre les mêmes données** : trajectoire
   (`tab:ens_traj` / `ensemble_n02`), haut (`tab:ens_haut` / `ensemble_n03`), cas-types (`tab:ens_cas` /
   `ensemble_n04`). La section n'a pas d'annexe propre. Je n'ai rien déplacé, car les tableaux portent plus
   d'information (variantes, années). L'auteur peut envoyer les tableaux dans l'annexe E et ne garder que les figures,
   ou l'inverse.
5. **Les parties 1 et 2 sont très chargées en figures** : 14 figures et 3 tableaux pour l'IR-CSG en 15 pages,
   11 figures et 3 tableaux pour l'immobilier. La figure `foncier_n06_naif` est entièrement contenue dans
   `foncier_n08_variation`, qui montre aussi la réforme naïve. On pourrait la supprimer et pointer, dans la sous-partie
   naïve, vers le panneau « réforme naïve » de n08. Cela demande un choix de l'auteur, puisque la charte veut un
   graphique pour la réforme naïve.

### Moyens
6. **`synthese_ensemble.py`, l. 507 : « +785 € » écrit en dur.** C'est la variante au barème inchangé ; il faut la
   variante recherchée sous contraintes (+102). Si on relance le script, il faut corriger cette chaîne.
7. **Barème de l'IR-CSG : seuils ambigus et forte pente.** Le texte de 1.4 ne dit pas si les seuils (« 16 % à
   20 000 €, 27 % à 25 000 € ») s'entendent par adulte, après cotisations, franchise comprise ou non. Surtout, le taux
   monte de 11 points sur 5 000 € entre 20 000 et 25 000 €. C'est une pente continue, mais elle ressemble à une marche
   pour un lecteur qui vient de lire « un barème sans marches ». À expliquer, ou à commenter avec la figure
   `ircsg_n09`.
8. **IR-CSG, partie 1.6 : contradiction possible avec la recette constante.** Le texte suggère de « faire converger le
   haut du barème dès la première année ». Or la synthèse suppose une recette constante chaque année pendant la
   convergence. Si le haut converge plus vite, la recette baisse pendant la transition. Il faut soit la chiffrer, soit
   retirer la suggestion.
9. **IS, partie 3.1 : deux recettes en part du PIB sans explication.** Le texte donne 2,0 % du PIB (recette nette de
   l'État en 2025) puis, deux phrases plus loin, 2,35 % (OCDE, 2023), sans expliquer la différence de périmètre et
   d'année. Je n'ai pas pu vérifier le périmètre exact de l'OCDE.
10. **Affirmations du corps signalées comme non vérifiées, que l'on pourrait vérifier simplement :**
    - la date du quotient familial (« au lendemain de la guerre, date non relue ») ;
    - l'abattement de 10 % sur les pensions en 1978 (« texte non relu ») ;
    - « l'impôt individuel dans la plupart des pays européens (non vérifié pays par pays) » ;
    - la règle canadienne de 2018 ;
    - Carbonnier (2021), lu par le seul résumé.

    Les vérifier enlèverait plusieurs réserves du cœur de la proposition.
11. **La contrainte « familles » de l'introduction n'est vérifiée nulle part dans la synthèse.** Une phrase de la
    section 5.5 pourrait le faire : les familles gagnent dans la proposition ; dans la variante du chèque, un couple à
    un revenu avec deux enfants paierait +92 €.

### Mineurs
12. **Redites voulues par DECISIONS.md, qui alourdissent un peu le texte.** « Ce n'est pas un effet sur la croissance »
    revient quatre fois : introduction, 1.4, 5.1 et note de la figure `ensemble_n01`. « Protège la trésorerie, pas le
    patrimoine » revient deux fois.
13. **Listes à puces argumentatives.** La plupart des listes du corps sont de vraies énumérations : règles, cas-types,
    options. Mais les listes de l'IS en 3.2 (dispositifs accumulés) et 3.4 (six règles, dont la dernière fait un
    paragraphe) portent un raisonnement, et gagneraient à être écrites en prose.
14. **Notes de lecture des figures.** Quelques notes, générées par les scripts (`figures/nu/*_note.tex`), reprennent
    des chiffres du texte. CLAUDE.md demande qu'une note ne recopie pas le texte. Je ne les ai pas modifiées, puisque
    ce sont des sorties de scripts.
15. **Renvois aux annexes.** `\thesection` vaut « Annexe X », d'où « à l'Annexe E » ou « (Annexe A) » au milieu d'une
    phrase. C'est correct, mais la majuscule est inhabituelle. On peut le corriger dans le document maître si l'on
    veut.
